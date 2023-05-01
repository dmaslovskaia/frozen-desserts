#!/bin/sh -e

# If running the rails server then create or migrate existing database
if [ "${*}" == "./bin/rails server -p 80 -b 0.0.0.0" ]; then
  ./bin/rails db:prepare
fi

exec "${@}"
