import os
from argparse import ArgumentParser
from datetime import datetime

from influxdb import InfluxDBClient

from gpuzlogutils.logfile_parser import parse_logs


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--hostname', default='localhost')
    parser.add_argument('--port', type=int, default=8086)
    parser.add_argument('--database', default='gpuz')
    parser.add_argument('-d', '--directory')
    parser.add_argument('-f', '--log-file')
    parser.add_argument('-g', '--gpu-name', required=True)
    parser.add_argument('--fieldnames', nargs='+')
    parser.add_argument('--batch-size', type=int, default=1)

    return parser.parse_args()


def influx_data_point(measurement, gpu_name, fields, timestamp):
    return {
        'measurement': measurement,
        'tags': {'gpuName': gpu_name},
        'fields': fields,
        'time': timestamp
    }


if __name__ == '__main__':
    args = parse_args()

    influx = InfluxDBClient(host=args.hostname,
                            port=args.port,
                            database=args.database)

    existing_databases = [d['name'] for d in influx.get_list_database()]
    if args.database not in existing_databases:
        influx.create_database(args.database)

    data_dir = args.directory or os.path.join(
        os.path.dirname(__file__), '..', 'log_data')

    rejected_values = {'', '-'}

    point_buffer = []

    for i, line in enumerate(parse_logs(data_dir, args.fieldnames,
                                        args.log_file, skip_first=True)):
        for k in args.fieldnames:
            try:
                line[k] = line[k].strip()
                if line[k] in rejected_values:
                    del line[k]
                else:
                    line[k] = float(line[k])
            except ValueError:
                pass
        timestamp = line.pop('time')
        point_buffer.append(
            influx_data_point('gpu', args.gpu_name, line, timestamp))
        if len(point_buffer) % args.batch_size == 0:
            influx.write_points(point_buffer)

    if len(point_buffer) > 0:
        influx.write_points(point_buffer)
