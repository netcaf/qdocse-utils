"""Self-contained SSH client + CLI for running commands on a remote Linux host."""

import argparse
import getpass
import logging
import sys
import time
from dataclasses import dataclass
from typing import Callable, Optional

import paramiko

logger = logging.getLogger(__name__)


@dataclass
class CommandResult:
    command: str
    exit_code: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.exit_code == 0


class RemoteHost:
    """A single SSH-reachable Linux target. Use as a context manager."""

    def __init__(
        self,
        host: str,
        port: int = 22,
        username: Optional[str] = None,
        password: Optional[str] = None,
        key_filename: Optional[str] = None,
        timeout: float = 10.0,
        command_timeout: Optional[float] = None,
        strict_host_key_checking: bool = False,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.timeout = timeout
        # Idle-read cap for run()/SFTP when the caller doesn't pass one: seconds of
        # silence (not total runtime) before a wedged host raises instead of hanging
        # the whole fleet run. None means the 60s default, so callers can pass a
        # possibly-absent config value (targets.toml command_timeout) straight through.
        self.command_timeout = 60.0 if command_timeout is None else command_timeout
        self.strict_host_key_checking = strict_host_key_checking
        self._client: Optional[paramiko.SSHClient] = None

    def connect(self) -> None:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(
            paramiko.RejectPolicy() if self.strict_host_key_checking else paramiko.AutoAddPolicy()
        )
        client.connect(
            hostname=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            key_filename=self.key_filename,
            timeout=self.timeout,
        )
        # Keepalives make a target that dies mid-command (power loss, kernel hang)
        # surface as a connection error within a few probes instead of a socket that
        # blocks until the OS-level TCP timeout.
        client.get_transport().set_keepalive(15)
        self._client = client
        logger.info(f"Connected to {self.username}@{self.host}:{self.port}.")

    def run(self, command: str, timeout: Optional[float] = None) -> CommandResult:
        """Execute a command on the remote host and return its result.

        timeout is an idle-read cap (seconds without output), not a total-runtime cap;
        omitted, it falls back to self.command_timeout so no call can hang forever.
        """
        if self._client is None:
            raise RuntimeError("Not connected. Call connect() or use as a context manager first.")
        if timeout is None:
            timeout = self.command_timeout
        _, stdout, stderr = self._client.exec_command(command, timeout=timeout)
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        exit_code = stdout.channel.recv_exit_status()
        logger.info(f"Ran '{command}' on {self.host}: exit_code={exit_code}")
        return CommandResult(command=command, exit_code=exit_code, stdout=out, stderr=err)

    def _open_sftp(self) -> paramiko.SFTPClient:
        """Opens an SFTP session with command_timeout as its idle-read cap, so a transfer
        that stalls (target dies mid-upload) raises instead of hanging; a healthy transfer
        of any size keeps data flowing and never trips it."""
        if self._client is None:
            raise RuntimeError("Not connected. Call connect() or use as a context manager first.")
        sftp = self._client.open_sftp()
        sftp.get_channel().settimeout(self.command_timeout)
        return sftp

    def read_remote_prefix(self, remote_path: str, num_bytes: int) -> bytes:
        """Reads only the first num_bytes of a remote file via SFTP, without downloading the
        whole thing -- useful for formats (like RPM) whose metadata header sits near the start
        of the file, well before the often much larger payload that follows it."""
        sftp = self._open_sftp()
        try:
            with sftp.open(remote_path, "rb") as f:
                return f.read(num_bytes)
        finally:
            sftp.close()

    def download(self, remote_path: str, local_path: str) -> None:
        """Download a file from the remote host via SFTP."""
        sftp = self._open_sftp()
        try:
            sftp.get(remote_path, local_path)
            logger.info(f"Downloaded '{remote_path}' from {self.host} to '{local_path}'.")
        finally:
            sftp.close()

    def upload(self, local_path: str, remote_path: str) -> None:
        """Upload a file to the remote host via SFTP."""
        sftp = self._open_sftp()
        try:
            sftp.put(local_path, remote_path)
            logger.info(f"Uploaded '{local_path}' to {self.host}:'{remote_path}'.")
        finally:
            sftp.close()

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> "RemoteHost":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


def reboot_and_wait(
    connect_kwargs: dict,
    initial_wait: int = 30,
    poll_interval: int = 5,
    max_polls: int = 60,
    on_progress: Optional[Callable[[str], None]] = None,
) -> bool:
    """Reboots the target and polls until it accepts SSH again.

    Opens a fresh connection to trigger the reboot (the existing connection is expected
    to drop), waits initial_wait seconds, then polls every poll_interval seconds.
    """
    try:
        with RemoteHost(**connect_kwargs) as remote:
            # sync before reboot so any just-written state files reach disk.
            remote.run("sync && reboot", timeout=10)
    except (paramiko.SSHException, OSError):
        pass  # expected — connection drops when the target reboots

    if on_progress:
        on_progress(f"    Waiting {initial_wait}s for reboot to start...")
    time.sleep(initial_wait)

    for i in range(max_polls):
        try:
            with RemoteHost(**connect_kwargs) as probe:
                probe.run("true", timeout=5)
            time.sleep(2)  # let freshly-booted services settle
            return True
        except (paramiko.SSHException, OSError):
            pass
        elapsed = initial_wait + (i + 1) * poll_interval
        if on_progress:
            on_progress(f"    Still offline... ({elapsed}s elapsed)")
        time.sleep(poll_interval)

    return False


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a command on a remote Linux host over SSH.")
    parser.add_argument("--host", required=True, help="Target hostname or IP.")
    parser.add_argument("--port", type=int, default=22, help="SSH port (default: 22).")
    parser.add_argument("--user", required=True, help="SSH username.")
    auth = parser.add_mutually_exclusive_group()
    auth.add_argument("--password", help="SSH password (omit to be prompted, or use --key-file).")
    auth.add_argument("--key-file", help="Path to an SSH private key file.")
    parser.add_argument("--timeout", type=float, default=10.0, help="Connection/command timeout in seconds.")
    parser.add_argument(
        "--strict-host-key-checking",
        action="store_true",
        help="Reject unknown host keys instead of auto-trusting them.",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to run on the remote host.")
    return parser


def main(argv: Optional[list] = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    args = build_arg_parser().parse_args(argv)

    command_parts = args.command[1:] if args.command and args.command[0] == "--" else args.command
    command = " ".join(command_parts).strip()
    if not command:
        logger.error("No command given.")
        return 2

    password = args.password
    if password is None and args.key_file is None:
        password = getpass.getpass(f"Password for {args.user}@{args.host}: ")

    try:
        with RemoteHost(
            host=args.host,
            port=args.port,
            username=args.user,
            password=password,
            key_filename=args.key_file,
            timeout=args.timeout,
            strict_host_key_checking=args.strict_host_key_checking,
        ) as remote:
            result = remote.run(command, timeout=args.timeout)
    except (paramiko.SSHException, OSError) as e:
        logger.error(f"SSH connection failed: {e}")
        return 1

    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.exit_code


if __name__ == "__main__":
    sys.exit(main())
