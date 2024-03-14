import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle, InteractionType, component
from datetime import datetime
import requests

class Repos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def repos(self, ctx, username: str, page: int = 1):
        url = f'https://api.github.com/users/{username}/repos'
        response = requests.get(url)
        if response.status_code == 200:
            repos = response.json()

            def create_embed(page):
                user_url = f'https://api.github.com/users/{username}'
                user_response = requests.get(user_url)
                user_data = user_response.json()
                user_avatar = user_data.get('avatar_url')

                embed = discord.Embed(title=f"{username}'s Repositories", color=0x7289da)
                embed.set_thumbnail(url=user_avatar)

                start_idx = (page - 1) * 5
                end_idx = min(start_idx + 5, len(repos))

                for i in range(start_idx, end_idx):
                    repo = repos[i]
                    description = repo['description'] or "No description"
                    language = repo['language'] or "Unknown"
                    embed.add_field(name=f"{i + 1} {repo['name']}", value=f"{description}\n• {language} - {'Private' if repo['private'] else 'Public'}", inline=False)

                embed.set_footer(text=f"Page {page}/{(len(repos) // 5) + 1} • {len(repos)} repositories")
                return embed

            message = await ctx.send(embed=create_embed(page), components=[
                Button(style=ButtonStyle.blue, label="⬅️", custom_id="prev"),
                Button(style=ButtonStyle.blue, label="➡️", custom_id="next"),
            ])

            while True:
                interaction = await self.bot.wait_for("button_click")
                if interaction.component.custom_id == "prev":
                    if page > 1:
                        page -= 1
                        await interaction.respond(type=InteractionType.UpdateMessage, embed=create_embed(page), components=[
                            Button(style=ButtonStyle.blue, label="⬅️", custom_id="prev"),
                            Button(style=ButtonStyle.blue, label="➡️", custom_id="next"),
                        ])
                elif interaction.component.custom_id == "next":
                    if page < (len(repos) // 5) + 1:
                        page += 1
                        await interaction.respond(type=InteractionType.UpdateMessage, embed=create_embed(page), components=[
                            Button(style=ButtonStyle.blue, label="⬅️", custom_id="prev"),
                            Button(style=ButtonStyle.blue, label="➡️", custom_id="next"),
                        ])
        else:
            await ctx.send("User not found or has no public repositories.")

def setup(bot):
    bot.add_cog(Repos(bot))
