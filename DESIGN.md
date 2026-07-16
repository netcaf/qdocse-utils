# QDocSE Tooling — Design Document

Status: §5's gap is closed — `lifecycle.py`/`console.py` are implemented and have grown
past the original proposal (license renewal, elevation, and a last-resort force-uninstall
path, none of which were anticipated in the original draft). §7's open questions are
resolved (see inline notes). §9/§10 are new: license `.dat` generation (`helpers/codec.py` +
`helpers/lic-codec`) and fleet-wide orchestration (`fleet.py`), both added after this document's
original draft, in response to real problems hit operating actual targets. §10.4: all runtime artifacts (download caches, lifecycle resume state) now live under
`var/`, out of the repo root — code layout itself unchanged. §10.5 is the newest entry:
`qdu.py`, a thin single entry point dispatching to every per-module CLI.

Covers the four actors below (§2 — a fourth, Local, was named explicitly after the original
draft; see below) and the modules that manage the full lifecycle, each independently
runnable via its own CLI, matching this project's existing convention (`release.py`,
`csp.py`, `target.py`, `console.py`, `lifecycle.py`, `fleet.py` are each a
standalone argparse CLI *and* an importable library; `config.py` and `downloads.py` are the
two modules with no CLI at all — see §1 point 1, §10.1).

`release.py`/`remote.py` were originally named `release_server.py`/`remote_host.py`;
renamed once a short-lived `local.py` module (introduced and later removed, §10.1) made "one
short noun per module" the norm across every top-level file, and the longer names were the
two holdouts.

## 0. Requirements (as given)

Recorded verbatim (translated/lightly formatted, content unchanged) so later discussion and
implementation can be checked against the original ask rather than against this document's
interpretation of it.

> 有三个角色：A，release服务器；B，CSP服务器；C，一系列不定数量和distro类型的客户端
>
> **A**：它会定期生成版本号和build号下的linux安装包。由于这个包是内核模块，所以它不仅区分
> distro（如centos或ubuntu），而且还会根据版本号，特别是内核版本号，生成对应的安装包，
> 甚至还包括x64和arm不同cpu架构的安装包。
>
> **B**：CSP服务器管理有两个主要功能：
> 1. 安装包上传和下载，有按照不同类型分类；
> 2. 管理C客户端，C客户端有license控制，CSP会管理每个客户端的license激活等操作。
>
> **C**：客户端，有两个重要功能：
> 1. 从CSP获取相应的版本和类型的安装包后，它要执行安装、升级、删除等操作。这部分主要涉及
>    操作系统的包管理；
> 2. 在安装后，它有一个客户端的管理命令 `QDocSEConsole`，这个命令可以实现对安装的客户端的
>    管理操作，这个命令有细节内容（见 `references/QDocSE-User-Guide-3_2_0.md`）。

`QDocSEConsole` behavior as directly observed and supplied by the user (terminal transcripts,
condensed — full detail in §5.1/§5.2 below):

- **Before activation (Unlicensed mode)**: only 9 subcommands available (`activate`,
  `commands`, `licence`, `license`, `list_acls`, `show_mode`, `version`, `view`,
  `view_monitored`). `show_mode` reports `Unlicensed`. Install (`dpkg -i`) and uninstall
  (`dpkg -P`) both work directly, no extra steps — uninstall printed `No license applied`.
- **After activation (Elevated mode)**: ~50 subcommands available (ACLs, encryption,
  monitoring, audit, install_prep, etc. — full list in §5.2). Uninstalling/upgrading in this
  state requires first running `QDocSEConsole -c install_prep on` and rebooting; skipping
  this step makes `dpkg -i`/`dpkg -P` fail with an explicit `UNINSTALL FAILURE` block
  instructing the operator to run `install_prep on` and reboot before retrying.
- Requirement: "通过上面的讨论，形成设计文档，覆盖这些功能。需要好好设计，模块化。并在每个
  模块中都可以有对应的CLI单独执行。同时如果需要，可以参考另一个关于所有功能的实现
  （`/root/.build/qdocse-dev`），并不是复制，而是参考是否有启发。" — i.e.: produce a modular
  design document covering all of the above, with each module independently runnable via its
  own CLI, optionally drawing inspiration (not copying) from the reference implementation at
  `/root/.build/qdocse-dev`.
- Follow-up requirement (this entry): record the requirements themselves in the design doc,
  not just the resulting design, so future discussion/implementation can be checked against
  the original ask.
- Follow-up requirement (this entry): re-review the design itself for "模块化清晰，功能单一，
  且组合灵活。同时稳定。然后尽量扁平化，不要太深的结构" — clearly modular, single-purpose per
  module, flexibly composable, stable, and as flat as possible (avoid deep structure). See §1.

## 1. Design principles (applies to every module below, old and new)

1. **One file per module, no subpackages.** Every module in this repo
   (`release.py`, `csp.py`, `target.py`, `console.py`, `lifecycle.py`,
   `fleet.py`, `remote.py`, `config.py`, `downloads.py`) is a single flat file: a small class
   or two with plain methods, a few `_cmd_*` CLI functions, a `build_arg_parser()`, a `func=`
   dispatch, and `main()`. No `commands/` subpackage, no per-command file, no
   auto-discovery/registry machinery. At the scale of "a handful of QDocSEConsole calls" that
   machinery is solving a problem (~50 files to manage) we don't have. `helpers/codec.py` is the
   one exception worth naming: it's a thin Python wrapper (`encode`/`encode_to_file`) around a
   separate Rust binary (`helpers/lic-codec`), not a module implementing logic itself, and it has
   no CLI of its own — `lifecycle.py` is the one thing that calls it (see §9).
