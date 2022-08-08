import os
from time import sleep
from OB1L1B import *
from threading import Thread


class Logs:
    def __init__(self):
        if 'logs' not in os.listdir():
            os.mkdir('logs')

    def get_activity(self, server_name, players, dates):
        self.logs_downloader(server_name)
        activity, date, logs = {}, None, None
        for player_check in players:
            activity[player_check.lower()] = {
                'local': 0,
                'global': 0,
                'private': 0,
                'warn': 0,
                'mute': 0,
                'kick': 0,
                'ban': 0,
                'join': [],
                'exit': [],
                'vanish_join': [],
                'vanish_exit': [],
                'vanish': False,
                'online': False,
                'show_nick': None
            }
        if dates[0] in self.client_dates and self.client_dates.index(dates[0]) > 0:
            file_date = self.client_dates[self.client_dates.index(dates[0]) - 1]
            logs = open(f'logs/{server_name}/{file_date}.txt', 'r', encoding='utf-8').readlines()
            for line in logs:
                log = get_log_type(line.split())
                if log['type'] and log['player'] in activity:
                    if log['type'] == 'join' and not activity[log['player']]['online']:
                        activity[log['player']]['online'] = True
                        if not activity[log['player']]['show_nick']:
                            activity[log['player']]['show_nick'] = line.split()[1]
                    elif log['type'] == 'exit' and activity[log['player']]['online']:
                        activity[log['player']]['online'] = False
                        if activity[log['player']]['vanish']:
                            activity[log['player']]['vanish'] = False
                    elif log['type'] == 'vanish':
                        if activity[log['player']]['vanish']:
                            activity[log['player']]['vanish'] = False
                        else:
                            activity[log['player']]['vanish'] = True
                    if log['type'] != 'exit' and not activity[log['player']]['online']:
                        activity[log['player']]['online'] = True
        unfinded_dates = '\n'.join([date for date in dates if date not in self.client_dates])
        if unfinded_dates:
            self.output(f'Не найдены логи за следующие даты:\n{unfinded_dates}')
            return
        for date in dates:
            logs = open(f'logs/{server_name}/{date}.txt', 'r', encoding='utf-8').readlines()
            for line in logs:
                log = get_log_type(line.split())
                if log['type'] and log['player'] in activity:
                    if log['type'] == 'join' and not activity[log['player']]['online']:
                        activity[log['player']]['online'] = True
                        activity[log['player']]['join'].append(unix_log(date, line))
                        if not activity[log['player']]['show_nick']:
                            activity[log['player']]['show_nick'] = line.split()[1]
                    elif log['type'] == 'exit' and activity[log['player']]['online']:
                        activity[log['player']]['online'] = False
                        if not activity[log['player']]['join']:
                            activity[log['player']]['join'].append(unix_log(date, logs[0]))
                        activity[log['player']]['exit'].append(unix_log(date, line))
                        if activity[log['player']]['vanish']:
                            if not activity[log['player']]['vanish_join']:
                                activity[log['player']]['vanish_join'].append(unix_log(date, logs[0]))
                            activity[log['player']]['vanish_exit'].append(unix_log(date, line))
                            activity[log['player']]['vanish'] = False
                    elif log['type'] == 'vanish':
                        if activity[log['player']]['vanish']:
                            if not activity[log['player']]['vanish_join']:
                                activity[log['player']]['vanish_join'].append(unix_log(date, logs[0]))
                            activity[log['player']]['vanish_exit'].append(unix_log(date, line))
                            activity[log['player']]['vanish'] = False
                        else:
                            activity[log['player']]['vanish_join'].append(unix_log(date, line))
                            activity[log['player']]['vanish'] = True
                    elif log['type'] in ['local', 'global', 'private', 'warn', 'mute', 'kick', 'ban']:
                        activity[log['player']][log['type']] += 1
                    if log['type'] != 'exit' and not activity[log['player']]['online']:
                        activity[log['player']]['join'].append(unix_log(date, line))
                        activity[log['player']]['online'] = True
                    elif (log['type'] != 'vanish' and activity[log['player']]['vanish']
                          and len(activity[log['player']]['vanish_join']) == 0):
                        activity[log['player']]['vanish_join'].append(unix_log(date, line))
        if date and logs:
            for pc in activity:
                if len(activity[pc]['join']) > len(activity[pc]['exit']):
                    activity[pc]['exit'].append(unix_log(date, logs[-1]))
                if len(activity[pc]['vanish_join']) > len(activity[pc]['vanish_exit']):
                    activity[pc]['vanish_exit'].append(unix_log(date, logs[-1]))
                activity[pc]['average_online_time'] = f"{beautiful_output_time(int(get_range_times(activity[pc]['join'], activity[pc]['exit'])/len(dates)))} ({beautiful_output_time(int(get_range_times(activity[pc]['vanish_join'], activity[pc]['vanish_exit'])/len(dates)))}) "
                activity[pc]['online_time'] = f"{beautiful_output_time(get_range_times(activity[pc]['join'], activity[pc]['exit']))} ({beautiful_output_time(get_range_times(activity[pc]['vanish_join'], activity[pc]['vanish_exit']))}) "
                if not activity[pc]['show_nick']:
                    activity[pc]['show_nick'] = pc
        return activity

    def log_download(self, date, server_name):
        with open(f'logs/{server_name}/{date}.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(get(f'{servers[server_name]["url"]}/{date}.txt')))
            self.output(f'Скачаны логи за {date}')

    def logs_downloader(self, server_name):
        if server_name not in os.listdir('logs'):
            os.mkdir(f'logs/{server_name}')
        self.client_dates = date_sort([date.split('.')[0] for date in os.listdir(f'logs/{server_name}')])
        self.logs_dates = []
        if not check_access(servers[server_name]['url']):
            self.output('Не удалось получить доступ к логам')
            return
        uns_dates = [date.split('>')[1].split('.')[0] for date in get(servers[server_name]['url']) if '.txt' in date]
        self.logs_dates = date_sort(uns_dates)
        thread_download = []
        if len(self.client_dates) > 0:
            thread_download.append(Thread(target=self.log_download, args=(self.client_dates[-1], server_name,)))
        for date in self.logs_dates:
            if date not in self.client_dates:
                thread_download.append(Thread(target=self.log_download, args=(date, server_name,)))
                self.client_dates.append(date)
        for date_download in thread_download:
            date_download.start()
        for date_download_wait in thread_download:
            date_download_wait.join()

    def output(self, log):
        pass
        # print(log)


def get_servers():
    for server_name in servers:
        if server_name in os.listdir('logs'):
            servers[server_name]['logs_dates'] = date_sort([date.split('.')[0] for date in os.listdir(
                f'logs/{server_name}')], True)
        else:
            servers[server_name]['logs_dates'] = ['1970-01-01']
    return servers


def logs_thread_downloader(server_name):
    while True:
        logs_api.logs_downloader(server_name)
        sleep(15)


logs_api = Logs()
for server in servers:
    thread_log_download = (Thread(target=logs_thread_downloader, args=(server,)))
    thread_log_download.start()
