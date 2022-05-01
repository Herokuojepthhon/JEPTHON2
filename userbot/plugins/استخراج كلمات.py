# Copyright (C) 2022 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
#

"""
Lyrics Plugin Syntax:
       .lyrics <aritst name> - <song nane>
"""
import os
import lyricsgenius
import random

from userbot.events import register
from userbot import CMD_HELP, LOGS, GENIUS


@register(outgoing=True, pattern="^.استخراج كلمات الاغنيه(?: |$)(.*)")
async def lyrics(lyric):
    if r"-" in lyric.text:
        pass
    else:
        await lyric.edit("`Error: please use '-' as divider for <artist> and <song>`\n"
                         "eg: `Nicki Minaj - Super Bass`")
        return
    if GENIUS is None:
        await lyric.edit("`يرجى اضافه فار خاص بالامر  !`")
        return
    else:
        try:
            GApi = GENIUS
            genius = lyricsgenius.Genius(GApi)
            args = lyric.text.split('.lyrics')[1].split('-')
            artist = args[0].strip(' ')
            song = args[1].strip(' ')
        except Exception:
            await lyric.edit("`يرجى اضافه اسم الفنان والاغنيه مثال : محمود التركي اشمك  `")
            return

    if len(args) < 1:
        await lyric.edit("`يرجى اضافه اسم الفنان والاغنيه مثال : محمود التركي اشمك`")
        return

    await lyric.edit(f"`البحث عن كلمات {artist} - {song}...`")

    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None

    if songs is None:
        await lyric.edit(f"Song **{artist} - {song}** not found!")
        return
    if len(songs.lyrics) > 4096:
        await lyric.edit("`حبيبي الكلمات مال الاغنيه كلش جبيره افتح الملف وحتشوفهن كلهن.`")
        with open("lyrics.txt", "w+") as f:
            f.write(f"Search query: \n{artist} - {song}\n\n{songs.lyrics}")
        await lyric.client.send_file(
            lyric.chat_id,
            "lyrics.txt",
            reply_to=lyric.id,
            )
        os.remove("lyrics.txt")
    else:
        await lyric.edit(f"**Search query**: \n`{artist} - {song}`\n\n```{songs.lyrics}```")
    return


CMD_HELP.update({
    "lyrics":
    "**Usage:** .`lyrics <artist name> - <song name>`\n"
    "__note__: **-** is neccessary when searching the lyrics to divided artist and song"
})