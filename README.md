# ZWIEGNET ProFTPD for Enterprise Linux 10

This repository rebuilds official ProFTPD source releases as RPM packages for Enterprise Linux 10 x86_64.

Target distributions:

- AlmaLinux 10
- Red Hat Enterprise Linux 10
- Oracle Linux 10
- Rocky Linux 10
- CentOS Stream 10

Packages are built on AlmaLinux 10 x86_64. They are intended for the Enterprise Linux 10 family but are not individually built or tested on every listed distribution.

**No warranty or support is provided.** Packages are supplied as-is. This repository does not provide commercial, security, or production support.

## Upstream source

- Project: https://www.proftpd.org/
- Official source repository: https://github.com/proftpd/proftpd
- Tracked release channel: stable GitHub releases only

The initial stable upstream source snapshot (v1.3.9e) is now present under `upstream/`. The synchronization workflow checks the official upstream GitHub Releases API every six hours. It excludes drafts and prereleases, downloads the latest stable release source archive, records its tag and SHA-256 checksum, and opens a pull request containing only the upstream snapshot change. The source snapshot is kept separate from the packaging files so packaging changes are never overwritten by upstream synchronization.

## Packages

The initial build produces the `proftpd` server RPM and source RPM. The server is built with TLS, SFTP, LDAP, and SQL support where the corresponding Enterprise Linux development libraries are available.

The package includes a systemd unit and a conservative default configuration. The service is not enabled automatically. Configure and secure the FTP service, including TLS and passive ports, before enabling it on an Internet-facing host.

## Versioning

The RPM version follows the upstream stable version. The RPM release uses `ZWIEGNET.N.el10`: `.el10` identifies the Enterprise Linux 10 build, and `N` increments for each successful published rebuild of the same upstream version. A new upstream version starts at `ZWIEGNET.1.el10`.

Example:

`proftpd-1.3.9e-ZWIEGNET.2.el10.x86_64.rpm`

## Automation

- Upstream stable releases are checked every six hours and manually on demand.
- A new source snapshot is submitted as a pull request; the upstream source is not edited as part of packaging work.
- Merging a reviewed upstream update triggers an AlmaLinux 10 x86_64 RPM build.
- The build validates the source checksum and RPM metadata.
- A GitHub Release is created only after a successful build and only if the build still corresponds to the current `main` commit.
- Failed or stale builds do not publish releases.

## License

ProFTPD is licensed under GPL-2.0-or-later. The upstream source archive includes the applicable license and copyright notices. This repository's RPM packaging scripts and metadata are maintained separately from upstream source.
