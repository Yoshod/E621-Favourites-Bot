from discord import Embed
from flask import make_response
from matplotlib.font_manager import json_dump
from nextcord.ext import commands, tasks
import requests
import nextcord
import json
import asyncio
from configutils import get_config

class Mainloop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.header = {"User-Agent": get_config("HEADERS", "useragent")}
        self.url = f"https://e621.net/favorites.json?user_id={get_config('USERS', 'hekkland')}"
        self.fave_changes.start()

    
    def make_request(self, url):
        response = requests.get(url, headers=self.header, auth=(get_config('USERNAME', 'username'), get_config('KEYS', 'e6apikey')))
        return response.json()

    def compare(self, data, user):
        first_run = False
        try:
            with open(f"{user}data.json", "r", encoding="utf-8") as f:
                posts = json.load(f)
        
        except:
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
                    print("We got a new one!")
            
            for post in old_posts:
                if post not in new_posts:
                    removed_posts.append(post)
                    print("They fucking killed him!")
        
        elif first_run:
            for post in data["posts"]:
                new_posts.append(post["id"])
                added_posts.append(post)
        
        return data, posts, new_posts, old_posts, added_posts, removed_posts

    @commands.command()
    async def bigtest(self, ctx):
        data = self.make_request()
        data, posts, new_posts, old_posts, added_posts, removed_posts = self.compare(data)
        added_post_count = len(added_posts)
        removed_post_count = len(removed_posts)
        overview_embed = nextcord.Embed(
            title="Favorites Update Report",
            description=f"**New Favorites**\n{added_post_count}\n\n**Removed Favorites**\n{removed_post_count}"
        )
        await ctx.send(embed=overview_embed)

        for post in data["posts"]:
            if post["id"] in added_posts:
                added_embed = nextcord.Embed(
                    title=f"Added - {post['id']}",
                    description=post["description"]
                )
                added_embed.add_field(name="Rating", value=post["rating"])
                added_embed.add_field(name="URL", value=f"[Jump!](https://e621.net/posts/{post['id']})")
                added_embed.set_image(post["file"]["url"])
                await ctx.send(embed=added_embed)

        for post in posts["posts"]:
            if post["id"] in removed_posts:
                removed_embed = nextcord.Embed(
                    title=f"Removed - {post['id']}",
                    description=post["description"]
                )
                removed_embed.add_field(name="Rating", value=post["rating"])
                removed_embed.add_field(name="URL", value=f"[Jump!](https://e621.net/posts/{post['id']})")
                removed_embed.set_image(post["file"]["url"])
                await ctx.send(embed=removed_embed)
    
    @tasks.loop(minutes=5.0)
    async def fave_changes(self):
        print("Part 1")
        channel = self.bot.get_channel(1014169602298748989)
        print("Part 2")
        url = f"https://e621.net/favorites.json?user_id={get_config('USERS', 'hekkland')}"
        data = self.make_request(url)
        print("Part 3")
        userid = get_config('USERS', 'hekkland')
        data, posts, new_posts, old_posts, added_posts, removed_posts = self.compare(data, userid)
        print("Part 4")
        added_post_count = len(added_posts)
        removed_post_count = len(removed_posts)
        
        if added_post_count > 0 or removed_post_count > 0:
            overview_embed = nextcord.Embed(
                title="Favorites Update Report",
                description=f"**New Favorites**\n{added_post_count}\n\n**Removed Favorites**\n{removed_post_count}"
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

        for post in posts["posts"]:
            if post["id"] in removed_posts:
                removed_embed = nextcord.Embed(
                    title=f"Removed - {post['id']}",
                    description=post["description"]
                )
                removed_embed.add_field(name="Rating", value=post["rating"])
                removed_embed.add_field(name="URL", value=f"[Jump!](https://e621.net/posts/{post['id']})")
                removed_embed.set_image(post["file"]["url"])
                await channel.send(embed=removed_embed)

        
        channel = self.bot.get_channel(1014169656577249371)
        url = f"https://e621.net/favorites.json?user_id={get_config('USERS', 'melanie')}"
        data = self.make_request(url)
        userid = get_config('USERS', 'melanie')
        data, posts, new_posts, old_posts, added_posts, removed_posts = self.compare(data, userid)
        added_post_count = len(added_posts)
        removed_post_count = len(removed_posts)
        if added_post_count and removed_post_count == 0:
            return
        
        if added_post_count > 0 or removed_post_count > 0:
            overview_embed = nextcord.Embed(
                title="Favorites Update Report",
                description=f"**New Favorites**\n{added_post_count}\n\n**Removed Favorites**\n{removed_post_count}"
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

        for post in posts["posts"]:
            if post["id"] in removed_posts:
                removed_embed = nextcord.Embed(
                    title=f"Removed - {post['id']}",
                    description=post["description"]
                )
                removed_embed.add_field(name="Rating", value=post["rating"])
                removed_embed.add_field(name="URL", value=f"[Jump!](https://e621.net/posts/{post['id']})")
                removed_embed.set_image(post["file"]["url"])
                await channel.send(embed=removed_embed)
        


def setup(bot):
    bot.add_cog(Mainloop(bot))
    