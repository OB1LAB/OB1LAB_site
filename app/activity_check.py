from app.logs_public_downloader import os
from app.logs_lib import log_type, unix_log, output_time, diff_times, date_range_str, date_sort


def get_activity(server_name, players, date_1, date_2):
    dates = date_range_str(date_sort([date_1], in_reverse=True, with_txt=False)[0],
                           date_sort([date_2], in_reverse=True, with_txt=False)[0])
    activity, date, logs, local_dates = {}, None, None, os.listdir(f'logs/public/{server_name}')
    for player_check in players:
        activity[player_check] = {
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
            'online': False
        }
    if dates[0] in local_dates and local_dates.index(dates[0]) > 0:
        file_date = local_dates[local_dates.index(dates[0]) - 1]
        logs = open(f'logs/public/{server_name}/{file_date}.txt', 'r', encoding='utf-8').readlines()
        for line in logs:
            log = log_type(line.split())
            if log['type'] and log['player'] in activity:
                if log['type'] == 'join' and not activity[log['player']]['online']:
                    activity[log['player']]['online'] = True
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
    if [date for date in dates if date + '.txt' not in local_dates]:
        return
    for date in dates:
        logs = open(f'logs/public/{server_name}/{date}.txt', 'r', encoding='utf-8').readlines()
        for line in logs:
            log = log_type(line.split())
            if log['type'] and log['player'] in activity:
                if log['type'] == 'join' and not activity[log['player']]['online']:
                    activity[log['player']]['online'] = True
                    activity[log['player']]['join'].append(unix_log(date, line))
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
    if not date or not logs:
        return activity
    for pc in activity:
        if len(activity[pc]['join']) > len(activity[pc]['exit']):
            activity[pc]['exit'].append(unix_log(date, logs[-1]))
        if len(activity[pc]['vanish_join']) > len(activity[pc]['vanish_exit']):
            activity[pc]['vanish_exit'].append(unix_log(date, logs[-1]))
        avg_online = output_time(int(diff_times(activity[pc]['join'], activity[pc]['exit']) / len(dates)))
        avg_online_vanish = output_time(int(diff_times(activity[pc]['vanish_join'],
                                                       activity[pc]['vanish_exit']) / len(dates)))
        all_online = output_time(diff_times(activity[pc]['join'], activity[pc]['exit']))
        all_online_vanish = output_time(diff_times(activity[pc]['vanish_join'], activity[pc]['vanish_exit']))
        activity[pc]['avg'] = f"{avg_online}<br>{avg_online_vanish}"
        activity[pc]['total'] = f"{all_online}<br>{all_online_vanish}"
        activity[pc].pop('join')
        activity[pc].pop('exit')
        activity[pc].pop('vanish_join')
        activity[pc].pop('vanish_exit')
    return activity
