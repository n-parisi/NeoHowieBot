import re

import discord
from neohowiebot.services import file_service


# All validator functions should return boolean and error message

def create_clip_validator(member: discord.Member, inputs):
    if not is_admin_request(member):
        return False, 'Clip creation is only available to admins (for now)'
    if 'youtube.com' not in inputs['link']:
        return False, 'Clip must be a link to youtube.com'
    if not is_timestamp(inputs['start']):
        return False, 'Start time must be in format HH:MM:SS.MM'
    if not 0 < float(inputs['duration']) <= 30:
        return False, 'Duration must be a number of seconds between 0 and 30'
    return True, ''


def save_clip_validator(clip_name):
    if clip_name in file_service.get_clips():
        return False, 'Clip with that name already exists'
    else:
        return True, ''


def create_delay_validator(member: discord.Member, inputs):
    if not is_admin_request(member):
        return False, 'Clip creation is only available to admins (for now)'
    for inp in inputs.split('\n'):
        clip_name = inp.split(',')[0]
        if clip_name not in file_service.get_clips():
            return False, f'{clip_name} is not a valid clip'
    return True, ''


def is_admin_request(member: discord.Member):
    return member.guild_permissions.administrator


def is_timestamp(timestamp):
    if re.match(r'\d{2}:\d{2}:\d{2}\.\d{2}', timestamp) is None:
        return False
    else:
        return True
