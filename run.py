import os
import requests
from mastodon import Mastodon
from pyaml import yaml
import sys
import time

with open("config.yaml", "r") as f:
    config = yaml.load(f)

BASE_URL = config["instance"]
searches = config["searches"]

if len(sys.argv) > 1:
    searches = [x for x in searches if x["user"].lower() == sys.argv[1].lower()]

for search in searches:
    user_creds = "{}.user.secret".format(search["user"])

    if not os.path.exists(user_creds):
        Mastodon.create_app("{}-app".format(search["user"]),
                api_base_url=BASE_URL,
                to_file="{}.app.secret".format(search["user"])
        )

        mastodon = Mastodon(
            client_id="{}.app.secret".format(search["user"]),
            api_base_url=BASE_URL
        )
        mastodon.log_in(
                search["user"],
                search["password"],
                to_file=user_creds
        )

    mastodon = Mastodon(
        access_token=user_creds,
        api_base_url=BASE_URL
    )

    r = requests.get("https://danbooru.donmai.us/posts.json?random=true&tags={}&rating=s&limit=1".format("+".join(search["query"])),
        auth=(config["danbooru"]["username"], config["danbooru"]["password"]))

    r = r.json()
    if len(r) == 0:
        continue
    r = r[0]["large_file_url"]
    u = requests.get(r)
    with open("/tmp/danbooru.png", "wb") as f:
        f.write(u.content)
    img = mastodon.media_post("/tmp/danbooru.png")["id"]

    mastodon.status_post(
      search.get("msg", "."),
      sensitive=search.get("nsfw", False),
      media_ids=[img],
      visibility="unlisted"
    )

    time.sleep(20)
