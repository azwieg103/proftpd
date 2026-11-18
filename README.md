# ZWIEGNET ProFTPD for Enterprise Linux 10

This repository rebuilds official ProFTPD source releases as RPM packages for Enterprise Linux 10 x86_64.

Target distributions:

- AlmaLinux 10
- Red Hat Enterprise Linux 10
- Oracle Linux 10
- Rocky Linux 10
- CentOS Stream 10

Packages are built on AlmaLinux 10 x86_64. They are intended for the Enterprise Linux 10 family but are not individually built or tested on every listed distribution.

## No warranty, support, or responsibility

**This software and these packages are provided AS IS, without warranty of any kind, express or implied.** ZWIEGNET and the repository maintainer provide no warranty, guarantee, security assurance, maintenance commitment, or technical support.

**You are solely responsible for evaluating, configuring, securing, testing, deploying, updating, monitoring, backing up, and operating this software and any system on which you install it.** You must independently assess whether it is appropriate for your environment and comply with all applicable laws, regulations, and security requirements.

To the maximum extent permitted by applicable law, ZWIEGNET and the maintainer disclaim responsibility and liability for any damages, losses, data disclosure, data loss, service interruption, security incident, or other consequences arising from downloading, installing, configuring, using, or being unable to use these packages. Nothing in this notice excludes liability that cannot legally be excluded.

These packages are not represented as security-audited, production-certified, or safe for exposure to the public Internet. Publishing an RPM does not constitute a security review or an endorsement of any deployment.

## Important security notice

The packaged default configuration is deliberately **fail-closed**: FTP logins are denied (DenyAll) and file overwriting is disabled. The service is not enabled automatically. An administrator must explicitly configure authentication, install and configure a trusted TLS certificate, enable mandatory TLS (TLSEngine on and TLSRequired on), and only then deliberately change the login policy to permit the intended users.

Before any network exposure, you are responsible for at least:

- Configuring and validating TLS with a certificate trusted by clients; require TLS for both control and data connections.
- Configuring the intended authentication mechanism and restricting which accounts may log in.
- Reviewing chroot/home-directory access, filesystem ownership, permissions, and upload/download policy.
- Configuring passive FTP ports and matching host, cloud, and network firewalls; expose only the ports actually required.
- Reviewing SELinux policy, systemd restrictions, logging, monitoring, rate limiting, and intrusion controls.
- Applying upstream security updates promptly and testing the complete configuration from an untrusted network.

Do not enable logins merely to make the daemon start working. Do not expose cleartext FTP to an untrusted network. FTPS configuration, certificate management, firewall policy, and authentication are administrator responsibilities. The sample configuration is a starting point, not a complete security baseline.

## Upstream source

- Project: https://www.proftpd.org/
- Official source repository: https://github.com/proftpd/proftpd
- Tracked release channel: stable GitHub releases only

The initial stable upstream source snapshot (v1.3.9e) is now present under upstream/. The synchronization workflow checks the official upstream GitHub Releases API every six hours. It excludes drafts and prereleases, downloads the latest stable release source archive, records its tag and SHA-256 checksum, and opens a pull request containing only the upstream snapshot change. The source snapshot is kept separate from the packaging files so packaging changes are never overwritten by upstream synchronization.

## Packages

The package builds the ProFTPD server with TLS, SFTP, LDAP, and SQL support where the corresponding Enterprise Linux development libraries are available. It includes a systemd unit with additional service restrictions. These measures do not replace a security review or administrator hardening.

## Versioning

The RPM version follows the upstream stable version. The RPM release uses ZWIEGNET.N.el10: .el10 identifies the Enterprise Linux 10 build, and N increments for each successful published rebuild of the same upstream version. A new upstream version starts at ZWIEGNET.1.el10.

Example:

proftpd-1.3.9e-ZWIEGNET.3.el10.x86_64.rpm

## Automation

- Upstream stable releases are checked every six hours and manually on demand.
- A new source snapshot is submitted as a pull request; the upstream source is not edited as part of packaging work.
- Merging a reviewed upstream update triggers an AlmaLinux 10 x86_64 RPM build.
- The build validates the source checksum and RPM metadata.
- A GitHub Release is created only after a successful build and only if the build still corresponds to the current main commit.
- Failed or stale builds do not publish releases.

## License

ProFTPD is licensed under GPL-2.0-or-later. The upstream source archive includes the applicable license and copyright notices. This repository's RPM packaging scripts and metadata are maintained separately from upstream source.
