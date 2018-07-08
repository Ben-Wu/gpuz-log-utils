import csv
import os
from argparse import ArgumentParser


def parse_logs(directory, fieldnames=None, log_to_read=None):
    log_files = log_to_read or os.listdir(directory)

    for log_file in log_files:
        with open(log_to_read or os.path.join(directory, log_file)) as f:
            reader = csv.DictReader((c.replace('\0', '') for c in f),
                                    fieldnames=fieldnames)
            # clean up fieldnames
            fieldnames = [f.strip().replace(' ', '') for
                          f in reader.fieldnames]

            reader.fieldnames = fieldnames
            for line in reader:
                yield line


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-f', '--log-file')
    parser.add_argument('--fieldnames', nargs='+')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    work_dir = os.path.dirname(__file__)
    data_dir = os.path.join(work_dir, '..', 'log_data')

    for line in parse_logs(data_dir, args.fieldnames, args.log_file):
        print(line)
