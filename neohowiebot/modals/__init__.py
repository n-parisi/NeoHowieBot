import discord
from discord.ui import Modal, InputText
from neohowiebot.views import ClipCreatedView, DisabledClipCreated, DelayCreatedView


class ClipCreationModal(Modal):
    def __init__(self) -> None:
        super().__init__(title='Create a New Clip')
        self.add_item(InputText(label='YouTube Link'))
        self.add_item(InputText(label="Start Time", value='00:00:00.00'))
        self.add_item(InputText(label="Duration"))

    async def callback(self, interaction: discord.Interaction):
        inputs_valid = True

        if inputs_valid:
            inputs = {'link': self.children[0].value,
                      'start': self.children[1].value,
                      'duration': self.children[2].value}

            # TODO: Would it look better to use embeds? I couldn't make it look that great on first pass.
            # e = discord.Embed(title="New clip created",
            #                   color=discord.Color.random(),
            #                   url=inputs['link'])
            # e.add_field(name='Author', value=interaction.user.display_name, inline=False)
            # e.add_field(name='Duration', value=inputs['duration'])
            # video_id = inputs['link'].split('=')[1]
            # e.set_thumbnail(url=f'http://img.youtube.com/vi/{video_id}/maxresdefault.jpg')

            await interaction.response.send_message(f'{interaction.user.display_name} created a new clip: \n{inputs["link"]}',
                                                    view=ClipCreatedView(interaction, inputs))
        else:
            await interaction.response.send_message('Invalid inputs.', ephemeral=True)


class EditClipModal(Modal):
    def __init__(self, inputs: object, source_interaction: discord.Interaction) -> None:
        """source_interaction is the interaction that spawed this modal"""
        super().__init__(title='Edit Clip')
        self.add_item(InputText(label='YouTube Link', value=inputs['link']))
        self.add_item(InputText(label='Start Time', value=inputs['start']))
        self.add_item(InputText(label='Duration', value=inputs['duration']))
        self.source_interaction = source_interaction

    async def callback(self, interaction: discord.Interaction):
        inputs_valid = True

        if inputs_valid:
            inputs = {'link': self.children[0].value,
                      'start': self.children[1].value, 'duration':
                          self.children[2].value}
            await interaction.response.send_message(f'{interaction.user.display_name} created a new clip: \n{inputs["link"]}',
                                                    view=ClipCreatedView(interaction, inputs))
            await self.source_interaction.edit_original_message(view=DisabledClipCreated(), content='Clip edited')
        else:
            await interaction.response.send_message('Invalid inputs.', ephemeral=True)


class SaveClipModal(Modal):
    def __init__(self) -> None:
        super().__init__(title='Save Clip')
        self.add_item(InputText(label="New clip name"))

    async def callback(self, interaction: discord.Interaction):
        inputs_valid = True

        if inputs_valid:
            clip_name = self.children[0].value
            await interaction.response.send_message(f'{interaction.user.display_name} Saved clip {clip_name}')
        else:
            await interaction.send_message('Save is invalid', ephemeral=True)


# This is ugly, and doesn't follow the pattern of the other modal by having an EditDelayModal
class CreateDelayModal(Modal):
    def __init__(self, inputs: object = None, source_interaction: discord.Interaction = None) -> None:
        super().__init__(title='Create Delay Clip')

        entry: InputText = InputText(
            label="Delay Input",
            placeholder="clip1, 10\nclip2, 20\nclip3,10",
            style=discord.InputTextStyle.long,
        )
        if inputs: entry.value = inputs
        self.add_item(entry)
        self.source_interaction = source_interaction

    async def callback(self, interaction: discord.Interaction):
        inputs = self.children[0].value
        inputs_valid = True

        if inputs_valid:
            await interaction.response.send_message(f'{interaction.user.display_name} created a delay clip.',
                                                    view=DelayCreatedView(interaction, inputs))
            if self.source_interaction:
                await self.source_interaction.edit_original_message(view=DisabledClipCreated(), content='Delay clip edited')
        else:
            await interaction.send_message('Delay inputs are invalid', ephemeral=True)





