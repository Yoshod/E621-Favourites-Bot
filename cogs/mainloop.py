from nextcord.ext import commands, tasks
import requests
import nextcord
import json
from configutils import get_config


class Mainloop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.header = {"User-Agent": get_config("HEADERS", "useragent")}
        self.fave_changes.start()

    def make_request(self, url):
        response = requests.get(url, headers=self.header, auth=(get_config('USERNAME', 'username'), get_config('KEYS', 'e6apikey')))
        return response.json()

    def compare(self, data, user):
        first_run = False
        try:
            with open(f"{user}data.json", "r", encoding="utf-8") as f:
                posts = json.load(f)

        except json.JSONDecodeError:
            first_run = True

        with open(f"{user}data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        with open(f"{user}data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        new_posts = []
        added_posts = []
        removed_posts = []
        old_posts = []

        if not first_run:
            for post in posts["posts"]:
                old_posts.append(post["id"])

            for post in data["posts"]:
                new_posts.append(post["id"])

            for post in new_posts:
                if post not in old_posts:
                    added_posts.append(post)

            for post in old_posts:
                if post not in new_posts:
                    removed_posts.append(post)

        elif first_run:
            for post in data["posts"]:
                new_posts.append(post["id"])
                added_posts.append(post)

        return data, added_posts, removed_posts

    @tasks.loop(minutes=5.0)
    async def fave_changes(self):
        for x in range(0, 2):
            match x:
                case 0:
                    channel = self.bot.get_channel(1014169602298748989)
                    userid = get_config('USERS', 'hekkland')
                    url = f"https://e621.net/favorites.json?user_id={userid}"

                case 1:
                    channel = self.bot.get_channel(1014169656577249371)
                    userid = get_config('USERS', 'melanie')
                    url = f"https://e621.net/favorites.json?user_id={userid}"

                case 2:
                    channel = self.bot.get_channel(1014169684473548861)
                    userid = get_config('USERS', 'reggie')
                    url = f"https://e621.net/favorites.json?user_id={userid}order:-id"

            data = self.make_request(url)
            data, added_posts, removed_posts = self.compare(data, userid)
            added_post_count = len(added_posts)
            removed_post_count = len(removed_posts)

            if added_post_count > 0 or removed_post_count > 0:
                overview_embed = nextcord.Embed(
                    title="Favorites Update Report",
                    description=f"**New Favorites**\n{added_post_count}"
                )
                await channel.send(embed=overview_embed)

            for post in data["posts"]:
                if post["id"] in added_posts:
                    added_embed = nextcord.Embed(
                        title=f"Added - {post['id']}",
                        description=post["description"]
                    )
                    added_embed.add_field(name="Rating", value=post["rating"])
                    added_embed.add_field(name="URL", value=f"[Jump!](https://e621.net/posts/{post['id']})")
                    added_embed.set_image(post["file"]["url"])
                    await channel.send(embed=added_embed)


def setup(bot):
    bot.add_cog(Mainloop(bot))