2. **Single responsibility per module, shown here as tiers rather than one arrow-diagram**
   (crossing arrows for every cross-tier read stopped being readable once there were nine
   modules — tiers plus a short prose note per cross-tier read is clearer):
   ```
   Foundation (no dependencies on each other):
       remote.py     config.py     downloads.py

   Talk to exactly one remote system:
       release.py (A)     csp.py (B)     console.py (C)

   Resolution (reads both A's and B's package listings):
       target.py

   Single-target orchestration:
       lifecycle.py

   Cross-target orchestration:
       fleet.py
   ```
   Cross-tier reads, in prose rather than arrows: `release.py`/`csp.py`'s own upload-related
   commands call `downloads.discover_local_packages()` for local-cache inventory.
   `lifecycle.py` owns its own per-host state (`_save_state()`/`_load_state()`/
   `_clear_state()`) and license `.dat` generation (`_generate_license_bytes()`/
   `_generate_license_file()`, wrapping `helpers/codec.py`, §9) directly -- these used to live in
   a separate `local.py`, folded back in once it became clear `lifecycle.py` was their only
   caller (§10.1). `target.py`'s `csp download --stage` uploads a downloaded package onto a
   target without installing it, reusing the same connection its own package-match already
   opened (§10.3). `fleet.py` only ever goes through `lifecycle.py`, never touches
   `console.py`/`target.py` directly.

   Every arrow (real or implied by the tiers above) is a plain Python import of plain
   functions — no interfaces, no plugin registries. `console.py` never builds `rpm`/`dpkg`/
   `reboot` commands; `lifecycle.py` never builds a `QDocSEConsole` argv string directly (it
   does own its `helpers/codec.py`/state-file calls directly, per above -- see §10.1).
3. **Plain values, not a Result/Status wrapper type.** Functions return `str`/`bool`/`tuple`/
   `dict`/`None`, or raise on a hard failure — exactly what `release.py`/`csp.py` do
   today. `qdocse-dev`'s `Result`/`ConsoleResult` dataclasses are a reasonable choice for
   *that* codebase but would be a second convention bolted onto this one for no real benefit.
4. **Flexible composition via small, single-purpose functions.** Each function is one remote
   check or one remote command (`get_mode`, `install_prep`, `reboot_and_wait`,
   `uninstall_package`, `verify_uninstalled`, ...). Orchestration (`run()`/`install()`/
   `uninstall()`) is just calling them in sequence with plain `if` branches — composable
   because each piece is independently callable and testable, not because of an abstraction
   layer. `fleet.py`'s functions are the clearest example added since the original draft: each
   is a thin per-host loop around one existing `lifecycle.py` function, not a re-implementation.
5. **Stability = idempotent + minimal persisted state.** Every orchestrating function checks
   current state before acting (`check_installed`, `get_mode`) so re-running it after a partial
   failure is safe. The only state worth persisting to disk is the one genuinely fragile step —
   surviving the SSH session dying across a `reboot` — stored as one flat JSON dict per host,
   not a `PhaseState` class with history tracking.
6. **Manual, deliberately-gated escape hatches stay separate from automatic flows.**
   `lifecycle.force_uninstall()` (§5.1) exists for a device that's genuinely stuck (e.g. an
   expired license with no way to renew/elevate it) and bypasses QDocSE's own license-gated
   uninstall entirely. Nothing in this codebase calls it without an explicit force opt-in —
   not `uninstall()`, not `reinstall()`, not `fleet_provision()` — and its CLI refuses to run
   without an explicit `--force` flag. By default a fleet-wide operation hitting a stuck host
   records it as a failure and moves on to the next host; a human decides whether to run
   `force-uninstall --force` against that one host afterward, or to re-run as
   `fleet clean --force`, which escalates a failed host to `force_uninstall()` automatically.
   Once inside that force-gated path, escalation *is* automatic (see §5.1): the human decision
   being gated is "reboot the box and bypass QDocSE's license dance", and the script-bypass
   fallbacks that follow are just that same decision executed to completion.

## 2. Actors

The original ask (§0) named three actors, A/B/C. A fourth, **Local**, is implicit in every
one of A/B/C's flows — every transfer between them already passes through local disk first —
but was never named. Naming it explicitly turned out to matter: it isn't just a passive
relay, it also *produces* something (license `.dat` files, §9) that never comes from A or B
at all. That distinction is what §10.1's `local.py` module formalizes.

| | Role | Responsibilities |
|---|---|---|
| **A** | Release server | Periodically produces Linux installer packages, one per (version, build, distro, kernel version, CPU arch). Each package is a kernel module, so it is version-locked to an exact `uname -r`. |
| **B** | CSP server | (1) Package management — upload/download/categorize packages for distribution. (2) Device/license management — tracks each client device and its license/activation state. |
| **C** | Client (target) | (1) Package lifecycle — install/upgrade/uninstall the kernel-module package. (2) Post-install management via `QDocSEConsole` — license activation, ACLs, encryption, auditing, etc. |
| **D** | Local | The machine these scripts run from. (1) Passive staging: every A↔B and B↔C package transfer lands here first (`var/downloads/`, §10.4) before moving on — nothing goes directly A→B or B→C. (2) Active producer: generates license `.dat` files (activation/elevation/renewal) entirely offline, no A/B involvement at all. (3) Persists `lifecycle.py`'s per-host state across a target reboot. |

Data/control flow: **A → D → B** (publish a build), **B → D → C** (a client's matching
package is downloaded locally, then staged/installed on the client), **D → C direct**
(license generation and application — bypasses A/B entirely), **C internal** (once
installed, `QDocSEConsole` manages the running module).

## 3. Current state — what exists

