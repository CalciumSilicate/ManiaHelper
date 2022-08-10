import math
from .base_class import BPMListBase


def beat_index_to_ms(beats, bpm, offset):
    return 1000 * 60 / bpm * beats + offset


def beat_index_by_ma(measure, beat_th, divisor):
    return measure + beat_th / divisor


def ms_by_ma(measure, beat_th, divisor, bpm, offset):
    return beat_index_to_ms(beat_index_by_ma(measure, beat_th, divisor), bpm, offset)


def ms_to_beat_index(ms, offset, bpm):
    return round((ms - offset) * bpm / 1000 / 60, 8)


def reformat_beat_index(beat_index):
    mdf = math.modf(beat_index)
    fl = mdf[0]
    it = mdf[1]
    for i in range(768):
        if i / 768 - fl >= 0:
            return int(it), int(i), 768
    return int(it) + 1, 0, 768


def convert_bpm(value):
    return round(60000 / value, 8)


def column_ma2osu(column, keys):
    return int(512 * (2 * column + 1) / (2 * keys))


def column_osu2ma(key_value, keys):
    return int((key_value * keys / 256 - 1) / 2)


def ms2bi_bpm_list(bpm_list: BPMListBase, ms):
    bpm_list_ = bpm_list.bpm_list
    offset = bpm_list_[0][0]
    passed_bpm_list = []
    beat_index = 0
    for i in bpm_list_:
        if ms >= i[0]:
            passed_bpm_list.append(i)
        else:
            break
    for i in range(1, len(passed_bpm_list)):
        t, bpm = passed_bpm_list[i]
        latest_t, latest_bpm = passed_bpm_list[i - 1]
        beat_index += ms_to_beat_index(t - latest_t, 0, latest_bpm)
    if passed_bpm_list:
        t, bpm = passed_bpm_list[-1]
        beat_index += ms_to_beat_index(ms - t, 0, bpm)
    return beat_index


def bi2ms_bpm_list(bpm_list: BPMListBase or list, bi, override_offset: int = None):
    bpm_list_ = bpm_list.bpm_list
    offset = bpm_list_[0][0] if override_offset is None else override_offset
    bi_list = []
    ms = offset
    for i in bpm_list_:
        t, bpm = i
        bi_list.append((ms2bi_bpm_list(bpm_list, t), bpm))
    passed_bi_list = []
    for i in bi_list:
        if bi >= i[0]:
            passed_bi_list.append(i)
        else:
            break
    for i in range(1, len(passed_bi_list)):
        bi_, bpm = passed_bi_list[i]
        latest_bi, latest_bpm = passed_bi_list[i - 1]
        ms += beat_index_to_ms(bi_ - latest_bi, latest_bpm, 0)
    bi_, bpm = passed_bi_list[-1]
    ms += beat_index_to_ms(bi - bi_, bpm, 0)
    return ms
