#!/usr/bin/env bash

set -e

bash util/up-version.sh
bash util/check-msg.sh
bash util/confirm.sh </dev/tty

exit 0
