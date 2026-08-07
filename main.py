import os
import discord
from discord import app_commands

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Logged in as {client.user}")
    print("✅ Slash commands synced!")


@tree.command(
    name="announce",
    description="Send a DM announcement to every server member."
)
@app_commands.checks.has_permissions(administrator=True)
async def announce(interaction: discord.Interaction, message: str):

    await interaction.response.send_message(
        "📨 Sending announcements...",
        ephemeral=True
    )

    sent = 0
    failed = 0

    for member in interaction.guild.members:
        if member.bot:
            continue

        try:
            await member.send(
                f"📢 **Q8Boost Announcements**\n\n{message}"
            )
            sent += 1
        except Exception:
            failed += 1

    await interaction.followup.send(
        f"✅ Finished!\n"
        f"📨 Sent: **{sent}**\n"
        f"❌ Failed: **{failed}**",
        ephemeral=True
    )


@announce.error
async def announce_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        if interaction.response.is_done():
            await interaction.followup.send(
                "❌ You must be an administrator to use this command.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ You must be an administrator to use this command.",
                ephemeral=True
            )


client.run(os.getenv("TOKEN"))
