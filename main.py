from lib import *

osu_file = 'test/XX_me - Escape (Tachyon) [Medium(dance-single)].osu'
ma_file = 'test/Various Artists - Malody 4K Extra Dan v3-Stream (ex1).mc'

osu_chart = OsuChart(osu_file).write_osu().write_ma()
ma_chart = MalodyChart(ma_file)
print(osu_chart.chart_dir)
