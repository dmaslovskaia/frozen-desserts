# Dockerfile.rails
FROM ruby:3.2.1-alpine AS builder

RUN apk add \
  build-base \
  sqlite
COPY Gemfile* .
RUN bundle install

FROM ruby:3.2.1-alpine AS runner

# Default directory
ENV INSTALL_PATH /opt/app
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

RUN apk add \
  sqlite \
  tzdata \
  nodejs

COPY --from=builder /usr/local/bundle/ /usr/local/bundle/
COPY . .

EXPOSE 3000
CMD ["rails", "server", "-b", "0.0.0.0"]