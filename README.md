# laminas-mvc-skeleton

## Introduction

This is a bot for tweeting music lyrics for a set artist, tweeting the lyrics at a specific interval. Unlike other projects this one was built to be run via docker, and as such can be used in very versatile manners.

## Installation

The easiest way to get going is to fill in auth.env with real world values and run

```bash
$ ./run.sh
```

This will build the docker image and run it locally.

Otherwise build the docker image by hand, copy it to target destination and run it there.

Genius API Access Token can be configured here: https://genius.com/api-clients.

Twitter API is found here: https://developer.twitter.com/en

You'll have to apply for developer access on Twitter.

## Environment variables

### Mandatory

```
GENIUS_ACCESS_TOKEN
TWITTER_API_KEY
TWITTER_API_SECRET
TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET
```

### Optional

todo

## Running Tests

todo
