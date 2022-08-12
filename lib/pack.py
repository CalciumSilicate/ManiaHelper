from config import *
from utils import decompress, compress_folder, get_file_dir, a_speed
from lib import *
import shutil
from copy import deepcopy
from time import time


class Pack:
    chart_list: dict = {'chart': {}, 'depress_dir': '', 'dir_name': ''}

    # {'chart_id': {'chart_fd': {}, 'chart': ChartBase}}

    def __init__(self, pack_fd):
        zip_name = os.path.split(pack_fd)[-1]
        depress_dir = os.path.join(DEPRESS_OUTPUT_DIR, '{}_{}'.format(round(time()), os.path.splitext(zip_name)[0]))
        decompress(pack_fd, depress_dir)
        osu_folder = get_file_dir('osu', depress_dir)
        mc_folder = get_file_dir('mc', depress_dir)
        self.chart_list['depress_dir'] = depress_dir
        self.chart_list['dir_name'] = os.path.split(depress_dir)[1]
        for file in os.listdir(osu_folder):
            if os.path.splitext(file)[-1] == '.osu':
                self.chart_list['chart'][file] = {'chart': OsuChart(os.path.join(osu_folder, file)), 'f': 'osu',
                                                  'status': 'original'}
        for file in os.listdir(mc_folder):
            if os.path.splitext(file)[-1] == '.mc':
                self.chart_list['chart'][file] = {'chart': MalodyChart(os.path.join(osu_folder, file)), 'f': 'mc',
                                                  'status': 'original'}
        if not os.path.exists(os.path.join(CHART_OUTPUT_DIR, self.chart_list['dir_name'])):
            os.makedirs(os.path.join(CHART_OUTPUT_DIR, self.chart_list['dir_name']))

    def write(self, __chart: dict, f=''):
        __pack = self.chart_list
        __output_dir = os.path.join(CHART_OUTPUT_DIR, __pack['dir_name'])
        __chart['chart'].write(os.path.join(
            __output_dir, '{}'.format(__chart['chart'].version)),
            __chart['f'] if not f else f)
        bg = __chart['chart'].bg
        if not os.path.exists(os.path.join(__output_dir, __chart['chart'].music)):
            shutil.copyfile(os.path.join(DEPRESS_OUTPUT_DIR, __pack['dir_name'], __chart['chart'].music),
                            os.path.join(__output_dir, __chart['chart'].music))
        if not os.path.exists(os.path.join(__output_dir, bg)):
            shutil.copyfile(os.path.join(DEPRESS_OUTPUT_DIR, __pack['dir_name'], bg),
                            os.path.join(__output_dir, bg))

    def write_all(self, f='', flag=None):
        if flag is None:
            flag = ['timed', 'original']
        __pack = self.chart_list
        __output_dir = os.path.join(CHART_OUTPUT_DIR, __pack['dir_name'])
        for __chart in __pack['chart'].values():
            if True and __chart['status'] in flag:
                self.write(__chart, f)
        compress_folder(
            os.path.join(CHART_ZIP_OUTPUT_DIR, __pack['dir_name'] + ('.osz' if f in ['', 'osu'] else '.mcz')),
            os.path.join(__output_dir))

    def write_timed(self, f=''):
        self.write_all(flag='timed')

    def write_original(self, f=''):
        self.write_all(flag='original')

    def close(self):
        print(os.path.join(DEPRESS_OUTPUT_DIR, self.chart_list['dir_name']))
        shutil.rmtree(os.path.join(DEPRESS_OUTPUT_DIR, self.chart_list['dir_name']))
        shutil.rmtree(os.path.join(CHART_OUTPUT_DIR, self.chart_list['dir_name']))

    def set_times(self, times, original_chart_index=0):
        times = float(times)
        c = self.chart_list['chart'][list(self.chart_list['chart'].keys())[original_chart_index]]
        original_chart: ChartBase = deepcopy(c['chart'])
        original_chart.set_times(times)
        a_speed('"' + os.path.join(DEPRESS_OUTPUT_DIR, self.chart_list['dir_name'], c['chart'].music) + '"',
                str(times),
                '"' + os.path.join(DEPRESS_OUTPUT_DIR, self.chart_list['dir_name'], original_chart.music) + '"')
        self.chart_list['chart'][original_chart.version] = {'chart': original_chart, 'f': c['f'], 'status': 'timed'}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
