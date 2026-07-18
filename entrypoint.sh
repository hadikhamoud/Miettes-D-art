#!/bin/sh
set -eu

if [ "${SECRET_KEY:-}" = "build-only-secret" ] || [ -z "${SECRET_KEY:-}" ]; then
    echo "SECRET_KEY must be configured as a runtime environment variable" >&2
    exit 1
fi

exec "$@"
