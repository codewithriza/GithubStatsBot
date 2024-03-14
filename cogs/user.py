import discord
from discord.ext import commands
import requests

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def user(self, ctx, username: str):
        url = f'https://api.github.com/users/{username}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            created_at = datetime.strptime(data['created_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y")
            updated_at = datetime.strptime(data['updated_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y")

            embed = discord.Embed(title=data['login'], description=data.get('bio', 'No bio provided'), color=0xFFD700)
            embed.set_thumbnail(url=data['avatar_url'])
            embed.add_field(name="Account Information", value=f"• **Name** : {data['name']}\n"
                                                              f"• **Creation** : `{created_at}`\n"
                                                              f"• **Updated** : `{updated_at}`\n"
                                                              f"• **Location** : {data.get('location', 'Unknown')}\n"
                                                              f"• **Hireable** : {data['hireable']}\n\n"
                                                              f"• **Repositories** : {data['public_repos']}\n"
                                                              f"• **Gists** : {data['public_gists']}\n\n"
                                                              f"• **Followers** : {data['followers']}\n"
                                                              f"• **Following** : {data['following']}", inline=False)

            embed.add_field(name="GitHub Streak Stats", value=f"[View Streak Stats](https://github-readme-streak-stats.herokuapp.com/?user={username}&theme=vue-dark&hide_border=true)", inline=False)
            embed.add_field(name="Top Languages Stats", value=f"[View Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username={username}&theme=vue-dark&show_icons=true&hide_border=true&layout=compact)", inline=False)

            if data.get('twitter_username'):
                embed.add_field(name="Twitter",value=f"[{data['twitter_username']}](https://twitter.com/{data['twitter_username']})", inline=False)
            if data.get('blog'):
                embed.add_field(name="Blog", value=f"[{data['blog']}](https://{data['blog']})", inline=False)

            embed.set_footer(text="GitHub Profile", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
            embed.url = f"https://github.com/{username}"

            await ctx.send(embed=embed)
        else:
            await ctx.send("User not found.")

def setup(bot):
    bot.add_cog(User(bot))