| Module | Covers | Status |
|---|---|---|
| `release.py` | A: browse version/build/distro tree, find/download packages | Done. Also extracts the exact compiled-for kernel version from each downloaded package and writes a `.kernel` sidecar (see §4). |
| `csp.py` | B.1: upload/list/download/delete packages on SAMGR. B.2: customer device list/activate/delete | Done. Upload tagging now uses the sidecar's exact kernel string instead of guessing from the distro folder name. |
| `target.py` | Resolves which package a given client needs, from either A or B, by exact kernel match (falling back to an `/etc/os-release` heuristic); can also stage the matched package onto the target without installing it | Done. `match`/`download` (against A), `csp match`/`csp download` (against B, git-style nested); each takes `--all` for every target in `targets.toml` instead of one. `csp download --stage` uploads to the target too — see §10.3. |
| `console.py` | C.2: drives `QDocSEConsole` on one target (mode, activation, elevation, renewal, `install_prep`, `finalize`, raw passthrough) | Done — see §5.2. |
| `lifecycle.py` | C.1: install/upgrade/uninstall/reinstall on one target, including the `install_prep` + reboot dance, plus license activation/renewal/elevation and a last-resort force-uninstall | Done — see §5.1. Also owns per-host state persistence and license `.dat` generation directly — see §10.1. |
| `helpers/codec.py` + `helpers/lic-codec` | Encodes/decodes the license `.dat` file format itself | Done — see §9. Only caller is `lifecycle.py`. |
| `downloads.py` | D: the local package-cache layout (`var/downloads/release/{version}/{build}/{distro}/`, §10.4) both `release.py` and `csp.py` read/write | Done — see §10.1. |
| `fleet.py` | Runs `lifecycle.py`'s operations across many targets (`check`/`clean`/`install`/`activate`/`provision`) | Done — see §10.2. |

## 4. The thing that makes package identity hard (already solved, context for §5)

Because the installer is a kernel module, its own `%pre` (rpm) / `preinst` (deb) script
hard-checks `uname -r` and refuses to install on a mismatched kernel — see
`release.extract_local_kernel_version()` / `get_package_kernel_version()`. We
already use this as the authoritative signal for "which package does this client need",
both against the release server (`target.py`'s `resolve_distro_by_kernel`) and against CSP
(`resolve_package_from_csp`, once `csp.py` tags uploads with that exact string). This
matters for §5.1 too: the lifecycle module doesn't need its own package-matching logic —
it just calls `target.find_package_for_target` / `find_package_from_csp`. Note that this
match only needs to be "found at all" (`pkg is not None`), not top-confidence
(`"exact"`/`"kernel"`) — a `"heuristic"` match is accepted by `install()` and by
`fleet.fleet_check()`'s package-readiness report just the same (see §10.2).

## 5. Role C

### 5.1 Package lifecycle (install / upgrade / uninstall / reinstall / license ops)

Grounded in `references/QDocSE-User-Guide-3_2_0.md` and confirmed live on real targets:

**Modes** (output of `QDocSEConsole -c show_mode`):
- `Unlicensed` — no license applied, or a *previously*-applied license has expired. These
  are **not the same state** despite reporting the same mode string: a device with license
  history routes `activate` to a hard refusal ("Must be in Elevated Mode") and requires
  `renewcommit` instead (see below); a truly fresh device accepts `activate`. `show_mode`
  alone can't distinguish them — `QDocSEConsole -c view`'s "License file: ..." line (present
  even when expired) is the tell.
- `De-elevated` — full self-defence active; nothing can be changed, including by QDocSE
  itself. Needs an **elevation file** (`QDocSEConsole -c elevate -ef <file> -t <duration>`)
  to move to Elevated before an upgrade/uninstall can even start.
- `Elevated` / `Learning` — full command set unlocked. Upgrade/uninstall are only
  possible from here.

**The install_prep dance** (required whenever the module is licensed/active, i.e. not
`Unlicensed`):
```
QDocSEConsole -c install_prep on      # only valid in Elevated/Learning, AND requires a
                                       # currently-valid license (an expired one refuses
                                       # install_prep too, even though show_mode says
                                       # Unlicensed the same as a never-licensed device)
reboot                                # required — disables protection cleanly
                                       # window: 40 min (3.0.2+) before it expires
{ rpm -e qdocse | dpkg -r qdocse }    # or rpm -U / dpkg -i for an upgrade
QDocSEConsole -c finalize             # (upgrade only) return to De-elevated
```
Skip the reboot (or run it again without first reinstalling/uninstalling) and the prep
expires after 40 minutes, re-establishing full security. Run `dpkg -i`/`-P` without doing
this first and the package's own `prerm`/`preun` refuses with an explicit error block
telling the operator to run `install_prep on` and reboot.

A subtlety hit live on a real device: the protected directories the package manages
(`/data`, `/data2`, `/qdoc/conf`, `/qdoc/bin`) are guarded by two different kernel
filesystem types with *different* enforcement — `bic_sgfs` (Security Guard) allows normal
root read/write/create even while unlicensed; `bic_dgfs`+`bic_ecryptfs` (Data Guard) blocks
both writes *and* deletes outright, `EPERM`, regardless of root. `umount`ing either without
a valid `install_prep` fails the same way ("must be superuser to umount") — this isn't the
kernel's ordinary busy-mount handling, it's the driver's own permission gate, so no
`umount -f`/`-l` flag routes around it.

**`lifecycle.py`'s actual shape** (grew past the original proposal once real devices forced
the extra cases below):
```
status(target)                            -- check_installed() + show_mode()
install(target, version, build, source="csp"|"release")
    -> resolves the package via target.find_package_for_target/find_package_from_csp,
       copies it over (reusing RemoteHost), runs rpm -i/dpkg -i, starts the service.
uninstall(target, elevation_file=None, elevation_duration="1h")
    -> mode-aware: Unlicensed -> remove directly.
                   De-elevated -> elevate (externally-supplied file, or generated locally
                                   if elevation_file is omitted -- see below) -> install_prep
                                   -> reboot -> remove.
                   Elevated/Learning -> install_prep -> reboot -> remove.
       On a verified success, also deletes the device's CSP customer record for its
       outgoing qid (best-effort, never fails the uninstall). Each reinstall mints a new
       random qid, and CSP never expires the old device record on its own, so without this
       cleanup a repeatedly-reinstalled host accumulates one permanently-orphaned CSP record
       per past install generation (found and cleaned up 14 stale records across the
       customer account before this was automated).
upgrade(target, version, build, elevation_file=None)
    -> same prep/reboot dance, then rpm -U/dpkg -i, then `console.finalize()`.
reinstall(target, version, build, source="csp"|"release", do_activate=False)
    -> uninstall() if already installed, then install(), then optionally activate().
activate(target, duration=2_678_400, mode=5)
    -> reads the target's real qid, finds its CSP customer-portal device record, generates
       an ACTIVATION .dat via local.generate_license_bytes() (see §10.1/§9) and pushes it
       through CSP's activate_device() API. Requires the device to have already checked in
       with CSP. Skips (returns True) if already activated and not yet expired.
renew(target, duration=2_678_400, mode=5)
    -> entirely local, no CSP: QDocSEConsole -c renewrequest -> local.generate_license_file()
       encodes a RENEWAL .dat -> QDocSEConsole -c renewcommit. Use instead of activate() when
       a device already has license history (activate() only works for a never-licensed
       device) and isn't CSP-managed, or CSP hasn't picked up the renewal yet. See §9 for
       why the renewal .dat's qid field is NOT the device's real qid.
elevate(target, duration="1h", mode=5)
    -> entirely local, no CSP: local.generate_license_file() encodes an ELEVATION .dat (real
       qid, same as activate()) and applies it via QDocSEConsole -c elevate. No-op if already
       Elevated/Learning.
force_uninstall(target)
    -> LAST RESORT, never auto-invoked (see §1 point 6): disables QDocSEService/
       qdocsesubagent (confirmed via `strings` against the real binary to be what both
       mounts the protected directories and loads the bic_* kernel modules) and the
       redundant /etc/modules-load.d entry, reboots, verifies nothing bic_* is loaded or
       mounted, then removes the package, escalating automatically if the package's own
       scripts refuse (they normally exit cleanly here, since %preun/prerm find nothing
       left to fight): ordinary removal first; then with the pre-removal script bypassed
       (rpm -e --nopreun / dpkg with the prerm file stubbed) for when that script itself
       is broken, e.g. a panic-corrupted DB failing its mode check -- the post-removal
       cleanup still runs; finally with all scripts skipped (rpm -e --noscripts /
       dpkg --purge with both scripts stubbed), where the package manager removes the
       packaged files by its own manifest and target.QDOCSE_RUNTIME_ARTIFACTS covers the
       runtime-generated leftovers by fixed path. Aborts without touching the package if
       post-reboot verification finds anything still loaded/mounted, rather than forcing
       a removal that would fight it.
```

