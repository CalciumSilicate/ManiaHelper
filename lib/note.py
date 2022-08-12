from .converter import beat_index_by_ma, bi2ms_bpm_list, column_ma2osu, column_osu2ma, reformat_beat_index, \
    ms2bi_bpm_list
from .base_class import NoteBase, BPMListBase


class MalodyNote(NoteBase):

    def __init__(self, bpm_list: BPMListBase, keys, note: dict):
        # Base Setting
        offset = bpm_list.offset
        beat_index = beat_index_by_ma(*note.get('beat', [0, 0, 0]))
        self.t_value = bi2ms_bpm_list(bpm_list, beat_index)
        self.column = note.get('column')
        if note.get('endbeat') is not None:
            end_beat_index = beat_index_by_ma(*note.get('endbeat', [0, 0, 0]))
            self.hold_time = bi2ms_bpm_list(bpm_list, end_beat_index) - bi2ms_bpm_list(bpm_list, beat_index)
        else:
            self.hold_time = 0

        if note.get('sound') is not None and note.get('vol') is not None:
            self.sound = note.get('sound')
            self.vol = note.get('vol')
        else:
            self.sound = ''
            self.vol = 0
        self.general_key = (self.t_value, self.hold_time, self.column, self.sound, self.vol)

        # Game Setting Malody
        self.malody_key = note

        # Game Setting Osu!
        key = '{},192,{}'.format(column_ma2osu(self.column, keys), int(self.t_value - 2 * offset))
        hold = '128,0,{}'.format(int(self.hold_time)) if self.hold_time else '1,0,0'
        self.osu_key = '{},{}:0:0:{}:{}'.format(key, hold, self.vol, self.sound)

        # Raw Info
        self.raw_info = self.malody_key

        self._ = keys

    def set_times(self, bpm_list, times):
        b = OsuNote(bpm_list, self._, self.get_osu())
        b.set_times(bpm_list, times)
        self.t_value = b.t_value
        self.hold_time = b.hold_time
        self.general_key = b.general_key
        self.osu_key = b.get_osu()
        self.malody_key = b.get_malody()
        self.raw_info = b.raw_info


class OsuNote(NoteBase):

    def __init__(self, bpm_list: BPMListBase, keys, note: str) -> None:
        # Analysis
        split_string = note.split(',')
        split_meta = split_string[-1].split(':')
        split_string.append(split_meta.pop(0))
        # Base Setting
        self.column = column_osu2ma(int(split_string[0]), keys)
        self.t_value = int(split_string[2])
        self.hold_time = int(split_string[5].split(':')[0])
        self.sound = split_meta[-1]
        self.vol = float(split_meta[-2])

        self.general_key = (self.t_value, self.hold_time, self.column, self.sound, self.vol)

        # Game Setting Osu!
        self.osu_key = note

        # Game Setting Malody
        self.malody_key = {  # ms_to_beat_index(self.t_value, offset, bpm_list[0])
            'beat': list(
                reformat_beat_index(
                    ms2bi_bpm_list(
                        bpm_list, self.t_value
                    )
                )
            ),
            'column': self.column
        }
        if self.hold_time > 1:
            self.malody_key['endbeat'] = list(
                reformat_beat_index(ms2bi_bpm_list(bpm_list, self.hold_time)))
        if self.vol:
            self.malody_key['sound'] = self.sound
            self.malody_key['vol'] = self.vol

        # Raw Info
        self.raw_info = self.osu_key

        self._ = keys

    def set_times(self, bpm_list, times):
        osu_split = self.get_osu().split(',')
        split_last = osu_split[-1].split(':')
        new = [*osu_split[:2], str(round(float(osu_split[2]) / times)), *osu_split[3:5],
               ':'.join([str(round(float(split_last[0]) / times)), *split_last[1:]])]
        self.__init__(
            bpm_list,
            self._,
            ','.join(new))
