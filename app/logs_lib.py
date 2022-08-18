import requests
from time import sleep
from datetime import datetime, timedelta


def log_type(log):
    if len(log) == 3 and log[2] == 'зашёл':
        return {
            'type': 'join',
            'player': log[1]
        }
    elif len(log) == 3 and log[2] == 'вышел':
        return {
            'type': 'exit',
            'player': log[1]
        }
    elif len(log) > 5 and log[2] == 'issued':
        if log[5].lower() == '/vanish':
            return {
                'type': 'vanish',
                'player': log[1]
            }
        elif (log[5].lower() in ['/tell', '/m', '/w', '/msg', '/pm', '/t', '/whisper', '/mail']
              and len(log) > 7 or log[5].lower() == '/r' and len(log) > 6):
            return {
                'type': 'private',
                'player': log[1]
            }
        elif log[5].lower() == '/warn' and len(log) > 6:
            return {
                'type': 'warn',
                'player': log[1]
            }
        elif log[5].lower() == '/mute' and len(log) > 6 or log[5].lower() == '/tempmute' and len(log) > 9:
            return {
                'type': 'mute',
                'player': log[1]
            }
        elif log[5].lower() == '/kick' and len(log) > 7:
            return {
                'type': 'kick',
                'player': log[1]
            }
        elif log[5].lower() == '/ban' and len(log) > 6 or log[5].lower() == '/tempban' and len(log) > 9:
            return {
                'type': 'ban',
                'player': log[1]
            }
    elif log[1] == '[L]':
        return {
            'type': 'local',
            'player': log[2].split(':')[0]
        }
    elif log[1] == '[G]':
        return {
            'type': 'global',
            'player': log[2].split(':')[0]
        }
    return {
        'type': None
    }


def req_get(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.splitlines()
        sleep(5)
        return req_get(url)
    except:
        sleep(5)
        return req_get(url)


def range_days(date_1, date_2):
    return range((to_datetime(date_2)-to_datetime(date_1)).days+1)


def get_server_logs_dates(server_name):
    return [date.split('>')[1].replace('</a', '') for date in req_get(server_name) if '.txt' in date]


def to_datetime(date):
    return datetime.strptime(date, '%d-%m-%Y')


def date_range_str(date_1, date_2, with_txt=False):
    if with_txt:
        return [(to_datetime(date_1) + timedelta(days=day)).strftime('%d-%m-%Y') + '.txt' for day in range_days(date_1,
                                                                                                                date_2)]
    return [(to_datetime(date_1) + timedelta(days=day)).strftime('%d-%m-%Y') for day in range_days(date_1, date_2)]


def date_sort(dates, reverse_date=False, with_txt=True, in_reverse=False):
    if '.txt' in dates[0]:
        if in_reverse:
            dates_unix = [datetime.strptime(date, '%Y-%m-%d.txt') for date in dates]
        else:
            dates_unix = [datetime.strptime(date, '%d-%m-%Y.txt') for date in dates]
    else:
        if in_reverse:
            dates_unix = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
        else:
            dates_unix = [datetime.strptime(date, '%d-%m-%Y') for date in dates]
    dates_unix.sort()
    if reverse_date:
        if with_txt:
            return [date.strftime('%Y-%m-%d')+'.txt' for date in dates_unix]
        return [date.strftime('%Y-%m-%d') for date in dates_unix]
    if with_txt:
        return [date.strftime('%d-%m-%Y')+'.txt' for date in dates_unix]
    return [date.strftime('%d-%m-%Y') for date in dates_unix]


def unix_log(date, log):
    unix = int(datetime.strptime(f'{date} {log.split()[0]}', '%d-%m-%Y [%H:%M:%S]').timestamp())
    return unix


def output_time(time):
    hours, time = int(time/3600), time-int(time/3600)*3600
    minutes, seconds = int(time/60), time-int(time/60)*60
    if hours < 10:
        output = f'0{hours}'
    else:
        output = str(hours)
    if minutes < 10:
        output += f':0{minutes}'
    else:
        output += f':{minutes}'
    return output


def diff_times(join_mass, exit_mass):
    time = 0
    for line in range(len(join_mass)):
        time += exit_mass[line]-join_mass[line]
    return time