`uninstall()`'s elevation step, when `elevation_file` isn't supplied, generates one locally
the same way `elevate()` does (`_local_elevate()`) rather than requiring the caller to have
an externally-issued file — this used to be a hard `ValueError` in the original
implementation, before local elevation generation was confirmed working.

State persistence: a flat JSON file per target, `var/state/<host>.json` (§10.4), holding just
`{"operation": "uninstall", "phase": "post_reboot", "package_manager": "dpkg"}` — written
right before the reboot, cleared on success. So `lifecycle.py uninstall --host X` run
again after the reboot recognizes "I already did install_prep, just finish the removal"
instead of re-running it. One caveat found in practice: this resume path skips straight to
`remove_package()` without re-checking whether `install_prep`'s 40-minute window has since
expired — if it has, the resume attempt fails with "install_prep has exceeded its time
limit" and the state file is cleared regardless, so simply re-running `uninstall` from
scratch (not resume) recovers cleanly.

**CLI** (own file, same convention as the rest):
```
python3 lifecycle.py status          --host <host>
python3 lifecycle.py install         --host <host> --version 3.2.0 --build 140 [--source csp]
python3 lifecycle.py uninstall       --host <host> [--elevation-file <path>]
python3 lifecycle.py upgrade         --host <host> --version 3.2.0 --build 142 [--elevation-file <path>]
python3 lifecycle.py reinstall       --host <host> --version 3.2.0 --build 142 [--source csp] [--activate]
python3 lifecycle.py activate        --host <host>
python3 lifecycle.py renew           --host <host>
python3 lifecycle.py elevate         --host <host> [--duration 1h]
python3 lifecycle.py force-uninstall --host <host> --force
```

### 5.2 `QDocSEConsole` management

`QDocSEConsole` has ~50 subcommands, and which ones are even *listed* by `-h` depends on the
current mode/license — 9 when Unlicensed, ~50 when Elevated. A typed Python wrapper for
every one of them would be speculative work for commands nothing here calls
programmatically, and (per §1) a `commands/` subpackage with one file per command is exactly
the deep structure to avoid at this scale. Flat, one file, no class hierarchy — `console.py`'s
actual wrapped set:

