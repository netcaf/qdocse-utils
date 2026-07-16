# QDocSE™ for Linux® User Guide

**Version 3.2.0**

---

Copyright © 2021-2026 BicDroid, Inc. All rights reserved.
http://www.bicdroid.com
Part Number: BD-QSL-3.2.0-a
Trademarks
QDoc and QDocSE are trademarks of BicDroid, Inc.
UNIX® is a registered trademark in the United States and other countries of The Open Group.
Linux® is the registered trademark of Linus Torvalds in the U.S. and other countries.
CentOS™ is a trademark of Red Hat, Inc.
Ubuntu® is a registered trademark of Canonical Ltd.
Intel is a registered trademark of Intel Corporation.
All other products mentioned are trademarks or registered trademarks of their respective companies.
Text styles: Liberation Serif, Liberation Mono
Creation tools: LibreOffice
Contents
Table of Contents
Contents..............................................................................................................3
Welcome..............................................................................................................9
Contacts..........................................................................................................9
Import or Use Certificate................................................................................9
Overview of the User Guide.............................................................................10
Footnotes are used to direct you to additional reading locations.................10
System Recommendations............................................................................11
Operating Systems...................................................................................11
Disk Space...............................................................................................11
CPUs........................................................................................................12
Memory...................................................................................................13
Example...................................................................................................13
Real life for customers.............................................................................13
Overview of QDocSE 3.2.0..............................................................................15
What’s New in 3.2.0.....................................................................................15
What’s New in 3.1.2.....................................................................................15
What’s New in 3.1.0.....................................................................................16
What’s New in 3.0.2.....................................................................................16
What’s New in 3.0.0.....................................................................................17
What’s New in 2.1.0.....................................................................................18
What’s New in 2.0.0.....................................................................................18
Purpose of QDocSE......................................................................................19
Introduction to versions 2.0.0, 2.1.0 & 3.X.Y..............................................21
DataGuard (DG)...........................................................................................22
SecurityGuard (SG)......................................................................................23
Program and Library Monitoring............................................................23
File Integrity Monitoring.........................................................................24
File Auditing............................................................................................25
ProcessGuard (PG).......................................................................................25
Self Defence.................................................................................................26
Defending Critical Parts of the Operating System..................................27
Invalid Programs and SOs............................................................................28
Encrypting Data............................................................................................29
File-based Encryption..............................................................................30
Device-based Encryption.........................................................................31
Installation.........................................................................................................32
Installation Programs To Use.......................................................................32
New Installation (Standalone)......................................................................32
Obtaining and Applying a License..........................................................33
New Installation (with CSP).........................................................................34
Obtaining and Applying a License (with CSP).......................................34
Upgrade Installation.....................................................................................35
Upgrade from 1.X.Y................................................................................35
Upgrade from 2.X.Y or 3.X.Y.................................................................37
Uninstalling/Removing................................................................................39
Downgrading or Re-installing......................................................................40
Applying the License....................................................................................40
Renewing a License......................................................................................41
Elevation File...............................................................................................42
Spaces in Directory and File Names............................................................44
Locale Settings (Country and Language).....................................................45
Operating Modes...............................................................................................45
De-elevated mode.........................................................................................45
Elevated mode..............................................................................................45
Learning mode..............................................................................................47
Learning Mode and Long Running Processes (i.e. Services)..................48
Learning Mode Summary........................................................................48
Licenses.............................................................................................................50
License Types...............................................................................................50
Encryption only (TDE)............................................................................50
Data Integrity checking...........................................................................51
Data Integrity checking with Encryption (TDE).....................................51
Data and Program Integrity checking......................................................52
Data and Program Integrity checking with Encryption (TDE)................52
Data Protection with Encryption (TDE)..................................................52
Auditing with Encryption (TDE).............................................................53
Operating System (OS) Security.............................................................53
License Expiry..............................................................................................53
License Type Change...................................................................................54
Configuration Overview & Planning................................................................55
Overview......................................................................................................55
Planning........................................................................................................55
Downtime, Disk space, Time to complete...............................................55
Additional Actions...................................................................................57
Re-Configuring later................................................................................58
Simple Example.......................................................................................58
Extended Example...................................................................................59
New Files......................................................................................................61
Renaming Files.............................................................................................63
Remote Disk Drives.....................................................................................64
Local Disk Drives.........................................................................................66
Invalid Programs and SOs (Shared Object files)..........................................66
Authorized List........................................................................................66
Monitored Programs and SOs..................................................................67
Configuration Commands.................................................................................69
Help.........................................................................................................69
License Types..........................................................................................69
acl_add..........................................................................................................70
acl_create......................................................................................................73
acl_destroy....................................................................................................74
acl_edit.........................................................................................................75
acl_export.....................................................................................................76
acl_file..........................................................................................................77
acl_import.....................................................................................................79
acl_list..........................................................................................................80
acl_program..................................................................................................82
acl_remove...................................................................................................83
activate..........................................................................................................84
add_integrity_check.....................................................................................86
add_monitored..............................................................................................88
adjust............................................................................................................89
audit..............................................................................................................92
cipher............................................................................................................94
cipher_mode.................................................................................................95
commands.....................................................................................................96
device_encrypt..............................................................................................97
elevate...........................................................................................................99
encrypt........................................................................................................101
encrypt_pattern...........................................................................................105
finalize........................................................................................................106
hash.............................................................................................................107
install_prep.................................................................................................108
licence.........................................................................................................109
license.........................................................................................................109
list...............................................................................................................109
list_device_encrypt.....................................................................................111
list_handles.................................................................................................112
list_monitored.............................................................................................112
monitor_update...........................................................................................113
protect.........................................................................................................113
push_config................................................................................................118
regen...........................................................................................................119
remove_integrity_check.............................................................................119
remove_monitored......................................................................................121
renewcommit..............................................................................................123
renewrequest...............................................................................................124
set_access...................................................................................................125
set_learning................................................................................................126
setlearning..................................................................................................127
set_security.................................................................................................127
show_mode.................................................................................................128
stop_audit...................................................................................................129
unencrypt....................................................................................................130
uninstall_prep.............................................................................................132
update_integrity_check..............................................................................132
update_keys................................................................................................133
update_monitored.......................................................................................134
upgrade_prep..............................................................................................136
unprotect.....................................................................................................136
unwatch......................................................................................................138
verify_integrity_check................................................................................139
verify_monitored........................................................................................141
version........................................................................................................142
view............................................................................................................142
view_monitored..........................................................................................144
watch..........................................................................................................145
Programming Interfaces..................................................................................147
QDOC_IOCTL_VERIFY_FILE................................................................147
QDOC_IOCTL_PROT_FILE....................................................................148
Frequently Asked Questions (FAQ)................................................................149
Troubleshooting..............................................................................................152
Glossary of Terms...........................................................................................154
Appendix A: Command lists by licensed........................................................165
Appendix B: Database Examples....................................................................169
Instructions to Protect MySQL Server 5.6 and later..................................169
Prerequisite............................................................................................169
Procedure...............................................................................................169
Instructions to Encrypt Oracle 19.3 DB.....................................................170
Prerequisite............................................................................................170
Procedure...............................................................................................170
Instructions to Protect Oracle Enterprise 11G DB.....................................171
Prerequisite............................................................................................171
Procedure...............................................................................................171
Instructions to Protect SAP ASE 16.0 DB..................................................172
Prerequisite:...........................................................................................172
Procedure:..............................................................................................172
Instructions to Protect ProgressDB 11.7....................................................173
Prerequisite:...........................................................................................173
Procedure:..............................................................................................173
Appendix C: glob patterns..............................................................................175
Examples...............................................................................................177
Appendix X: copyrights..................................................................................178
The Regents of the University of California..............................................178
Welcome
Thank you for purchasing QDocSE 3.2.0 for Linux®. We hope this User Guide
will help answer all of your questions about installation, configuration and
security behaviour. In addition to the Table of Contents you just read there is
also a comprehensive Index at the end of this User Guide.
We recommend that you read through the User Guide completely before
starting to install or configure. The knowledge you gain beforehand will help
make your experience smooth.
Contacts
If you have questions that are not answered by this User Guide then please
contact: support@bicdroid.com.
If you have questions about purchasing QDocSE then please contact
sales@bicdroid.com.
You may also visit the BicDroid web site, http://www.bicdroid.com, to read
additional material, such as white papers, about QDocSE and other products
available.
The specific web site mentioned in this User Guide for obtaining a package, a
license file, a license renewal file, or an elevation file is:
https://qdocument.bicdroid.com.
Import or Use Certificate
Some countries, not all, require that software using ciphers must have an
import or use certificate (e.g. France). You should confirm for your location.
Overview of the User Guide
The User Guide is primarily a technical document for administrators. However,
having a good comprehension about the different aspects of QDocSE1 will help
when preparing the system, installing, configuring, and running.
This user guide assumes that you are already a competent Administrator of
basic tasks on Linux® systems.
We recommend you read through the complete User Guide at least once before
starting your installation or upgrade. This will help you make better decisions.
To help you read the User Guide here is a short list of meanings (in bold); the
Glossary has a complete list:
• QDocSE refers to version 3.2.0 unless explicitly stated
• QDocSEConsole refers to the command line utility
• DG is short for DataGuard
◦ DGFS is a file system to help implement DG
• SG is short for SecurityGuard
◦ SGFS is a file system to help implement SG
• PG is short for ProcessGuard
◦ PGFS is a file system to help implement PG
• bold monospace indicates shell command line usage in a sentence
• bold monospace indicates QDocSE command usage in a sentence
• monospace in example blocks indicates shell command line usage
• Comments between ‘{‘ and ‘}’ are not shell commands
Footnotes are used to direct you to additional reading locations.
Additional terms are described in the Glossary.
1 See page 15.
System Recommendations
The follow system recommendations are guidelines only. Many sites have
unique environments. If you have specific questions you may talk with your
sales representative, sales engineer or support who will try to provide answers.
Operating Systems
QDocSE is available for a wide variety of Linux® distributions beyond those
listed below. If you have a particular distribution in your environment not
listed then please contact sales.
Sample list of Linux distributions:
• CentOS 7.2 to 7.9 • CULinux
• Ubuntu 18.X, 20.X, 22.X, 24.X • HikVision OS
• Oracle Linux 7 & 8 • SUSE/OpenSUSE
• Kylin v10 • Euler OS
• NeoKylin • Red Hat Enterprise Linux
• UOS (UnionTech OS) 20
• Rocky Linux
Disk Space
There are several considerations regarding disk space. This is discussed again
later in the User Guide section Configuration Overview & Planning.
First there is the disk space used by the installation of QDocSE. The package
itself is approximately 4MB in size. The installation will take approximately
11MB of disk space.
Second is the disk space used by the QDocSE configuration. The amount of
space used by configuration is directly proportional to the number of files
being protected and encrypted. Each file encrypted will use an additional 2
disk blocks, usually 8KB, of disk space. For internal tables about 250 bytes per
file on average (depending on the length of the full pathname). As an example,
if you protect and encrypt 1000 files then approximately 6.5MB of additional
disk space will be used.
The third consideration is if you decide to increase the swap space for the
system. Swap space is used by programs in user space. The kernel does not use
swap space (it only uses real memory). Therefore additional swap space may
be useful during configuration when you have a large number of files to protect
(greater than 200,000).
A fourth consideration is the amount of free disk space available. A common
rule is that a disk should try to stay below 80% full. After encrypting files you
will still want to maintain the used disk space below 80%. There is an
appendix to this User Guide that has an example of working through this
calculation. Once your calculations are completed you may want to use the
Volume Manager to add more available disk space.
If you have an extreme amount of data to encrypt then the time to complete the
encryption will have a direct effect on what value you provide to the ‘-t’ option
of the activate and elevate commands to set the Elevation Time. For
example, if you estimate that encryption will take 36 hours then the value
provided to the ‘-t’ option should be longer than 36 hours for completion
reasons. You can always use the finalize command to move to De-elevated
mode earlier.
CPUs
The minimum your system should have available is 2 CPU cores.
CPU usage by QDocSE will mostly involve security evaluation and encryption-
decryption. Therefore there is a direct relationship between the number of
processes concurrently accessing protected and encrypted files (and at what
level of intensity) and the number of CPU cores required.
As a rule of thumb (which is a heuristic that may not match your environment)
for every 40 high-load processes that are read/writing we recommended an
additional CPU core.
Memory
The minimum your system should have available is 4GB.
Once configuration is completed then the majority of memory being used by
QDocSE will be allocated within the kernel (not user space). The kernel
memory is never swapped so the amount of swap available will have a minimal
effect on improving performance. The amount of memory used by QDocSE is
directly related to the number of files being protected (by the protect
command, not by encryption). If you are protecting fewer than 20,000 files
then very likely you won’t need more memory. We recommend an additional
1GB of memory if you protect more than 250,000 files (this should be good up
to 2 million files) that are regularly accessed.
Example
As a real life example, at BicDroid Labs we regularly protect more than 1
million files on a system with 2 CPUs, 4GB of memory and a 2TB disk (the
disk was at 20% capacity). The load is “medium” for resource usage (CPU and
memory) in user space. If there was more activity in user space then we would
have added more memory to reduce user space swap activity.
Real life for customers
Actual customer configuration information cannot be shared of course. But a
few interesting details about some of the known maximum statistics can be
shared. Please understand that these systems have additional memory and disks
to match these statistics.
The maximum number of files that have been converted from plaintext to
encrypted on the same system is more than than 14 million. The time to
process took about 220 hours for an average of 64,000 files per hour. The sizes
of the 14 million files varied but we were not informed of the total size.
However, based on our internal tests this would likely have a total size around
44TB.
Overview of QDocSE 3.2.0
The descriptions for What’s New for versions 2.0.0 and 2.1.0 are included for
completeness since there may be users upgrading from 1.4.X. Each sub-section
highlights the significant changes from the previous release.
What’s New in 3.2.0
This version includes the following changes and additions.
a) QDocSE Access Control Lists (ACLs) integrated into QDocSE security
with 10 specific, new commands for creating, editing and applying
ACLs: acl_add, acl_create, acl_destroy, acl_edit, acl_export,
acl_file, acl_import, acl_list, acl_program and acl_remove.
Other commands have been enhanced with options (encrypt and
protect commands), or display changes (view and list commands).
b) New command set_access.
c) Options added to view command.
What’s New in 3.1.2
This version includes the following changes and additions.
a) The ‘-excl’ option added to several commands.
b) Updated key material synchronization with CSP.
c) New command cipher_mode.
d) New command set_security.
e) New command update_keys.
f) New command encrypt_pattern.
g) New special option value with the device_encrypt command.
h) The device_encrypt now supports DMcrypt’s ‘cryptsetup’ from version 1.2.
What’s New in 3.1.0
This version includes the following changes and additions.
a) Encryption support added for block devices with new commands
device_encrypt and list_device_encrypt.
b) Number of parallel threads encrypting during configuration can be
manually overridden (‘-t’ option) with add_integrity_check,
encrypt and protect 2 commands.
c) Cipher SM4 using aarch64 (ARM) hardware acceleration extensions
added for all Linux kernel version supported by QDocSE. Contingent
on the accelerators provided by each CPU.
d) Support for additional Linux kernel versions and Linux distributions.
What’s New in 3.0.2
This version includes the following changes and additions.
a) Licensing model changes allowing customers to select having the
enhanced OS Security or not.
b) Cipher SM4 using x86_64 hardware acceleration for all Linux kernel
versions supported by QDocSE.
c) Relocated QDocSE configuration files to improve boot behaviour with
multi-disk systems.
d) Encryption option added to the add_integrity_command.
e) Improved support for ARM-based systems (aka aarch64).
f) O_DIRECT support added (used by many DBs).
g) The ‘-M’ option has been removed from commands. No limit now.
2 When ‘-e yes’ is specified.
What’s New in 3.0.0
This version includes a new licensing model, communication with a new CSP3,
three new major features and four minor feature adjustments. This is an
abbreviated list of those items. Longer descriptions occur later in this User
Guide.
a) A new licensing model allows customers to select which functionality
they want to be active.
b) The maximum available Elevation time has been extended from 90
days to 1096 days.
c) A new command named commands is available to list the active
commands based on the current license.
d) New encrypt-only and unencrypt-only commands.
e) Two sets of commands for file integrity monitoring. One set is for data
files, and the second set is for programs and shared libraries.
f) A set of commands for file auditing.
g) The list command display has been improved for readability and has
been updated for the new features.
h) A new list_handles command to display which running processes
have open files to a directory QDocSE will be protecting or encrypting.
i) The chkmntstatus command has been removed; it is no longer
required.
j) The setcollector and viewcollector commands have been
removed. The collector IP setting is now configured on the collector
(aka CSP).
k) A new message delivery system along with many new message types.
This reflects new features added in this release and to meet standards
requirements for QDocSE becoming certified.
3 Central Sentry Platform. Refer to the CSP User Manual for more information. This
replaces the previous collector of logging information.
l) Additional security enhancements for self-defence.
What’s New in 2.1.0
We have maintained this section for reference.
This version includes two minor changes, two new minor features and one new
significant change since the previous version. This is a list of those items.
Longer descriptions occur later in this User Guide.
a) The cipher used for encrypting files can now be selected. There is a
default cipher at installation based on your locale.
b) The setcollector command now allows for an alternate network
address.
c) The default Elevation time must be specified when a license or
elevation file is used. Previously it was always 24 hours. This is to
allow for more flexibility with configuration and Learning mode.
d) The set_learning command has been extended to accept the
arguments “on” and “off”
e) The list command output now displays “normal” for files that are not
protected.
What’s New in 2.0.0
We have maintained this section for reference.
Many new features and improvements have been implemented since the
previous version. This is a list of those items. For several items a longer
description occurs later in this User Guide.
a) Faster configuration by several factors
b) More files allowed to be encrypted
c) Stronger data file protection (DG)
d) Real-time monitoring of authorized programs and libraries (SG)
e) Authorized processes’ memory and file handles guarded (PG)
f) Multiple protection points improvements
g) Remote mount protection improvements
h) Self-defence to prevent being disabled, with self-verification
i) Security design with a “when an intruder...” not “if an intruder...”
implementation
j) Full defence against the administrator account for guarding against
possibilities of intruders and/or corrupted insiders
k) Extended system defence to help protect non-QDocSE parts of the
operating system (we are all in the same boat)
l) Better integration with SELinux
m) Variable size inode table for better performance with more compact
entries
n) Improved hashing functions
o) Security is self-enclosed (not relying on host system being up-to-date)
p) Single package installation
q) Available on more distributions
r) Various bug fixes
Purpose of QDocSE
Your computers are valuable to you. They are expensive pieces of hardware
connected together with network cables. They are so important that you keep
them in locked rooms with lots of A/C and security cameras. Very rarely
someone tries to steal this hardware, but if they do you can usually replace it
within a few days if not a few hours.
What is the more valuable to you is your data. Bad people are constantly trying
to get your data to steal or ransom it. Sometimes data can even be invaluable
because it can’t be replaced. You may have backups but restoring that data,
assuming it has not been corrupted, is time consuming and expensive. It won’t
be a few days; if backups restore successfully then the process has just begun.
It will be days, weeks or months of work to complete. Doing that could be a
very depressing effort. If you spend enough time, money and effort preparing
so you can restore everything within a couple of hours then you are likely in a
situation where each minute of downtime is costing millions of dollars. You
want to avoid downtime regardless of it being weeks, days or minutes.
Protecting your data must be your most important goal. The focus and purpose
of QDocSE is protecting data. If an intruder or malicious insider cannot
change, destroy or ransom your data then you can sleep easier. You can sleep
soundly when you know QDocSE is helping maintain valid access to your data
so your systems keep functioning. Perhaps even saving you millions of dollars.
QDocSE 3.2.0 is designed with the adage that it is when, not if, an intruder will
break into your system. There are many existing methods for an intruder to
gain access to your computer systems with new methods being discovered
daily. Imagine your computer system is your house. What if an intruder breaks
into your house and then he discovers he can’t steal anything, he can’t smash
anything and he can’t read your diary? All the intruder can do is wander
around aimlessly! That is part of QDocSE’s philosophic goal.
With data protection being the focus, file protection is just the beginning. The
security must expand to protect other pathways for getting to the data. This
means protecting the programs and libraries on disk with seamless, real time
monitoring (not periodic scans that leave gaps of opportunity). This also means
protecting the memory of running processes – validating running processes’
code too. It means that no user should have exceptional powers to access the
data on disk or in memory – security applies to everyone without exception.
Intruders turning off security programs and features has become commonplace.
QDocSE guards itself so it cannot be turned off. And it is done in-depth so that
even if one part is attacked there is another layer backing it up. Once set into
operational mode an intruder posing as the Administrator cannot re-configure
or turn off QDocSE.
Even QDocSE must run with the operating system. This means that the OS is
the next vulnerable point of attack for an intruder attempting to skirt around
security. Therefore QDocSE sets additional protections on key operating
system parts so an intruder cannot create modifications combined with reboot
as a bypass to security. With a Trusted Environment computer QDocSE
enhances security and helps make sure that computer is not compromised on
reboot.
Introduction to versions 2.0.0, 2.1.0 & 3.X.Y
QDocSE versions 2.0.0 & 2.1.0 represent a significant advancement in design
from earlier versions; this represents significant implementation effort as well.
QDocSE 3.0.0 added new features requested by customers and required by
some standards. QDocSE 3.1.0 adds more features and expands functionality of
some previous features. Therefore the following sub-sections provide
additional details to help you understand what is happening with different parts
of the QDocSE system.
We identify several different QDocSE security features as Guards. All Guards
communicate with the QDocSE Security Module (SM). Short descriptions of
each Guard follows. Together the Guards provide comprehensive security
protection over data-at-rest, data-in-use, limiting program access to data,
validating programs & shared libraries, shield running programs from
modification & data extraction, and more.
The final aspect of security is QDocSE’s self-defence. This is a collection of
features so that intruders that gain administrative privileges cannot turn off,
neutralize, or reconfigure QDocSE. A side-effect of these features is that it
extends security to other parts of the operating system resulting in a security
enhancement that is system-wide.
DataGuard (DG)
This Guard’s primary purpose is controlling access to protected data saved in
files. It works in conjunction with SG and the QDocSE Security Module (SM).
During configuration, files are added to the list of protected files. During this
configuration data-at-rest protection can be enhanced by having these files
encrypted.
Data files being protected can only be accessed by authorized programs.
Validation of authorized programs is handled by SG (more in the next section
for details). DG checks normal file access permissions, consults the SM and
asks SG if the program accessing the data is authorized and validated. If all
checks pass successfully then access is allowed. This control procedure means
that ransomware cannot double encrypt data files, and cannot exfiltrate data
either. This strict access control bridges data-at-rest and data-in-use protection.
Having files encrypted by QDocSE means enhanced data-at-rest protection. If
someone literally removes the disk then they will not have access to the data.
Decrypted access is only allowed for authorized and validated programs. The
authorized programs do not need any additional knowledge about the file being
encrypted so you do not need to modify your programs4.
Encryption and decryption is handled by DG. Every customer has a unique
master key for cryptography. This allows a site to easily share files among
different computers running QDocSE. Offsite locations (with a different master
key) cannot access the files even if they have QDocSE installed. As an
enhancement each encrypted file has a per file key so that if someone has the
computational power to crack the key of one file the other files remain
protected.
4 This is also known as transparent data encryption (TDE).
DG is implemented in part as a file system: DGFS. This means seamless, real-
time control over the access to the files. There are no timing gaps or windows
of opportunity.
The access control that DG provides prevents typical ransomware attacks
because the intruder’s encryption tool(s) has no access to these files. Similarly,
malware intent on damaging or changing data in these files is also blocked.
SecurityGuard (SG)
This Guard is responsible for checking programs and their shared libraries
once QDocSE is enabled, and validating QDocSE monitored data files. During
configuration each program added to the authorized programs list has a
signature created for it, and every shared library used by that program, plus
shared libraries used by those shared libraries, have a signature created. This
creates a comprehensive catalog that will be used later by SG to validate
running programs. Also during configuration your data files can have a
signature created to monitor their validity or integrity.
Program and Library Monitoring
There are many security products that calculate signatures for programs on
disk in a periodic scan. This periodic method leaves many gaps that are
windows of opportunity for a 2-Monty shuffle with a compromised program –
compromised by side-loading. Part of SG is implemented as the file system
SGFS which monitors the programs and libraries on disk in real-time
seamlessly. SG will immediately know when a change has happened on disk.
The commands related to SG have “monitor” as part of their names.
SG implements security better by confirming the signatures of the programs
and libraries when they are loaded into memory to be run. There is no window
of opportunity for a compromise. Once a program and the shared libraries are
loaded into memory then the security of the running program is provided by
PG (more about this in the next section).
SG reports each program’s validity to SM and DG so that permission to access
protected files is only granted to authorized, validated programs. SG operates
in a fail-safe manner. For example, if an intruder replaces one of your
authorized programs then SG immediately marks that program as invalid.
Even after a reboot SG knows that program is invalid. Invalid programs are not
allowed access to protected data files.
Currently SG does not stop an Administrator, also known as “root” or the
super-user, from changing files for programs and shared libraries. The
programs will be marked invalid if such changes happen (regardless of who
does it) and access to protected data will be denied. When program and shared
library files are restored to their original content matching the signatures then
validation can be successful again.
There are valid reasons for an administrator to update programs. For these
updates or changes to be recognized as valid requires QDocSE to accept the
changes. To accept any configuration change requires QDocSE to be in
Elevated mode5 and then the signatures of the authorized programs and shared
libraries to be recalculated. Refer to the commands verify_monitored and
update_monitored for more details6 about signature re-verification.
File Integrity Monitoring
A security variation of SG can be used for file integrity or file validity
monitoring. Integrity monitoring means the contents of a file are watched in
real-time, with no time gaps of opportunity, to confirm whether the contents
have been modified. If a modification does happen then a log message is
generated immediately and sent to CSP. If a modified file is restored then a log
message is generated immediately.
Integrity is not a 90 per cent thing,
not a 95 per cent thing;
5 See page 45; going into Elevated mode requires additional security steps.
6 See pages 145 and 135.
either you have it or you don’t.
-- Peter Scotese
With QDocSE file integrity, monitoring is a 100% thing. Other products do
periodic scans that are resource intensive and have large time windows of
opportunity – in even a single minute computers can perform a huge number of
operations. This is why QDocSE is designed to have zero opportunities for
malware to change and restore a file under integrity monitoring without it
being detected. QDocSE detects all changes 100% of the time while using very
few resources.
Each file has a digital signature calculated so that each file’s integrity can be
validated when the system is booted/re-booted. While the system is running the
File Integrity variation of SGFS means every write is known immediately
before it is applied.
File integrity monitoring is best applied to files that should not be changing. If
files are changing regularly then either protect or audit should be used
instead.
We do like to remind the reader that QDocSE’s protect command, with
DataGuard (DG), will stop unauthorized file modifications.
File Auditing
Tracking which users are accessing which files can be done, without using the
protect command, by using QDocSE’s audit commands: audit and
stop_audit. This generates a log message each time one of the files under
audit is opened but does not limit which programs can change the file contents.
ProcessGuard (PG)
This Guard is responsible for protecting running programs so that sensitive
data cannot be extracted or changed, and that code injections are not possible.
This protects programs regardless of which user is attempting to access the
running program. Only programs authorized to access protected data files are
under PG’s protection. This is data-in-use protection.
As a consequence of this PG protection some programs such as gdb 7 will not
function on running QDocSE authorized programs. Though programs such as
ps will continue to work, the information available about running authorized
programs will be very limited.
PG consults SM to know which programs are authorized. Then access to the
memory, executable code, the stack, file handles, etc. of each authorized
process is limited to the process itself. Any other process will be denied access.
This sometimes causes side-effects for non-authorized programs because they
cannot read the memory of other processes. But safety and security is our first
priority.
Self Defence
Just a few years ago intruders focused on working around, tricking or hiding
from security programs. Then intruders realized that if they have
administrative privilege they can just turn security programs off. Even when
external monitoring supports these security programs by providing alerts when
something is amiss, there is a time delay8. Plus, the administrator getting the
alert might be busy doing something else, or the administrator might literally
be sleeping at home. Worse yet, the intruder may have compromised the
external monitoring tool too!
As mentioned earlier in the User Guide, our philosophy is that it is when
intruders break into your system, not if they break in. And assuming the
intruder will be limited to an unprivileged account is wishful thinking.
Therefore each endpoint that has QDocSE has to be able to defend your data
completely on its own. Yes, there is external monitoring of each endpoint, but
7 gdb is an example of a well-known utility that can read and change the memory of a
running process; it can be used by bad actors to inject malware into active processes.
8 Remember, computers can complete a lot actions in 2 or 5 minutes.
security needs to be comprehensive and in-depth. This means each QDocSE
endpoint needs to prevent an intruder from disabling, tricking or re-configuring
QDocSE itself.
There are a variety of techniques QDocSE uses for self-defence including using
the Guards. Full self-defence is active when QDocSE is in De-elevated mode.
Being in De-elevated mode means no configuration can be changed, that active
security modules cannot be unmounted, unloaded or disabled, and key aspects
of other critical parts of the computer system also cannot be modified.
Security is not a static design and QDocSE’s self defence is subject to this
condition as well. Therefore it is important that when a new update of QDocSE
is available you install it as soon as possible.
There are specific files that QDocSE maintains with configuration information
that no user or program is allowed to access, other than QDocSE itself of
course. These files are labelled as special in the display of the list command9.
This is a strong level of security and self-protection maintained in Elevated and
De-elevated modes.
Defending Critical Parts of the Operating System
On different operating systems intruders have found novel ways around
security. While the intruders may have ways of directly attacking and/or
disabling some security programs, sometimes it is easier and faster to attack
the OS – why do more work when you don’t have to?
For example, some ransomware gangs attacking Linux® systems will modify
the GRUB files and reboot the system. The modifications they add include, but
are not limited to, encrypting your data during the boot process. This can be
efficient for the gang because all of the system’s resources are available for
their nefarious purpose(s), no security programs are active and no one can
login to stop this process. QDocSE protects the GRUB files (and other system
files) from being changed unless QDocSE is in Elevated mode. This way the
9 See page 109 for the list command.
intruders cannot ransom your OS via GRUB file changes – a reboot will simply
be a reboot using the original non-modified GRUB (and other) files.
We provide the same protection for some other system files too. BicDroid will
have additional enhancements in this area in future releases10.
As a consequence of protecting these OS files some administrative tasks must
now take place when QDocSE is in Elevated mode. This means obtaining an
elevation file to move into Elevated mode11. These are not administrative tasks
that will be changing daily or even weekly so the inconvenience is more than
balanced with the additional security. Professionally run IT operations already
plan and schedule their administrative tasks days or weeks ahead of time.
Therefore, planning ahead to obtain a QDocSE elevation file is a minor task.
So that you know which administrative tasks might be affected, these are the
type of OS protected directories where the content is now enforced as read-
only unless QDocSE is in Elevated mode:
• Boot directories
• Kernel object blacklist directories
• Kernel object load directories
• Configuration directories, including
◦ the SELinux configuration directory
◦ everything under the /etc directory
Others may be added in the future.
These system directories, and their files, are protected as read-only as part of
QDocSE’s self defence to prevent a malicious intruder, or insider, from turning
off QDocSE. System directories and files that are enforced as read-only by
QDocSE are labelled as shielded in the display of the list command12.
10 No, we’re not going to give bad people the ideas here.
11 See page 45.
12 See page 109.
Invalid Programs and SOs
As described above in the Security Guard (SG) section the signatures of
programs and Shared Objects (SOs) are verified when the program is being
loaded. If the program and/or one or more of the SO signatures are invalid then
the program is marked as invalid – the program will still run but it is denied
access to all protected data files.
You can start your investigation using the QDocSEConsole utility’s and
view
verify_monitored commands. You can use the view command to check that
the program is in the list of programs allowed to access protected data files.
You can use the verify_monitored command to show which programs
and/or SOs have changed signatures.
If the program is not in the authorized list then you will need to have QDocSE
in Elevated mode to authorize the program using the adjust command.
If the program and/or one or more of the SOs have a changed signature then
you may have a security problem. Some action has changed the program
and/or SO file which has resulted in a new and different signature. Security
Guard (SG) will not validate it. You need to start an investigation to determine
if the change is valid and safe, or if the change is unexpected and possibly
malicious.
If you determine that the change is valid and safe then you will need to update
the signatures QDocSE considers valid. Do not be hasty! Double-check and
triple-check. You do not want to be tricked or fooled. Be aware that someone
may use Social Engineering to trick or pressure you into accepting the changes.
If the change is unexpected then your system may have been compromised.
There are security features that QDocSE provides for self-protection that makes
it harder for malware such as digital currency miners and C2 programs to hide
and make changes to the system. The design and implementation of QDocSE is
to continue to protect your data even when an intruder with malware has
entered your system, but you still need to take action! A complete description
about what actions you should take is beyond the scope of this User Guide.
Encrypting Data
With QDocSE there are two methods of encrypting data: file-based encryption,
and device-based encryption. File-based encryption can be done with the
encrypt and protect commands13. Device-based encryption can be done with
the device_encrypt command14.
Encryption is performed using the default settings for the cipher and cipher
mode. The default cipher and default cipher mode are set at installation based
on your computer’s language settings. These defaults can be changed using the
cipher and cipher_mode commands respectively.
The time needed to complete encryption is based on the total number of bytes
of data, the cipher, the cipher mode, CPU performance, memory available, and
disk speed.
File-based Encryption
QDocSE provides transparent access to encrypted data in files. This means that
existing programs do not need to be modified to read plaintext from the file
when they are Authorized to access. Non-Authorized programs are denied
access. With several of the licenses all programs are Authorized. With any
license that includes Protection, programs must be specifically added to the
Authorized list with the adjust command15. Of course, normal system access
controls must still be met.
Every encrypted file has two sections: a data section and a metadata section.
The data section contains an encrypted version of the plaintext data. The
metadata section contains information about how the data section is encrypted.
13 See pages 101 and 113.
14 See page 97.
15 See page 89.
Every file has a unique File Encryption Key (FEK) that is not known to
anyone. The FEK is kept securely within the metadata section by encryption
using a key called the Effective File Encryption Key (EFEK). This is an
industry standard practice. The EFEK is managed by QDocSE and CSP. A new
EFEK can be supplied by CSP to QDocSE and then applied quickly to all
encrypted files through an update procedure. Industry best practices
recommend this EFEK update happen at regular intervals or when there has
been a security issue.
Device-based Encryption
QDocSE provides transparent access to encryption data in block devices. This
means that existing programs, or file systems mounted onto a block device do
not need to be modified to read plaintext from the block device. The block
device is encrypted as single whole unit.
A File Encryption Key (FEK) is used to encrypt the block device. Similar to
the file-based encryption, the FEK is kept within metadata using an Effective
File Encryption Key (EFEK) that is managed by QDocSE and CSP.
Installation
Installation Programs To Use
We currently recommend using only the utilities rpm and dpkg for installing
and upgrading the QDocSE software packages. When using rpm or dpkg then
only QDocSE will be installed and no other packages will be installed or
upgraded as a side-effect. This is important for many sites wanting to maintain
a stable and unchanged configuration. In contrast, the utilities yum and apt will
usually try to download and install updates for many other packages.
rpm is used with Red Hat and Red Hat derived systems such as CentOS and
Oracle Linux. dpkg is used with Debian derived systems such as Ubuntu.
The one exception for upgrading a package is when you will be using the
device_encrypt command to encrypt a block device. Having the cryptsetup
package at version 2.0 is a minimum requirement in order to have DMcrypt
support.
There are 2 slightly different installation situations: (A) standalone, and (B)
with CSP. Each is described in its own section below.
Note: If you are changing your license type then use the same instructions as a
New Installation.
New Installation (Standalone)
Starting with QDocSE 2.0.0 there is a single package file used for installation16.
The package file’s name will end in either “.rpm” or “.deb” depending on the
distribution of Linux® you are using. This remains true for QDocSE 3.2.0.
16 Yes, this includes QDocSE 2.1.0 and 3.X.Y.
The assumption is that you, as the administrator, have already gone through
install planning earlier. Refer to that specific section in this User Guide for
details17.
NOTE: If you decide to uninstall an existing version of QDocSE and do a
“fresh” install of QDocSE then you will lose your existing configuration.
Starting with QDocSE 3.0.2 the package is obtained directly from the BicDroid
Sales Engineer or from the CSP. Earlier versions were obtained from the
BicDroid website but this no longer happens.
On RPM-based systems (includes CentOS):
rpm -i ./qdocse-3.2.0-1.x86_64.rpm
On Debian-based systems (includes Ubuntu):
dpkg -i ./qdocse-3.2.0-1_amd64.deb
NOTE: You will need to run the commands above using the sudo utility if you
are not using the administrator account (aka “root” or super-user).
Obtaining and Applying a License
Once the QDocSE installation has completed you will need to apply a license.
The steps are:
1. Login to the license website:
https://c.bicdroid.com:7777/#/login
2. Select from the menu on the left edge “My Licenses”,
3. From the top of the page select the button “New License”,
4. Upload the QID to the web server from the file “/qdoc/conf/qid.txt”,
5. Click the button to generate the matching license file,
17 See page 55. The installation section comes before the planning section because knowing
the installation procedures will help with the planning.
6. Download the license (or activation) file to the QDocSE machine,
7. Now use that activation file.
QDocSEConsole -c activate -af ActivateFile -t 9d
Once the license has been installed then QDocSE will automatically be placed
in Elevated mode. In the example above Elevated mode will last for 9 days.
You can now configure and use QDocSE with the command line at the installed
machine.
New Installation (with CSP)
These instructions assume that you are using CSP version 5.0 or later, and that
CSP is already running.
A self-enclosed shell script will be provided by the CSP to match your system.
This script includes the QDocSE package and information about the CSP
installation. The script knows which installer to use. Now run the script:
sh ./qdocse.sh
Once installation is complete then QDocSE will contact CSP and send some
information. You will need to go to the CSP and find the panel “Engine
Category”, “Inactive”. On this panel click the “Activate” button which will
download the CSP version of the QID file18 for the QDocSE just installed.
A pop-up window should now appear to obtain the license by downloading.
Obtaining and Applying a License (with CSP)
The steps are:
1. The CSP pop-up window should re-direct you to login to the license
website: https://c.bicdroid.com . c n :7777/#/logi n
2. Select from the menu on the left edge “My Licenses”,
18 CSP modifies its copy of the QID file.
3. From the top of the page select the button “New License”,
4. Upload the CSP version of the QID file to the web server,
5. Click the button to generate the matching license (or activation) file,
6. Download the license (or activation) file to the QDocSE machine,
7. Now use that activation file.
QDocSEConsole -c activate -af ActivateFile -t 9d
Once the license has been installed then QDocSE will automatically be placed
in Elevated mode. In the example above Elevated mode will last for 9 days.
You must now connect QDocSE to the CSP using the csp-passphrase. Run the
command:
QDocSEConsole -c csp_passphrase
You will be prompted twice for the passphrase. The second time is to confirm
you entered it correctly the first time.
You can now configure and use QDocSE from both the CSP and the command
line on the installed machine.
Upgrade Installation
Upgrading QDocSE is different when upgrading from version 1.X.Y versus
upgrading from 2.X.Y and 3.X.Y. The first variation is with QDocSE version
1.X.Y (e.g. 1.4.3) and the second variation is with QDocSE version 2.X.Y or
3.X.Y. There is more security with the 2.X.Y and 3.X.Y versions so more steps
are required to work with this security.
Upgrade from 1.X.Y
As the administrator (aka “root”) you can run the upgrade with very few steps.
You may leave QDocSE 1.X.Y in De-elevated mode, or have it in Elevated
mode.
You can download the new package the same way as a New Installation
described earlier in this User Guide. Once your system is in a safe state then
you can upgrade QDocSE.
Before upgrading read the NOTE below about long-running programs so you
can have the system in a safe state.
You can use the following recommended commands:
On RPM-based systems:
rpm -U ./qdocse-3.2.0-1.x86_64.rpm
On Debian-based systems (includes Ubuntu):
dpkg -i ./qdocse-3.2.0-1_amd64.deb
NOTE: You will need to run the commands above using the sudo utility if you
are not using the administrator account (aka “root”).
A package named public-stackable-filesystem was installed as part of
version 1.X.Y. This package is no longer required with QDocSE 2.0.0 or 3.0.0
and you should remove it now:
On RPM-based systems:
rpm -e public-stackable-filesystem
On Debian-based systems (includes Ubuntu):
dpkg -r public-stackable-filesystem
During the upgrade all programs in the authorized programs list will have their
signatures calculated and all of the SOs used by these programs will have their
signatures calculated as well. This will provide full SG security on the
programs and SOs. All previously protected files will continue to be protected
by DG.
NOTE: If you have any long running programs, daemons or services running
that are authorized programs with version 1.X.Y then you will need to stop
these programs before running the upgrade command19. This will ensure the
full security cycle has been performed. A more detailed explanation is in the
section Learning Mode and Long Running Processes20. Stopping the long
running program or service will also allow the QDocSE drivers and file
systems to be changed to the newer, better versions.
If you want to do any configuration changes at this time then you will need to
obtain an elevation file. Refer to the Elevation File section later in this User
Guide21.
Because of the new features added with QDocSE 2.0.0 and 3.0.0 you may want
to do some configuration changes or enhancements.
Upgrade from 2.X.Y or 3.X.Y
The self-defence features available with QDocSE 2.X.Y and 3.X.Y mean that
an upgrade can only be accomplished when QDocSE is in Elevated mode.
Once in Elevated mode, but before starting the upgrade, you must issue the
install_prep command22, and reboot. Certain features of security can only be
turned off with a reboot after the install_prep command has been run.
NOTE: Before issuing the install_prep command you should stop any long
running programs, daemons or services running that are authorized programs.
A more detailed explanation is in the section Learning Mode and Long
Running Processes23.
Security NOTE: When you issue the install_prep command it will become
active after the reboot.
Security NOTE: When you issue the install_prep command it will only be
valid for a maximum of 15 minutes with version 2.X.Y and a maximum of 40
19 For example, to stop a service do “systemctl stop XXX” where XXX is the service name.
20 See page 48.
21 See page 42.
22 See page 108.
23 See page 48.
minutes with versions after 3.0.2. If a reboot happens after 15/40 minutes then
the install_prep command will have expired. If you reboot within those 15/40
minutes but do not do an upgrade then QDocSE will have full security
established at the end of the 15/40 minutes.
The upgrade steps/commands for all distributions are:
{ obtain elevation file }
{ download upgrade package file }
QDocSEConsole -c elevate -ef ElevationFile -t 1d
QDocSEConsole -c install_prep on
{ reboot }
then, after boot, either do
rpm -U qdocse-3.2.0-1.x86_64.rpm
or
dpkg -i qdocse-3.2.0-1_amd64.deb
{ perform any configuration changes if needed }
QDocSEConsole -c finalize
NOTE: You will need to run the commands above using the sudo utility if you
are not using the administrator account (aka “root”).
An upgrade cannot take place while QDocSE is in De-elevated mode. Full
security is activated and, as such, even QDocSE cannot turn portions of itself
off. If security doesn’t apply to everyone, including QDocSE, then how strong
is it (or isn’t)?
If, during the upgrade, you see a message about QDocSE needing to be in
Elevated mode then the elevate command must not have been successful.
Similarly if you see a message that install_prep has not be run then you
missed this required step.
Uninstalling/Removing
Performing a removal or uninstall can only be accomplished when QDocSE is
in Elevated mode. This is part of the self-defence security. Once in Elevated
mode but before starting the removal you must issue the install_prep
command24, and reboot.
Warning: Uninstalling will not decrypt files. Before uninstalling you must use
the unprotect and/or unencrypt commands25 to remove protection and
decrypt files.
You should plan the uninstall in the same manner that you planned the install.
You should ensure that the files are not in use, particularly if they need to be
decrypted, so that no data corruption happens.
The removal/uninstall commands for all distributions are:
{ obtain elevation file }
QDocSEConsole -c elevate -ef ElevationFile -t 1d
{ commands to decrypt any encrypted files }
QDocSEConsole -c install_prep on
{ reboot }
then either
rpm -e qdocse
or
dpkg -r qdocse
NOTE: You will need to run the commands above using the sudo utility if you
are not using the administrator account (aka “root”).
24 See page 108.
25 See page 131.
While not required, we recommend an additional reboot of the system after the
successful removal of the QDocSE package.
During removal if you see a message about QDocSE needing to be in Elevated
mode then the elevate command must not have been successful.
Downgrading or Re-installing
Do not attempt to downgrade from QDocSE 2.X.Y or 3.X.Y to an earlier
version. This is not supported.
Do not attempt to re-install the QDocSE 2.X.Y or 3.X.Y package. This is not
supported for security implementation reasons. You would need to perform a
remove or uninstall, and then perform another install.
Applying the License
With a new installation QDocSE is not fully active and cannot be configured
until a valid license is applied.
If the installation of QDocSE is done with the new CSP then CSP will handle
the licensing.
The license being applied will determine which commands are available. There
are several commands that are always available while others are only active
with a particular license type. The command descriptions indicate when each
command will be available. Your license can have one or more license types
combined together26.
With a successful installation a special file is generated named
“/qdoc/conf/qid.txt”. The content of this special file is unique to each
installation. That is, with each system or endpoint that QDocSE is installed on
the content of this special file will differ meaning each license file will be
unique to a specific system.
26 Refer to your sales representative for more information.
There are several steps to applying a valid license:
1. Provide the /qdoc/conf/qid.txt” to the license generation program.
2. Generate the new license.
3. Download the license file to the specific endpoint. Note that this
license file may also be referred to as an activation file by BicDroid
Support.
4. Apply the license using the activate command:
QDocSEConsole -c activate -af LicenseFile -t 5d
5. Observe that the license is successfully applied. If it is not successful
then please read the Troubleshooting section on page 152.
You should now be in Elevated mode27 and be able to configure QDocSE. See
the section Configuration Overview and Planning on page 55.
If you have a problem then please refer to the Troubleshooting section on page
152 or contact BicDroid Support.
NOTE: The “-t 5d” above indicates that Elevated mode will last for 5 days.28
NOTE: For security reasons you should delete the license file once it has been
successfully used. Once a license file has been used it cannot be reused.
Renewing a License
Licenses for QDocSE are typically valid for 180 to 1096 days depending on
your sales agreement. To have seamless security coverage it is best to apply a
new or updated license before the current license expires.
You can obtain a new or updated license using the same method you used for
the original license. Of course you must make arrangements with BicDroid
Sales beforehand for this to succeed.
27 See page 45.
28 See page 84.
If you are using CSP then refer to the CSP documentation for instructions.
If you are using the license generator then you will perform the following
steps. Issue the renewrequest command29 to create a special text file that will
be uploaded to the license generator:
QDocSEConsole -c renewrequest -rf renew_output.txt
Provide the renew_output.txt file to the license generator, and have the license
generator create the renewal license file. Now download the new license file to
the local system.
The final step on your local system is applying the new licence. To apply the
new license while a previous license is still active you will use the
renewcommit
command30.
QDocSEConsole -c renewcommit -cf NewLicenseFile
where “NewLicenseFile” is the file just downloaded.
When successful you will be in Elevated mode (see page 45 for details) and be
able to configure QDocSE. You may perform configuration changes or use the
finalize command to leave the configuration unchanged.
QDocSEConsole -c finalize
If you have a problem then please refer to the Troubleshooting section on page
152 or contact BicDroid Support.
NOTE: For security reasons you should delete the license file once it has been
successfully used.
Elevation File
An elevation file is similar to a license file but leaves the time length of the
license unchanged. This allows you to change QDocSE from De-elevated mode
29 See page 124.
30 See page 123.
to Elevated mode. This must be done if you want to change or update the
configuration of QDocSE or the system (when OS Security is active).
NOTE: This is a security procedure.
After an elevation file is applied then Elevated mode will last until the
Elevation Time31 expires (set by the ‘-t’ option with the elevation command).
You can issue the finalize command32 earlier to return to De-elevated mode.
You will want to update the configuration if you need to update any of the
authorized programs or the shared libraries they use. Updated programs and
shared libraries will have different signatures. When the signature of an
authorized program or shared library has changed then QDocSE will block that
program from accessing protected data. Putting QDocSE into Elevated mode
and accepting the new signatures is you stating that you trust the changes.
You can obtain an elevation file in a manner similar to how you obtain a
license file: it may be done via CSP or with the license generator.
If you are using CSP then refer to the CSP documentation for instructions.
If you are using the license generator then you will perform the following
steps.
Upload the QID file, “/qdoc/conf/qid.txt”, from the system you want to Elevate
to the license generator. Then have the license generator create an elevation
file.
You can use each elevation file once only -- it cannot be used a second time.
If, or when, you need to move to elevation mode again you must obtain a new
elevation file. This is part of the security procedures with QDocSE to protect
against intruders or malicious insiders that have gained access to the
administrator’s account.
31 See page 46.
32 See page 106.
When you have downloaded the elevation file you can apply it with the
elevate
command33.
QDocSEConsole -c elevate -ef ElevateFile -t 1d
Needing to obtain an elevation file effectively results in a method of 2-factor
authentication because whoever is using the administrator account (aka root)
must go through an intentionally disruptive set of actions to get the elevation
file. This prevents a intruder who gains Administrator privileges from turning
off or adjusting QDocSE security. A malicious insider must go through the
same process and, because of this security intention, we recommend that the
person at your company with the authority to obtain a license or elevation file
be different from the person doing the system administration.
NOTE: For security reasons you should delete the elevation file once it has
been successfully used.
Spaces in Directory and File Names
Typically on UNIX® and UNIX®-like systems users will avoid spaces in
directory and file names because of the need to escape the spaces and/or
enclose the name within single quotes. However, with the use of GUI programs
spaces occur more often in names than when using a command line in a shell.
QDocSE can handle spaces in both directory and file names. You will need to
escape space characters so that the shell will not interpret the space or use the
space as a field separator. An example of using the backslash to escape spaces
in a filename is:
cat name\ with\ spaces
Understand that we are not encouraging you to start using spaces in your
directory and/or file names. We are merely stating that we can handle the use
of spaces in directory and/or file names.
33 See page 99.
Locale Settings (Country and Language)
During installation the locale setting for the system will determine the default
cipher for file encryption. The default locale when installing most Linux
distributions is the United States and English. To meet encryption standards in
your region it is best to set the locale to your actual location and language.
Operating Modes
There are three modes of operation for QDocSE: De-elevated mode, Elevated
mode, and Learning mode. These modes are only relevant when QDocSE is
fully licensed. There are several different license types that you can read about
in the Licenses section on page 50.
De-elevated mode
This is the normal operating mode after configuration has been completed.
This is the mode that full security is active for OS Security.
Configuration settings cannot be removed or changed. Additional directories,
depending on the license type, can still be added.
Access to protected data files will limited to authorized programs only.
Authorized programs and the shared libraries those programs use will be
monitored for validity. If CSP or a collector has been configured then
messages are being sent from QDocSE about successful and unsuccessful
access attempts along with a heartbeat34.
Elevated mode
In this mode QDocSE can be configured.
34 Messages are not sent to BicDroid. The collector is installed at your site.
In this mode OS Security is reduced so configuration can happen.
Data files can be added or removed from the protected lists. Authorized
programs, along with shared libraries, can be added or removed from the
validation/signature lists, a collector can be set/reset, Learning mode can be
activated, etc.
The maximum length of time that Elevated mode lasts is set by the ‘-t’ option
to the activate and elevate commands (this is called Elevated Time). The
start of Elevated Time is when the activate or elevate command is
performed. When the Elevated Time expires then QDocSE will move to De-
elevated automatically from both Elevated and Learning modes.
In Elevated mode several aspects of security are disabled so that the
configuration can be changed. QDocSE will automatically move to De-elevated
mode for security reasons when the Elevated time expires35. You can also
explicitly move to De-elevated mode with the finalize command36 using
QDocSEConsole.
If you have made any changes to configuration for authorized programs and/or
shared libraries then remember to issue the push_config command37 with
QDocSEConsole to update QDocSE. Issuing the finalize command38 will also
cause push_config to be done, but no further configuration changes can
happen after finalize.
QDocSE will be in Elevated mode after the license has been successfully
applied. If QDocSE has moved into De-elevated mode then you will need to
obtain an elevation file39 to move into Elevated mode.
All commands available for a license can be used in Elevated mode.
35 Yes, we are repeating this point but it is important.
36 See page 106.
37 See page 118.
38 See page 106.
39 See page 42.
Learning mode
This operating mode is an enhanced version of Elevated mode. If the Elevated
Time has expired then Learning mode cannot be active.
In this mode security is reduced so configuration can happen (same as with
Elevated mode because this is part of Elevated mode).
Learning mode helps you configure QDocSE automatically. This can be very
helpful with complex systems where it can be difficult to determine which
programs are using the protected data files.
Learning mode determines which programs are accessing the protected data
files by watching for new opens to these files. Then the program doing the
open is added to the list of authorized programs. If a program is running before
Learning mode starts and this program already has a file open then Learning
mode will not detect it. Therefore you should re-start these types of programs
after changing to Learning mode.
In Learning mode you run all of the programs that you normally do. QDocSE
will notice which programs are accessing protected data files and add them to
the authorized list of programs. You can review the list of authorized programs
and explicitly remove and/or block programs that Learning mode has added.
You can move between Learning mode and Elevated mode, and back again,
using the set_learning command40 with QDocSEConsole.
Like Elevated mode, QDocSE will automatically move from Learning mode to
De-elevated mode for security reasons when the Elevated Time has expired.
Learning mode can only be active while the Elevated Time has not expired.
For example, if during the license activation you set the Elevated time to 48
hours then this is the maximum time that you may be in Learning mode too.
This same logic applies when an Elevation file is used and an Elevation time is
set.
40 See page 126.
Using the finalize command will also end Learning mode because it ends
Elevated mode. A push_config command is done when Learning mode ends
by the finalize command or when the Elevated Time has expired.
Learning Mode and Long Running Processes (i.e. Services)
Long running processes are often daemons or services, but can also be any
process that will run for a long period of time. These are often running to
support e-mail, databases, webservers, etc. For QDocSE we are interested in
the long running processes that will be accessing protected data files. These
programs will need to be added to the list of authorized programs. Learning
mode makes it easier to determine these programs.
However, since these long running programs started running before QDocSE
was installed, QDocSE hasn’t verified that program and its SOs when it was
loading. Thus no validation could be done. QDocSE can only validate a
program when it is being loaded.
Therefore long running programs will need to be re-started (stopped and a new
instance started/loaded) once Learning mode has been completed41. This way a
new instance of the program is loaded which will be evaluated by SG and then
protected by PG. Note that same situation happens when an upgrade from
QDocSE 1.4.X happens because 1.4.X does not have the Guards (SG, PG, and
DG).
If you do not restart the long running programs then QDocSE will deny access
to the protected data files.
The list_handles 42 command can be used to identify running programs that
have open files under directories monitored by QDocSE.
Learning Mode Summary
This is a brief review of the steps described above:
41 After either push_config or finalize has happened.
42 See page 112.
1. Be in Elevated mode.
2. Use list_handles command.
3. Stop long running programs (so Learning mode sees new opens).
4. Change to Learning mode.
5. Protect data files.
6. Use/re-start the long running programs so Learning mode sees the
relationships.
7. Leave Learning mode to Elevated mode (this will do push_config)
with the command “set_learning off”.
Licenses
License types are used to select which QDocSE functions are active. Most
commands are not available until a license is activated or applied after QDocSE
is installed.
Activating or applying a license is described in the section Obtaining and
Applying a License on page 33.
License Types
For QDocSE the available license types are:
1. Encryption only (aka Transparent Data Encryption)
2. Data Integrity checking
3. Data Integrity checking with Encryption (TDE)
4. Data and Program Integrity checking
5. Data and Program Integrity checking with Encryption (TDE)
6. Data Protection with Encryption (TDE)
7. Auditing with Encryption (TDE)
The license types listed above can also have Operating System (OS) Security
added. Each license type, and OS Security are described below.
Encryption only (TDE)
Data files can be encrypted providing data-at-rest security. While QDocSE is
running any program accessing an encrypted file will do so transparently. The
encryption of data files is transparent to the programs consuming the data; the
programs only read and write the unencrypted data. Encryption and decryption
are handled transparently by QDocSE without program involvement. This
permits existing programs to access encrypted files without modification or
upgrade. This means existing programs require no change. This is often
referred to as Transparent Data Encryption (TDE).
Encryption ciphers available are described with the cipher command43. This
allows you to select your preferred cipher. A default cipher is chosen at
installation based on the country your system is located within.
Under specific directories, chosen by you, files will be encrypted. At initial
configuration you can chose all files or specific files to become encrypted. Any
new files added to these directories will become encrypted. Some file types,
such executables files, will not be encrypted.
Data Integrity checking
Data files will be examined to produce a unique signature for each file under
directories that you specify. Executable files, also known as programs, are not
data files and therefore are not part of this license.
If someone modifies the content of one of these files then the signature for that
file is marked as invalid. If that file is modified back to its original content then
it will be marked as valid again. When the content of a file is changed then
messages are sent to CSP.
If the content change of a file is intended, then its signature can be updated to
produce a new valid signature.
New files created under one of these directories will not have a signature.
Data Integrity checking with Encryption (TDE)
This is the same as Data Integrity checking (see above) with the option of
encrypting all or selected data files. Encrypted files are accessed as
Transparent Data Encryption (TDE).
43 See page 94.
Data and Program Integrity checking
This is the same as Data Integrity checking (see above) plus integrity
checking of program files (executables) and the shared libraries those
programs use.
Program Integrity is greater than just an individual file. Programs are usually
comprised of an executable file plus all of the shared libraries that the program
uses. For a program’s integrity to be valid all of its parts must also be valid.
For example, if a program uses 4 different shared libraries then the integrity of
the running program is the program itself plus each of the 4 shared libraries
with each having an individual signature. When this program is run then all 5
signatures must be valid for the running program to be valid. When a program
is not valid then messages are sent to CSP for each and every part that is not
valid.
Data and Program Integrity checking with Encryption (TDE)
This is the same as Data and Program Integrity checking (see above) with
the option of encrypting all or selected data files – programs and shared
libraries will not be encrypted.
Programs and libraries that are intentionally updated can have their signatures
updated.
Data Protection with Encryption (TDE)
Data Protection limits access to specific data files by programs in an
authorized list. Programs in the authorized list have their files and the shared
libraries used under Program Integrity. Authorized programs that are not
valid are not allowed to access the protected data files.
Data files under protection can be encrypted for TDE access and data-at-rest
security.
Auditing with Encryption (TDE)
This is a method of monitoring data files under directories you have chosen.
When an audited file is opened by a program then a message will be sent to
CSP. Data files being audited can be encrypted for TDE access and data-at-rest
security.
Operating System (OS) Security
The license types described above can provide monitoring, alert messages and
access protection within a specific scope of security. As long as QDocSE is
running without interference then it will provide the functionality described
with each license.
However, if an intruder accesses your system and obtains the power of the
super-user (aka “root”) then there are actions this bad guy can do to stop or by-
pass QDocSE (when there is no OS Security). With OS Security added to your
license then the bad actions of an intruder against QDocSE and the system in
general can be prevented. OS Security uses multiple methods to provide data
security and system security so that you have data-in-use, data-at-rest and
reboot security (enhancing secure boot).
License Expiry
When your license expires you are encouraged to renew your license with your
BicDroid Sales representative.
An expired license means that full functionality of QDocSE will not be
available. When a license expires then the following functionality will no
longer be available:
• alert messages to CSP will stop (integrity, protect & audit)
• signatures for data and program files will not be monitored
• data file protection will no longer apply (no access restrictions)
• new data files will not be encrypted
• new data files will not be protected
Note that encrypted files will continue to have TDE access because QDocSE
will not block you from reading your own data. However, if you uninstall
QDocSE without decrypting your files then your programs will not be able to
read the files as plaintext.
License Type Change
It is possible to change the type of license you are using with QDocSE. After
you have spoken with your BicDroid sales representative then the QDocSE
website that you downloaded license files from will be updated for the license
change. Go through the same procedure described in the section Obtaining
and Applying a License on page 33 using the activate command.
Configuration Overview & Planning
Overview
For most customer sites the configuration will be straight-forward. The
organization of your computers likely already has data files to be protected
grouped together under one or more directories that are separate from
directories that the programs and shared libraries are located in.
QDocSE cannot mix protected data files and authorized programs in the same
directory. You will need to move them into separate directories if you currently
have both in the same directory.
We recommend that you do the installation when the system is not in use. This
will (a) provide a faster installation, and (b) a clearer configuration. When
none of the files to be protected are being read from, written to, created,
deleted, etc. then it will be clear what has and has not been protected and/or
authorized.
If you are going to use Learning mode then remember that it has a maximum
use time based on the Elevation Time44. Therefore you should install just
before the start of a normal work day and set the Elevation Time based on the
time to configure and/or how long you need Learning mode to be active. Even
with Learning mode you will need to specify manually the directories/files that
need protection.
Planning
Downtime, Disk space, Time to complete
This is the window of time when the system will not be used and
configuration, which can include file encryption, will take place. You can
44 See page 46.
prepare for the downtime by learning ahead of time which directories/files
need protecting, and which programs access those files. If you do not already
know which programs access the files you will be protecting then you may
want to use Learning mode or list_handles command to determine the
programs.
Downtime is best used for specifying the directories/files to be protected and
optionally encrypted with the QDocSEConsole utility. Without too much
surprise, encryption will be what takes the longest time to complete.
The time to protect 1 million files under a single directory will take between 15
seconds and 1 minute depending on the speed of the system, the organization
of the directory and the size of the files. In short, there is not a lot of downtime
to account for when just protecting directories/files (no encryption).
The time to encrypt will depend on the number of files and the total size of all
of the files. It will also depend how much load the system is experiencing for
non-QDocSE activities. QDocSE uses as much CPU and disk throughput as it
can to try and finish the encryption as quickly as possible.
It is best practice to have none of the files to be protected and/or encrypted in
use during configuration because this will prevent data corruption and/or data
loss. During configuration QDocSE reads the original unencrypted file and
writes the encrypted version in a temporary file. When encryption finishes the
temporary file is moved to replace the original file. If a user is writing changes
to the original file during encryption then these changes may be lost partially
or completely which could cause data corruption.
You will need to have additional space on the disk to handle encrypted files
being slightly larger and for the temporary encrypted copies. The disk should
be no more than 80% full for typical performance reasons.
QDocSE will currently encrypt 6 files or more in parallel to maximize disk, file
system throughput and CPU usage. The specific number is based on the
number of CPU cores the system has.
When you know the files that will be protected and encrypted you should
calculate the space they currently use, and count the number of files. This
information can be used to make a time estimate. As a professional
Administrator you likely already know the tools you can use to obtain this
information but for other readers we will suggest reading the manual pages for
the utilities du,wc and/or perl.
For example:
du -hs /usr/local/data1
ls -1R /usr/local/data1 | wc -l
will provide the total space used and then the number of files and directories.
These are estimates that will be close enough for our calculations45. Assume du
returned “10G” and the second command line returned “2000”. This means we
have approximately 2000 files using approximately 10GB of space.
The file processing overhead is the same regardless of the size of the file. For
2000 files on a 2 CPU core VM of CentOS 7.6 the overhead is approximately
0.9 seconds. For 10GB being encrypted over 2000 files the time to complete
everything, including the overhead, is approximately 32 seconds46.
From this you can extrapolate that 100GB would be 320 seconds (5 minutes,
20 seconds) and 1TB would be 3200 seconds (53 minutes, 20 seconds).
Additional Actions
For programs that will be added to the authorized programs list, and for data
files that will be protected we recommend you start using Access Control Lists
(ACLs). This adds a much finer-grained control over access than the traditional
User, Group & Other access control. This finer-grained control will enhance
security.
45 Yes, we know this is an over-estimate – this is a simplified example.
46 This assumes that no other activity is consuming CPU or other resources while this
happens.
You can read more about ACLs on the manual pages for acl, getfacl, and
setfacl. When you use the utility ls with the ‘-l’ option a ‘+’ will appear
with the traditional permissions to indicate that a file has an ACL attached to it.
Some Linux systems will also be using SELinux for more security. QDocSE
security works in a complementary, non-interfering way with SELinux.
Therefore you can also use SELinux to add more security. The complexity of
SELinux means it is beyond the scope of discussion in this User Manual but
there are many documents available that you can easily find.
Re-Configuring later
Once QDocSE has been moved into De-elevated mode it cannot be moved back
to Elevated mode (or Learning mode) without an elevation file. This effectively
results in a method of 2-factor authentication (2FA) because whoever is using
the administrator account (aka “root”) must go through an intentionally
disruptive set of actions to get the elevation file. Moving from De-elevated
mode to Elevated mode is a security procedure.
To obtain an elevation file you will need to login to the QDocSE registration
web site. Best procedure is to keep the login password for the QDocSE
registration site different from any other password used at your site and do not
keep that password on any of your site’s computers that an intruder will have
access to. Remember, an intruder will get access to all of your computers
eventually – you are not paranoid if you are right.
To protect against a malicious insider we recommend that the login and
password to the web site to obtain a license file or an elevation file be kept
private by a person who is different from the Administrator of the systems
QDocSE is installed on.
Simple Example
Configuration uses the QDocSEConsole utility to issue the commands. Here is
a sample with just the commands for configuration on a CentOS 7 system.
rpm -i qdocse-3.2.0-1.rpm
{ The qid.txt file is submitted to the registration
website and a license file is then downloaded }
QDocSEConsole -c activate -af ActivateFile -t 5d
{ remove license file once used }
QDocSEConsole -c protect -e no -d /usr/data1
QDocSEConsole -c protect -e yes -d /usr/data2 -dp ‘*.txt’
QDocSEConsole -c unprotect -d /usr/data1 -dp ‘*.tgz’
QDocSEConsole -c adjust -apf /usr/bin/cat
QDocSEConsole -c adjust -apf /usr/bin/vi
QDocSEConsole -c adjust -bpf /usr/bin/less
QDocSEConsole -c view
QDocSEConsole -c view_monitored
QDocSEConsole -c push_config
QDocSEConsole -c finalize
Extended Example
This is a longer example for a more complex but common scenario that many
customers have at their site. It is unlikely to match your situation exactly but
may be close enough to provide guidance or clues for your situation.
For this example let’s assume that MySQL has been installed and you want to
protect all of its database files. You also want to allow MySQL to access those
database files. There may be other programs accessing those database files,
but, for this example, you don’t know exactly which other programs.
Because you are unsure of all of the programs that will be accessing the
protected data files Learning mode is the easiest option to assist you in
determining this information.
First you need to install and apply the license. This has been described in detail
earlier in the manual so we won’t repeat it here. This will place QDocSE in
Elevated mode.
For this example we’re going to protect the database/tables under the directory
“/var/lib/mysql”.
Next let’s protect the database files and move to Learning mode:
QDocSEConsole -c protect -e yes -d /var/lib/mysql
QDocSEConsole -c setlearning on
You should now re-start and use MySQL and all other programs that might
access those database files. QDocSE in Learning mode will notice the access to
the protected files and automatically add the programs to the authorized
programs list.
Once you have run all of the programs and each program has accessed the
protected database files you can leave Learning mode to activate these new
entries in the authorized programs list. There may be programs added that you
did not directly execute – these additions will be a side-effect of other
programs you did use executing these programs. It is possible that you do not
want one or more those programs to be in the authorized programs list.
You can use the view_monitored command47 to see a complete list of
programs and their shared libraries pending to be added.
Leaving Learning mode or using the push_config command48 will inform
QDocSE that the pending programs and shared libraries are now active.
QDocSEConsole -c setlearning off
QDocSEConsole -c push_config
47 See page 145.
48 See page 118.
If you do not use one of the commands above then remember that QDocSE will
move to De-elevated mode and automatically perform a push_config
command when Elevated Time49 has finished.
You will discover now that you are in De-elevated or Elevated mode and that
MySQL access to the protected database files is denied. As mentioned earlier in
the User Guide the MySQL service (or daemon) is a long running process50 that
was started before it was added to the authorized programs list. This means
that MySQL program has not gone through the SG evaluation to determine that
it and the shared libraries loaded with it are valid – no security evaluation has
happened with it, thus safe security is to deny access. A freshly loaded MySQL
service will go through the SG evaluation. Therefore you need to restart the
MySQL service – this will stop the current instance and start a new instance of
the MySQL service.
systemctl restart mysqld
The equivalent will be accomplished if you feel the need to reboot your system
instead.
NOTE: This same or similar set of steps will apply for other brands of
databases as well such as Oracle or Postgres.
NOTE: If you are using an Oracle DB that uses ASM then you will want to
use the encrypt_device command because ASM uses a device instead of a
file. For a more specific example refer to BicDroid Sales Engineer.
New Files
The majority of this User Guide is about existing files and how they are treated
when specific commands are executed. It is possible to create new files in a
directory or subdirectory of a QDocSE watched directory. There are specific
rules for new files: (a) when they will be protected and/or encrypted, (b) if the
new files are created by an authorized program or not, (c) which license is
49 See page 46.
50 See page 48.
currently active, and (d) has a pattern been set with the encrypt_pattern
command51 for the watched directory. The following table lists the rules. The
difference between Local and Remote drives are discussed in the sections
following this section. Note that Authorized programs need to be specified
when the license type requires their selection during configuration; with the
Encrypt-only license all programs are Authorized. When an encrypt pattern has
been specified then the file will be encrypted only when the pattern matches.
When no encrypt pattern is specified then this is treated as always matching.
1. Authorized program (local and remote drives):
a) Directory protected and encrypted: new files protected and
encrypted.
b) Directory protected only: new files protected only.
c) Directory not protected: new files not protected.
d) Directory is encrypted only: new files encrypted.
e) Directory is not encrypted: new files are not encrypted.
f) Directory is audited only: new files audited.
g) Directory is verified (integrity): new files not verified.
h) Directory is verified (integrity) and encrypted: new files are not
verified and new files are encrypted
2. Non-Authorized program:
a) Directory protected and encrypted, local drive: new files not
protected and not encrypted.
b) Directory protected and encrypted, remote drive: new files cannot
be created.
c) Directory protected only, local drive: new files not protected.
51 See page 105.
d) Directory protected only, remote drive: new files cannot be created.
e) Directory not protected: new files not protected.
f) Directory is encrypted only: new files encrypted.
g) Directory is audited only: new files audited.
h) Directory is verified (integrity): new files not verified.
i) Directory is verified (integrity) and encrypted: new files not
verified and the new files encrypted
Renaming Files
When the names of files are changed (renamed or moved) QDocSE security
rules will have an effect on the success.
When a rename will result in moving the file from a directory not under
QDocSE protection to being under QDocSE protection then the “New Files”
rules will apply (see previous section). This applies for Authorized and non-
Authorized programs.
When a rename will result in moving a QDocSE protected file to a directory
not under QDocSE protection only an Authorized program will be successful.
Non-Authorized programs will fail. When successful, the file will not be
protected or encrypted.
When a rename will result in moving a QDocSE protected file to another
directory that is QDocSE protected, only an Authorized program will be
successful; non-Authorized programs will fail. When successful the file will be
protected.
When a rename will result in moving a QDocSE protected and encrypted file to
another directory that is QDocSE protected and encrypted, only an Authorized
program will be successful; non-Authorized programs will fail. When
successful the file will be protected and encrypted.
When a rename will result in moving a file not protected by QDocSE to
another location not protected by QDocSE then QDocSE security is not
involved.
When an encrypted file is renamed from an encrypted directory to a non-
encrypted directory then the file will be in plaintext.
When an plaintext file is renamed from a non-encrypted directory to an
encrypted directory then the file will be encrypted.
When a plaintext file is renamed from an encrypted directory and stays in that
same directory then the file remains in plaintext.
When a plaintext file is renamed from an encrypted directory to a different
encrypted directory then the file will be encrypted.
Remote Disk Drives
Remote or Network disk drives are commonly used with Intranets. There are
different types of remote drives. The most common type supported by UNIX®
and Linux® systems is NFS. QDocSE officially supports NFS versions 3 and 4.
Other types are available with remote drivers for Linux® but the stability of
those drivers is sometimes questionable – particularly with older versions of
Linux® distributions. For example, the CIFS driver with CentOS 7.X went
through a long period of instability (crashing). The most recent update, as of
this writing, seems to be stable but more testing is required to satisfy our QA
department. As such, you may, at your own discretion, use QDocSE with a
CIFS remote drive but support will be very limited.
The type of server or manufacturer providing the remote drive is not as critical
as that server adhering strictly to the NFS protocol. That is, the remote server
being a NAS device, Linux server, FreeBSD server or Windows server
shouldn’t be a worry as long as the NFS protocol is strictly followed.
For security reasons QDocSE prevents additional kernel modules from being
loaded shortly after boot has started. The reason for this is to prevent an
intruder from loading their own kernel module to by-pass security and/or
present erroneous information52. We mention this here because support for NFS
remote drives are loaded as kernel modules on demand. As a consequence, if
you are going to protect a remote drive then it must be mounted at boot time.
That is, it must be added to the /etc/fstab file. This also means that QDocSE
protection can start virtually immediately for this remote drive.
You must also understand that QDocSE will protect access to files on a remote
drive for programs running on the local system. If a different computer has
also mounted the same remote drive then access control on that different
computer is controlled by that different computer.
When files on a remote drive will be encrypted it is best for them to be
encrypted on the host system (the computer where the disk is local). This is
more efficient because encrypting over the network will take a very long time.
Thus QDocSE should be installed on any system providing a local disk as a
remote mount to other computers.
It is best to have files on a remote drive encrypted because this provides over
the wire security (data in motion). Since all QDocSE installations with the
same customer use a common encryption keyset each QDocSE “endpoint” will
do encryption/decryption locally which will be transparent to local programs.
The remote system providing the remote disk will not perform any encryption
or decryption for the QDocSE endpoint.
We recommend that with each QDocSE endpoint the watch command53 be used
to specify QDocSE mounts so encryption and decryption can happen
transparently for programs local to the endpoint system. If you no longer need
the QDocSE mounts then you can use the unwatch command54 which will
leave the files on the server in there encrypted state.
52 This is a common technique used by digital currency miners, and ransomware attackers.
53 See page 146.
54 See page 139.
Local Disk Drives
QDocSE supports most of the native Linux® file system types such as xfs, ext3,
ext4, etc. It is with local drives that the greatest protection can be achieved
because full control of the file system is with the local computer. You should
avoid exporting local drives that you are protecting to other computers because
then some of the control for access to files is extended to those other
computers.
If you do export a local drive to other computers then every one of those
computers mounting this drive must have QDocSE installed and configured to
protect the drive. As mentioned earlier, all of the files with an exported file
system should be encrypted because this will provide data in motion security.
Invalid Programs and SOs (Shared Object files)
When QDocSE adds a program and its Shared Objects (SOs) to the Authorized
list or to the monitored programs list, signatures are calculated for each
individual program and SO. These signatures are used to validate processes
(running programs) to decide if they are allowed to access protected data files
(when in the Authorized list), or if warning messages should be sent to CSP if
a monitored program or SO is changed.
Authorized List
If a program or Shared Object (SO) has changed and it is in the Authorized list
for accessing protected data files then it will be blocked. The running program
will receive an “EPERM” error code when trying to open a file. The change
can be to one, more than one or all files that are used to create the running
process.
To help diagnose which files have been changed you can use the
verify_monitored command55. This will display the programs and SOs
whose signatures do not match.
You should carefully verify why these files have changed since the QDocSE
configuration was made. For security and safety reasons make no assumptions
about why the changes have happened, and be careful of social engineering
tricks.
With a well managed computer site the Administrators plan ahead when
updates for installed packages will happen. If someone has made an update or
change without permission then a detailed inspection of what files, packages,
etc. this individual has used and where they obtained them from is required. Do
not automatically agree with the changes.
When you have planned updates, remember to obtain packages only from very
trusted sites and to verify the package signatures. After packages are updated
check that only the files you expected to change have changed.
To update the signatures of programs and/or SOs you must be in Elevated
mode. Moving from De-elevated to Elevated mode requires obtaining an
Elevation File56. Once in Elevated mode you can then use the
update_monitored command57 to update the signatures. Remember to use the
finalize command58 when you have completed updating the signatures so
that full QDocSE security will be restored. You will need to re-start long-
running program (as described earlier).
Monitored Programs and SOs
Monitored programs only monitor the files on the disk and do not validate
running processes. This is why they are not allowed access to protected data
files. When a signature is created to only monitor a program, all of the SOs that
55 See page 142.
56 See page 42.
57 See page 135.
58 See page 106.
the program depends on will also have signatures created. This is important
because a running process is the sum of all of the parts that it is composed of.
When a file for a program is changed the signature changes and a message will
be sent to CSP.
You can view the files that have been changed with the verify_monitored
command59. You should verify who has changed these files and why they
changed these files.
The update_monitored command60 can be used to create new signatures. You
can be selective about which files you want to update – you do not need to
update all of the files at once that have changed signatures.
You must be in Elevated mode to update the signatures. Moving from De-
elevated to Elevated mode requires obtaining an Elevation File61. Once in
Elevated mode you can then use the update_monitored command62 to update
the signatures. Remember to use the finalize command63 when you have
completed updating the signatures so that full QDocSE security will be
restored.
59 See page 142.
60 See page 135.
61 See page 42.
62 See page 135.
63 See page 106.
Configuration Commands
This is an alphabetical organization of the commands available with the
QDocSEConsole utility. Commands are specified with the “-c” option. For
example:
QDocSEConsole -c show_mode
Most commands can only be used in Elevated mode or Learning mode. Some
commands can be used in any mode (“All”). The “Active modes” line with
each command description will indicate in which modes a command can be
used.
For all commands if an option is provided that is unknown to that command
then an error message will be displayed.
Help
With every command you can print a help message by providing a “-h” option
with the command. For example:
QDocSEConsole -c view -h
Will display the help message for the view command. Each help message will
describe what the command does, the options available, an example and notes
about the command.
You can display a list of available commands that match your license by
doing:
QDocSEConsole -c commands
License Types
With each command the License Type indicates which license type will have
the command available. The following table provides the list of license types.
There is the option to have each of these license types with or without OS
Security but this does not change any of the commands’ descriptions. When a
command is available with all licenses then “All” will be shown.
A) Protect with Encrypt64
B) Encrypt
C) Audit
D) Data File Integrity
E) Program File Integrity
F) Data File Integrity with Encrypt
G) Data File and Program File Integrity (see D, E & F)
Refer to the section Licenses for a long description of each license65.
acl_add
This command will add entries to an existing ACL. New ACLs are created
with the acl_create command. Existing ACLs can be listed with the
acl_list command. The acl_add command can be run multiple times to add
multiple entries to a single ACL. An ACL entry can be removed with the
acl_remove command. ACL entries may be reordered with the acl_edit
command. Refer to the ACL Overview Section of the User Guide for a more
detailed description of ACLs.
An ACL entry will either allow or deny a specific user, group or program
access to a protected file. Refer to the protect command for information
about protected files and applying an ACL to a file or files. It is required that
one of user, group or program is a specified option for an entry – and only one
of them.
64 This is equivalent to the license type available with QDocSE 2.X and earlier.
65 See page 50
An ACL is an Access Control List. The list can be composed of one or more
ACL entries. Each time the acl_add command is run it will add an additional
ACL entry to the specific ACL at the end of the current entries. The order of
the entries in the list can be important for security reasons. The order of the
entries can be changed with the acl_edit command.
In addition to a user, group or program being specified for an entry, you may
have a set of times and/or days that the allow or deny entry will apply. You can
also specify the mode a file can be accessed (read, write, execute). These two
specifications are optional.
Each individual ACL can have entries entirely as user/group , or entirely as
program. An ACL of program entries cannot have user/group entries. An ACL
of user/group entries cannot have program entries. This is important when
assigning the ACL ID to specific command options.
Active modes: Elevated, Learning
License type: A
The available options are:
-a
-b
-d
-g <group_name | group_id>
-i <acl_id>
-l
-m <access_mode>
-p <program index>
-t <time_specification>
-u <user_name | user_id>
The ‘-a’ option specifies that the new entry is an “allow” entry. It cannot be
used with the ‘-d’ option.
The ‘-b’ option specifies that the program referenced by the program index
(‘-p’) is a program used to backup files. Backup programs can read, but not
write, files and the file contents will contain full data: the ciphertext and per
file metadata. It can only be used with the ‘-p’ option. It cannot be used with
the ‘-l’ option.
The ‘-d’ option specifies that the new entry is a “deny” entry. It cannot be used
with the ‘-a’ option.
One of option ‘-a’ or ‘-d’ must be specified.
The ‘-g’ option specifies that new entry applies to a specific group by
<group_name> or <group_id>. It cannot be used with the ‘-p’ option or the ‘-
u’ option. This can be applied to a new ACL or an access ACL. An access ACL
specifies the access permissions for a user or group.
The ‘-i’ option specifies the ACL identifier <acl_id> for the new entry. This
is a required option.
The ‘-l’ option specifies that the program referenced by the program index
(‘-p’) is a program that is limited to reading, and not writing, the ciphertext of
files – the per file metadata will not be accessible. The program will never
obtain plaintext. It can only be used with the ‘-p’ option. It cannot be used with
the ‘-b’ option.
The ‘-m’ option specifies the file mode to match for allowing or denying access
to the protected file. The <access_mode> can be the combination of ‘r’ ,’w’ or
‘x’ where ‘r’ means read access, ‘w’ means write access and ‘x’ means
executable access. For an allow entry the open request must match exactly or a
sub-set for the allow to happen. For a deny entry, a match to any will invoke
the denial.
The ‘-p’ option specifies the <program index> for the new entry. It cannot be
used with the ‘-g’ option or the ‘-u’ option. The number is the value from the
view command’s list of authorized programs. This can be applied to a new ACL
or a program ACL. A program ACL specifies which programs (instead of users
or groups) that are allowed to open ACL protected files.
The ‘-t’ option specifies the time parameters for allowing or denying access to
the protected file. This option is optional, and this option may be specified
more than once per entry. The time parameter can be a combination of hour
ranges (in the 24-hour format) with or without days of the week being
specified. For example you can specify Monday to Friday, 0900h to 1500h for
matching an allow entry – if the user tries to access a file at any other time/day
then this will mean the allow entry does not matching meaning the allow will
not happen and the next entry in the list will be checked.
The ‘-u’ option specifies that new entry applies to a specific user by
<user_name> or <user_id>. It cannot be used with the ‘-g’ option or the ‘-p’
option. This can be applied to a new ACL or an access ACL. An access ACL
specifies the access permissions to a file for a user or group.
Examples:
QDocSEConsole -c acl_add -i 1 -a -m rw -u ted
QDocSEConsole -c acl_add -i 1 -a -m r -u sam -t 09:00:00-
15:00:00
Errors:
Missing required ‘-i’ option.
One of option ‘-a’ or ‘-d’ must be specified.
Only one of ‘-b’ or ‘-l’ allowed.
One of option ‘-g’, ‘-p’ or ‘-u’ must be specified.
Missing required ‘-m’ option.
No ACL configuration file found.
Invalid program index.
Invalid user ID.
Invalid group ID.
Missing user, group or program option.
acl_create
This command is used to create a new ACL that is empty of entries and
associate a new ACL identifier (ACL ID) with it. All other ACL commands
will use this ACL ID to clearly and correctly identify which ACL is being
referenced or changed.
If an ACL is ever destroyed then the matching ACL ID will not be reused.
When the command completes it displays the new ACL ID value.
Active modes: Elevated, Learning
License type: A
There are no options for this command.
Example:
QDocSEConsole -c acl_create
Errors:
No ACL configuration file found..
acl_destroy
This command will destroy or delete the specified ACL entirely when there are
no entries unless the ‘-f’ option is used. To remove an ACL entry refer to the
acl_remove command.
Active modes: Elevated, Learning
License type: A
The available options are:
-f
-i <acl_id>
The ‘-f’ option will force all of the ACL’s entries to be removed before the
ACL itself is destroyed.
The ‘-i’ option is a required option for this command. The option takes the
ACL ID.
Example:
QDocSEConsole -c acl_export /tmp/acl_config
Errors:
Missing required ‘-i’ option.
No ACL configuration file found.
X is not a valid ACL ID.
ACL ID X’s ACL list is not empty.
acl_edit
This command allows you to change the order of the ACL entries for a specific
ACL. As explained in Section AA of this User Guide, the order of ACL entries
is important when determining whether access is allowed or denied.
Active modes: Elevated, Learning
License type: A
The available options are:
-e <entry_number>
-i <acl_id>
-p <new_position>
The ‘-e’ option specifies the entry number of the ACL that you want to move.
This option is required. The entry number matches the acl_list display.
The ‘-i’ option specifies that the existing ACL ID. This option is required.
The ‘-p’ option specifies the new entry position. This option is required. The
valid new position can be specified with a numeric location or one of the
words “up”, “down”, “top”, “bottom”, “first”, “last”, begin” or “end”.
Examples:
QDocSEConsole -c acl_edit -i 2 -e 3 -p up
QDocSEConsole -c acl_edit -i 2 -e 3 -p down
QDocSEConsole -c acl_edit -i 2 -e 3 -p 2
Errors:
Missing required ‘-e’ option.
Missing required ‘-i’ option.
Missing required ‘-p’ option.
No ACL configuration file found.
X is not a valid ACL ID.
No change – item does not need to move.
Error with acl_edit.
acl_export
This command will display QDocSE settings for ACL configuration that can be
imported onto other systems running QDocSE so the same configuration exists
on all systems.
Active modes: Elevated, Learning
License type: A
The ‘-f’ is the only required option for this command. The option takes the
filename of the file to write the ACL configuration to.
-f <export_file_name>
Example:
QDocSEConsole -c acl_export -f /tmp/acl_config
Errors:
Missing required ‘-f’ option.
No ACL configuration yet.
Open ACL configuration error.
Memory allocation error.
ACL configuration read error.
ACL export error.
acl_file
This command allows the user to set the user and/or program ACL IDs for a
specific file or for a set of files under a specified directory. With the directory
option glob patterns can to specified to include or exclude files with certain
patterns in their name.
Active modes: Elevated, Learning
License type: A
The available options are:
-d <directory_name>
-dp <matching_pattern>
-excl <excluding_pattern>
-A <acl_id>
-P <acl_id>
The ‘-d’ option specifies the directory containing the files to apply ACL IDs.
By default the ACL IDs will be applied to all files and sub-directories
recursively.
Use of ‘-dp’ is optional. The matching pattern will be used to select which files
under the named directory will be assigned the ACL IDs with the ‘-A’ and/or ‘-
P’ options (described below). The pattern for matching follows the glob(7)
rules. Refer to the glob manual page, Appendix C, for details66. When
<matching_pattern> is specified then only the filenames that match the
pattern in the directory and sub-directories are added to the match list. When a
pattern is specified it should be enclosed between single quotes to prevent the
shell from interpreting special characters before the pattern is given to
QDocSEConsole.
66 Refer to a copy in Appendix C (page 176).
When the ‘-dp’ option is used and this does not select all files under the
directory, then the non-matching files will remain unchanged; whichever ACL
IDs were assigned before stay the same.
The ‘-excl’ specification is optional. When <excluding_pattern> is
specified then matching files will be removed from the list. Note that when
both ‘-dp’ and ‘-excl’ are specified the ‘-dp’ matches are added to the list and
then the ‘-excl’ matches are removed from the match list.
NOTE: When both ‘-dp’ and ‘-excl’ are specified the ‘-dp’ matches are
added to the list first and then the ‘-excl’ matches are removed from the list
last. Both options use the glob rules for composing the pattern.
The ‘-A’ option specifies the ACL ID for users/groups opening the file. When
this option is not specified then the current user/group ACL ID will be
unchanged.
The ‘-P’ option specifies the ACL ID for programs opening the file. When this
option is not specified then the current program ACL ID will be unchanged.
Example:
QDocSEConsole -c acl_file -d datadir2 -P 2 -A 4
QDocSEConsole -c acl_file -d datadir2 -dp ‘*.doc’ -P 5
Errors:
Option ‘-d’ must be specified.
One or both options ‘-A’ or ‘-P’ must be specified.
No ACL configuration found.
Invalid ACL ID specified to ‘-A’.
Invalid ACL ID specified to ‘-P’.
Path does not exist.
Directory does not exist.
Not a directory.
Filename path too long.
Operation not permitted.
acl_import
This command will import the provided ACL configuration file to set the
QDocSE ACL configuration. Any previous ACL configuration will be
overridden. Specific files on the local system will still need to be set to use the
ACL IDs with this new configuration.
If the import file is not a valid QDocSE ACL file then an error will be reported.
Active modes: Elevated, Learning
License type: A
The ‘-f’ is the only required option for this command. The option takes the
filename of the file to read the ACL configuration from.
-f <input_file_name>
Example:
QDocSEConsole -c acl_import -f /tmp/acl_config
Errors:
Missing required option ‘-f’.
Import file missing.
Import file open error.
Open ACL configuration error.
Memory allocation error.
ACL import read error.
ACL import hash verify error.
File lseek error.
ACL import error.
Import file trim error.
Bad magic number in ACL import file.
acl_list
This command will display all of the active ACLs and their entries. A specific
ACL can be displayed with the ‘-i’ option. The display includes numeric
position information that can be used with other ACL commands.
Active modes: Elevated, Learning
License type: A
Command Aliases: list_acl, list_acls
The available option is:
-i <acl_id>
The ‘-i’ option specifies that a specific ACL with <acl_id> should be
displayed only.
With each ACL the ACL ID is displayed.
Each ACL can have zero or more entries. With zero entries the message “No
entries (Deny)” is displayed. With one or more entries then “Entry:” is
displayed with the entry number. This entry number can be used with the
acl_remove command’s ‘-e’ option.
Each entry will display the type: Allow or Deny.
Each entry will display the user or group or program index that must match for
the entry to be evaluated. The UID, GID or program index will be displayed
followed by the readable name: user name, group name, or program path.
Each entry will display the mode which can be read (r), write (w) and/or
executable (x). When the open request matches any of the entry’s modes then it
is successful. When the open request has more modes than the entry then it will
not be successful.
Each entry will display the times of day and week that the entry will be
successfully matched. When there is no match then it is not successful.
When the UID/GID/index matching is successful, plus the mode matching is
successful, plus the time is successful then the type of entry will be the action
(Allow or Deny). When the UID/GID/index is successful but the mode or time
is not successful then the entry will Deny.
When the UID/GID/index is not successfully matched then this entry will be
skipped and the next entry in numerical order will be checked.
When all entries have been checked, including when there are zero entries, and
there are no more entries to evaluate then a Deny will happen for this ACL.
When there have been changes to the ACL configuration that has not be
pushed to the QDocSE system the message “Pending configuration: see
push_config command” will be displayed.
Example:
QDocSEConsole -c acl_list
QDocSEConsole -c acl_list -i 6
Errors:
No ACL configuration file found.
acl_program
This command sets the ACL to be associated with an authorized program. The
same setting can be performed as an option with the adjust command. A valid
ACL will have User/Group entries (not program entries).
When the associated ACL is not matched then the running program will be
invalid which means it cannot access ACL protected data files.
When the associated ACL is matched then the running program may be valid.
The program must still pass other criteria to be valid (e.g. file and shared
object signatures).
The associated ACL must have at least one entry.
Active modes: Elevated, Learning
License type: A
The available options are:
-A <acl_id>
-p <program_index>
The ‘-A’ option specifies which ACL should be associated with the authorized
program (read the ‘-p’ option below). The ACL must contain user/group
entries only. This option is required.
The ‘-p’ option specifies the authorized program. The <program_index> is the
number displayed with the view command. This option is required.
Examples:
QDocSEConsole -c acl_program -A 1 -p 1
QDocSEConsole -c acl_program -A 7 -p 3
Errors:
ACL is empty. Cannot assign.
ACL needs user/group entry. Cannot assign.
Program index X does not exist.
acl_remove
This command removes a single entry from the specified ACL. To delete an
entire ACL refer to the acl_destroy command. To move or re-order the ACL
entries refer to the acl_edit command.
Active modes: Elevated, Learning
License type: A
The available options are:
-A
-a
-d
-e <entry_position>
-g <group_name>
-i <acl_id>
-p <program_index>
-u <user_name>
The ‘-A’ option specifies that all ACL entries will be removed.
The ‘-a’ option specifies an “allow” entry will be selected for removal.
The ‘-d’ option specifies a “deny” entry will be selected for removal.
The ‘-e’ option specifies the entry number (from the acl_list command)
selected for removal. This is the preferred option for clearly selecting an entry.
The ‘-g’ option specifies the group name or group id selected for removal.
The ‘-i’ option specifies which ACL will have entries removed. This option is
required.
The ‘-p’ option specifies the program index that will be selected for removal.
The ‘-u’ option specifies the user name or user id selected for removal.
Note: Only one option of ‘-e’, ‘-g’, ‘-p’ or ‘-u’ may be specified at the same
time.
Examples:
QDocSEConsole -c acl_remove -i 1 -e 4
QDocSEConsole -c acl_remove -i 2 -A
QDocSEConsole -c acl_remove -i 2 -a -u ted
Errors:
Missing required ‘-i’ option.
No ACL configuration file found.
Invalid program index.
Invalid user ID.
Invalid group ID.
Missing user, group, entry or program option.
activate
This command is used to activate, or install, the QDocSE license. This will
change QDocSE from Unlicensed to Elevated mode. For obtaining a license
file refer to the section Applying the License67. The ‘-f’ or ‘-af’ option is
required because it specifies the license file. The ‘-t’ option is required
because it sets Elevated Time.
This command can be used to change the license type when a new license file
is provided. It is used the same way as when the original license was applied.
NOTE: For security reasons you should delete the license file once it has been
successfully used.
Active modes: De-elevated
License Type: No License
67 See page 40.
Command Aliases: license, licence
The available options are:
-af <activate_file>
-f <activate_file>
-t <value><time_unit>
-V
where <activate_file> is the name of the license file.
The ‘-t’ option is required and specifies the maximum length of time that
QDocSE will stay in Elevated mode. This Elevation Time affects Learning
mode. When Elevation Time has expired then QDocSE will automatically
move from Learning mode or Elevated mode to De-elevated mode. <value> is
a positive number paired with the optional <time-unit> to specify the time. A
<time-unit> will be one of ‘d’ (days, the default), ‘h’ (hours), ‘m’ (minutes) or
‘s’ (seconds). The maximum is the equivalent of 1096 days.
When choosing a value to set Elevated Time remember to take into account the
time estimated to encrypted all of your data plus some extra time, and/or the
length of time you want to have Learning mode active. For example, if you
estimate the time to encrypt all files will take 36 hours then ‘-t 44h’ may be a
good setting. As another example, if you estimate it will take 8 hours to
configure and encrypt all files, and after that you want to run in Learning mode
for 2 days then ‘-t 3d’ may be a good setting.
The ‘-V’ option will activate Learning mode immediately after the license file
has been validated. Learning mode is part of Elevated mode. For more
information about Learning mode refer to the Learning mode section of this
User Guide.
Example:
QDocSEConsole -c activate -f ActivateFile -t 6h
Errors:
If the license file does not match this endpoint installation then an error
will be displayed.
If this license file has been applied to this endpoint before then an error
will be displayed.
If there is a problem with the format of the license file then an error
message will be displayed.
If the “ActivateFile” does not exist then an error message will be
displayed.
If the Elevation time specified with ‘-t’ is an invalid time or longer
than 1096 days then an error message will be displayed.
add_integrity_check
This command adds files to QDocSE’s list of integrity monitored files. That is,
each file’s integrity will remain the same. Each file added will be monitored in
real time. Messages are sent to CSP when a file is accessed, modified or
restored. When added to the list each file is read to produce a hash that is used
later to determine if it has been modified or restored when a write to the file
has happened – the write detection is done in real time, not by periodic
scanning.
You must not use this command for files that are programs or shared libraries.
Instead refer to the add_monitored command.68
With data monitored files messages will be generated when the files have been
modified, restored or accessed.
Active modes: Elevated, Learning
License type: D, F
The available options are:
-d <directory>
-dp <matching_pattern>
-excl <excluding_pattern>
-e [ yes | no ]
68 See page 88.
-t <number_of_threads>
The ‘-d’ option is required. <directory> is the directory that contains the files
to be monitored. By default all files under the directory, and its sub-directories
are added.
Use of ‘-dp’ is optional. The <matching_pattern> will be used to select
which files under the named directory will be added. The pattern for matching
follows the glob(7) rules. Refer to the glob manual page for details69. When a
pattern is specified it should be enclosed between single quotes to prevent the
shell from interpreting special characters before the pattern is given to
QDocSEConsole. This option works with local drives only; it has no effect with
remote drives.
When the ‘-dp’ option is used and this does not select all files under the
directory, then the non-matching files will not be monitored (unless they were
monitored before). Remember that this option has no effect with remote drives.
Use of ‘-excl’ is optional. When <excluding_pattern> is specified then
matching files will be removed from the list. Note that when both ‘-dp’ and ‘-
excl’ are specified the ‘-dp’ matches are added to the list first and then the ‘-
excl’ matches are removed from the list second.
The ‘-e’ is optional. When not specified the default parameter is “no”. When
the parameter is “yes” then the selected files will be also be encrypted.
The ‘-t’ option specifies the number of threads to use when encrypting files.
The default is a value calculated based on the number of CPUs on the system.
The maximum value is 63.
The time to complete this command is dependant on the number of files and
the total size of all of the files.
Refer to the list command70 to see a list of files and their current integrity
status.
69 Refer to a copy in Appendix C (page 176).
70 See page 109.
Remember: You must not use this command for files that are programs or
shared libraries. Instead refer to the add_monitored command.
Examples:
QDocSEConsole -c add_integrity_check -d /home/ted/data
Errors:
If the ‘-d’ option is missing then an error will be displayed.
If the ‘-d’ option does not specify a directory then an error will be
displayed.
If the ‘-e’ option is specified with a bad parameter then an error will be
displayed.
With the ‘-dp’ and ‘-excl’ options when <matching_pattern> is not a
valid glob pattern then an error will be displayed.
If the license is invalid then an error will be displayed.
If QDocSE is not in Elevated mode or Learning mode then an error will
be displayed.
add_monitored
This command adds files to QDocSE’s list of monitored program files. It will
monitor each program and plus all of the shared libraries each uses. This
command does not authorize programs for accessing protected data like the
adjust command does.71
Monitored program files messages will be generated when the program or
shared library files have been modified, restored or accessed.
71 See page 89.
Refer to the view_monitored command to see a list of currently monitored
programs and shared libraries72, or the list_monitored command73 to see a
list with information specific to a program.
Active modes: Elevated, Learning
License Type: E
The available options are:
-p <program>
where <program> is the filename or path of an executable.
Examples:
QDocSEConsole -c add_monitored -p /usr/bin/xargs
Errors:
If the ‘-p’ option is missing.
If the ‘-p’ option does not specify a program.
If the license is invalid.
If QDocSE is not in Elevated mode.
You cannot specify QDocSEConsole or QDocSEService as <program>.
The <program> specified doesn’t exist.
adjust
This command is used to adjust or set the list of programs that are authorized
or blocked from accessing protected data.
Active modes: Elevated, Learning
72 See page 145.
73 See page 112.
License Type: A
The available options are:
-A <acl_id>
-apf <program_path>
-api <index_number>
-b <index_number>
-bpf <program_path>
-V
where <index_number> is the number displayed in the view command74, and
where <program_path> is the full filename path of a program. The options
starting with ‘b’ will block the program from accessing protected files. The
options starting with ‘a’ will allow the program to access protected files.
The ‘-A’ option specifies the ACL identification number (ID) that will be
associated with this program. The <acl_id> is the number from the acl_list
command. Refer to the acl_* commands for more information about
configuring ACL entries. This ACL setting works in conjunction with QDocSE
protection functionality to limit which programs can or cannot open protected
data files. When the ACL ID is not specified then this is the equivalent of
fixed, built-in ACL ID 0 (zero) which has an “allow access” setting.
The ‘-apf’ option allows a program specified by <program_path>, a full path,
to access protected data files.
The ‘-api’ option allows a program specified by <index_number> (as
displayed by the view command) to access protected data files. The ‘-api’
option can be used to move a program from the blocked list to the allowed list.
The ‘-b’ option moves a program from the allowed list to the blocked list using
the <index_number> displayed by the view command.
The ‘-bpf’ option puts a program specified by <program_path>, a full path,
onto the blocked list. Blocked programs are not allowed to access protected
74 See page 147.
files. This option is most often used when in Learning mode so that specified
programs will not be added to the allowed list.
The ‘-V’ option will add an ACL entry for the specified program to a default
program ACL when Learning mode is active. The entry will be for read-write
access and plaintext access.
It will take time to process each program being added to the authorized list
because every shared library used by the program is being evaluated too. The
larger the programs and/or the greater the number of libraries then the longer it
will take to process.
Typically on Unix-like systems just the traditional permissions with User,
Group and Other are applied to executable programs. Adding more fine-
grained control using ACLs (Access Control Lists) to the executable programs
can add a lot more security – particularly with the programs you are adding to
the authorized programs list. QDocSE limits access to protected data files to
specific authorized programs. By applying ACL entries you can specifically
identify users allowed, and disallowed, to run the programs75.
NOTE: You cannot specify a program that is located in a directory that has any
of its data files being protected by DG. Authorized programs must be
monitored by SG.
Examples:
QDocSEConsole -c adjust -apf /usr/bin/less
QDocSEConsole -c adjust -bpf /usr/bin/vi
QDocSEConsole -c adjust -b 2
Errors:
If an index_number is not currently valid then an error message will be
displayed.
If the path for a program is not valid then an error message will be
displayed.
If QDocSE does not have a valid license then an error message will be
displayed.
75 We’ve made this recommendation with the protect command for protected data files too.
NOTE: You should avoid authorizing programs that are general purpose
utilities such as cat, bash, more, vi, ssh, etc. because running these is allowed
for so many user accounts. These general purpose utilities are regularly a target
for Trojan malware.
NOTE: Remember our suggestion that you use ACLs for authorized programs
to limit who has permission to run these programs.
audit
This command will add files to the list of audit files. When files are audited a
message will be sent to CSP each time a file is accessed. Auditing does not
determine if a file’s content has been changed.76
Active modes: Elevated, Learning
License type: C
The available options are:
-d <directory>
-dp <matching_pattern>
-excl <excluding_pattern>
-e [ yes | no ]
The ‘-d’ option is required: where <directory> is the directory, and sub-
directories, containing the files to be audited. By default all files under the
directory, and its sub-directories are added.
The ‘-dp’ specification is optional. When <matching_pattern> is specified
then only the filenames that match the pattern in the directory and sub-
directories are added.
Use of ‘-dp’ is optional. The pattern will be used to select which files under the
named directory will be audited. The pattern for matching follows the glob(7)
76 Refer to the add_integrity_check command on page 86.
rules. Refer to the glob manual page for details77. When a pattern is specified it
should be enclosed between single quotes to prevent the shell from interpreting
special characters before the pattern is given to QDocSEConsole. This option
works with local drives only; it has no effect with remote drives.
When the ‘-dp’ option is used and this does not select all files under the
directory, then the non-matching files will not be audited (if they were not
audited encrypted before). Again, remember that this option has no effect with
remote drives.
The ‘-excl’ specification is optional. When <excluding_pattern> is
specified then matching files will be removed from the list. Note that when
both ‘-dp’ and ‘-excl’ are specified the ‘-dp’ matches are added to the list and
then the ‘-excl’ matches are removed from the list.
The ‘-e’ is optional. When not specified the default parameter is “no”. When
the parameter is “yes” then the selected files will be also be encrypted.
Refer to the list command78 to see which files are audited.
Examples:
QDocSEConsole -c audit -d /usr/local/conf
Errors:
If the ‘-d’ option is missing then an error will be displayed.
If the license is invalid then an error will be displayed.
If QDocSE is not in Elevated mode or Learning mode then an error will
be displayed.
If the ‘-e’ option specifies a value other then “yes” or “no” then an
error will be displayed.
77 Refer to a copy in Appendix C (page 176).
78 See page 109.
With the ‘-dp’ and ‘-excl’ options when <matching_pattern> is not a
valid glob pattern then an error will be displayed.
If the directory is a remote mount type not supported then an error will
be displayed.
cipher
This command will change the default cipher used for encrypting files. Files
that are already encrypted with a particular cipher will not automatically
change to the new cipher setting. The list command display will show which
cipher is used with files that are encrypted.
When you change the default cipher you continue to have the same access to
files encrypted with previous cipher selection.
At installation the default cipher is set based on your locale. The locale of your
system was set when you installed Linux® for the first time.
The ciphers currently available are specified by different standards in different
locales. The default cipher is AES when QDocSE doesn’t match the system
locale to one of the non-AES ciphers’ locale specified for the standard in that
locale.
The performance of each cipher is different and this will affect how long it
takes to encrypt new files, and the subsequent reads and writes to those files.
QDocSE provides the same performance for the available ciphers across all of
the Linux® kernel versions supported. For example, aes and sm4 ciphers both
use the Intel x86_64 instructions NI, AVX and AVX2 for faster cipher
calculations with Linux® kernels 3.X to 6.X. Linux® normally only offers sm4
in the mid-5.X and later kernel versions. Also understand that if the version of
Linux® does not offer AVX or AVX2 then QDocSE cannot use it.
Active modes: Elevated
License Type: All
The available options are:
aes
camellia
kalyna
sm4
Where only one of the four options shown above must be provided79. For
reference, AES is for North America plus most of Europe80, Camellia is for
Japan81, Kalyna for Ukraine, and SM4 for China.
Example:
QDocSEConsole -c cipher kalyna
Errors:
If an invalid cipher name was specified then an error will be displayed.
cipher_mode
This command will change the default cipher mode that will be used when a
new file is being encrypted. Changing the cipher mode will not change existing
encrypted files.
When you change the default cipher mode you continue to have the same
access to files encrypted with previous cipher mode(s).
At installation the default cipher mode is set based on your default cipher.
Refer to the cipher command for related information.
Active modes: Elevated, Learning
License type: all
79 If you require a cipher not specified then please contact BicDroid about adding it.
80 NESSIE has both AES and Camellia as selected ciphers.
81 CRYPTREC has both Camellia and AES on the Recommended Ciphers List.
Options for this command are:
[ cbc | ctr ]
When cbc is selected then the current cipher will use CBC mode.
When ctr is selected then the current cipher will use CTR mode.
Example:
QDocSEConsole -c cipher_mode ctr
Errors:
If QDocSE is not licensed or is in De-elevated mode then an error
message about this is displayed.
commands
This lists the commands that are available and active for the current license.
This makes it easier to determine what actions you can perform.
Active modes: All
License type: All
The available option is:
-a
The ‘-a’ option will display all of the commands regardless of the current
license.
Remember that you can use the ‘-h’ option with any command to have help for
that command displayed. Appendix A contains a table listing every command
and which licenses it is available with.
Example:
QDocSEConsole -c commands
Errors:
None.
device_encrypt
This command will encrypt a block device. The status of encrypted block
devices are displayed with the list_device_encrypt 82 command.
The regular QDocSE command encrypt is for regular files presented by a file
system such as XFS or ext4. A block device file is closer to a raw presentation
of the disk storage and needs to be handled differently. Oracle’s ASM uses
block device files for performance reasons. If you want to encrypt data stored
with ASM then device_encrypt is the command to use.
Support for device encryption is aided by DMcrypt’s ‘cryptsetup’ tool for
version 1.2 and later.
Active modes: Elevated, Learning
License type: A, B
The available options are:
-a [ mount | no ]
-b <backup_directory>
-b delete_all_existing_data_on_source
-b source_is_already_encrypted -i <bdid>
-b zeroize_first_100MB_of_encrypted
-s <src_device>
The ‘-a’ option is optional. This option substitutes the original device name
with the full encrypted device name. The purpose of the ‘-a’ option is to allow
for existing mount commands, in scripts or configuration files, to use the
original device name – the “/etc/fstab” file’s content is one example. As an
option example, with ‘-a’ specified then “/dev/sda1” will be mounted as
“/dev/sda1/<bic_encrypted>” where <bic_encrypted> will be a UUID. The
default is no.
82 See page 111.
The ‘-b’ option is required. There are 4 choices for the argument that is used
with ‘-b’ described below. Only one ‘-b’ argument can be used per command.
<backup_directory>
This option specifies the full path of the directory where the original
data will be temporary archived.
source_is_already_encrypted -i <bdid>
This special option value, with the required ‘-i <bdid>’ option, can be
used to recover access to a previously encrypted device. Examples
include when the device is moved to a different machine, or when a
previous QDocSE with an encrypted device was uninstalled. This
special option value is useful in “multipath” situations where the same
device appears with more than one device ID, or appears on several
machine simultaneously via a SAN. In all cases the device should be
encrypted only once, and all subsequent references to the same device
should use this special option value. You can reference an existing
<bdid> for a device using the list_device_encrypt command83.
delete_all_existing_data_on_source
This special option value can be used instead of <backup_directory>
to request that the ‘-s’ <source_device> be securely wiped and
encrypted with no backup copy made. This is faster than making a
backup and copying it back but all data on the <source_device> will
be lost.
zeroize_first_100MB_of_encrypted
This special option value can be used instead of <backup_directory>
to request that the resulting encrypted device has its first 100MB
written with zeros with no backup copy made. This is significantly
faster than manually saving a backup of the data and then copying it
back. NOTE: all data on the <source_device> will be irretrievable.
This is useful for certain applications that fail if they see non-zero data
83 See page 111.
at the beginning of a volume.
WARNING: Only use this option once per device. Never repeat.
The ‘-s’ option is required. This option specifies the full path for the block
device to be encrypted.
Example (line wraps):
QDocSEConsole -c device_encrypt -s /dev/mapper/raid1
-b /extra/space -a mount
Errors:
When the ‘-a’ option is used and its argument is not “no” or “mount”
then an error message is displayed.
When the ‘-b’ option is used and no argument supplied then an error
message is displayed.
With ‘-s’, if a device or volume is specified that doesn’t exist then an
error message is displayed.
elevate
This command is to change QDocSE from De-elevated mode to Elevated
mode. This requires a new elevation file as part of the security process so that a
non-authorized intruder cannot move to Elevated mode to change the
configuration of QDocSE. Each elevation file can only be used once.
Active modes: De-elevated
License type: All
The available options are:
-ef <elevate_file>
-f <elevate_file>
-t <value><time_unit>
where <elevate-file> is the name of the elevation file to allow QDocSE to
move from De-elevated mode to Elevated mode. The ‘-b’ option is deprecated
and will be removed in a future release.
The ‘-t’ option is required and specifies the maximum length of time that
QDocSE will stay in Elevated mode. This Elevation Time affects Learning
mode. When Elevation Time has expired then QDocSE will automatically
move to De-elevated mode. <value> is a positive number paired with the
optional <time_unit> to specify the time. A <time_unit> will be one of ‘d’
(days, the default), ‘h’ (hours), ‘m’ (minutes) or ‘s’ (seconds). The maximum is
the equivalent of 1096 days.
NOTE: For security reasons you should delete the elevation file once it has
been successfully used.
Example:
QDocSEConsole -c elevate -f ElevateFile -t 200m
Errors:
If the elevation file does not match this endpoint installation then an
error will be displayed.
If this elevation file has been applied to this endpoint before then an
error will be displayed.
If there is a problem with the format of the elevation file then an error
message will be displayed.
If the Elevation time specified with ‘-t’ is an invalid time or longer
than 1096 days then an error message will be displayed.
encrypt
This command will encrypt files using the default cipher and default cipher
mode. Refer to the cipher command84 for information about the cipher. All
programs will have access to the encrypted files that had access to the plaintext
files with most licenses (‘B’ to ‘G’); licenses with protection (‘A’) will be
limited to Authorized programs. Programs successfully accessing the encrypted
files will be provided the plaintext version transparently.
Every new file is encrypted with a unique File Encryption Key (FEK) for the
file’s data. Every FEK is kept within the encrypted section of the file’s
metadata. File metadata is encrypted using an Effective File Encryption Key
(EFEK). The EFEK used is based on the current key identifier (“KeyID”) and
can be updated using the update_keys command85. New KeyIDs are
distributed to QDocSE endpoints by CSP.
When a new file is created then the file data and file metadata both use the
current cipher and cipher mode defaults (as displayed with the view
command).
Active modes: Elevated, Learning
License type: A, B, F, G
The available options are:
-A <acl_id>
-B
-d <directory>
-D <parallel_directory>
-dp <matching_pattern>
-excl <excluding_pattern>
84 See page 94.
85 See page 134.
-N
-o <output_file>
-P <acl_id>
-R yes
-t <number_of_threads>
where <directory> is the directory, and sub-directories, containing the files to
be encrypted. By default all files under the directory, and its sub-directories are
added. Also by default the plaintext file will be replaced with encrypted files in
the same <directory>.
With ‘-D’, when <parallel_directory> is specified, the plaintext files will
be left unchanged in <directory> and encrypted copies will be placed in
<parallel_directory>; the <directory> and <parallel_directory> will
have the same hierarchy.
When <matching_pattern> is specified with ‘-dp’ then only the filenames
that match the pattern in the directory and sub-directories are added to the
match list.
Use of ‘-dp’ is optional. The pattern will be used to select which files under the
named directory will be encrypted. The pattern for matching follows the
glob(7) rules. Refer to the glob manual page, Appendix C, for details86. When
<matching_pattern> is specified then only the filenames that match the
pattern in the directory and sub-directories are added to the match list. When a
pattern is specified it should be enclosed between single quotes to prevent the
shell from interpreting special characters before the pattern is given to
QDocSEConsole. This option works with local drives only; it has no effect with
remote drives.
When the ‘-dp’ option is used and this does not select all files under the
directory, then the non-matching files will remain unencrypted (if they were
86 Refer to a copy in Appendix C (page 176).
unencrypted before). Remember that this option has no effect with remote
drives.
The ‘-excl’ specification is optional. When <excluding_pattern> is
specified then matching files will be removed from the list. Note that when
both ‘-dp’ and ‘-excl’ are specified the ‘-dp’ matches are added to the list and
then the ‘-excl’ matches are removed from the match list.
NOTE: When both ‘-dp’ and ‘-excl’ are specified the ‘-dp’ matches are
added to the list and then the ‘-excl’ matches are removed from the list. Both
options use the glob rules for composing the pattern.
The ‘-A’ option sets the user access for all of the matching files to <acl_id>.
This option sets the default user access ACL for new files. Refer to the acl_*
commands for more information.
The ‘-B’ option will run the encrypt command in the background like a
daemon. This allows the Administrator to use the terminal for other tasks or to
logout of the terminal with the encrypt command continuing without
interruption. The ‘-B’ option should be used with the ‘-o’ option. Some sites
will automatically logout terminals that have been inactive for a certain
number of minutes which would end the encrypt command because of a
SIGHUP. This option separates the command from the terminal so the
command will not be affected by SIGHUP. Customers with data to be
encrypted that will take many hours or days will find this option helpful.
The ‘-d’ option is mandatory.
The ‘-D’ option is for customers that want to leave their original plaintext
unchanged and have encrypted copies of those files put in a separate directory.
The ‘-N’ option specifies that only new files will be encrypted.
The ‘-o’ option saves QDocSEConsole’s terminal output to a file. It is intended
to be used with the ‘-B’ option so that an Administrator can read the file to
determine what the encrypt command has completed.
The ‘-P’ option sets the program access for all of the matching files to
<acl_id>. This option sets the default program access ACL for new files.
Refer to the acl_* commands for more information.
The ‘-R’ option specifies that a file system will be treated the same as a remote
file system for encryption87. This is a useful option with union file systems88
that do not provide a consistent inode value for each file across reboots.
The ‘-t’ option specifies the number of threads to use when encrypting files.
The default is a value calculated based on the number of CPUs on the system.
The maximum value is 63.
Examples:
QDocSEConsole -c encrypt -d /home/roger/data
Errors:
If the ‘-d’ option is missing.
With ‘-d’ when <directory> is not a directory.
With ‘-D’ when <parallel_directory> is not a directory.
With ‘-dp’ or ‘-excl’ when then pattern is not a valid glob syntax then
an error message will be displayed.
With ‘-o’ when <output_file> cannot be created or written to then an
error message will be displayed.
With ‘-R’ when any value other than “yes” then an error message will
be displayed.
When ‘-t’ specifies a value greater than 63 or less than 1 an error
message will be displayed.
If the license is invalid.
87 See page 64 for more information about remote file systems.
88 Oracle’s ASM behaves like a union file system though it is a volume manager.
If QDocSE is not in Elevated mode or Learning mode then an error will
be displayed.
encrypt_pattern
This command saves a glob pattern for a specific directory that has already
been set for file encryption with the encrypt command89. A different pattern
can be specified for each directory. For each new file created under the specific
directory that matches the glob pattern it will be encrypted; files not matching
the glob pattern will be plaintext.
glob patterns must conform to IEEE Std 1003.2-1992 (aka “POSIX.2”) and
X/Open Portability Guide Issue 4, Version 2 (aka “XPG4.2”). The QDocSE
implementation is based on the BSD implementation, and a description can be
found in Appendix C90.
When no glob pattern is saved then this is the same as always matching.
Saved patterns will be displayed with the list command91.
NOTE: We always recommend that the patterns are within single quotes to
prevent the shell interpreting or expanding the pattern.
Active modes: Elevated
License type: A, B, F, G
The available options are:
-d <directory>
-p <pattern>
The ‘-d’ and ‘-p’ options are mandatory.
89 See page 101.
90 See page 176.
91 See page 109.
With the ‘-d’ option the <directory> specifies a directory that is already
being monitored by QDocSE to encrypt files. Directories already monitored
can be displayed with the list command.
With the ‘-p’ option the <pattern> will be used to select which new files
under the named directory will be encrypted files.
Examples:
QDocSEConsole -c encrypt_pattern -p ‘*.dat’ -d
/home/roger/datadir
QDocSEConsole -c encrypt_pattern -p ‘*/subdir[123]/*’ -
d /home/roger/datadir
Errors:
If QDocSE does not have a valid license then an error message will be
displayed.
If QDocSE is not in Elevated mode or Learning mode then an error
message will be displayed.
If the option ‘-d’ is not specified then an error message will be
displayed.
If the option ‘-p’ is not specified then an error message will be
displayed.
If the <directory> specified with the ‘-d’ option is not already
monitored then an error message will be displayed.
finalize
This command moves QDocSE from Elevated mode or Learning mode to De-
elevated mode immediately. This prevents any further changes to the
configuration of QDocSE and full security becomes active.
If there is any pending configuration change (or changes) that have not yet
been “pushed” by the push_config command then finalize will perform the
push_config.
NOTE: QDocSE will automatically change to De-elevated mode when the
Elevation Time92 expires. This is a safety measure.
Active modes: Elevated, Learning
License type: A, C, D, E
There are no options for this command.
Example:
QDocSEConsole -c finalize
Errors:
If QDocSE does not have a valid license then an error message will be
displayed.
hash
This command allows you to change the default hash algorithm that is used for
calculating the hash for data integrity files.
The default algorithm used is Blake2b.
Active modes: Elevated, Learning
License type: All
The option for this command is to specify one of:
[ blake2 | md5 | sha256 | sm3 ]
Example:
QDocSEConsole -c hash blake2
92 See page 46.
Errors:
If an invalid cipher name was specified then an error will be displayed.
If a hash name was not provided then an error will be displayed.
If the current license is invalid then an error will be displayed.
If QDocSE is not in Elevated mode or Learning mode then an error will
be displayed.
install_prep
This command is used to prepare QDocSE for being either upgraded to a new
version or uninstalled. This command can only be run when the license is valid
and when QDocSE is in Elevated mode. You may need to use the elevate
command to move into Elevated mode93.
For security reasons an upgrade or uninstall/removal can only happen when in
Elevated mode. This prevents an intruder that has obtained administrator
access from removing QDocSE from the system.
After running this command you will need to reboot the system so that certain
portions of QDocSE security may be disabled cleanly. If you do not upgrade or
uninstall then security will be fully re-established within 40 minutes of the
command being issued.
Active modes: Elevated, Learning
License type: All
Command aliases: upgrade_prep, uninstall_prep
The available options are:
on
off
93 See page 45.
where on will prepare the system, and off will clear a previous on (before the
reboot). If you use the off option followed by reboot then QDocSE will start
with full security, and an upgrade or uninstall/removal will not be possible.
Example:
QDocSEConsole -c install_prep on
Errors:
If neither the ‘on’ nor ‘off’ action is specified then an error message is
displayed.
licence
This command is an alias for the activate command94.
license
This command is an alias for the activate command95.
list
This command lists the status of files in a particular directory or the status of a
specific file. The file or directory specified does not need to be a QDocSE
protected directory. The output will indicate whether each file is encrypted or
not encrypted as well as labels indicating if the file is protected or normal. The
list may also include some files with different labels such as block, character,
fifo, folder, link, socket, special or shielded. The file mode attribute is also
displayed for each file.
When a file is encrypted the type of cipher used for the encryption will be
displayed in brackets.
94 See page 84.
95 See page 84.
The meaning of each label is:
• audited – the file is audited
• block – a block special device
• character – a character special device
• encrypted – the file is encrypted and the cipher used is displayed
• fifo – a Unix FIFO device
• folder – a directory
• integrity – the data file is monitored for change and access, also shows status
• link – a file linked to another file
• monitored – the program or shared library file is monitored for change and
access, shows status (for authorized and monitored settings)
• normal – a file that QDocSE does not guard or monitor
• not_encrypted – the file is not encrypted
• protected – a file with access limited by QDocSE
• shielded – a file or directory shielded by QDocSE to be read-only
• socket – a file socket
• special – a file that is special to QDocSE and strongly protected (no access)
Refer to the section on Self Defence on page 26 for more information about
special and shielded files.
Active modes: De-elevated, Elevated, Learning
License type: All
The available option is:
-d <file_or_directory-name>
where <file_or_directory-name> is the directory to list the contents of, or a
specific file. The named directory can be any directory on the system. When
this option is not specified then the current directory will be used.
Example:
QDocSEConsole -c list -d /opt/qdoc
QDocSEConsole -c list -d /tmp/XXX/demo.pdf
Errors:
If a file or directory is specified that doesn’t exist then an error message
is displayed.
list_device_encrypt
This command will list the block devices currently encrypted by QDocSE and
the status information for each. The information displayed are the cipher used
for encryption, the disk ID, the bdid (“BicDroid id)” for the device, the
mapped device and whether the block device is automapped. If there are
additional links to the block device then they will be displayed. Information
displayed will have been configured by the command device_encrypt 96.
NOTE: the device_encrypt command97 requires providing the corresponding
bdid when using the ‘-b source_is_already_encrypted’ option.
Active modes: De-elevated, Elevated, Learning
License type: A, B
There are no options for this command.
Example:
QDocSEConsole -c list_device_encrypt
Errors: There are no errors for this command.
96 See page 111.
97 See page 97.
list_handles
This command will list a process ID (PID) with the matching program name
for each process that has an open file descriptor to a file or directory specified
with the command.
Active modes: Elevated, Learning
License type: E
The option for this command is:
-d <directory>
where <directory> is the directory that will be checked for open file handles.
The named directory can be any directory on the system.
Example:
QDocSEConsole -c list_handles -d <directory>
Errors:
If the ‘-d’ option is missing then an error will be displayed.
With ‘-d’, when <directory> is not a directory then an error will be
displayed.
If the current license is invalid then an error will be displayed.
list_monitored
This command will list information about a specific monitored program. The
list will display the names of the program and each of the shared libraries that
the program uses along with file size, signature and status. The status will
show either “monitored” or “not_monitored”.
Active modes: De-elevated, Elevated, Learning
License type: E
The option for this command is:
-p <program>
Example:
QDocSEConsole -c list_monitored -p /usr/bin/more
Errors:
If the ‘-p’ option is missing then an error will be displayed.
With ‘-p’, if <program> is not a valid path then an error will be
displayed.
list_acl
This command is an alias for the acl_list command. See also list_acls.

list_acls
This command is an alias for the acl_list command.

Logging
This command controls the QDocSE logging configuration. It allows the
administrator to configure what events are logged and where log messages
are sent.
Active modes: Elevated, Learning
License type: All
Refer to the QDocSE User Guide page 115 for full option details.

monitor_update
This command is an alias for the update_monitored command98.
protect
This command specifies which data file(s) should be protected. Protected data
files are only accessible to authorized programs. As an option the data files
may be left in “plain text” or encrypted. When data files are encrypted the
contents are translated back to “plain text” automatically for authorized
programs – also known as Transparent Data Encryption (TDE). New files
created by an authorized program will have protection added.
NOTE: If you do not specify any authorized programs with the adjust
command then there will be no access to any protected data files in De-
elevated mode.
NOTE: If you want to reverse the action of a protect command then use the
unprotect command (see page 137).
98 See page 135.
NOTE: Executable files will not be protected. If a file has an ELF header,
regardless of the file mode being executable or not, then it will not be
protected. If you want an executable file to be added to the list of authorized
programs then it cannot reside in a protected directory.
NOTE: Do not run the protect command while the shell’s present working
directory (pwd) is in or under a directory that has files you want to protect. If
you do then you will be in a strange “permission bubble” that will not have
protection enabled (no one else can enter this bubble). Changing to a new
directory will clear this “bubble”.
When specifying which data files to protect you must understand whether the
files are on a local or remote file system. Remote file systems include NFS,
CIFS, AFS, etc. Local file systems are on disks directly connected to the
system; not accessed over the network.
With local file systems you can specify a directory, or specify a directory with
a file matching or excluding pattern. When a directory alone is specified then
all files under that directory will be protected. When a directory with a file
matching pattern (‘-dp’) is specified then only the filenames matching that
pattern under that directory will be protected; excluded files (‘-excl’) will not
be protected. You can use the protect command multiple times with different
file matching patterns for the same directory.
Remote directories and their contents are not completely controlled by the
local system or QDocSE for that matter. Remote directories are shared among
the original host and, potentially, many other systems. It is too costly and
difficult as a remote system to track all of the changes in real-time. Therefore
when you specify a remote directory with the protect command all of the
files under that directory become protected, and the file matching or excluding
pattern will be ignored. You must also understand that QDocSE only has
control over what the local system does to the remote directory. This means
that for complete coverage there needs to be QDocSE installed on the original
host system and every remote systems using the directory.
The patterns for matching or exclusion follows the glob(7) rules. Refer to the
glob manual page for details99. When a pattern is specified it should be
enclosed between single quotes to prevent the shell from interpreting special
characters before the pattern is given to QDocSEConsole.
Regardless of the directory, the matching pattern or excluding pattern you can
specify whether you want the protected files to be encrypted or not. When
encryption is specified (“yes”) then it will take longer to complete the
protection. But the security of the system is significantly enhanced because of
data-at-rest protection. The additional amount of time to encrypt is directly
proportional to the size of all of the files to be encrypted added together.
Encrypting files on a remote directory will take longer due to network
communications. All QDocSE endpoints with the same master key can
decrypt/encrypt this remote mount. Please understand that each customer gets a
different master key and there is no access overlap amongst master keys.
Furthermore, there is no “super master key”.
When encryption is happening several files will be worked on in parallel to
maximize CPU, driver and disk throughput. CPU usage of QDocSEConsole can
appear as num_of_cpus * 100% for some time periods. This is expected and
normal.
The protect command operates by finding all of the files that match and then
begins processing the files. That is two separate steps. While files are being
processed a progress summary is displayed. The more files you have the longer
protection will take. If there are a lot of files to match then you may not see
any progress message for a long period of time. When the progress messages
are printing this is an estimate.
An additional consideration that we recommend that you implement is the use
of ACLs100 on the protected data files101. Traditional Unix-like file permissions
are very broad with the scope of protection as User, Group and Other. These
99 Refer to a copy in Appendix C (page 176).
100Access Control Lists.
101We’ve made this recommendation with the adjust command for authorized programs too.
are very crude ranges compared to using ACLs. Being able to specifically list
users that are allowed and disallowed will enhance data security.
There is a special “race case” that users ask about: what is the status of a file
created under the <directory> after the command has started? In most cases
the file will be a regular file (unprotected). If the encryption option is “yes”
then the file will be encrypted and unprotected. If you have already configured
authorized programs with the adjust command and the push_config
command then new files created by the authorized program will be protected.
NOTE: DO NOT reboot or shutdown the system during protection, especially
with encryption happening. Wait until QDocSEConsole finishes and the shell
prompt appears.
Active modes: De-elevated, Elevated, Learning
License type: A
Available options are:
-A <acl_id>
-d <directory>
-dp <pattern_match>
-excl <pattern_exclusion>
-e [ yes | no ]
-P <acl_id>
-R yes
-t <number_of_threads>
Each option above can only be specified once except for the ‘-d’ option. The
‘-e’ and ‘-d’ options must always be specified.
Use of ‘-excl’ is optional.
The ‘-A’ option sets the user access for all of the matching files to <acl_id>.
This option sets the default user access ACL for new files. Refer to the acl_*
commands for more information.
The ‘-P’ option sets the program access for all of the matching files to
<acl_id>. This option sets the default program access ACL for new files.
Refer to the acl_* commands for more information.
The ‘-R’ option specifies that a file system will be treated the same as a remote
file system for encryption102. This is a useful option with union file systems103
that do not provide a consistent inode value for each file across reboots. All
files will be protected and the ‘-dp’ option will be ignored.
The ‘-t’ option specifies the number of threads to use when encrypting files.
The default is a value calculated based on the number of CPUs on the system.
The maximum value is 63.
Use of ‘-dp’ is optional. The pattern will be used to select which files under the
named directory will become protected. The pattern for matching follows the
glob(7) rules. Refer to the glob manual page for details104. When a pattern is
specified it should be enclosed between single quotes to prevent the shell from
interpreting special characters before the pattern is given to QDocSEConsole.
This option works with local drives only; it has no effect with remote drives.
When the ‘-dp’ option is used, and does not select all files under the directory,
then the non-matching files will remain unprotected and unencrypted (unless
they were encrypted before). Again, remember that this option has no effect
with remote drives.
The ‘-excl’ specification is optional. When <excluding_pattern> is
specified then matching files will be removed from the list. Note that when
both ‘-dp’ and ‘-excl’ are specified the ‘-dp’ matches are added to the list and
then the ‘-excl’ matches are removed from the match list.
102See page 64 for more information about remote file systems.
103Oracle’s ASM behaves like a union file system though it is a volume manager.
104Refer to a copy in Appendix C (page 176).
Examples:
QDocSEConsole -c protect -d /usr/data1 -e yes
QDocSEConsole -c protect -d /usr/data2 -dp ‘*.doc’ -e no
QDocSEConsole -c protect -e no -d /usr/data -excl ‘*gz’
Errors:
If the directory does not exist then an error message is displayed.
If neither ‘yes’ nor ‘no’ is used with the ‘-e’ option then an error
message is displayed.
With the ‘-dp’ and ‘-excl’ options when <matching_pattern> is not a
valid glob pattern then an error will be displayed.
If QDocSE not licensed then an error message is displayed.
push_config
This command commits the changes in configuration for authorized programs
and their shared libraries, and for the ACL configuration to the QDocSE
system. You should review the changes before performing the push_config
command by running the acl_list, view and view_monitored commands105.
This command is an important part of security. Reviewing the list of changes
with the acl_list and view_monitored command should be done before
running the push_config command. You, as a competent, professional
Administrator, want to verify the changes – you may notice a shared library
that should not be used by the program you are authorizing. If someone has
compromised the computer before QDocSE was installed then you may notice
the problem before committing your changes with push_config.
NOTE: If you issue the finalize command then the push_config command
will automatically be done.
105See page 143 and page 145 respectively.
Active modes: Elevated, Learning
License type: A, E
There are no options for this command.
Example:
QDocSEConsole -c push_config
Errors:
If QDocSE not licensed then an error message is displayed.
If QDocSE not in Elevated mode or Learning mode then an error
message is displayed.
regen
This command will regenerate the configuration files for QDocSE using the
existing configuration. This will not change the configuration. This command
is available in case there has been a disk failure that has damaged configuration
files.
Active modes: De-elevated, Elevated, Learning
License type: All, Unlicensed
There are no options for this command.
Example:
QDocSEConsole -c regen
Errors:
There are no errors.
remove_integrity_check
This command will stop monitoring selected data files. By default all files
under the specified directory will be selected. Optionally files under this
directory matching a pattern will be selected.
The selected data files will no longer cause any messages to be generated when
the files are changed or are accessed.
Refer to the add_integrity_check command for more details about
monitoring data files.106
Active modes: Elevated, Learning
License type: D
The available options are:
-d <directory>
-dp <matching_pattern>
-excl <excluding_pattern>
The ‘-d’ option is required. The ‘-d’ option specifies a directory that integrity
checking will be removed from. All files currently being monitored will no
longer be monitored unless the ‘-dp’ option has been used and it did not select
all of the monitored files.
Use of ‘-dp’ is optional. The pattern will be used to select which files under the
named directory will no longer have their integrity checked. The pattern for
matching follows the glob(7) rules. Refer to the glob manual page for details.
When a pattern is specified it should be enclosed between single quotes to
prevent the shell from interpreting special characters before the pattern is given
to QDocSEConsole. This option works with local drives only; it has no effect
with remote drives.
106See page 86.
When the ‘-dp’ option is used and this does not select all integrity files under
the directory, then the non-matching files will remain monitored and encrypted
(if they were encrypted before). Remember that this option has no effect with
remote drives.
The ‘-excl’ specification is optional. When <excluding_pattern> is
specified then matching files will be removed from the list. Note that when
both ‘-dp’ and ‘-excl’ are specified the ‘-dp’ matches are added to the list and
then the ‘-excl’ matches are removed from the match list.
Example:
QDocSEConsole -c remove_integrity_check -d my_dir
Errors:
If the current license is invalid then an error will be displayed.
If QDocSE is not in Elevated or Learning mode then an error will be
displayed.
With the ‘-d’ option when <directory> has not been specified then an
error will be displayed.
With the ‘-d’ option if the directory <directory> does not exist then
an error will be displayed.
With the ‘-d’ option when <directory> specified is not a directory
then an error will be displayed.
With the ‘-dp’ option when <matching_pattern> is not a valid glob
pattern then an error will be displayed.
remove_monitored
This command will stop monitoring selected programs and might stop
monitoring shared library files. Remember that monitored programs are similar
to but not the same as authorized programs.107
Any shared library files used by the program will no longer be monitored if
this program is the last monitored program using them. When other monitored
programs are using a shared library then the shared library continues to be
monitored.
Programs no longer monitored will not have messages sent to CSP if they are
modified. Shared libraries no longer monitored will not have messages sent to
CSP if they are modified.
Refer to the add_monitored command for more details about monitoring
program and shared library files.
Refer to the view_monitored command to see a list of currently monitored
programs and shared library files.
Active modes: Elevated, Learning
License type: E
The available options are:
-p <program>
where <program> specifies the full path of the program to stop monitoring.
The ‘-p’ option is required.
Example:
QDocSEConsole -c remove_monitored -p /usr/bin/sha256
Errors:
107Refer to the adjust command on page 89 for more details.
A <program> was not specified with the ‘-p’ option.
The <program> specified is not currently monitored.
The <program> specified is not a program.
QDocSEConsole cannot be specified as a <program>.
QDocSEService cannot be specified as a <program>.
If the current license is invalid then an error will be displayed.
When QDocSE is not in Elevated or Learning mode then an error will
be displayed.
renewcommit
This command is used to update the QDocSE license. As a best practice this
command should be used before the current license expires to maintain OS
security coverage. However, this command can still be applied if the previous
license has expired.
Before using the renewcommit command you will need to run the
renewrequest command to obtain a new license.
The new license file will be downloaded by you from the QDocSE web site
after the renewrequest command has been run. Contact your BicDroid sales
engineer for more details.
The renewcommit command can be run anytime after the original license was
applied. For example, you can run this command 3 weeks early.
NOTE: For security reasons you should delete the license file once it has been
successfully used.
Active modes: De-elevated, Elevated, Learning
License type: All
Options for this command are:
-f <new_license_filename>
-cf <new_license_filename>
Where <new_license_filename> is the location of the file with the new
license. The ‘-cf’ option is deprecated and will be removed in a future release.
Example:
QDocSEConsole -c renewcommit -f NewLicenseFile
Errors:
If the license file does not match the QDocSE endpoint then an error
message is displayed.
If the file is not a license file then an error message is displayed.
If the file does not exist then an error message is displayed.
renewrequest
This command is used to generate a special text file that will be uploaded to
the BicDroid web site as part of obtaining a new license.
The special text file is specific to the computer it is created on. This will help
match the new license to the specific computer.
NOTE: The path that you specify for the <renew_request_filename> cannot
be one of the directories that is protected by either DG or SG.
After the renew file is create you will upload it to the QDocSE web site. This
will allow you to then click a button to generate a new license file, and then
download the new licence file. Refer to the renewcommit command to apply
the new license.
Active modes: De-elevated, Elevated, Learning
License type: All
The option for this command is:
-f <renew_request_filename>
-rf <renew_request_filename>
Where <renew_request_filename> is the location to write the file with the
renew request content. The ‘-rf’ option is deprecated and will be removed in a
future release.
Example:
QDocSEConsole -c renewrequest -f RenewFile
Errors:
If the output file is not specified with the ‘-f’ option then an error
message is displayed.
If the output file is not specified with the ‘-rf’ option then an error
message is displayed.
If the file does not exist then an error message is displayed.
set_access
This command sets the QDocSE access mode for user accounts with the
capability CAP_DAC_OVERRIDE.
Active modes: Elevated, Learning
License type: all
Options for this command are:
[ inspector | normal ]
When inspector is specified then data access is extended for user accounts
with the Linux capability CAP_DAC_OVERRIDE. A Linux capability is similar to
a special privilege on some other operating systems. With QDocSE, when
ACLs are being used, the Linux capabilities are blocked to enhance normal
security. With inspector mode if the user account would normally be denied
access to a file’s plaintext data, and the user account has the capability
CAP_DAC_OVERRIDE then read-only access to the encrypted data will be
permitted.
When normal is specified then Linux capabilities are blocked when QDocSE
ACLs are being used. User accounts allowed access will have read and/or write
access to plaintext data. User accounts not allowed access will be denied any
access.
The current access status is displayed with the view command’s “Working
Mode” line.
Example:
QDocSEConsole -c set_access normal
Errors:
Must be in Elevated mode to apply command.
No license or expired license.
Invalid value specified.
Unknown option specified.
set_learning
This command sets QDocSE into Learning mode. You can only change to
Learning mode from Elevated mode. Learning mode is an extension of
Elevated mode. When either the finalize command is used or when Elevated
Time108 expires then QDocSE will move to De-elevated mode. Learning mode
is not active in De-elevated mode.
Refer to the User Guide section Learning mode on page 47 for a complete
description of Learning mode.
108See page 46.
Active modes: Elevated, Learning
License type: A
Options for this command are:
[ off | on | 0 | 1 ]
When off or 0 is specified then QDocSE will move to Elevated mode if
currently in Learning Mode.
When on or 1 is specified then QDocSE will move to Learning mode if
currently in Elevated mode.
Only one of off, on, 0 or 1 can be specified at the same time. For clarity we
discourage the use of 0 or 1.
Example:
QDocSEConsole -c setlearning on
Errors:
If QDocSE is not licensed or is in De-elevated mode then an error
message about this is displayed.
setlearning
This command is an alias for the set_learning command.
set_security
This command controls how key material is managed for encrypting files.
Active modes: Elevated, Learning
License type: all
Options for this command are:
[ central | normal ]
When central is specified then key material is not stored on the local machine
and key material must be sent, or re-sent, from CSP when the local machine is
booted. Any programs accessing encrypted files before CSP has sent, or re-
sent, the key material will be paused until the key material successfully arrives.
Paused in this case means the program is suspended in a non-interruptible
state.
When normal is specified then key material is stored on the local machine
after it has been sent from CSP the first time. With key material stored locally
then programs accessing encrypted files will not be paused when starting after
the local machine boots.
The current security status is displayed with the view command’s “Working
Mode” line.
Example:
QDocSEConsole -c set_security normal
Errors:
Must be in Elevated mode to apply command.
No license or expired license.
Invalid value specified.
Unknown option specified.
show_mode
This command will display the current mode of QDocSE.
Active modes: De-elevated, Elevated, Learning, Unlicensed
License type: All
This command has no options.
There are four possible modes: Unlicensed, De-elevated, Elevated and
Learning.
Example:
QDocSEConsole -c show_mode
Errors:
There are no errors.
show_raw
This command displays the raw content of a QDocSE configuration file. It is
intended for diagnostic and inspection purposes.
Active modes: De-elevated, Elevated, Learning
License type: All
The available options are:
-C
-f <filename>
The '-C' option displays the raw ciphertext content.
The '-f' option specifies the file to display.
Example:
QDocSEConsole -c show_raw -C -f my_data1.txt
Errors:
If the '-f' option is missing then an error message is displayed.
If the file does not exist then an error message is displayed.
stop_audit
This command will stop auditing files in the directory indicated. The default is
to stop auditing all of the files in the named directory. The ‘-dp’ option may be
used to stop auditing selected files. If any of the selected files are encrypted
then they will be decrypted.
Refer to the audit command109 for more detail about auditing files.
Active modes: Elevated, Learning
License type: C
The available options for this command are:
-d <directory>
-dp <pattern_match>
-excl <excluding_pattern>
where <directory> is the directory the audited files are located.
The ‘-d’ option is required.
Use of ‘-dp’ is optional. The pattern will be used to select which files under the
named directory will no longer be audited. The pattern for matching follows
the glob(7) rules. Refer to the glob manual page for details. When a pattern is
109See page 92.
specified it should be enclosed between single quotes to prevent the shell from
interpreting special characters before the pattern is given to QDocSEConsole.
This option works with local drives only; it has no effect with remote drives.
When the ‘-dp’ option is used and this does not select all files under the
directory, then the non-matching files will remain audited and encrypted (if
they were audited and encrypted before). Again, remember that this option has
no effect with remote drives.
The ‘-excl’ specification is optional. When <excluding_pattern> is
specified then matching files will be removed from the list. Note that when
both ‘-dp’ and ‘-excl’ are specified the ‘-dp’ matches are added to the list and
then the ‘-excl’ matches are removed from the match list.
Example:
QDocSEConsole -c stop_audit -d /home/ted/data1
Errors:
If the current license is invalid then an error will be displayed.
If QDocSE is not in Elevated or Learning mode then an error will be
displayed.
When ‘-d’ or <directory> has not been specified then an error will be
displayed.
With ‘-d’, if the directory <directory> does not exist then an error
will be displayed.
With ‘-d’, when the <directory> specified is not a directory then an
error will be displayed.
With the ‘-dp’ option when <matching_pattern> is not a valid glob
pattern then an error will be displayed.
unencrypt
This command will unencrypt (decrypt) the files in the specified directory and
sub-directories.
NOTE: Do not shutdown or reboot the system while unencrypt is running. You
may risk the integrity of the data files if you do. Wait until QDocSEConsole
finishes and the shell prompt appears.
Active modes: Elevated, Learning
License type: B
Options for this command are:
-d <directory>
-dp <pattern_match>
-excl <excluding_pattern>
-t <number_of_threads>
The ‘-d’ option is mandatory and specifies a directory that has previously been
encrypted by QDocSE using the encrypt command110.
Use of ‘-dp’ is optional. The pattern will be used to select which files under the
named directory will be unencrypted. The pattern for matching follows the
glob(7) rules. Refer to the glob manual page for details. When a pattern is
specified it should be enclosed between single quotes to prevent the shell from
interpreting special characters before the pattern is given to QDocSEConsole.
This option works with local drives only; it has no effect with remote drives.
When the ‘-dp’ option is used and this does not select all encrypted files under
the directory, then the non-matching files will remain encrypted (if they were
encrypted before). Remember that this option has no effect with remote drives.
110See page 101.
The ‘-excl’ specification is optional. When <excluding_pattern> is
specified then matching files will be removed from the list. Note that when
both ‘-dp’ and ‘-excl’ are specified the ‘-dp’ matches are added to the list and
then the ‘-excl’ matches are removed from the match list.
The ‘-t’ option specifies the number of threads to use when encrypting files.
The default is a value calculated based on the number of CPUs on the system.
The maximum value is 63.
Example:
QDocSEConsole -c unencrypt -d /home/ted/data1
Errors:
If any errors are encountered while decrypting they are displayed.
With ‘-d’, if the <directory> specified does not exist then an error
message about this is displayed.
With the ‘-dp’ option when <matching_pattern> is not a valid glob
pattern then an error will be displayed.
When ‘-t’ specifies a value greater than 63 or less than 1 an error
message will be displayed.
If QDocSE is not licensed or is in De-elevated mode then an error
message about this is displayed.
uninstall_prep
This command is an alias for the install_prep command111.
111See page 108.
update_integrity_check
This command will update the signature for the specified data file. This
command is intended to be used when you know a valid change has happened
with the file.
This command is not for monitored programs or shared libraries. Refer to the
update_monitored command for updating signatures for programs and shared
libraries.
NOTE: You should always investigate if the change in signature should be
allowed for a data file. Do not blindly accept the change.
Active modes: Elevated, Learning
License type: D
There is one option for this command:
-f <filename>
where <filename> is the name of the data file requiring the signature update.
Example:
QDocSEConsole -c update_integrity_check -f
/home/ted/bird.txt
Errors:
If the ‘-f’ option is missing then an error message is displayed.
If <filename> does not specify a valid filename then an error message
is displayed.
If the current license is invalid then an error message is displayed.
If QDocSE is not in Elevated mode or Learning mode then an error
message is displayed.
update_keys
This command will update the Effective File Encryption Key (EFEK) for all of
the encrypted files under the specified directory path. The File Encryption Key
(FEK) remains unchanged. The EFEK will be updated using the current cipher,
current cipher mode, and current key identifier (“KeyID”). New KeyIDs are
distributed to QDocSE endpoints by CSP.
This command can be safely run when programs have files currently open or
not. The command may also be safely repeated. If for some reason the system
is rebooted while the update is happening then the update can be safely
repeated once the system has finished booting.
Active modes: Elevated
License type: A, B, C, E, G
This command takes one argument which is a directory path that QDocSE is
guarding:
<directory_path>
Example:
QDocSEConsole -c update_keys /home/data1
Errors:
If any errors are encountered while updating they are displayed.
Must be in Elevated mode to apply command.
No license or expired license.
Directory path not specified.
update_monitored
This command is used to update the QDocSE information about a monitored
program, shared library or environment variable. This command can only be
used in Elevated mode112.
Monitored programs are programs authorized to access protected data files.
Shared libraries for this command are ones used by authorized programs. The
environment variable is the allowable setting for specific environment
variables when an authorized program is accessing protected data files.
When an authorized program or one of the shared libraries that it uses is
updated then access to protected data files will stop because the signature has
changed. A new signature must be calculated for the changed program or
shared library. By running this command you are accepting the signature
change for this program or shared library. Be careful: if a signature has
changed that you did not expect to change then you should perform a complete
investigation before accepting the changed signature.
Active modes: Elevated, Learning
License type: E
The available options are:
-p <program_path>
-l <shared_library_path>
-e <env_var>
Only one of ‘-p’, ‘-l’ or ‘-e’ may be specified at the same time. Each option
can be specified once only.
If you want to add a program to the authorized list then you should use the
adjust command.
112See page 45.
Shared libraries are only added when they are used by an authorized program
or a monitored program.
Only supported environment variable names can be specified. Currently only
LD_LIBRARY_PATH is supported. The value for the environment variable will be
taken from the current user’s environment (usually the administrator).
When you have completed all changes you must use the push_config
command for the changes to become active.
NOTE: You should always investigate if the change in signature should be
happening for a program or shared library. Do not blindly accept the change.
Example:
QDocSEConsole -c update_monitored -p /usr/bin/cat
QDocSEConsole -c update_monitored -l /usr/lib/libmono-
2.0.so
QDocSEConsole -c update_monitored -e LD_LIBRARY_PATH
QDocSEConsole -c push_config
NOTE: There are several environment variables that if set will invalidate an
authorized program from accessing protected data files because of security
concerns. The current list of banned environment variables includes
LD_PRELOAD, LD_AUDIT, LD_ELF_PRELOAD and LD_DEBUG_OUTPUT.
Errors:
If QDocSE is not licensed then an error message is displayed.
If QDocSE is not in Elevated mode or Learning mode then an error
message is displayed.
If an attempt is made to update the signatures of QDocSEConsole and/or
QDocSEService then an error message is displayed.
upgrade_prep
This command is an alias for the install_prep command113.
unprotect
This command will remove QDocSE protection from data files that were
previously protected (see page 113). Data files that were encrypted by QDocSE
will be decrypted in the specified directory and sub-directories.
NOTE: Do not shutdown or reboot the system while unprotect and/or
decryption are still running. You may risk the integrity of the data files if you
do. Wait until QDocSEConsole finishes and the shell prompt appears.
Unprotecting will take longer than protecting because there are more checks
that occur for completeness and safety. Even if you specified earlier during
protection that the files were not to be encrypted, unprotect will check that
each file is not encrypted – if an encrypted file is found it will be decrypted.
When the command starts it will collect information first before processing
that information. Once processing starts, a progress report will be displayed.
When there are a large number of files that are to be unprotected and decrypted
the amount of time will be proportional to the total number of bytes needing to
be decrypted.
This command works for local and remote directories. Remote directories will
take longer to unprotect because of the network communications overhead.
Active modes: Elevated, Learning
License type: A
Options for this command are:
-d <protected_directory>
-dp <pattern_match>
113See page 108.
-excl <excluding_pattern>
The ‘-d’ option is mandatory and specifies a directory that has previously been
protected by QDocSE (using the protect command114).
Use of ‘-dp’ is optional. The pattern will be used to select which files under the
named directory will be unprotected. The pattern for matching follows the
glob(7) rules. Refer to the glob manual page, Appendix C115, for details.
When a pattern is specified it should be enclosed between single quotes to
prevent the shell from interpreting special characters before the pattern is given
to QDocSEConsole. This option works with local drives only; it has no effect
with remote drives.
When the ‘-dp’ option is used and does not select all files under the directory,
then the non-matching files will remain protected and encrypted (if they were
encrypted before). Remember that this option has no effect with remote drives.
The ‘-excl’ specification is optional. When <excluding_pattern> is
specified then matching files will be removed from the list. Note that when
both ‘-dp’ and ‘-excl’ are specified the ‘-dp’ matches are added to the list and
then the ‘-excl’ matches are removed from the match list.
Example:
QDocSEConsole -c unprotect -d /usr/data
QDocSEConsole -c unprotect -d /usr/data1 -dp ‘*.txt’
Errors:
If any errors are encountered while unprotecting or decrypting they is
displayed.
With ‘-d’, if the directory specified does not exist then an error
message about this is displayed.
114See page 113.
115Appendix C starts at page 176
With the ‘-dp’ option when <matching_pattern> is not a valid glob
pattern then an error will be displayed.
If QDocSE is not licensed or is in De-elevated mode then an error
message about this is displayed.
unwatch
This command will remove QDocSE mounts from the specified directory
without changing the files (i.e. will not decrypt files like the unencrypt
command will). This command is intended as the reverse of the watch
command116.
This should only be used with remote directories (such as NFS client
directories) so that the encryption state of the files on the remote server are not
changed.
Active modes: De-elevated, Elevated, Learning
License type: A, B
The option is:
-d <directory>
where <directory> specifies the directory to remove the “watch” mount from.
Example:
QDocSEConsole -c watch -d /mnt/data/essays
Errors:
An error message will be displayed if directory does not exist. Check
<directory> for typographical errors. If the directory is a remote file
system then check that it has been mounted.
116See page 146.
An error message will be displayed if the path provided is not a
directory (e.g. is a file).
An error message will be displayed if the directory is not being
watched.
If QDocSE is not licensed then an error message about this is displayed.
verify_integrity_check
This command will list the signature status of data files. It will display the files
that are monitored with “integrity” and then show if those files are currently
“valid” or “invalid” when compared to its signature.
Active modes: Elevated, Learning, De-elevated
License type: D
The options for this command are:
-d <directory>
-dp <pattern_match>
-excl <excluding_pattern>
-i
-u
-v
The ‘-d’ option is mandatory and specifies a directory that has previously been
had the the add_integrity_check command117 applied to it.
Use of ‘-dp’ is optional. The pattern will be used to select which files under the
named directory will be unprotected. The pattern for matching follows the
glob(7) rules. Refer to the glob manual page, Appendix C118, for details.
117See page 86.
118Appendix C starts at page 176
When a pattern is specified it should be enclosed between single quotes to
prevent the shell from interpreting special characters before the pattern is given
to QDocSEConsole. This option works with local drives only; it has no effect
with remote drives.
When the ‘-dp’ option is used and does not select all files under the directory,
then the non-matching files will continue to be monitored and encrypted (if
they were encrypted before). Remember that this option has no effect with
remote drives.
The ‘-excl’ specification is optional. When <excluding_pattern> is
specified then matching files will be removed from the list. Note that when
both ‘-dp’ and ‘-excl’ are specified the ‘-dp’ matches are added to the list and
then the ‘-excl’ matches are removed from the match list.
The use of ‘-i’, ‘-u’ or ‘-v’ is optional. These options change what is
displayed. The ‘-i’ option will show only files with invalid signatures. The ‘-
u’ option will show only files without signatures. The ‘-v’ option will show
only files with valid signatures.
Example:
QDocSEConsole -c verify_integrity_check -d /opt/data
Errors:
If QDocSE is not licensed then a message will be displayed.
If the ‘-d’ option was not specified then a message will be displayed.
If <directory> does not exist then a message will be displayed.
With ‘-d’, if <directory> does not specify a directory then a message
will be displayed.
With the ‘-dp’ option when <matching_pattern> is not a valid glob
pattern then an error will be displayed.
verify_monitored
This command will check that the authorized programs and shared libraries
have signatures matching what QDocSE calculated previously, and then display
a list of programs and/or shared libraries that have signatures that do not
match.
Active modes: De-elevated, Elevated, Learning
License type: A, E
There are no options.
Example:
QDocSEConsole -c verify_monitored
When authorized programs are displayed you can use the update_monitored
command119 with the ‘-p’ option to accept the change.
When shared libraries are displayed you can use the update_monitored
command with the ‘-l’ (small ell) option to accept the change.
NOTE: You should always investigate if the change in signature should be
happening for a program or shared library. Do not blindly accept the change.
Errors:
There are no errors. The information displayed will be the programs
and shared libraries with signatures that do not match QDocSE’s
records.
version
This command displays the version of the currently installed QDocSE, the
keyset in use, the date & time the package was built, and a special id.
Active modes: De-elevated, Elevated, Learning
119See page 113.
License type: All, Unlicensed
There are no options.
Example:
QDocSEConsole -c version
Errors:
There are no errors.
view
This command displays the current authorized programs, blocked programs,
watch points (aka protected directories, or aka mount points), license status
and expiry, and working mode120.
Active modes: De-elevated, Elevated, Learning
License type: All, Unlicensed
The options for this command are:
-a
-b
-l
-w
-H
By default when no options are provided this command behaves as if the
options ‘-a’, ‘-b’, ‘-l’ and ‘-w’ are provided.
Option ‘-a’ will display authorized programs.
Option ‘-b’ will display programs blocked from authorization.
120See page 45.
Option ‘-l’ will display license information and status.
Option ‘-w’ will display watch points.
Option ‘-H’ will suppress printing the section headings and separators of the
options above.
In the display each authorized and blocked program will have an index number
with it. That index number may be used for ‘-b’ and ‘-api’ option of the
adjust command, the ‘-p’ option of the acl_add command, the ‘-p’ option of
the acl_program command, and the ‘-p’ option of the acl_remove command.
The ID numbers with the directories under the watch point section are for your
visual reference. They are not used with any other commands.
The current default cipher will be displayed with the license information and
status. The possible cipher names are ‘aes’, ‘camellia’, ‘kalyna’ and ‘sm4’.
To look at the shared libraries being used by authorized programs use the
view_monitored
command121.
Example:
QDocSEConsole -c view
Errors:
There are no errors.
121See page 149.
view_monitored
This command will display what QDocSE is monitoring. The display will
include authorized programs, shared libraries used by authorized programs, the
LD_LIBRARY_PATH setting, and pending updates. It is important to pay
attention to pending updates displayed because they will need to be “pushed”
to become effective/active with the push_config command122. Look carefully
at the paths of the programs and the paths of the shared libraries.
There is always the possibility that your computer has compromised software
before QDocSE is installed. If you notice a library path or library name that
you believe should not be in the list then you should investigate. The additional
time investigating an unfamiliar library is worth the knowledge gained and the
confidence maintained.
It is recommended that you run the view_monitored command before you run
each push_config command, and before you run the finalize command123. A
review of the displayed paths for programs and shared libraries is a best
practice.
Active modes: Elevated, Learning
License type: All
There are no options.
Example:
QDocSEConsole -c view_monitored
Errors:
There are no errors.
122See page 118.
123See page 106.
watch
This command adds a directory to the protected list. We discourage the use of
the watch command for local file systems in favour of the protect command.
Technically this command is a variation of the protect command124.
When the directory is a remote file system new files will be protected and/or
encrypted depending on the license type. With this command, for local file
systems, existing files are not protected or encrypted. New files created by an
authorized program under this directory125 will be added to the list of protected
files and encrypted.
If you will be mounting the same remote file systems on several QDocSE
endpoints then this command is better to use than the protect command. If
you want a remote file system to have its files encrypted then it will be most
efficient to do the encryption on the host system where the files are local and
you have QDocSE installed there. If the remote file system is hosted on a
system that cannot have QDocSE installed then select just one of the QDocSE
endpoints to do the encryption with the protect command and all other
QDocSE endpoints to use the watch command after.
Remote file systems may not be immediately mounted when QDocSE begins to
attempt to protect the file system at boot. When protection begins will depend
on the remote host, the network and when the mounting completes.
The counter-command is the unwatch command126.
Active modes: De-elevated, Elevated, Learning
License type: A, B
The option is:
-d <directory>
124See page 113.
125Including all sub-directories.
126See page 139.
where <directory> specifies the directory where the “watch” mount will be
placed.
Example:
QDocSEConsole -c watch -d /mnt/data/essays
Errors:
An error message will be displayed if directory does not exist. Check
<directory> for typographical errors. If the directory is a remote file
system then check that it has been mounted.
An error message will be displayed if the path provided is not a
directory (e.g. is a file).
An error message will be displayed if the directory is a remote file
system type that is not supported.
An error message will be displayed if the directory is already being
watched.
If QDocSE is not licensed then an error message about this is displayed.
Programming Interfaces
The majority of QDocSE operates in a transparent manner so that users do not
need to modify their programs. However, there are some situations where users
do want to modify their programs for specific cooperation with QDocSE.
Currently this cooperation can be programmatically done using the ioctl()
API with specific request values. For the purposes of this User Guide it is
assumed that you already know how to correctly write a program with the
ioctl() API.
A summary of available ioctl() request values are, after including the
header file “<sys/ioctl.h>”:
1. #define QDOC_IOCTL_VERIFY_FILE _IO(‘q’, 41, char *)
2. #define QDOC_IOCTL_PROT_FILE _IO(‘q’, 22)
All other values are either reserved or unused.
QDOC_IOCTL_VERIFY_FILE
When the ioctl() returns with an error and errno equal to ENOTTY then
this indicates that the file, and the directory it is located in, is not monitored by
QDocSE.
When the ioctl() returns successfully then the results returned in the ‘char’
argument’s memory will be one of four values:
a) ‘U’, Capital U. This indicates that the file’s status is currently
unchecked. This mean no hash or signature is kept for this file.
b) ‘N’, Capital N. This indicates that the file’s status is currently
unknown. This could indicate an error occurred.
c) ‘V’, Capital V. This indicates that the file is monitored and the file’s
status is currently valid.
d) ‘I’, Capital I. This indicates that the file is monitored and the file’s
status is currently invalid.
QDOC_IOCTL_PROT_FILE
When the ioctl() returns with ‘-1’ (an error) and errno equal to ENOTTY
then this indicates that the file, and the directory it is located in, is not
monitored by QDocSE.
When the ioctl() returns a value of ‘0’ then the file is not a protected file.
When the ioctl() returns a value of ‘1’ then the file is a protected file.
Frequently Asked Questions (FAQ)
1. Q: Is QDocSE available for operating systems other than the ones listed
in this User Guide?
A: Yes. Please contact Sales to ask about a specific OS.
2. Q: Does QDocSE protect data when an intruder has obtained access to
the “root” account?
A: Yes when OS Security is active. QDocSE guards the protected data
so that access to that data is limited to the authorized programs
regardless of the user account. Furthermore, the configuration of
QDocSE cannot be changed by the intruder and QDocSE cannot be
turned off or disabled by the intruder while QDocSE is in De-elevated
mode.
3. Q: How long will it take to encrypt all of my protected files?
A: There are many factors. The speed of your disk, bus speed of your
motherboard, CPU speed and number of CPUs, the number of files, the
total size of all data to be encrypted. It is difficult to provide a general
answer for everyone. We can state that QDocSE 2.0.0 and later versions
are several factors faster than QDocSE 1.4.3 and earlier versions. Please
refer to the Planning section of this User Guide127 for more
information.
4. Q: What is Learning Mode?
A: Refer to the User Guide section describing Learning Mode on page
47.
127See page 55.
5. Q: How do I move back to Elevated mode?
A: You will need to obtain an elevation file and apply it using the
elevate command. Refer to page 42 for details.
6. Q: How do I know a file is protected or encrypted?
A: You can use the list command to show that status. Refer to page
109 for details.
7. Q: How do I know which programs are authorized to access protected
files?
A: The view command will display the list of authorized programs.
Refer to page 143 for details.
8. Q: I updated a package (not QDocSE) and I want to know if new
signatures need to be calculated?
A: The verify_monitored command128 will check the programs and
shared libraries, then display those that do not have signatures matching
QDocSE’s copy of the signatures. Please note that for security reasons
QDocSE will need to be in Elevated mode to use the
update_monitored command129 to accept the changes.
9. Q: Can I increase security more after QDocSE is installed and
configured?
A: Yes. As discussed with the adjust and protect commands we
recommend the use of ACLs (Access Control Lists) for the authorized
programs and the protected data files. This will help control, in finer
detail, which specific users are allowed and disallowed to run the
programs and access the files. If you have obtained a license that is set
128See page 145.
129See page 113.
to “No OS Security” then you can upgrade to a license that does have
“OS Security”.
10.Q: If I upgrade from QDocSE 1.4.3 to 2.0.0 (or later versions) will the
new security features be automatically used based on my previous
configuration?
A: In short, yes. Authorized programs and the SOs they use will have
signatures calculated and will be added to the SG monitored list. After
the upgrade you should use the view and view_monitored command
to double-check the configuration. Also read the User Guide section
Upgrading130.
130See page 35.
Troubleshooting
1. The QDocSE package will not install
Please check that you are using the “root” or administrator account, or
you are using an account that is authorized to use the sudo utility to
perform the installation.
2. T he license cannot be applied
Each QDocSE requires the license in the license file to match
specifically. If you have uploaded the “/qdoc/conf/qid.txt” file from an
endpoint that is different from the endpoint you are installing the
license on then you will get an error.
3. You want to configure QDocSE but it is in De- elevated mode
When the license or an elevation file is applied then QDocSE will move
to Elevated mode. If you already applied the license then it may be that
all of the Elevated Time has passed since it was applied or the
finalize command was issued to move to De-elevated mode. If so,
then you will need to obtain an elevation file. Refer to the User Guide
section about elevation 131.
4. M y program is being denied access to protected data files
During configuration in Elevated mode you need to add programs to
the authorized list so they will be allowed access to protected data files.
This will add the program and all SOs that are used by that program to
the authorized list which is monitored by QDocSE’s Security Guard
(SG). Refer to the adjust and push_config commands.
5. My program is in the authorized list and being denied access
There are two different possibilities. The first possibility is that the
program is a long running program that was not restarted– refer to the
section on Long Running Programs132. The second possibility is that
131See page 42.
132See page 48.
one or more signatures used to validate the program and the SOs it uses
when loading are no longer valid – refer to the section on Invalid
Programs and SOs133.
6. I want to change a system file that is being shielded by QDocSE
System files that are enforced as read-only by QDocSE will have the
shielded label in the display from the list command. To change one of
these files you will need to move QDocSE into Elevated mode134 with
an elevation file. When you have completed the change then move
QDocSE back to De-elevated mode to have all security enabled.
133See page 66.
134See page 42.
Glossary of Terms
Anti-virus (AV) – Security software that examines files looking for specific
patterns that indicate malware.
ACL (Access Control List) – this provides fine-grained discretionary access
rights for files and directories. BicDroid recommends these be used with
authorized programs and protected data files.
APT – Advanced Persistent Threat. Usually followed by a number to identify a
specific group or gang involved with malware and/or computer infiltration.
BicDroid – The company that produces QDocSE.
boot attacks – where malware takes (or attempts to take) control of a system
during boot or safe mode when security programs are not yet running.
C2 – aka CC, aka C&C. An abbreviation for Command and Control software
(malware) that an infiltrator will install to maintain access and/or to exfiltrate
data.
CERT – aka US-CERT, U.S. Computer Emergency Security Team. Monitors
serious computer incidents and issues alerts.
CSP (Central Sentry Platform) – the data collector of messages from QDocSE
along with a GUI to display analytics.
Exfiltration – The removal of data from a computer to an external location.
Fileless – When malware is only in-memory with no on-disk copy.
Firewall – Security software focused on controlling network communications
in and out of the computer to prevent non-legitimate access.
IAB (Initial Access Broker) – An open market, mostly on the Dark Web, for
RaaS actors to purchase access to victims’ computers.
Leakware – Software that appears to perform or continue to perform a specific
task but has been modified to collect and exfiltrate sensitive data.
LSM – Linux Security Modules, a framework for implementing security on
Linux systems. QDocSE works in complementary manner with LSMs.
MaaS (Malware-as-a-Service) – For hire sites that will penetrate sites to install
malware.
MAC – Meaning either Mandatory Access Control (for files), or Message
Authenticate Code (for ensuring data integrity). QDocSE uses both.
Malware – Malicious software that infiltrates a computer. There are a variety
of different actions malware may do including, but not limited to, damaging
data, allowing non-legitimate access, exfiltrating data.
Ransomware – A cyber attack where users are denied access to their files
unless a ransom is paid. Usually achieved by file encryption. Often leveraging
off-the-shelf tools.
RaaS (Ransomware as a Service) – The rental or hiring tools and/or services
for a fee. May be a flat rate, time used rate and/or a percentage of the ransom.
RAT (Remote Access Trojan) – aka "Creepware". The tool includes C2.
Riskware – Usually free software that a company or people may use to save
costs but has components to do data exfiltration, time bomb, ransomware,
destroy data and/or even damage infrastructure.
ROP (Return Oriented Programming) - an exploitation technique attacking the
stack. An advanced version of stack smashing.
Scans – Periodic checks or examinations of files, network ports, attached
hardware, etc.
Sensitive data – Personal or corporate data that a bad guy can use to gain
money or power. Examples are credit card (CC) numbers, SIN/SSN, birth
dates, bank account numbers, passwords, etc.
Side Loading – A method where a DLL (Windows) or SO (Unix/Linux/Mac) is
replaced or modified so that control of a system can be achieved or sensitive
data can be accessed and/or transferred. Malware C2 (command & control) is
often done this way to appear as an "innocent" process.
Signature – A calculation made to identify the uniqueness of a file. Any change
to the file will result in a different signature.
SIME – BicDroid's "Smart Integration of MAC and Encryption" (with MAC
meaning Mandatory Access Control), where the two "seamlessly work
together" without the need for key management being performed by a human.
SO injection – On Unix/Linux/Mac systems, a Shared Object file is modified
with malware and is then loaded into an active process.
Siphon – Malware added or injected into software on a computer to drain data
without users of that software being aware.
Spyware – Describes software with malicious behaviour that aims to gather
information about a person or organization and send such information to
another entity in a way that harms the user.
ThreatWare – aka Scareware. When a bad guy threatens to expose or remove
users' data (scare the owner). Differs from Ransomware because the bad guy
has no access to the user system.
Transparent Data Encryption (TDE) – When applications read and write
plaintext data to an encrypted file. The encryption/decryption is transparent to
the application because the application is both unchanged and unaware that of
the data encryption/decryption.
Trojan horse – aka Trojan. A method of penetrating a computer system with
malware under the cover of a friendly program or file. On Linux systems
Trojans are often placed in standard utilities such as cat, bash, and/or ssh.
They are also placed in daemons or services such as sshd or httpd.
Index
A
Access Control List.....................................................................................71
Access Control Lists..............................................................................57, 91
ACL configuration.................................................................................76, 79
ACL entry....................................................................................................70
ACL ID........................................................................................................73
acl_add.........................................................................................................70
acl_create.....................................................................................................73
acl_destroy...................................................................................................74
acl_edit........................................................................................................75
acl_export....................................................................................................76
acl_file.........................................................................................................77
acl_import....................................................................................................79
acl_list.........................................................................................................80
acl_program.................................................................................................82
acl_remove..................................................................................................83
ACLs..............................................................................................57, 91, 115
activate...................................................................................................12, 84
add_integrity_check....................................................................................86
add_monitored.............................................................................................88
adjust....................................................................................89, 113, 135, 143
Administrator...........................................................................24, 26, 33, 118
aes........................................................................................................95, 143
Applying the License...................................................................................40
audit.......................................................................................................25, 92
audited.......................................................................................................110
Auditing with Encryption (TDE)................................................................53
authorized....................................................................................................89
Authorized List............................................................................................66
authorized program....................................................................................134
authorized programs....................................................60, 113, 141, 142, 144
B
block..........................................................................................................110
blocked programs......................................................................................142
C
camellia...............................................................................................95, 143
CAP_DAC_OVERRIDE...........................................................................125
capability...................................................................................................125
character.....................................................................................................110
chkmntstatus................................................................................................17
CIFS.....................................................................................................64, 114
cipher.....................................................................................18, 94, 109, 143
cipher_mode................................................................................................95
commands..............................................................................................17, 96
configuration..............................................................................106, 119, 152
Contacts.........................................................................................................9
CPUs............................................................................................................12
create...........................................................................................................73
D
daemon........................................................................................................61
daemons.......................................................................................................48
Data and Program Integrity checking..........................................................52
Data and Program Integrity checking with Encryption (TDE)...................52
data file......................................................................................................113
Data Integrity checking...............................................................................51
Data Integrity checking with Encryption (TDE).........................................51
Data Protection with Encryption (TDE)......................................................52
database.................................................................................................59, 61
databases......................................................................................................48
DataGuard...................................................................................................22
De-elevated mode......26, 35, 42, 45, 46, 47, 58, 96, 99, 100, 106, 107, 113,
126, 127, 132, 138, 149, 152
defend..........................................................................................................26
device_encrypt.............................................................................................97
DG.........................................................................................................10, 22
DGFS...........................................................................................................22
Disk Space...................................................................................................11
Downgrading...............................................................................................40
E
e-mail...........................................................................................................48
EFEK.........................................................................................................133
elevate......................................................................................12, 44, 99, 108
elevated mode..26, 34, 35, 37, 39, 41, 42, 43, 45, 46, 47, 58, 84, 85, 96, 99,
100, 106, 107, 108, 113, 126, 127, 132, 134, 138, 149, 150, 152
Elevated mode,............................................................................................37
Elevated mode...........................................................................................126
Elevated Time..................................................................................46, 47, 84
Elevation......................................................................................................18
elevation file..........................................................37, 42, 43, 46, 58, 99, 100
Elevation Time..............................................................................12, 85, 100
ELF header................................................................................................113
encrypt.......................................................................................................101
encrypt_pattern..........................................................................................105
encrypted...................................................................................................110
encryption..................................................................................................115
Encryption Key..........................................................................................133
Encryption only (TDE)................................................................................50
endpoint.......................................................................................................65
environment variable.........................................................................135, 136
exfiltrate.......................................................................................................22
F
FEK...........................................................................................................133
fifo.............................................................................................................110
File Auditing................................................................................................25
file integrity.................................................................................................24
File Integrity Monitoring.............................................................................24
finalize...........................................................................46, 48, 106, 126, 152
fnmatch......................................................................................................176
folder..........................................................................................................110
G
gdb...............................................................................................................25
glob......77, 78, 87, 88, 93, 94, 102, 103, 104, 105, 115, 117, 118, 120, 121,
129, 130, 131, 132, 137, 138, 140, 141, 176
grep............................................................................................................176
GRUB..........................................................................................................27
Guard...............................................................................................22, 23, 25
Guards.........................................................................................................21
H
hash............................................................................................................107
I
inspector....................................................................................................125
install_prep..........................................................................................37, 108
installation...................................................................................................32
Installation Programs To Use......................................................................32
integrity......................................................................................................110
Introduction.................................................................................................21
intruders.......................................................................................................26
Invalid Programs...................................................................................28, 66
investigate..........................................................................132, 135, 142, 144
investigation................................................................................................29
K
kalyna..................................................................................................95, 143
L
LD_LIBRARY_PATH.......................................................................135, 144
Learning mode.....................................45, 46, 47, 58, 60, 106, 126, 127, 149
licence........................................................................................................109
license........................................................................................................109
License Expiry.............................................................................................53
license file......................................................................................58, 84, 123
license type............................................................................................40, 69
License Types........................................................................................50, 69
Licenses.......................................................................................................50
link.............................................................................................................110
list........................................................................................................18, 109
list_device_encrypt....................................................................................111
list_handles................................................................................................112
list_monitored............................................................................................112
Local Disk Drives........................................................................................66
locale...........................................................................................................45
long running process...................................................................................61
Long running processes...............................................................................48
long running programs..................................................................36, 37, 152
M
memory........................................................................................................13
monitor_update..........................................................................................113
monitored...................................................................................................110
Monitored Programs....................................................................................67
monitoring.................................................................................................144
MySQL........................................................................................................59
N
Network.......................................................................................................64
New.............................................................................................................18
new files......................................................................................................61
New Installation..........................................................................................32
NFS......................................................................................................64, 114
normal........................................................................................................110
not_encrypted............................................................................................110
O
operating system..........................................................................................21
Operating System (OS) Security.................................................................53
Operating Systems.......................................................................................11
Oracle..........................................................................................................61
Overview.....................................................................................................10
P
package........................................................................................32, 150, 152
parallel_directory.......................................................................................102
paranoid.......................................................................................................58
PG..........................................................................................................10, 25
planning.................................................................................................33, 55
Postgres.......................................................................................................61
ProcessGuard...............................................................................................25
program.......................................................................................................23
protect..................................................................................25, 113, 114, 149
protected....................................................................................................110
protected data..............................................................................................22
protected directory.....................................................................................109
protection...................................................................................................136
ps.................................................................................................................26
Purpose........................................................................................................19
push_config......................................................46, 60, 61, 118, 119, 135, 144
Q
QDocSEConsole......................................................................10, 56, 69, 115
R
regen..........................................................................................................119
Remote.........................................................................................................64
Remote Disk Drives....................................................................................64
remote drive encrypted................................................................................65
removal........................................................................................................39
remove_integrity_check............................................................................119
remove_monitored.....................................................................................121
Removing....................................................................................................39
rename.........................................................................................................63
renewcommit.......................................................................................42, 123
Renewing a License.....................................................................................41
renewrequest........................................................................................42, 124
restart...........................................................................................................61
S
security..................................................21, 22, 23, 26, 27, 91, 108, 118, 150
SecurityGuard..............................................................................................23
Self Defence................................................................................................26
self-defence.................................................................................................26
SELinux.......................................................................................................58
service..........................................................................................................61
services........................................................................................................48
set_access..................................................................................................125
set_learning...................................................................................18, 47, 126
set_security................................................................................................127
setcollector.............................................................................................17, 18
setlearning.................................................................................................127
SG..........................................................................................................10, 23
SGFS...........................................................................................................23
Shared libraries..........................................................................135, 141, 144
shared library.................................................................................23, 91, 118
shielded................................................................................................28, 110
show_mode................................................................................................128
signature..........................................................................23, 25, 29, 134, 156
signatures.......................................................................................23, 29, 141
sm4......................................................................................................95, 143
socket.........................................................................................................110
space............................................................................................................56
Spaces..........................................................................................................44
special..................................................................................................27, 110
stop_audit............................................................................................25, 129
sudo...............................................................................................33, 38, 152
system files..................................................................................................27
T
TDE...........................................................................................................156
Transparent Data Encryption.....................................................................156
Trojan..........................................................................................................92
U
unencrypt...................................................................................................130
uninstall.......................................................................................................39
uninstall_prep............................................................................................132
Uninstalling.................................................................................................39
unprotect............................................................................................113, 136
unwatch...............................................................................................65, 138
update_integrity_check.............................................................................132
update_keys...............................................................................................133
update_monitored..............................................................................134, 141
Upgrade Installation....................................................................................35
upgrade_prep.............................................................................................136
V
valid.............................................................................................................41
verified.........................................................................................................48
verify_integrity_check...............................................................................139
verify_monitored.................................................................................24, 141
version.......................................................................................................142
view.....................................................................................90, 118, 142, 144
view_monitored.................................................................................118, 144
viewcollector...............................................................................................17
W
watch...................................................................................................65, 145
web site....................................................................................................9, 58
/
/etc...............................................................................................................28
/etc/fstab......................................................................................................65
/qdoc/conf/qid.txt....................................................................40, 41, 43, 152
Appendix A: Command lists by licensed
With each license type there are a select number of commands available that
match that license type. You can always issue the commands command to have
QDocSE display the list of commands available that match the current license:
QDocSEConsole -c commands
For each license type column below the commands available have an ‘X’.
Command
desnecilnU
ylno
noitpyrcnE
ytirgetnI
ataD
noitpyrcnE
,ytirgetnI
ataD
ytirgetnI
margorP
&
ataD
noitpyrcnE
,ytirgetnI
margorP
&
ataD
noitpyrcnE
,noitcetorP
ataD
noitpyrcnE
htiw
gnitiduA
acl_add X X
acl_create X X
acl_destroy X X
acl_edit X X
acl_export X X
acl_file X X
acl_import X X
acl_list X X
acl_program X X
acl_remove X X
activate X
add_integrity_check X X X X X
Command
desnecilnU
ylno
noitpyrcnE
ytirgetnI
ataD
noitpyrcnE
,ytirgetnI
ataD
ytirgetnI
margorP
&
ataD
noitpyrcnE
,ytirgetnI
margorP
&
ataD
noitpyrcnE
,noitcetorP
ataD
noitpyrcnE
htiw
gnitiduA
add_monitored X X
adjust X
audit X X
authorize X
cipher X X X X X X X
cipher_mode X X X X X X X
commands X X X X X X X X
device_encrypt X X
elevate X X X X X X X
encrypt X X
encrypt_pattern X X X X X
finalize X X X X X X
hash X X X X X X X
install_prep X X X X X X X
licence X
license X
list X X X X X X X X
list_acls
list_device_encrypt X X
list_handles X X X X X X X
list_monitored X X X
monitor_update X X X
protect X X X
Command
desnecilnU
ylno
noitpyrcnE
ytirgetnI
ataD
noitpyrcnE
,ytirgetnI
ataD
ytirgetnI
margorP
&
ataD
noitpyrcnE
,ytirgetnI
margorP
&
ataD
noitpyrcnE
,noitcetorP
ataD
noitpyrcnE
htiw
gnitiduA
push_config X X X
remove_integrity_check X X X X X
remove_monitored X X X
renewcommit X X X X X X X
renewrequest X X X X X X X
set_access X X X X X
set_learning X
set_security X X X X X X X
show_mode X X X X X X X X
stop_audit X
update_integrity_check X X X X X
update_keys X X X X X
update_monitored X X X
unencrypt X X
uninstall_prep X X X X X X X
upgrade_prep X X X X X X X
unprotect X
unwatch X X
verify_integrity_check X X X X X
verify_monitored X X X
version X X X X X X X X
view X X X X X X X X
view_monitored X X X X X X X X
Command
desnecilnU
ylno
noitpyrcnE
ytirgetnI
ataD
noitpyrcnE
,ytirgetnI
ataD
ytirgetnI
margorP
&
ataD
noitpyrcnE
,ytirgetnI
margorP
&
ataD
noitpyrcnE
,noitcetorP
ataD
noitpyrcnE
htiw
gnitiduA
watch X
Appendix B: Database Examples
All examples in this appendix assume you are the super-user “root” or are
using an Administrator account that will use sudo to execute the commands.
The named distribution of Linux® in the example can often be one of the many
other Linux® distributions.
Instructions to Protect MySQL Server 5.6 and later
Prerequisite
1. CentOS/Red Hat 7.X or Oracle Linux 7.X,
2. MySQL server 5.6 and later versions,
3. QDocSE installed, licensed and Elevated.
Procedure
1. Stop the MySQL service:
a) community edition:
systemctl stop mysqld
b) enterprise edition:
systemctl stop mysql
2. Protect the database and authorize the MySQL program ($database
represents the name of the database to be protected):
QDocSEConsole -c protect -d /var/lib/mysql/$database
QDocSEConsole -c adjust -apf /usr/sbin/mysqld
QDocSEConsole -c push_config
3. Restart the MySQL service:
a) community edition:
systemctl start mysqld
b) enterprise edition:
systemctl start mysql
Instructions to Encrypt Oracle 19.3 DB
NOTE: This example is not for Oracle Database using ASM or RAC.
This example encrypts the data only.
Prerequisite
1. CentOS 7.6,
2. Oracle Enterprise 19.3 Database,
3. Data location “/u01/app/oracle/oradata/ORCLDB”,
4. QDocSE 3.2.0: installed, licensed and Elevated
Procedure
1. Shutdown all applications using the Oracle database and shutdown the
Oracle database:
sqlplus / as sysdba
Connected to:
Oracle Database 19c Enterprise Edition Release 19.0.0.0.0
– Production Version 19.30.0.0.0
SQL> shutdown immediately
Database closed.
Database dismounted.
ORACLE instance shutdown.
SQL> quit
2. Encrypt the data:
QDocSEConsole -c encrypt -d /u01/app/oracle/oradata/ORCLDB
3. Wait for encryption to complete. Encryption completes in about 12
minutes for 200GB.
4. Restart the Oracle database:
sqlplus / as sysdba
SQL> startup
Total System Global Area {additional output}
SQL> quit
Instructions to Protect Oracle Enterprise 11G DB
NOTE: This example is not for Oracle ASM or RAC.
This example protects the data files only.
Prerequisite
1. Oracle Linux 7.X,
2. Oracle Enterprise 11g Database,
3. QDocSE installed, licensed and Elevated,
4. This system has been restarted at least once since Oracle Enterprise has
been setup .
Procedure
1. Stop all applications interacting with the Oracle database, including
sqlplus, dbca, etc. Also properly shutdown all instances of the Oracle
database that are running.
systemctl stop oracle
2. Protect the databases and authorize the Oracle program. First line
wraps.
QDocSEConsole -c protect -d
$ORACLE_INSTALL/app/$ORACLE_GROUP/oradata
QDocSEConsole -c adjust -apf $ORACLE_HOME/bin/oracle
where $ORACLE_INSTALL is the path to the directory the Oracle
software is installed in, $ORACLE_GROUP is the group assigned to
manage the Oracle database, and $ORACLE_HOME is the path to the
directory containing the executables of the Oracle software.
NOTE 1: These are the default paths and may be different depending
on the settings chosen at installation time.
NOTE 2: The oradata contains each global database as a subdirectory.
To only protect a specific database, add that database's global name to
the end of the path after the -d flag.
3. Restart the Oracle database:
systemctl start oracle
Instructions to Protect SAP ASE 16.0 DB
Prerequisite:
1. SUSE Linux 11 SP3 (kernel 3.0.101-0.47.105),
2. SAP ASE 16.0 Database,
3. QDocSE installed, licensed and Elevated,
Procedure:
1. Making sure the SAP ASE database is not running. If it is running, then
make sure:
a) Run the shell script $SAP_HOME/SYBASE.sh or
$SAP_HOME/SYBASE.csh
b) isql -Usa -Ppassword -Sserver_name
c) issue two commands: shutdown and go
2. Protect the databases and Authorize ASE dataserver program
QDocSEConsole -c protect -d $SAP_HOME/data
QDocSEConsole -apf $SAP_HOME/ASE-16_0/bin/dataserver
where $SAP_HOME is the install directory specified during installation.
For the isql command, sa is default system admin, can be set during
installation, while server_name is name of default server, and -p flag
might not be required.
NOTE: These are the default paths and may be different depending on
the settings chosen at installation time.
Instructions to Protect ProgressDB 11.7
Prerequisite:
1. CentOS/Red Hat 7.X,
2. ProgressDB (at least OpenEdge Enterprise RDBMS),
3. QDocSE installed, licensed and Elevated.
Procedure:
1. Stop the remote database and agent from Progress OpenEdge Explorer.
Go to 127.0.0.1:9090 in your browser, login, and stop the database
and agent.
2. Stop the ProgressDB service:
a)fathom -stop
b)proadsv -stop
3. Protect the local database directory. $database represents the database
directory path relative to where the operation is being done.
QDocSEConsole -c protect -d $database
4. Authorize 6 processes with the following commands:
QDocSEConsole -c adjust -apf /usr/dlc/bin/_dbutil
QDocSEConsole -c adjust -apf /usr/dlc/bin/_mprosrv
QDocSEConsole -c adjust -apf /usr/dlc/bin/_mprshut
QDocSEConsole -c adjust -apf /usr/dlc/bin/_dbagent
QDocSEConsole -c adjust -apf /usr/dlc/bin/_sqlsrv2
QDocSEConsole -c adjust -apf /usr/dlc/jdk/jre/bin/java
5. Restart the ProgressDB service:
a)fathom -start
b)proadsv -start
6. Start the remote database and agent from Progress OpenEdge Explorer.
Go to 127.0.0.1:9090 in your browser, login, and start the database
and agent.
Appendix C: glob patterns
This appendix is a copy of the glob manual page that describes the valid
patterns. It is always recommended that the patterns have single quotes around
them so they do not get interpreted or expanded by the shell.
For QDocSE the command that uses glob patterns is encrypt_pattern. More
commands will use glob patterns in the future.
glob — shell-style pattern matching
Globbing characters (wildcards) are special characters used to perform pattern
matching of pathnames and command arguments in the csh(1), ksh(1), and
sh(1) shells as well as the C library functions fnmatch (3) and glob(3). A glob
pattern is a word containing one or more unquoted ‘?’ or ‘*’ characters, or
“[..]” sequences.
Globs should not be confused with the more powerful regular expressions used
by programs such as grep (1) . While there is some overlap in the special
characters used in regular expressions and globs, their meaning is different.
The pattern elements have the following meaning:
?
Matches any single character.
*
Matches any sequence of zero or more characters.
[..]
Matches any of the characters inside the brackets. Ranges of characters
can be specified by separating two characters by a ‘-’ (e.g. “[a0-9]”
matches the letter ‘a’ or any digit). In order to represent itself, a ‘-’ must
either be quoted or the first or last character in the character list.
Similarly, a ‘]’ must be quoted or the first character in the list if it is to
represent itself instead of the end of the list. Also, a ‘!’ appearing at the
start of the list has special meaning (see below), so to represent itself it
must be quoted or appear later in the list.
Within a bracket expression, the name of a character class enclosed in
‘[:’ and ‘:]’ stands for the list of all characters belonging to that class.
Supported character classes:
alnum cntrl lower space
alpha digit print upper
blank graph punct xdigit
A character class may not be used as an endpoint of a range.
[!..]
Like [..], except it matches any character not inside the brackets.
\
Matches the character following it verbatim. This is useful to quote the
special characters ‘?’, ‘*’, ‘[’, and ‘\’ such that they lose their special
meaning. For example, the pattern “\\\*\[x]\?” matches the string “\
*[x]?”.
Note that when matching a pathname, the path separator ‘/’, is not matched by
a ‘?’, or ‘*’, character or by a “[..]” sequence. Thus, /usr/*/*/X11 would match
/usr/X11R6/lib/X11 and /usr/X11R6/include/X11 while /usr/*/X11 would not
match either. Likewise, /usr/*/bin would match /usr/local/bin but not /usr/bin.
This QDocSE glob implementation is based on the BSD implementation with
an enhancement to support extended glob patterns. Extended glob patterns
allow for one or more different glob patterns to be specified; patterns are
separated by the ‘|’ character within a pair of brackets, ‘(‘ and ‘)’. When one of
the patterns match then there is a successful match. The leading ‘(‘ may be
prefixed with a ‘!’ character to negate the result of the extended glob pattern.
An extended glob pattern cannot be nested within another pattern.
Examples
*dog*
Matches any filename or directory name that contains “dog”.
*test[123].txt
Matches any filename that ends with “test1.txt”, “test2.txt” or “test3.txt”.
*test[:digit:]
Matches any filename that ends with “test0”, “test1”, “test2”, “test3”, “test4”,
“test5”, “test6”, “test7”, “test8”, or “test9”.
(*tom.txt|*sam.txt)
Matches any file name that ends with “tom.txt” or “sam.txt”.
!(*[:xdigit:]|*odt)
Matches when the filename has no hexadecimal suffix and the filename
doesn’t end with “odt”.
Appendix D: Encrypted file transfer
Sometime you will need to transfer QDocSE encrypted data files from one
machine to a new machine. You can use the backup authorized program
specified with the QDocSE ACLs.
The QDocSE ACLs have a special identifier for programs that perform
backups. The administrator can set which programs have this special
authorization. Backup programs are allowed to read encrypted files for the
metadata and encrypted data.
The following is an example for transferring encrypted data files. This uses
the tar utility as the authorized program for doing backups. It is assumed
that ACL ID 2, a program ACL, is already assigned to the data files. A
command (below) will add tar to ACL ID 2 as a backup program.
The following criteria needs to be met before starting the file transfer:
1. The user accounts and groups on the source and destination machines
must be identical.
2. The destination machine must have enough free disk space for the file
transfer.
3. For file integrity, there must be no programs changing any of the files on
the source machine.
Then the following QDocSE commands will be run on the source machine:
A. QDocSEConsole -c adjust -apf /bin/tar
a. Assume the program index value set for tar is "4".
B. QDocSEConsole -c acl_add -i 2 -a -b -m r -p 4
C. QDocSEConsole -c push_config
D. QDocSEQDocSEConsole -c acl_export -f saved_config
E. tar cf saved.tar <directory>
Now transfer the files "saved.tar" and "saved_config" from the source
machine to the destination machine.
The following QDocSE commands will be run on the destination machine:
A. QDocSEConsole -c acl_import -f saved_config
B. tar xf saved.tar
C. QDocSEConsole -c encrypt -d <directory>
Step C will not take too long because the data is already encrypted. If you
are using CSP then it will be updated about the changes on the destination
machine.
The next step is for you to verify that the data on the destination machine is
without error, and test that your programs can access the data correctly.
Once you are comfortable that the destination machine is correct you can
remove the data from the source machine. If you are using CSP you will
want to unencrypt the <directory> to update CSP:
QDocSEConsole -c unencrypt -d <directory>

Appendix X: copyrights
This appendix includes the notices attributed with specific copyrights for
source code included with QDocSE.
The Regents of the University of California
THIS SOFTWARE IS PROVIDED BY THE REGENTS AND
CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.