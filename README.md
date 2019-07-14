# Danbooru Fediverse Poster

Searches danbooru for images and posts them via mastodonAPI to any
fediverse server

## Installation

```bash
pip3 install -r requirements.txt
cp config.example.yaml config.yaml
```

and edit your config file

## Configuration

We need 3 sections for the config file

- searches: describes the danbooru searches to make and the users to post to
  - required keys:
    - user: your username
    - password: your password
    - query: an array of tags to search on danbooru
  - options keys:
    - nsfw: bool, mark uploads as sensitive
- danbooru:
  - required keys:
    - username: your username
    - password: your password
- instance: the https url for your fedi instance

## Running

```bash
python3 run.py
```
