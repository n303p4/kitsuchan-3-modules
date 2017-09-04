#!/usr/bin/env python3

"""Linux news command(s)."""

from bs4 import BeautifulSoup

from k3 import commands

BASE_URL_ARCH = "https://www.archlinux.org"
BASE_URL_ARCH_NEWS = "https://www.archlinux.org/news"


@commands.cooldown(6, 12)
@commands.command(aliases=["archnews", "anews"])
async def arch(ctx):
    """Fetch the latest Arch Linux news."""
    async with ctx.bot.session.get(BASE_URL_ARCH_NEWS) as response:
        if response.status == 200:
            text = await response.text()
            soup = BeautifulSoup(text)
        else:
            await ctx.send("Couldn't fetch Arch Linux news at this time.")
            return
    link_list = soup.find_all("a", href=True)
    counter = 0
    message = [
        ctx.f.bold("Arch Linux News"),
        ctx.f.no_embed_link(BASE_URL_ARCH_NEWS)
    ]
    for link in link_list[:5]:
        if "/news/" in link['href']:
            post_url = BASE_URL_ARCH + link['href']
            formatted_link = ctx.f.no_embed_link(post_url)
            message.append(f"\n{link.string}\n{formatted_link}")
            counter += 1
    await ctx.send("\n".join(message))
