# Dockerfile.rails
FROM ruby:3.2.1-alpine AS builder

# Install related packages and build the application dependencies
RUN apk add \
  build-base \
  postgresql-dev
COPY ../../Gemfile* .
RUN bundle install

FROM ruby:3.2.1-alpine AS runner

# Set default working directory and user
ENV APP_PATH /app
RUN mkdir -p $APP_PATH
WORKDIR $APP_PATH

# Install related packages
RUN apk add \
  postgresql-dev \
  tzdata \
  nodejs

# Copy application files and dependencies from previous step
COPY --from=builder /usr/local/bundle/ /usr/local/bundle/
COPY ../.. .

# Entrypoint prepares the database.
ENTRYPOINT ["./docker-entrypoint.sh"]

# Start the server by default, this can be overwritten at runtime
EXPOSE 3000
CMD ["./bin/rails", "server"]
