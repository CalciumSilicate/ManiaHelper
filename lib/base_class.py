import copy
import math
import os
from time import time
from .api import load_file_malody, raw_load
import json
from config import CHART_OUTPUT_DIR
from res import osu_mould, malody_mould


class BPMListBase:
    bpm_list = []  # [(t, bpm)]
    offset = None

    # Game
    malody_bpm = None
    osu_bpm = None

    raw_info = None

    def get_osu(self) -> str:
        return self.osu_bpm

    def get_malody(self):
        return self.malody_bpm

    def get_raw(self):
        return self.raw_info

    def set_times(self, times):
        pass

    def sort(self):
        self.bpm_list = list(sorted(self.bpm_list, key=lambda x: x[0]))


class NoteBase:
    # Base Setting
    t_value: int = None  # ms
    column: int = None
    hold_time: float = None
    general_key: tuple = None  # (time_th, hold_time, column, sound, vol)
    sound = None
    vol = None
    _: int = None

    # Game Setting
    osu_key: str = None
    malody_key: dict = None

    # Raw Info
    raw_info: str or dict = None

    def get_osu(self):
        return self.osu_key

    def get_malody(self):
        return self.malody_key

    def get_raw(self):
        return self.raw_info

    def set_times(self, bpm_list, times):
        pass


class ChartBase:
    song_name: str = None
    unicode_song_name: str = None
    artist_name: str = None
    unicode_artist_name: str = None

    version: str = None
    creator: str = None
    preview_time: int = 0

    music: str = None
    bg: str = None
    chart_file: str = None
    chart_dir: str = None

    bpm_list: BPMListBase = None
    note_list: list[NoteBase] = None
    offset: float = None
    column: int = None

    raw_chart: str or dict = None

    osu_chart: str = None
    malody_chart: dict = None

    create_time: int = None

    def __init__(self, chart_file, is_load=True):
        self.chart_file = chart_file
        self.chart_dir = os.path.dirname(os.path.abspath(chart_file))
        if is_load:
            self.load_file()
            self.analyze()
        self.create_time = math.floor(time())
        self.note_list = list(sorted(self.note_list, key=lambda x: x.t_value))
        self.refresh_chart()

    def load_file(self):
        pass

    def analyze(self):
        pass

    def get_osu(self) -> str:
        return self.osu_chart

    def get_malody(self) -> dict:
        return self.malody_chart

    def refresh_chart(self):
        return self.refresh_malody_chart().refresh_osu_chart()

    def refresh_malody_chart(self):
        _ = copy.deepcopy(malody_mould)
        _['meta']['creator'] = self.creator
        _['meta']['background'] = self.bg
        _['meta']['version'] = self.version
        _['meta']['time'] = self.create_time
        _['meta']['song'] = {'title': self.song_name, 'artist': self.artist_name, 'id': 0}
        _['meta']['mode_ext']['column'] = self.column
        _['time'] = self.bpm_list.get_malody()
        _['note'] = [
            {
                'beat': [0, 0, 1],
                'sound': self.music,
                'vol': 100,
                'type': 1,
                'offset': self.offset
            }
        ]

        self.malody_chart = _
        for note in self.note_list:
            _['note'].insert(-2, note.get_malody())

        return self

    def refresh_osu_chart(self):
        _ = copy.deepcopy(osu_mould)
        _ = _.replace('$music_name', self.music). \
            replace('$preview_time', str(self.preview_time)). \
            replace('$song_name', self.song_name). \
            replace('$unicode_song_name', self.unicode_song_name). \
            replace('$artist_name', self.artist_name). \
            replace('$unicode_artist_name', self.unicode_artist_name). \
            replace('$creator', self.creator). \
            replace('$version', self.version). \
            replace('$keys', str(self.column)). \
            replace('$bg_name', self.bg). \
            replace('$bpm_list_str', self.bpm_list.get_osu().strip())
        note_list = []
        for note in self.note_list:
            note_list.append(note.get_osu())
        _ = _.replace('$note_list_str', '\n'.join(note_list).strip())

        self.osu_chart = _

        return self

    def write(self, path=os.path.join(CHART_OUTPUT_DIR, '$n'), f='osu', is_time=True):
        path = path.replace(r'$n', self.song_name)
        if f not in path:
            path = path + '.' + f
        path = os.path.splitext(path)[0] + '_{}.{}'.format(int(time()), f) if is_time else path
        if not os.path.exists(os.path.dirname(os.path.abspath(path))):
            os.mkdir(os.path.dirname(os.path.abspath(path)))
        with open(path, 'w') as fl:
            fl.write(str(self.osu_chart if f == 'osu' else (json.dumps(self.malody_chart) if f == 'mc' else ['cnm'])))
        return self

    def write_osu(self, path=os.path.join(CHART_OUTPUT_DIR, '$n'), is_time=True):
        return self.write(path, 'osu', is_time)

    def write_ma(self, path=os.path.join(CHART_OUTPUT_DIR, '$n'), is_time=True):
        return self.write(path, 'mc', is_time)

    def set_bpm(self, bpm):
        bpm = float(bpm)
        return self.set_times(round(bpm / self.bpm_list.bpm_list[0][1], 4))
        pass

    def set_times(self, times):
        times = float(times)
        self.version += '({}x)'.format(times)
        self.preview_time = 0
        self.music = '{}_{}x.mp3'.format(os.path.splitext(self.music)[0], times)
        self.bpm_list.set_times(times)
        self.offset = self.bpm_list.offset
        self.raw_chart = None

        __note_list = []
        for note in self.note_list:
            note.set_times(
                self.bpm_list,
                times)
            __note_list.append(note)
        self.note_list = __note_list
        self.refresh_chart().create_time = time()
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self
