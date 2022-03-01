import discord
from discord.ui import Modal, InputText
from neohowiebot.views import ClipCreatedView, DisabledClipCreated, DelayCreatedView
from neohowiebot.services import create_clip, play_clip, file_service, mix_clips
from neohowiebot.validators import create_clip_validator, save_clip_validator, create_delay_validator


class ClipCreationModal(Modal):
    def __init__(self) -> None:
        super().__init__(title='Create a New Clip')
        self.add_item(InputText(label='YouTube Link'))
        self.add_item(InputText(label="Start Time", value='00:00:00.00'))
        self.add_item(InputText(label="Duration"))

    async def callback(self, interaction: discord.Interaction):
        inputs = {'link': self.children[0].value,
                  'start': self.children[1].value,
                  'duration': self.children[2].value}
        valid = create_clip_validator(interaction.user, inputs)

        if valid[0]:
            # TODO: Would it look better to use embeds? I couldn't make it look that great on first pass.
            await interaction.response.defer()
            create_clip(inputs['link'], inputs['start'], inputs['duration'], 'resources/tmp.mp3')
            await interaction.followup.send(content=f'{interaction.user.display_name} created a new clip: \n{inputs["link"]}',
                                                    view=ClipCreatedView(interaction, inputs))
            if interaction.user.voice:
                await play_clip(interaction.user.voice.channel, 'tmp')
        else:
            await interaction.response.send_message(valid[1], ephemeral=True)


class EditClipModal(Modal):
    def __init__(self, inputs: object, source_interaction: discord.Interaction) -> None:
        """source_interaction is the interaction that spawed this modal"""
        super().__init__(title='Edit Clip')
        self.add_item(InputText(label='YouTube Link', value=inputs['link']))
        self.add_item(InputText(label='Start Time', value=inputs['start']))
        self.add_item(InputText(label='Duration', value=inputs['duration']))
        self.source_interaction = source_interaction

    async def callback(self, interaction: discord.Interaction):
        inputs = {'link': self.children[0].value,
                  'start': self.children[1].value,
                  'duration':self.children[2].value}
        valid = create_clip_validator(interaction.user, inputs)

        if valid[0]:
            await interaction.response.defer()
            create_clip(inputs['link'], inputs['start'], inputs['duration'], 'resources/tmp.mp3')
            await interaction.followup.send(content=f'{interaction.user.display_name} created a new clip: \n{inputs["link"]}',
                                                    view=ClipCreatedView(interaction, inputs))
            await self.source_interaction.edit_original_message(view=DisabledClipCreated(), content='Clip edited')
            if interaction.user.voice:
                await play_clip(interaction.user.voice.channel, 'tmp')
        else:
            await interaction.response.send_message(valid[1], ephemeral=True)


class SaveClipModal(Modal):
    def __init__(self) -> None:
        super().__init__(title='Save Clip')
        self.add_item(InputText(label="New clip name"))

    async def callback(self, interaction: discord.Interaction):
        clip_name = self.children[0].value
        valid = save_clip_validator(clip_name)

        if valid[0]:
            await interaction.response.defer()
            file_service.save_clip(clip_name)
            await interaction.followup.send(content=f'{interaction.user.display_name} saved clip {clip_name}')
        else:
            await interaction.response.send_message(valid[1], ephemeral=True)


# This is ugly, and doesn't follow the pattern of the other modal by having an EditDelayModal
class CreateDelayModal(Modal):
    def __init__(self, inputs: object = None, source_interaction: discord.Interaction = None) -> None:
        super().__init__(title='Create Delay Clip')

        entry: InputText = InputText(
            label="Delay Input",
            placeholder="clip1, 10\nclip2, 20\nclip3",
            style=discord.InputTextStyle.long,
        )
        if inputs: entry.value = inputs
        self.add_item(entry)
        self.source_interaction = source_interaction

    async def callback(self, interaction: discord.Interaction):
        inputs = self.children[0].value
        valid = create_delay_validator(interaction.user, inputs)

        if valid[0]:
            metadata = build_clip_metadata(inputs)
            await interaction.response.defer()
            mix_clips(metadata)
            await interaction.followup.send(content=f'{interaction.user.display_name} created a delay clip.',
                                                    view=DelayCreatedView(interaction, inputs))
            if self.source_interaction:
                await self.source_interaction.edit_original_message(view=DisabledClipCreated(), content='Delay clip edited')
            if interaction.user.voice:
                await play_clip(interaction.user.voice.channel, 'tmp')
        else:
            await interaction.response.send_message(valid[1], ephemeral=True)


def build_clip_metadata(inputs: str):
    meta = []
    pos = 0
    for inp in inputs.split('\n'):
        filename = file_service.get_clip_file(inp.split(',')[0])
        meta.append((filename, pos))
        if len(inp.split(',')) > 1:
            pos += int(inp.split(',')[1])
    return meta



