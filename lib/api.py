import json
import re


def load_file_osu(file_path) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_file_malody(file_path) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


raw_load = load_file_osu


def is_uni(char):
    return re.match(r'^[A-Za-z0-9_\-/&%$#@!^)(?>;:\'"\[\]{}=+*]*$', char)


def unify(string: str) -> str:
    _ = list(string)
    _del = []
    for x in _:
        if not is_uni(x):
            _del.append(x)
    for i in _del:
        _.remove(i)
    return ''.join(_)


def analyze_osu_raw(chart: str) -> dict:
    _ = {}
    flag = None
    for line in chart.splitlines():
        line = line.strip()
        if line.startswith('//') or line.startswith('osu file format') or line == '':
            continue
        if line.startswith('['):
            flag = line[1:-1]
        if flag not in _ and flag is not None:
            _[flag] = {} if flag not in ['Events', 'TimingPoints', 'HitObjects'] else []
        split_line = line.split(':')
        child_flag = split_line[0].strip()
        value = ':'.join(split_line[1:]).strip()
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                value = str(value)
        if flag not in ['Events', 'TimingPoints', 'HitObjects'] and not line.startswith('['):
            _[flag][child_flag] = value
        elif flag in ['Events', 'TimingPoints', 'HitObjects'] and not line.startswith('['):
            _[flag].append(line)
    return _
