import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
@commands.has_permissions(administrator=True)
async def announce(ctx, *, message):
    sent = 0
    failed = 0

    for member in ctx.guild.members:
        if member.bot:
            continue

        try:
            await member.send(
                f"📢 **Q8Boost Announcements**\n\n{message}"
            )
            sent += 1
        except:
            failed += 1

    await ctx.send(f"✅ Done! Sent: {sent} | Failed: {failed}")

@announce.error
async def announce_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You must be an administrator to use this command.")

bot.run("YOUR_BOT_TOKEN")
