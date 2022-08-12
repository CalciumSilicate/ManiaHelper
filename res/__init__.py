# Don't Change This File
# 请勿修改此文件

malody_mould = {
    "meta": {
        "$ver": 0,
        "creator": "$creator",
        "background": "$bg_name",
        "version": "$version",
        "id": 0,
        "mode": 0,
        "time": "$time",
        "song": {
            "title": "$song_name",
            "artist": "$artist_name",
            "id": 0
        },
        "mode_ext": {
            "column": "$column",
            "bar_begin": 0
        }
    },
    "time": [],
    "effect": [],
    "note": [
        {
            "beat": [
                0,
                0,
                1
            ],
            "sound": "$music_name",
            "vol": 100,
            "type": 1,
            "offset": "$offset"
        }
    ],
    "extra": {
        "test": {
            "divide": 4,
            "speed": 100,
            "save": 0,
            "lock": 0,
            "edit_mode": 0
        }
    }
}
osu_mould = '''
osu file format v14

[General]
AudioFilename: $music_name
AudioLeadIn: 0
PreviewTime: $preview_time
Countdown: 0
SampleSet: Soft
StackLeniency: 0.7
Mode: 3
LetterboxInBreaks: 0
SpecialStyle: 0
WidescreenStoryboard: 0

[Editor]
DistanceSpacing: 1.2
BeatDivisor: 4
GridSize: 8
TimelineZoom: 2.4

[Metadata]
Title:$song_name
TitleUnicode:$unicode_song_name
Artist:$artist_name
ArtistUnicode:$unicode_artist_name
Creator:$creator
Version:$version
Source:ManiaHelper
Tags:ManiaHelper by CalciumSilicate
BeatmapID:0
BeatmapSetID:-1

[Difficulty]
HPDrainRate:8
CircleSize:$keys
OverallDifficulty:8
ApproachRate:5
SliderMultiplier:1.4
SliderTickRate:1

[Events]
//Background and Video events
0,0,"$bg_name",0,0

[TimingPoints]
$bpm_list_str

[HitObjects]
$note_list_str
'''.strip()
