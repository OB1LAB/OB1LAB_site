import requests
from config import *
from datetime import datetime, timedelta


def get_log_type(log):
    if len(log) == 3 and log[2] == 'зашёл':
        return {
            'type': 'join',
            'player': log[1].lower()
        }
    elif len(log) == 3 and log[2] == 'вышел':
        return {
            'type': 'exit',
            'player': log[1].lower()
        }
    elif len(log) > 5 and log[2] == 'issued':
        if log[5].lower() == '/vanish':
            return {
                'type': 'vanish',
                'player': log[1].lower()
            }
        elif log[5].lower() in config['pm_list'] and len(log) > 7 or log[5].lower() == '/r' and len(log) > 6:
            return {
                'type': 'private',
                'player': log[1].lower()
            }
        elif log[5].lower() == '/warn' and len(log) > 6:
            return {
                'type': 'warn',
                'player': log[1].lower()
            }
        elif log[5].lower() == '/mute' and len(log) > 6 or log[5].lower() == '/tempmute' and len(log) > 9:
            return {
                'type': 'mute',
                'player': log[1].lower()
            }
        elif log[5].lower() == '/kick' and len(log) > 7:
            return {
                'type': 'kick',
                'player': log[1].lower()
            }
        elif log[5].lower() == '/ban' and len(log) > 6 or log[5].lower() == '/tempban' and len(log) > 9:
            return {
                'type': 'ban',
                'player': log[1].lower()
            }
    elif log[1] == '[L]':
        return {
            'type': 'local',
            'player': log[2].split(':')[0].lower()
        }
    elif log[1] == '[G]':
        return {
            'type': 'global',
            'player': log[2].split(':')[0].lower()
        }
    return {
        'type': None
    }


def get_activity_time(join_mass, exit_mass, days=0):
    if days:
        return beautiful_output_time(int(get_range_times(join_mass, exit_mass)/days))
    return beautiful_output_time(get_range_times(join_mass, exit_mass))


def beautiful_output_time(time):
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
    if seconds < 10:
        output += f':0{seconds}'
    else:
        output += f':{seconds}'
    return output


def get_range_times(join_mass, exit_mass):
    time = 0
    for line in range(len(join_mass)):
        time += exit_mass[line]-join_mass[line]
    return time


def to_datestr(date, reverse=False):
    if reverse:
        return date.strftime('%Y-%m-%d')
    return date.strftime('%d-%m-%Y')


def to_datetime(date):
    return datetime.strptime(date, '%d-%m-%Y')


def get_range_days(date_1, date_2):
    return range((to_datetime(date_2)-to_datetime(date_1)).days+1)


def get_range_dates(date_1, date_2):
    return [to_datestr(to_datetime(date_1)+timedelta(days=day)) for day in get_range_days(date_1, date_2)]


def unix_log(date, log):
    unix = int(datetime.strptime(f'{date} {log.split()[0]}', '%d-%m-%Y [%H:%M:%S]').timestamp())
    return unix


def date_sort(dates, reverse=False):
    dates_unix = [to_datetime(date) for date in dates]
    dates_unix.sort()
    return [to_datestr(date, reverse) for date in dates_unix]


def check_access(url):
    if requests.get(url).status_code == 200:
        return True
    return False


def get(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.splitlines()
        return get(url)
    except:
        return get(url)


def update_player_list():
    all_staff, staff_list, staff_dict, junior_staff = requests.get(url_staff).json(), [], {}, {}
    for server in all_staff[3:6]:
        junior_staff[server['title'].replace('- ', '')] = [
            admin['name'] for admin in server['moders'] if admin['group'] in junior_staff_ranks]
        staff_list.extend([admin for admin in server['moders']])
    for player in staff_list:
        if player['name'] not in staff_dict:
            staff_dict[player['name']] = player['group']
    return staff_dict, junior_staff
