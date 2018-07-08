import csv
import os
from argparse import ArgumentParser


def parse_logs(directory=None, fieldnames=None, log_to_read=None,
               skip_first=False):
    """Gets all the lines of all the csv's in a directory or reads
        from a single file

    :param directory: path to directory with csv's;
        will only read given file if None
    :param fieldnames: names of columns in csv;
        will read column names from csv if None
    :param log_to_read: path to single log file to read
    :yield: line of csv as a dict
    """
    if directory is None and log_to_read is None:
        raise ValueError('either path to directory to read from or '
                         'path to log file must be given')

    log_files = (log_to_read or
                 [f for f in os.listdir(directory) if
                  f.endswith('.csv') or f.endswith('.txt')])

    for log_file in log_files:
        with open(log_to_read or os.path.join(directory, log_file)) as f:
            reader = csv.DictReader((c.replace('\0', '') for c in f),
                                    fieldnames=fieldnames)
            # clean up fieldnames
            fieldnames = [f.strip().replace(' ', '') for
                          f in reader.fieldnames]
            reader.fieldnames = fieldnames
            if skip_first:
                reader.__next__()
            for line in reader:
                yield dict(line)


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
