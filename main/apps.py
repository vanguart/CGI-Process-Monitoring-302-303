from django.apps import AppConfig
import os
import importlib
import asyncio
import threading
import schedule
import time


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            schedule.every(10).seconds.do(run_sync)
            t = threading.Thread(target=run_schedule)
            t.setDaemon(True)
            t.start()


def run_sync():
    print("Started extractation")
    asyncio.run(asyncFunctionGetLogsApi())
    print("Ended extractation")


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


async def asyncFunctionGetLogsApi():
    arquivo = importlib.import_module('apps.logs.services')
    await arquivo.connectionToApi()