```python
run_console(remote, args) -> CommandResult   # every function below is one call to this
show_mode(remote) -> str                     # 'unlicensed'|'de-elevated'|'elevated'|'learning'|'not_installed'|'unknown'
version(remote) -> dict
view(remote) -> dict                         # authorized/denied programs, watch points, license/mode fields
activate(remote, file, duration) -> dict
elevate(remote, file, duration) -> dict
renewrequest(remote, remote_path=...) -> dict  # returns the pending-renewal request number (see §9)
renewcommit(remote, file) -> dict
finalize(remote) -> dict
install_prep(remote, mode) -> dict           # mode: "on"|"off"; aliases uninstall_prep/upgrade_prep
raw(remote, args) -> CommandResult           # passthrough: console.py raw --host X -- list_acls
```

Each function is a plain, independently-testable piece (per §1 point 4) — no `Opt`
dataclass, no discovery/registry, no `ConsoleResult` wrapper type (just the existing
`CommandResult`/plain return values, per §1 point 3). The CLI is one `_cmd_*` function per
command plus a `set_defaults(func=...)` per subparser, same as every other module here.
Growing this set by hand later (one function + one CLI entry) is the upgrade path if a
command earns first-class wrapping — still flat, no indirection to learn.

`lifecycle.py` calls `console.show_mode()`/`console.install_prep()`/`console.activate()`/
etc. directly — it never shells out to `QDocSEConsole` itself. That keeps "how do I run a
QDocSEConsole command" in exactly one place. `console.py` in turn has no idea `helpers/codec.py`
or `local.py` exists — it just runs whatever `.dat` file path it's given; `lifecycle.py` is
the one that calls `local.py` to generate that file first (§10.1).

## 6. End-to-end flows (tying modules together)

**Fresh deploy, resolving against CSP:**
```
csp.py samgr upload --version 3.2.0 --build 140        # B.1, already done earlier
lifecycle.py reinstall --host 10.10.142.244 --version 3.2.0 --build 140 --source csp --activate
    -> uninstall() if already installed
    -> target.find_package_from_csp(...)                # resolution (existing)
    -> RemoteHost SFTP copy + rpm -i/dpkg -i
    -> activate()                                        # C.2, via CSP customer portal
```

**Safe uninstall (mode-aware):**
```
lifecycle.py uninstall --host 10.10.142.244
    -> console.show_mode() == "elevated"
    -> console.install_prep("on")
    -> reboot + wait-online (persisting state in case the SSH session dies here)
    -> dpkg -r qdocse / rpm -e qdocse
    -> verify (rpm -q / dpkg-query no longer reports installed)
    -> best-effort: delete the device's now-stale CSP customer record
```

**Safe upgrade:**
```
lifecycle.py upgrade --host 10.10.142.244 --version 3.2.0 --build 142
    -> same install_prep + reboot dance
    -> rpm -U / dpkg -i the new package
    -> console.finalize()   # De-elevated, full security restored
```

**Recovering an expired, non-CSP-managed device (no reboot yet possible until licensed):**
```
lifecycle.py renew --host 10.10.142.244
    -> console.renewrequest() -> request_number
    -> local.generate_license_file() encodes a RENEWAL .dat with qid=request_number (not the real qid!)
    -> console.renewcommit()  -> mode: unlicensed -> de-elevated
lifecycle.py elevate --host 10.10.142.244
    -> local.generate_license_file() encodes an ELEVATION .dat with qid=<real device qid>
    -> console.elevate()      -> mode: de-elevated -> elevated
lifecycle.py uninstall / reinstall ...   # now unblocked, install_prep works normally
```

## 7. Decisions made (originally "open questions")

1. **State file location/format**: a flat dict, one JSON file per host. Originally
   `config/state/<host>.json`, next to `targets.toml`; moved to `var/state/<host>.json` once
   `var/` collected all runtime artifacts (§10.4) — state is runtime data, not configuration.
2. **How much of `QDocSEConsole` to wrap**: the curated flat function set in §5.2, grown
   twice since the original draft (`renewrequest`/`renewcommit`, once license renewal turned
   out to need them).
3. **`lifecycle.py install`'s default source**: `--source csp`, with `--source release` as
   an override — as recommended, unchanged.
4. **Elevation/license files**: `lifecycle.py` generates them via `local.py`
   (`generate_license_bytes()`/`generate_license_file()`, §10.1 — which itself wraps
   `helpers/codec.py`) and SFTPs them over itself (`activate()`/`renew()`/`elevate()`/
   `_local_elevate()`) — the original draft only anticipated SFTP-ing an *externally-supplied*
   file; local generation turned out to be possible and is now the default, with an
   externally-supplied file still accepted as an override (`--elevation-file`).
5. **Where `lifecycle.py`/`console.py` fit relative to `deploy.py`**: **not** folded into
   `deploy.py` as originally suggested. Instead, a second, independent orchestrator
   (`fleet.py`) was added beside it — see §10.2 for why. (`deploy.py` itself was later removed
   entirely, once its remaining pieces turned out to belong elsewhere — see §10.3.)

## 8. Inspiration credit

What's taken from `/root/.build/qdocse-dev` (specifically
`qdocse/lifecycle/{install,uninstall,state,reboot}.py` and `qdocse/ops/_console/`): the mode
table (`unlicensed`/`de-elevated`/`elevated`/`learning`), the install_prep→reboot→remove
sequencing including the 40-minute-window and package-manager-detection caveats, and the
*concept* of persisting state across a reboot.

What's deliberately **not** taken, per the flatness/single-convention review in §1: the
`commands/`-subpackage-with-one-file-per-command structure, the `ConsoleCommand`/`Opt`
class hierarchy and pkgutil-based discovery, and the `Result`/`Status`/`ConsoleResult`
dataclass wrapper types. Those fit `qdocse-dev`'s own conventions but would add a second,
deeper structure on top of this project's existing flat, function-based, plain-return-value
style for no benefit at the scale we actually need. The modules also reuse *this* project's
existing `RemoteHost`, `target.py` resolution, and `config.py`/`targets.toml`
infrastructure rather than re-deriving SSH/transport/inventory handling from scratch.

