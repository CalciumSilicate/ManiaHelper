from .converter import beat_index_by_ma, beat_index_to_ms, bi2ms_bpm_list, reformat_beat_index, ms2bi_bpm_list
from .base_class import BPMListBase
from copy import deepcopy


class MalodyBPM(BPMListBase):

    def __init__(self, offset, bpm_list, sound_note):
        self.offset = t = int(offset)
        self.bpm_list = []
        is_first = True
        for x in range(len(bpm_list)):
            bpm = bpm_list[x]
            if is_first:
                is_first = False
                self.bpm_list.append((t, bpm.get('bpm')))
            else:
                latest_bpm = bpm_list[x - 1]
                new_beat_index = beat_index_by_ma(*bpm.get('beat'))
                latest_beat_index = beat_index_by_ma(*latest_bpm.get('beat'))
                t += beat_index_to_ms(new_beat_index - latest_beat_index, latest_bpm.get('bpm'), 0)
                self.bpm_list.append((float(t), float(bpm.get('bpm'))))

        self.malody_bpm = bpm_list

        self.osu_bpm = ''
        str_list = []
        for i in self.bpm_list:
            t, bpm = i
            str_list.append('{},{},4,1,0,0,1,0'.format(t - 2 * offset, 60000 / bpm))
        self.osu_bpm = '\n'.join(str_list)

        self.raw_info = bpm_list
        if sound_note['beat'] != [0, 0, 1]:
            tmp = deepcopy(self)
            beat_offset = bi2ms_bpm_list(tmp, beat_index_by_ma(*sound_note['beat']))
            self.__init__(beat_offset + self.offset, bpm_list, {'beat': [0, 0, 1]})


class OsuBPM(BPMListBase):

    def __init__(self, bpm_list: str):
        split_string = bpm_list.strip().splitlines()
        self.offset = -int(split_string[0].split(',')[0])
        for bpm in split_string:
            split_bpm = bpm.replace('\n', '').split(',')
            self.bpm_list.append((float(split_bpm[0]), 60000 / float(split_bpm[1])))
        self.osu_bpm = bpm_list.strip()

        self.malody_bpm = []

        for i in self.bpm_list:
            t, bpm = i
            self.malody_bpm.append({
                'beat': list(reformat_beat_index(ms2bi_bpm_list(self, t - float(self.offset)))),
                'bpm': bpm
            })
        self.sort()
