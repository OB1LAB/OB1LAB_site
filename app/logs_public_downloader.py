import os
from time import sleep
from threading import Thread
from app.logs_lib import req_get, date_sort, get_server_logs_dates
from app.config import download_logs_url


def logs_downloader():
    while True:
        for server_name in download_logs_url:
            server_dates = date_sort(get_server_logs_dates(download_logs_url[server_name]))
            local_dates = os.listdir(f'logs/public/{server_name}')
            for date in server_dates:
                if date not in local_dates:
                    with open(f'logs/public/{server_name}/{date}', 'w', encoding='utf-8') as file:
                        file.write('\n'.join(req_get(f'{download_logs_url[server_name]}/{date}')))
            with open(f'logs/public/{server_name}/{server_dates[-1]}', 'w', encoding='utf-8') as file:
                file.write('\n'.join(req_get(f'{download_logs_url[server_name]}/{server_dates[-1]}')))
        sleep(5)


def start_thread_logs_download():
    thread_log_download = Thread(target=logs_downloader)
    thread_log_download.start()