## 9. License `.dat` generation (`helpers/codec.py` + `helpers/lic-codec`)

Not part of the original draft — added once it became clear `activate()`/`elevate()`/
`renew()` needed a way to produce license files without depending on BicDroid's own license
generator being available for every test target.

**Shape:** `helpers/lic-codec` is a small Rust binary (source at `/root/.build/lic_codec`,
vendored here as a prebuilt binary since the Rust toolchain isn't part of this repo's own
stack); `helpers/codec.py` is a thin subprocess wrapper exposing `LicKind` (`ACTIVATION`/
`ELEVATION`/`RENEWAL`), `LicInfo` (`qid`, `foot_print`, `duration`, `mode`, `magic`), and
`encode()`/`encode_to_file()`. No `decode` on the Python side — `helpers/lic-codec`'s own
`inspect`/`<kind> decode` subcommands cover that for debugging.

**The crypto, once corrected to match the real product** (`lic_codec` commit
`a7ba7e5`): AES-256, a *fixed* key+IV derived from the real `QDocSEConsole`'s
`AESKEYFORCONFIG` scheme (not a guessed/reconstructed one), **no padding** (zero-fill to the
16-byte block boundary, `EVP_CIPHER_CTX_set_padding(ctx, 0)` in the original, not PKCS7).
Getting this wrong (an earlier, incorrect key + PKCS7 assumption) produced files that were
internally self-consistent — `lic-codec` could encode and then decode its own output fine —
but were rejected outright by the real `QDocSEConsole`, which is a trap worth remembering:
self-consistency of a codec proves nothing about compatibility with the real target.

