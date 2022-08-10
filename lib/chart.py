from .note import MalodyNote, OsuNote
from .bpm import OsuBPM, MalodyBPM
from .base_class import ChartBase
from .api import load_file_osu, analyze_osu_raw, load_file_malody, unify
import re

chart_type_list = ['osu', 'mc']


class OsuChart(ChartBase):
    raw_chart: str

    def load_file(self):
        self.raw_chart = load_file_osu(self.chart_file)

    def analyze(self):
        _ = analyze_osu_raw(self.raw_chart)
        _meta = _['Metadata']
        _general = _['General']
        _events = _['Events']
        _timing_points = _['TimingPoints']
        _hit_objects = _['HitObjects']
        _difficulty = _['Difficulty']

        self.song_name = _meta['Title']
        self.unicode_song_name = _meta['TitleUnicode']
        self.artist_name = _meta['Artist']
        self.unicode_artist_name = _meta['ArtistUnicode']

        self.version = _meta['Version']
        self.creator = _meta['Creator']
        self.preview_time = _general['PreviewTime']

        self.music = _general['AudioFilename']
        self.bg = re.findall(r'0,0,\"(.*?)\",0,0', _events[0])[0]

        self.bpm_list = OsuBPM('\n'.join(_timing_points))
        self.column = _difficulty['CircleSize']
        self.note_list = list(OsuNote(self.bpm_list, self.column, x) for x in _hit_objects)
        self.offset = self.bpm_list.offset


class MalodyChart(ChartBase):
    raw_chart: dict

    def load_file(self):
        self.raw_chart = load_file_malody(self.chart_file)

    def analyze(self):
        _ = self.raw_chart
        _meta = _['meta']
        _song = _meta['song']
        _note = _['note']
        _time = _['time']
        _sound_note = None
        for note in _note:
            if 'sound' in note:
                _sound_note = note
        _note.remove(_sound_note)

        self.song_name = _song['title']
        self.unicode_song_name = unify(self.song_name)
        self.artist_name = _song['artist']
        self.unicode_artist_name = unify(self.artist_name)

        self.version = _meta['version']
        self.creator = _meta['creator']
        self.preview_time = 0

        self.music = _sound_note['sound']
        self.bg = _meta['background']

        self.bpm_list = MalodyBPM(_sound_note.get('offset', 0), _time, _sound_note)
        self.column = _meta['mode_ext']['column']
        self.note_list = list(MalodyNote(self.bpm_list, self.column, x) for x in _note)
        self.offset = self.bpm_list.offset
