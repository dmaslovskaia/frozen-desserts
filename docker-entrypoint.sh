#!/bin/sh -e

if [ "$RAILS_ENV" == "test" ] || [ "$RAILS_ENV" == "development" ]; then
  # if start in dev or test mode migrate database and run rspec tests
  bundle exec rails db:prepare
  bundle exec rspec --format documentation --fail-fast
else
  # if start in prod mode only migrate database
  bundle exec rails db:prepare
fi

exec "${@}"
