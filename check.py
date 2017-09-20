import csv
from os import listdir, path, walk
from glob import glob
from os.path import isfile, join
from subprocess import call
import argparse

script_path = path.dirname(__file__)
if script_path:
    script_path += '/'

parser = argparse.ArgumentParser(description='Rewrite the awslogs.conf file')
parser.add_argument('--list', dest='list_file', help='A CSV file of directories')
parser.add_argument('--conf', dest='conf_file', help='Sample AWS conf file')
args = parser.parse_args()

list_path = args.list_file if args.list_file else script_path + 'list.csv'
conf_path = args.conf_file if args.conf_file else script_path + 'awslogs.conf'

print('Using list file', list_path, ' and conf file', conf_path)

logs = []
with open(list_path) as log_list_file:
    log_csv = csv.DictReader(log_list_file)
    for row in log_csv:
        logs.append(row)

with open(conf_path) as conf_file:
    log_conf = conf_file.read()

log_list = []
for log in logs:
    log_dir_path = log['dir']
    if log['recursive']:
        log_files = [y for x in walk(log_dir_path) for y in glob(join(x[0], '*'))]
    else:
        log_files = [join(log_dir_path, f) for f in listdir(log_dir_path)]

    log_files = [f for f in log_files if isfile(join(log_dir_path, f))]
    
    for log_file in log_files:
        log_stream = log_file.replace(log_dir_path + '/', '')
        print('log stream', log_stream)

        log_conf += "\n"
        log_conf += '[' + log_file + ']'+"\n"

        if log['datetime_format']:
            log_conf += 'datetime_format = ' + log['datetime_format'] + "\n"

        log_conf += 'file = '+ log_file + "\n"
        log_conf += 'log_stream_name = ' + log_stream +"\n"
        log_conf += 'initial_position = start_of_file' +"\n"
        log_conf += 'log_group_name = ' + log['log_group_name'] +"\n"

active_conf_path = '/var/awslogs/etc/awslogs.conf'
with open(active_conf_path, 'r+') as active_conf_file:
    active_conf = active_conf_file.read()
    if active_conf!=log_conf:
        print('Active conf and log conf are different. Will rewrite file and restart log service')
        active_conf_file.seek(0)
        active_conf_file.write(log_conf)
        active_conf_file.truncate()
        call(["service", "awslogs", "restart"])
