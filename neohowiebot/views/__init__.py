import discord
import neohowiebot.modals as modals
from neohowiebot.services import play_clip


class ClipCreatedView(discord.ui.View):
    def __init__(self, view_creation_interaction: discord.Interaction = None, creation_inputs: object = None):
        """view_creation_interaction is the interaction that sent the msg containing this view"""
        super().__init__()
        self.view_creation_interaction = view_creation_interaction
        self.creation_inputs = creation_inputs

    @discord.ui.button(label="Replay", style=discord.ButtonStyle.primary)
    async def replay(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(view=self)
        if interaction.user.voice:
            await play_clip(interaction.user.voice.channel, 'tmp')

    @discord.ui.button(label="Save", style=discord.ButtonStyle.green)
    async def save(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(modals.SaveClipModal())

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.red)
    async def edit(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(
            modals.EditClipModal(self.creation_inputs, self.view_creation_interaction))


class DisabledClipCreated(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Replay", style=discord.ButtonStyle.primary, disabled=True)
    async def replay(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label="Save", style=discord.ButtonStyle.green, disabled=True)
    async def save(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.red, disabled=True)
    async def edit(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass


# So much ugly boiler plate....
class DelayCreatedView(discord.ui.View):
    def __init__(self, view_creation_interaction: discord.Interaction = None, creation_inputs: str = None):
        """view_creation_interaction is the interaction that sent the msg containing this view"""
        super().__init__()
        self.view_creation_interaction = view_creation_interaction
        self.creation_inputs = creation_inputs

    @discord.ui.button(label="Replay", style=discord.ButtonStyle.primary)
    async def replay(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(view=self)
        if interaction.user.voice:
            await play_clip(interaction.user.voice.channel, 'tmp')

    @discord.ui.button(label="Save", style=discord.ButtonStyle.green)
    async def save(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(modals.SaveClipModal())

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.red)
    async def edit(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(
            modals.CreateDelayModal(self.creation_inputs, self.view_creation_interaction))
