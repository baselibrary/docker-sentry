#!/bin/bash
set -e

cd "$(dirname "$(readlink -f "$BASH_SOURCE")")"

versions=( "$@" )
if [ ${#versions[@]} -eq 0 ]; then
	versions=( */ )
fi
versions=( "${versions[@]%/}" )


for version in "${versions[@]}"; do
  fullRelease="$(git ls-remote --tags https://github.com/getsentry/sentry.git | cut -d$'\t' -f2 | grep -E '^refs/tags/'"${version}"'.[0-9]$' | cut -d/ -f3 | sort -rV | head -n1 )"
  (
		set -x
		cp docker-entrypoint.sh "$version/"
		sed '
			s/%%SENTRY_MAJOR%%/'"$version"'/g;
			s/%%SENTRY_RELEASE%%/'"$fullRelease"'/g;
		' Dockerfile.template > "$version/Dockerfile"
	)
done
