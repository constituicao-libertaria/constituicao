FROM ruby:3.4.2

COPY Gemfile Gemfile.lock ./

RUN bundle install
