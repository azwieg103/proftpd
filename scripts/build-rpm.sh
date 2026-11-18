#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

test -s upstream/VERSION
test -s upstream/SOURCE_SHA256
version="$(tr -d '[:space:]' < upstream/VERSION)"
expected_sha="$(tr -d '[:space:]' < upstream/SOURCE_SHA256)"
archive="upstream/proftpd-${version}.tar.gz"

[[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+[a-z]?$ ]] || {
  echo "Unexpected stable ProFTPD version: $version" >&2
  exit 1
}
[[ "$expected_sha" =~ ^[0-9a-f]{64}$ ]] || {
  echo "Invalid upstream SHA-256 value." >&2
  exit 1
}
test -s "$archive"
printf '%s  %s\n' "$expected_sha" "$archive" | sha256sum --check -

topdir="$ROOT/rpmbuild"
rm -rf "$topdir" dist
mkdir -p "$topdir"/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS} dist
cp "$archive" "$topdir/SOURCES/proftpd-${version}.tar.gz"
cp packaging/proftpd.conf "$topdir/SOURCES/proftpd.conf"
cp packaging/proftpd.service "$topdir/SOURCES/proftpd.service"
cp packaging/sysconfig.proftpd "$topdir/SOURCES/sysconfig.proftpd"
cp packaging/proftpd.tmpfiles "$topdir/SOURCES/proftpd.tmpfiles"
cp packaging/proftpd.logrotate "$topdir/SOURCES/proftpd.logrotate"

release="${RPM_RELEASE:-ZWIEGNET.1.el10}"
rpmbuild -ba packaging/proftpd.spec \
  --define "_topdir $topdir" \
  --define "proftpd_version $version" \
  --define "proftpd_release $release"

find "$topdir/RPMS" "$topdir/SRPMS" -type f -name '*.rpm' -exec cp -v {} dist/ \;

binary="$(find dist -maxdepth 1 -type f -name 'proftpd-[0-9]*.x86_64.rpm' ! -name '*debuginfo*' ! -name '*debugsource*' -print -quit)"
source="$(find dist -maxdepth 1 -type f -name 'proftpd-*.src.rpm' -print -quit)"
test -n "$binary"
test -n "$source"
rpm -qp --qf '%{NAME} %{VERSION}-%{RELEASE} %{ARCH}\n' "$binary"
rpm -qpl "$binary" | grep -Fx /usr/sbin/proftpd
rpm -qpl "$binary" | grep -Fx /usr/lib/systemd/system/proftpd.service

echo "Built ProFTPD ${version}-${release}"
