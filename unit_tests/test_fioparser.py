import os
import unittest
import fioparser
from mock import patch, call


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestFioparser(unittest.TestCase):

    @patch('fioparser.add_benchmark_metric')
    def test_process_results(self, mock_add_benchmark_metric):
        _expected_calls = [
            call('fio_read_bandwidth', 'FIO read bandwidth (B/s)',
                 172507),
            call('fio_read_iops', 'FIO read IOPS',
                 42.115978),
            call('fio_read_latency', 'FIO read latency (ns)',
                 297241023.51435),
            call('fio_read_clat_min', 'FIO read clat min (ns)',
                 6505387),
            call('fio_read_clat_max', 'FIO read clat max (ns)',
                 3548298824),
            call('fio_read_clat_mean', 'FIO read clat mean (ns)',
                 296849992.620846),
            call('fio_read_clat_stddev', 'FIO read clat stddev (ns)',
                 415530491.24428),
            call('fio_read_clat_1_000000', 'FIO read clat 1.000000 (ns)',
                 18481152),
            call('fio_read_clat_5_000000', 'FIO read clat 5.000000 (ns)',
                 40632320),
            call('fio_read_clat_10_000000', 'FIO read clat 10.000000 (ns)',
                 55312384),
            call('fio_read_clat_20_000000', 'FIO read clat 20.000000 (ns)',
                 84410368),
            call('fio_read_clat_30_000000', 'FIO read clat 30.000000 (ns)',
                 116916224),
            call('fio_read_clat_40_000000', 'FIO read clat 40.000000 (ns)',
                 145752064),
            call('fio_read_clat_50_000000', 'FIO read clat 50.000000 (ns)',
                 179306496),
            call('fio_read_clat_60_000000', 'FIO read clat 60.000000 (ns)',
                 221249536),
            call('fio_read_clat_70_000000', 'FIO read clat 70.000000 (ns)',
                 274726912),
            call('fio_read_clat_80_000000', 'FIO read clat 80.000000 (ns)',
                 354418688),
            call('fio_read_clat_90_000000', 'FIO read clat 90.000000 (ns)',
                 557842432),
            call('fio_read_clat_95_000000', 'FIO read clat 95.000000 (ns)',
                 1082130432),
            call('fio_read_clat_99_000000', 'FIO read clat 99.000000 (ns)',
                 2432696320),
            call('fio_read_clat_99_500000', 'FIO read clat 99.500000 (ns)',
                 3036676096),
            call('fio_read_clat_99_900000', 'FIO read clat 99.900000 (ns)',
                 3539992576),
            call('fio_read_clat_99_950000', 'FIO read clat 99.950000 (ns)',
                 3539992576),
            call('fio_read_clat_99_990000', 'FIO read clat 99.990000 (ns)',
                 3539992576),
            call('fio_write_bandwidth', 'FIO write bandwidth (B/s)', 181888),
            call('fio_write_iops', 'FIO write IOPS', 44.406273),
            call('fio_write_latency', 'FIO write latency (ns)',
                 1871492023.66404),
            call('fio_write_clat_min', 'FIO write clat min (ns)',
                 202075267),
            call('fio_write_clat_max', 'FIO write clat max (ns)',
                 7923538876),
            call('fio_write_clat_mean', 'FIO write clat mean (ns)',
                 1870606285.43553),
            call('fio_write_clat_stddev', 'FIO write clat stddev (ns)',
                 1311956210.532654),
            call('fio_write_clat_1_000000', 'FIO write clat 1.000000 (ns)',
                 299892736),
            call('fio_write_clat_5_000000', 'FIO write clat 5.000000 (ns)',
                 438304768),
            call('fio_write_clat_10_000000', 'FIO write clat 10.000000 (ns)',
                 566231040),
            call('fio_write_clat_20_000000', 'FIO write clat 20.000000 (ns)',
                 792723456),
            call('fio_write_clat_30_000000', 'FIO write clat 30.000000 (ns)',
                 1044381696),
            call('fio_write_clat_40_000000', 'FIO write clat 40.000000 (ns)',
                 1283457024),
            call('fio_write_clat_50_000000', 'FIO write clat 50.000000 (ns)',
                 1501560832),
            call('fio_write_clat_60_000000', 'FIO write clat 60.000000 (ns)',
                 1837105152),
            call('fio_write_clat_70_000000', 'FIO write clat 70.000000 (ns)',
                 2264924160),
            call('fio_write_clat_80_000000', 'FIO write clat 80.000000 (ns)',
                 2734686208),
            call('fio_write_clat_90_000000', 'FIO write clat 90.000000 (ns)',
                 3539992576),
            call('fio_write_clat_95_000000', 'FIO write clat 95.000000 (ns)',
                 4865392640),
            call('fio_write_clat_99_000000', 'FIO write clat 99.000000 (ns)',
                 6341787648),
            call('fio_write_clat_99_500000', 'FIO write clat 99.500000 (ns)',
                 6543114240),
            call('fio_write_clat_99_900000', 'FIO write clat 99.900000 (ns)',
                 6945767424),
            call('fio_write_clat_99_950000', 'FIO write clat 99.950000 (ns)',
                 7952400384),
            call('fio_write_clat_99_990000', 'FIO write clat 99.990000 (ns)',
                 7952400384)]

        _series_file = os.path.join(THIS_DIR,
                                    '../test/resources',
                                    '4M_randrw_2.json')
        _result = fioparser.process_results(_series_file)
        mock_add_benchmark_metric.assert_has_calls(_expected_calls)
        self.assertEqual(30, _result)

    @patch('fioparser.Gauge')
    def test_add_benchmark_metric(self, mock_gauge):
        fioparser.add_benchmark_metric('fio_write_iops',
                                       'description',
                                       'value')
        mock_gauge.assert_called_with('fio_write_iops',
                                      'description',
                                      ['model', 'unit'])

    def test_get_series_files(self):
        proper_result = ['4k_randread_1.json',
                         '4k_randread_2.json',
                         '4k_randread_3.json']
        discovered_series_files = fioparser.get_series_files(
            '4k_randread',
            os.path.join(THIS_DIR, '../test/resources'))
        self.assertEqual(proper_result, discovered_series_files)
