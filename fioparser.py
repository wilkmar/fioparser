import json
import argparse
import glob
import os
import time
import logging as log
from prometheus_client import start_http_server, Gauge

metrics = {}


def process_results(series_file):
    """Process json result by series and send metrics to the Prometheus

    :param series_file: file name for a single series run
    :return:
    """
    with open(series_file, 'r') as f:
        _result = json.load(f)

    log.info(f"Processing file: {series_file}")
    log.info(f"Time: {_result['time']}. "
             f"Global options: {_result['global options']}")
    _runtime = int(_result["global options"]["runtime"])

    for job in _result["jobs"]:
        for metric in ('read', 'write'):
            bandwidth = job[metric]["bw"]
            iops = job[metric]["iops"]
            # lat_ns is broadly slat + clat so
            # represents what the calling application
            # would actually see in terms of latency
            latency = job[metric]["lat_ns"]["mean"]
            if all((bandwidth, iops, latency)):
                add_benchmark_metric(
                    'fio_{}_bandwidth'.format(metric),
                    'FIO {} bandwidth (B/s)'.format(metric),
                    bandwidth
                )
                add_benchmark_metric(
                    'fio_{}_iops'.format(metric),
                    'FIO {} IOPS'.format(metric),
                    iops
                )
                add_benchmark_metric(
                    'fio_{}_latency'.format(metric),
                    'FIO {} latency (ns)'.format(metric),
                    latency
                )
            # But add some more detailed latency reporting anyway
            _keys = ('min', 'max', 'mean', 'stddev')
            for _key in _keys:
                add_benchmark_metric(
                    'fio_{}_{}_{}'.format(metric,
                                          'clat',
                                          _key),
                    'FIO {} {} {} (ns)'.format(metric,
                                               'clat',
                                               _key),
                    job[metric]["clat_ns"][_key]
                )
            percentiles = job[metric]["clat_ns"]["percentile"]
            for percentile, latency in percentiles.items():
                add_benchmark_metric(
                    'fio_{}_{}_{}'.format(
                        metric,
                        'clat',
                        percentile.replace('.', '_')),
                    'FIO {} {} {} (ns)'.format(metric,
                                               'clat',
                                               percentile),
                    latency
                )
    return _runtime


def add_benchmark_metric(label, description, value):
    """
    labels:
        fio_{read|write}_{iops,bandwidth,latency}
        rbd_bench_{read|write}_??
        rados_bench_{read|write}_??
    """
    if label not in metrics:
        metrics[label] = Gauge(
            label, description,
            ['model', 'unit']
        )
    metrics[label].labels(
        'fioparser', 'no-juju').set(value)
    log.debug(f"Setting metric {label} ({description}): {value}")


def get_series_files(series, directory):
    """Return the series files

    :param series: fio series bs_ops, ie 4k_read
    :param directory: dir where the series files are
    :return:
    """
    files = []
    os.chdir(directory)
    for file in glob.glob("*" + series + "*.json"):
        files.append(file)
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(description='Proccess fio json results')
    parser.add_argument('series',
                        help='combination of block size and rw/operation in '
                             'fio, ie 4k_randread')
    parser.add_argument('-d', '--directory',
                        dest='directory',
                        help='directory where the fio result json files '
                             'are stored')
    parser.add_argument('--debug', dest='debug',
                        action='store_true',
                        help='enable debug logging (default: False)')
    parser.set_defaults(debug=False)
    args = parser.parse_args()
    if args.debug:
        log.basicConfig(level=log.DEBUG)
    else:
        log.basicConfig(level=log.INFO)
    log.debug(f"args: series={args.series} directory={args.directory} "
              f"debug={args.debug}")

    start_http_server(8088)
    series_files = get_series_files(args.series, args.directory)
    log.info("Discovered series files: " + str(series_files))

    _runtime = -1
    for series_file in series_files:
        if _runtime > 0:
            # mimic real time data collection interval
            time.sleep(_runtime)
        _runtime = process_results(series_file)

    log.info("Done")


if __name__ == '__main__':
    main()
