import asyncio
import random
import subprocess

import boto3
import os
import discord
from pydub import AudioSegment


class FileService:
    def __init__(self):
        self.bucket = os.getenv("RESOURCE_BUCKET")
        self.clip_prefix = os.getenv("CLIPS_PREFIX")
        self.local_path = 'resources/sounds/'

    def sync_resources(self):
        client = boto3.resource('s3')
        bucket = client.Bucket(self.bucket)
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)
        for obj in bucket.objects.filter(Prefix=self.clip_prefix):
            if obj.key[-1] != "/" and not os.path.exists(obj.key):  # Ignore S3 'folders'
                print(f'Downloading {obj.key}...')
                bucket.download_file(obj.key, obj.key)

    def get_clips(self):
        return [filename[:filename.index(".")] for filename in os.listdir(self.local_path)]

    def get_clip_file(self, clip):
        for filename in os.listdir(self.local_path):
            if clip == filename[0:-4]:
                return self.local_path + filename

    def save_clip(self, clip_name):
        local_file = self.local_path + clip_name + '.mp3'
        os.rename('resources/tmp.mp3', local_file)

        client = boto3.client('s3')
        client.upload_file(
            local_file, self.bucket, local_file,
            ExtraArgs={'StorageClass': 'STANDARD'}
        )

    def get_clip_file(self, clip):
        for filename in os.listdir(self.local_path):
            if clip == filename[0:-4]:
                return self.local_path + filename


file_service = FileService()
file_service.sync_resources()


# Playback Functions (find a better home for this)
async def play_clip(channel, clip_name):

    if clip_name == 'random':
        clip_name = random.choice(file_service.get_clips())
    if clip_name == 'tmp':
        clip_path = 'resources/tmp.mp3'
    else:
        clip_path = file_service.get_clip_file(clip_name.strip())

    voice_client = await channel.connect()
    source = discord.FFmpegPCMAudio(clip_path)
    voice_client.play(source)
    while voice_client.is_playing():
        await asyncio.sleep(1)
    await voice_client.disconnect()


def create_clip(yt_resource, start, duration, output_file):
    resources = str(subprocess.check_output(["yt-dlp", "-g", yt_resource])).split("\\n")
    subprocess.call(['ffmpeg', '-y', '-ss', start, '-i', resources[1], '-t', duration, '-b:a', '192k', output_file])


# clips_metadata is list of tuples (clip file path, position in ms).
# Overlay all audio at interval specified by delay. Save to filesystem
def mix_clips(clips_metadata):
    # Parse all clips
    clips = [(AudioSegment.from_wav(path) if '.wav' in path else AudioSegment.from_mp3(path), position)
             for path, position in clips_metadata]

    # Determine duration of new sound
    dur = max([len(clip) + position for clip, position in clips])

    [len(clip) + position for clip, position in clips]

    # Create silent sound, overlay other sounds on top
    final_sound = AudioSegment.silent(duration=dur)
    for clip, pos in clips:
        final_sound = final_sound.overlay(clip, position=pos)

    # Save the final result
    final_sound.export('resources/tmp.mp3', format='mp3')