**The one qid subtlety that cost the most time** (`lic_codec` commit `7f9f324`): the `qid`
field means different things for different `LicKind`s.
- `ACTIVATION`/`ELEVATION`: `qid` = the target's real `/qdoc/conf/qid.txt` value.
- `RENEWAL`: `qid` = the **pending renewal request number** from
  `QDocSEConsole -c renewrequest -rf <file>` (that file's first line) — *not* the device's
  real qid. Passing the real qid here is what produces the misleading "The file is not for
  this machine. No valid renew item in the file." rejection; it isn't actually a
  machine-identity check, it's checking the submitted renewal against the specific pending
  request. The request number is single-use (burns on the first successful `renewcommit`) and
  is presumably invalidated by generating a new one, so encode+commit promptly after the
  `renewrequest` call rather than caching an old request number.

Also confirmed empirically and worth remembering: `activate` (not `renewcommit`) is
`QDocSEConsole`'s "first license ever" path — it hard-refuses ("Must be in Elevated Mode",
a misleading error for what's actually "you already have license history") on a device that
has ever had a license before, even if that license has since expired and `show_mode`
currently reports the same `Unlicensed` string a never-licensed device would. `renew()`
(§5.1) exists specifically for that case.

## 10. Local (D) and cross-target orchestration

### 10.1 `local.py` — introduced, then removed once its shape became clear

Not part of the original draft. Grew out of naming Local as a real actor (§2): a few things
that were previously either duplicated or living in the wrong file turned out to all be the
same concern -- local-machine bookkeeping -- once that was made explicit. It held three
things: local package-cache inventory, `lifecycle.py`'s per-host state, and license `.dat`
generation, each with its own CLI (`local.py cache list`/`clear`, `local.py state
show`/`clear`).

**Removed later, in two different ways, once actually questioned ("does this need to keep
existing?").** The CLI turned out to be pure sugar: `cache list`/`clear` are just "look at/rm
files under `downloads/{version}/{build}/{distro}/`," and `state show`/`clear` are just "look
at/rm a JSON file under `config/state/<host>.json`" -- both directly replaceable by `ls`/
`find`/`cat`/`rm` on well-known paths, no bespoke command needed. Gone entirely, along with
`clear_local_packages()`/`list_state_hosts()` (only ever called by their own now-deleted CLI
commands -- dead code once it was gone).

That left three functions with real programmatic callers, but they didn't all need the same
fix:

- **Package cache** (`discover_local_packages()`, `KERNEL_SIDECAR_SUFFIX`) has *two*
  independent consumers: `release.py` writes the `.kernel` sidecar when downloading, `csp.py`
  reads it back to batch-discover what's ready to upload. Whichever of those two files this
  code moved into, the *other* would have to import it from there -- exactly the
  `release.py`↔`csp.py` cross-dependency §1 point 2 and §10.3 both work to avoid (the same
  reasoning that kept `publish` from just moving into `csp.py`, see §10.3). So this piece
  needed to stay neutral -- moved to a new, minimal `downloads.py` (no CLI, no state, nothing
  else -- just this).
- **Lifecycle state** (`save_state()`/`load_state()`/`clear_state()`) and **license
  generation** (`generate_license_bytes()`/`generate_license_file()`) have exactly *one*
  consumer each: `lifecycle.py`. No cross-dependency risk, so no reason for a separate file --
  folded directly back into `lifecycle.py` as private helpers (`_save_state()` etc.,
  `_generate_license_bytes()` etc.), undoing the earlier "made public since they're general
  local bookkeeping" call from when `local.py` was first introduced. In hindsight they weren't
  general -- they had exactly one caller the whole time.

Net effect: `local.py` is gone. `downloads.py` is the only piece that genuinely needed to
stay neutral, and it stayed minimal (still no SSH/`RemoteHost` knowledge -- same foundational
tier as `config.py`, §1 point 2). `lifecycle.py` owns its own state/license logic directly
again, same as before `local.py` ever existed -- the state-file bug that originally justified
making `clear_state()` reachable standalone (a stale state file once made
`lifecycle.py` resume incorrectly mid-session) is still fixable, just via `rm
var/state/<host>.json` directly instead of a dedicated command.

### 10.2 Fleet-wide orchestration (`fleet.py`)

Not part of the original draft, and initially implemented as new commands bolted onto
`deploy.py` before being split out — worth recording why.

**Why not `deploy.py`:** §7's original recommendation was to fold cross-target-fleet
operations into `deploy.py` once `lifecycle.py` existed. In practice, doing that produced a
9-subcommand CLI (`publish`/`download`/`upload`/`target`/`check`/`clean`/`install`/
`activate`/`provision`) conflating two unrelated concerns: `deploy.py`'s original four
commands only ever move package *files* between servers (release server -> CSP -> one
target's disk, no install/license logic, no `lifecycle.py` import); the fleet commands only
ever manage install *state* across *many* targets via `lifecycle.py`. Splitting them into
two files — neither importing the other — fixed both the CLI's readability (`deploy.py -h`
and `fleet.py -h` are each short and thematically coherent) and kept the dependency graph
honest (§1 point 2): a file that imports `lifecycle.py` is doing a different job than one
that doesn't, so it's a different file. (`deploy.py` no longer exists at all as of §10.3 --
this section describes why the split happened at the time, not the current file layout.)

**`fleet.py`'s shape:** every host is processed sequentially (not concurrently — simpler to
reason about given SSH+reboot is already involved per host, and nothing else in this
codebase uses threading), and one host's failure never stops the rest:
```
fleet_check(hosts, version=None, build=None, source="csp")
    -> read-only: per host, status (installed/version/mode, same as lifecycle.py status)
       and, if version+build given, whether target.find_package_for_target/
       find_package_from_csp can resolve a package for it (without downloading) -- matches
       install()'s own gate (pkg is not None), not confidence tier (see §4).
fleet_clean(hosts, elevation_file=None)    -> per host: lifecycle.uninstall() if installed.
fleet_install(hosts, version, build, source="csp")  -> per host: lifecycle.install().
fleet_activate(hosts)                      -> per host: lifecycle.activate().
fleet_provision(hosts, version, build, source="csp")
    -> per host: lifecycle.reinstall(..., do_activate=True) -- delegates to reinstall()'s
       own per-host short-circuit rather than chaining fleet_clean/fleet_install/
       fleet_activate separately, so a host whose clean fails doesn't still get an install
       attempt.
```
`fleet_clean()`/`fleet_provision()` never call `lifecycle.force_uninstall()` — per §1 point
6, that stays a manual, separately-invoked escape hatch; a stuck host is reported as a
failure in the fleet summary; force-removing it is a deliberate follow-up decision, not part
of automatic fleet cleanup.

**CLI:** each command takes either `--all` (every target in `targets.toml`) or one-or-more
repeatable `--host` (mutually exclusive, exactly one required — no implicit default
across an operation that includes uninstalling things), and prints a one-line-per-host
summary at the end.

### 10.3 Trimming, then removing, `deploy.py` (multiple rounds)

**`download`/`upload` (pre-existing duplication, not new).** Not something this session's
refactors introduced -- `deploy.py` originally also had `download` and `upload`
subcommands, predating `local.py`/the renames. Once `fleet.py`'s 9-subcommand mess (§10.2)
prompted a closer look at what actually belongs in a cross-cutting orchestrator file, these
two turned out to be genuinely redundant, not just differently named: `deploy.py download`
called the exact same `ReleaseServer.download_all()` that `release.py`'s own `download`
subcommand already exposes directly, and `deploy.py upload` called the same
`CSPSAMGR.upload_tagged_packages()`/`discover_local_packages()` path `csp.py samgr upload`
already exposes directly -- same arguments, same behavior, just reimplementing each remote
module's own connection setup a second time in a different file.

**`publish` (removed later, different reason).** `deploy.py` briefly kept `publish`
(release.py's download + csp.py's upload, chained) alongside `target` as the two commands
that genuinely sequence *multiple* modules. Removed once it became clear `publish` had no
honest inverse: deleting a published package is CSP-only (no release-server step), so it
belongs in `csp.py`, not here -- meaning "undo `deploy.py publish`" would always have meant
crossing files to `csp.py samgr delete`, no matter where `publish` lived. Since the two
steps `publish` chained already work fine run separately -- `release.py download` then
`csp.py samgr upload`, same `--version`/`--build`/`--distro` shape either way -- there was
no real capability lost by removing it, only a redundant "combined" entry point with a
one-sided pairing. `csp.py samgr upload`/`csp.py samgr delete` are the real publish/unpublish
pair, and they already live together in the same file.

**`target` (removed last, `deploy.py` deleted entirely).** With `publish` gone, `target`
(resolve the client's matching CSP package, download it, SFTP-upload it onto the target,
stop short of installing -- that's `lifecycle.py`'s job) was the only thing left in
`deploy.py`. Comparing it to what already existed elsewhere showed it wasn't pulling its
weight as a separate file: `target.py`'s own `csp-download` command (since renamed `csp
download`, below) already did the match+download half, using a *better* matcher
(`find_package_from_csp()`'s exact-kernel match, vs. `deploy.py target`'s plain
`resolve_distro()`) -- `deploy.py target` was really just `target.py csp-download` plus one
upload step, with worse matching. Rather than keep a whole file around for one step,
`csp-download` gained a `--stage` flag that does that one step too, reusing the SSH
connection `find_package_from_csp()` already opened instead of reconnecting. `deploy.py` had
nothing left in it and was deleted.

Net effect: `deploy.py` is gone entirely. Every workflow it used to cover is now one of:
`release.py download` + `csp.py samgr upload` (publish), `csp.py samgr delete` (unpublish),
or `target.py csp download --stage` (stage on a target) -- each living in the single module
that already owned the rest of that work, none of them needing a dedicated cross-cutting
file.

**`target.py`'s own commands restyled to git-style nesting, and `match-all`/`csp-match-all`
dropped.** `target.py` had been the one holdout still using flat, dash-joined command names
(`csp-match`, `csp-download`, `match-all`, `download-all`, `csp-match-all`,
`csp-download-all`) instead of the nested-subcommand style the rest of the project already
used (`csp.py samgr upload`, etc.). Restyled: `csp-match`/`csp-download` nested under a `csp`
group (`csp match`/`csp download`); each `-all` variant folded into a `--all` flag on its
base command (`match --all` instead of a separate `match-all`, etc.) rather than kept as a
separate dash-suffixed command.

While auditing all twelve commands for this restyle, `match-all` and `csp-match-all`
specifically turned out to be a real duplicate, not just a styling mismatch: `fleet.py check
--version V --build B --source {csp,release}` already resolves, for every target, whether a
matching package exists -- the exact same match-only check `match-all`/`csp-match-all` did,
just as one part of a report that also covers install status/mode per host. Dropped both;
`fleet.py check` is the one place that check now lives. `download`/`csp download` (which
actually fetch files, not just check) had no such overlap -- `fleet.py install`/`provision`
go further than that (they install), so "download to every target's local cache without
installing" still only exists via `target.py download --all`/`csp download --all`.

### 10.4 Runtime artifacts moved under `var/` (code layout unchanged)

A structure review asked whether the repo root needed restructuring. Conclusion: the flat
one-file-per-module code layout stays (§1 point 1 — deliberately chosen, and already
stress-tested by `local.py`/`deploy.py` coming and going), but the root *was* accumulating
runtime artifacts mixed in with code, and two of them exposed real defects:

- **CSP re-downloads polluted the cache root.** `csp.download_package()` writes into the
  given directory using the server's `Content-Disposition` filename — the pk_name registered
  at upload (e.g. `se-water0506-auto-3.2.0-148CentOS-7.6-3.2.0-148`, no `.rpm`/`.deb`
  suffix). Every caller passed `DEFAULT_DOWNLOAD_DIR` itself, so these landed loose at
  `downloads/` top level, outside the `{version}/{build}/{distro}/` layout — and would have
  been scanned as a bogus "version" dir by `discover_local_packages()`/`latest_local_build()`
  had one ever been named like a version.
- **`DEFAULT_DOWNLOAD_DIR` followed `os.getcwd()`**, so running any command from a different
  directory silently grew a second cache there.
- **`config/state/` held runtime state under the config dir.** The mechanism itself was
  re-judged and kept — it is load-bearing (uninstall/upgrade resume across the target reboot,
  the window where the local process most plausibly dies; without it a rerun costs an extra
  `install_prep` + reboot cycle) and near-free (one small JSON per host, cleared on success).
  Only its location was wrong: state is runtime data, not configuration.

The fix is one `var/` tree, anchored to the repo directory (not cwd), all gitignored:

```
var/downloads/release/{version}/{build}/{distro}/   # the release cache, layout unchanged
var/downloads/csp/{version}/{build}/                # CSP re-downloads (new, was downloads/ root)
var/state/<host>.json                               # lifecycle resume state (was config/state/)
```

The CSP tree is separate from the release tree so `discover_local_packages()` never sees it
(pk_name files are not cache entries: no extension, no `.kernel` sidecar). It deliberately
has no `{distro}` level: a CSP match's `DistroMatch.distro` is a synthesized
`osName+osVersion-Kern...` string, not a clean directory name, and the pk_name filename
already encodes the distro, so `{version}/{build}/` is enough to keep builds apart with no
collision within one. CSP re-downloads are transient anyway (fetched at install time,
immediately SFTP'd to the target) — the tree is for inspection, not reuse; nothing reads it
back.

Code impact was confined to path constants and download call sites: `config.py` gained
`VAR_DIR`/`CSP_DOWNLOAD_DIR` and re-anchored `DEFAULT_DOWNLOAD_DIR`; `lifecycle.py`'s
`local_dir` parameters now default to `None` meaning "the per-source default tree"
(`--local-dir` still overrides); `target.py csp download` defaults to the CSP tree;
`STATE_DIR` moved. No install/uninstall/license logic changed.

### 10.5 `qdu.py` — one entry point over the per-module CLIs

The per-module CLIs (§1 point 1) stayed, but with seven of them the operator had to
remember which file owned which verb. `qdu.py` is a thin dispatcher: the first argument
names a module, everything after it is passed verbatim to that module's existing
`main(argv)` — `qdu.py csp samgr list` is exactly `python csp.py samgr list`. It was
deliberately kept a dispatcher rather than one merged argparse tree: merging would force
every module to export a `register_parser(subparsers)` hook and re-couple modules that §1
keeps independent, for no gain beyond an auto-generated top-level help (which `qdu.py`
hand-writes in seven lines instead). Modules are imported lazily, one per invocation, so
no command pays the import cost — or a broken import — of the other six. The only
subtlety: argparse derives its usage `prog` from `basename(sys.argv[0])`, so the
dispatcher rewrites `sys.argv[0]` to `"qdu.py <command>"` before delegating, making nested
`--help` output read correctly. Direct `python <module>.py ...` invocation still works
everywhere; `qdu.py` adds discoverability and replaces nothing.
