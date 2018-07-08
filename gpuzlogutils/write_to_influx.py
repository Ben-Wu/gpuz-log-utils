import os
from argparse import ArgumentParser

from influxdb import InfluxDBClient

from gpuzlogutils import logfile_parser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--hostname', default='localhost')
    parser.add_argument('--port', default=8086, type=int)
    parser.add_argument('--database', default='gpuz')
    parser.add_argument('-d', '--directory')
    parser.add_argument('-f', '--log-file')
    parser.add_argument('-g', '--gpu-name', required=True)
    parser.add_argument('--fieldnames', nargs='+')

    return parser.parse_args()


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

    for line in logfile_parser.parse_logs(data_dir, args.fieldnames, args.log_file):
        print(line)
