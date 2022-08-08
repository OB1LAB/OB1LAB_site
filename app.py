import json
from logs import *
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/add_log/<server_logs>', methods=['POST'])
def add_log(server_logs):
    global date_logs, unixtime
    server_logs = server_logs.replace('№', '#')
    if request.get_json(force=True)['secret_key'] == secret_key and server_logs in os.listdir('logs'):
        logs_request = request.get_json(force=True)['logs']
        for line in logs_request:
            if unixtime:
                if len(line.split()[0]) == 10 and line.split()[0][9] == ']':
                    if int(datetime.strptime(line.split()[0], '[%H:%M:%S]').timestamp()) < unixtime:
                        date_logs = datetime.now().strftime("%d-%m-%Y.txt")
            unixtime = int(datetime.strptime(line.split()[0], '[%H:%M:%S]').timestamp())
            with open(f'logs/{server_logs}/{date_logs}', 'a', encoding='UTF-8') as file:
                file.write(line)
    elif request.get_json(force=True)['secret_key'] != secret_key:
        return "ПАШОЛ НАХУЙ"*2000
    return 'Not found'


@app.route('/logs', methods=['GET'])
def get_logs_servers():
    server_logs_list = [date.replace('#', "№") for date in os.listdir('logs')]
    server_logs_list.sort()
    return render_template('logs_servers.html', servers=server_logs_list)


@app.route('/logs/<server_logs>', methods=['GET'])
def get_logs_dates(server_logs):
    server_logs = server_logs.replace('№', '#')
    if server_logs in os.listdir('logs'):
        dates = date_sort([date.split('.')[0] for date in os.listdir(f'logs/{server_logs}')])
        return render_template('logs_dates.html', dates=dates, server=server_logs.replace('#', '№'))
    return 'Не найдено'


@app.route('/logs/<server_logs>/<date>', methods=['GET'])
def get_logs(server_logs, date):
    server_logs = server_logs.replace('№', '#')
    if server_logs in os.listdir('logs') and date in os.listdir(f'logs/{server_logs}'):
        logs = open(f'logs/{server_logs}/{date}', 'r', encoding='utf-8').read()
        for color in colors_codes:
            logs = logs.replace(color, colors_codes[color])
        logs = [log for log in logs.splitlines() if 'Tried to add entity minecraft' not in log]
        return render_template('logs.html', logs=logs, server=server_logs.replace('#', '№'), parser=False)
    return 'Не найдено'


@app.route('/logs/<server_logs>/<date>/parser', methods=['GET'])
def get_logs_parser(server_logs, date):
    server_logs = server_logs.replace('№', '#')
    if server_logs in os.listdir('logs') and date in os.listdir(f'logs/{server_logs}'):
        logs = open(f'logs/{server_logs}/{date}', 'r', encoding='utf-8').read()
        for color in colors_codes:
            logs = logs.replace(color, colors_codes[color])
        logs = [log for log in logs.splitlines() if 'Tried to add entity minecraft' not in log]
        return render_template('logs.html', logs=logs, server=server_logs.replace('#', '№'), parser=True)
    return 'Не найдено'


@app.route('/logs/<server_logs>/<date>/html', methods=['GET'])
def get_logs_html(server_logs, date):
    server_logs = server_logs.replace('№', '#')
    if server_logs in os.listdir('logs') and date in os.listdir(f'logs/{server_logs}'):
        logs = open(f'logs/{server_logs}/{date}', 'r', encoding='utf-8').read()
        for color in colors_codes:
            logs = logs.replace(color, colors_codes[color])
        logs = [log for log in logs.splitlines() if 'Tried to add entity minecraft' not in log]
        return '\n'.join(['<b><span style="color: #555555;">'+line+'</span></b>' for line in logs if 'Tried to add entity minecraft' not in line])
    return 'Не найдено'


@app.route('/api/getPlayers', methods=['GET'])
def getPlayers():
    update_player_list()
    return json.dumps(update_player_list()[0])


@app.route('/api/getJuniorStaff', methods=['GET'])
def getJuniorStaff():
    return json.dumps(update_player_list()[1])


@app.route('/api/getServersDates', methods=['GET'])
def getServersDates():
    servers_dates, server_list = {}, get_servers()
    for server_name_date in server_list:
        servers_dates[server_name_date] = server_list[server_name_date]['logs_dates']
    return json.dumps(servers_dates)


@app.route('/api/getActivity', methods=['POST'])
def get_activity():
    data = json.loads(request.data.decode())
    date1 = data['date1'].split('-')
    date2 = data['date2'].split('-')
    date1.reverse()
    date2.reverse()
    date1, date2 = '-'.join(date1), '-'.join(date2)
    return json.dumps(logs_api.get_activity(data['server'], data['players'], get_range_dates(date1, date2)))


@app.route('/tools/activity_check', methods=['GET'])
def activity_check():
    return render_template('activity_check.html', servers=servers, first_server=next(iter(servers)))


if __name__ == '__main__':
    from waitress import serve
    secret_key, unixtime, date_logs = 'cB/`/*qgIJxS&!/*D#Z!AhEo!HyDB_]:SyW', 0, datetime.utcnow().strftime("%d-%m-%Y.txt")
    serve(app, host="0.0.0.0", port=3001)
