import discord
from discord.commands import slash_command, Option
from discord.ext import commands
import os
from neohowiebot.modals import ClipCreationModal, CreateDelayModal
from neohowiebot.services import file_service, play_clip
from neohowiebot.views import PlayerView

GUILD_ID = int(os.getenv("GUILD_ID"))


async def clip_search(ctx: discord.AutocompleteContext):
    if ctx.value == '':
        return ['random']
    else:
        return [clip for clip in file_service.get_clips() if ctx.value in clip.lower()][:25]


class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="create", guild_ids=[GUILD_ID])
    async def create(self,
                     ctx: discord.ApplicationContext,
                     mode: Option(str, 'Chose what to create', choices=['clip', 'delay'])):
        """Create something new"""
        if mode == 'clip':
            modal = ClipCreationModal()
        elif mode == 'delay':
            modal = CreateDelayModal()
        await ctx.interaction.response.send_modal(modal)

    @slash_command(name="play", guild_ids=[GUILD_ID])
    async def play(self, ctx: discord.ApplicationContext,
                   clip: Option(str, 'Pick a clip', autocomplete=clip_search)):
        """Play a clip"""
        selection = clip if clip else 'random'
        if (selection not in file_service.get_clips()) & (selection != 'random'):
            await ctx.respond(f'{selection} is not a valid clip', ephemeral=True)
        else:
            user = ctx.interaction.user
            if user.voice is not None:
                await ctx.respond(f'{ctx.user.display_name} played {selection}')
                await play_clip(user.voice.channel, selection)

    @slash_command(name="player", guild_ids=[GUILD_ID])
    async def player(self, ctx: discord.ApplicationContext):
        """Create a player"""
        await ctx.interaction.response.send_message(content='Press play button for a random clip', view=PlayerView())
