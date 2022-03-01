import discord
from discord.commands import slash_command, Option
from discord.ext import commands
import os
from neohowiebot.modals import ClipCreationModal, CreateDelayModal
from neohowiebot.services import file_service, play_clip

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
        if selection not in file_service.get_clips():
            await ctx.respond(f'{selection} is not a valid clip', ephemeral=True)
        else:
            user = ctx.interaction.user
            if user.voice is not None:
                await ctx.respond(f'{ctx.user.display_name} played {selection}')
                await play_clip(user.voice.channel, selection)

    # TODO: For MVP:
    #   1. [DONE] Delay modal
    #   2. [DONE] Actual files
    #   3. [DONE] Playback
    #   4. [DONE] Create and replay
    #   5. [DONE] Save clips
    #   6. [DONE] Create delay
    #   6. [DONE] Validators
    #   7. Docker-ify the application (Podman time?) w/ runDocker.sh script (no docker-compose)
    # TODO: Future:
    #   1. Stats / Database
    #   2. Player command (Not sure how to do this one unless can ignore a button)
    #   3. Way to list all clips
    #   4. Better way to unstuck the voice client
    #   5. Get start time from yt link
    #   6. Allow 'random' in delay
