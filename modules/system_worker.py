import asyncio
import psutil
import cpuinfo
import distro
import platform
import json
from logging import Logger
from modules.event import EventHookAsync
from modules.logger import AppLogger
from time import time
from threading import Thread


class SystemInfoWorker:
    """
        This class automaticaly run a background worker
        Get hardware system informations and trigger an event with an EventHook

        On init, the worker is run in an infinite loop in a new thread

        Events function can be binded to the property onChange:
        self.onChangeAsync += myFunction
    """

    __read_tick: int
    __queue_size: int
    __queue: dict
    __logger: Logger

    onChangeAsync: EventHookAsync

    def __init__(self, read_tick=2, queue_size=30) -> None:
        self.__logger = AppLogger().get_logger(type(self).__name__)
        self.__read_tick = read_tick
        self.__queue_size = queue_size
        self.__queue = {"static": {}, "periodic": []}
        self.onChangeAsync = EventHookAsync()
        thread = Thread(target=self.__loop_in_thread__)
        thread.start()

    def __loop_in_thread__(self) -> None:
        eventLoop = asyncio.new_event_loop()
        eventLoop.run_until_complete(self.start_worker())

    async def start_worker(self) -> None:
        """ Start the periodic worker, this function fire an event every `readTick` seconds """

        previous_tick = 0
        self.__queue["static"] = self.get_static_system_info()
        while True:
            unix_seconds = int(time())
            if unix_seconds % self.__read_tick == 0 and previous_tick != unix_seconds:
                self.__logger.debug("Get periodic info")
                info = self.get_periodic_system_info()
                info["time"] = unix_seconds * 1000
                while len(self.__queue["periodic"]) >= self.__queue_size:
                    self.__queue["periodic"].pop(0)

                self.__queue["periodic"].append(info)
                await self.onChangeAsync.invoke_async(json.dumps(self.__queue))
                previous_tick = unix_seconds
            await asyncio.sleep(0.1)  # to keep low CPU load

    def get_periodic_system_info(self) -> dict:
        """ Get hardare information which change over time """

        memory_info = psutil.virtual_memory()._asdict()
        cpu_freq = psutil.cpu_freq()._asdict()
        cpu_percent = psutil.cpu_percent()
        cpu_cores = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count(logical=True)

        host_partitions = psutil.disk_partitions()
        disk_infos = []
        for partitions in host_partitions:
            current = psutil.disk_usage(partitions.mountpoint)._asdict()
            current["mountpoint"] = partitions.mountpoint
            disk_infos.append(current)

        system_info = {
            "memoryInfo": memory_info,
            "cpuInfo": {
                "frequence": cpu_freq,
                "percent": int(cpu_percent),
                "cores": cpu_cores,
                "threads": cpu_threads
            },
            "diskInfo": disk_infos
        }

        return system_info

    def get_static_system_info(self) -> dict:
        """ Get static information which not change over time (like cpu name, os name ect...) """

        cpu_name = cpuinfo.get_cpu_info()['brand_raw']
        platform_name = platform.system()
        os_version = ''
        os_kernel = ''
        if platform_name == 'Windows':
            os_version = platform.release()
            os_kernel = platform.version()
        else:
            os_version = distro.name(pretty=True)
            os_kernel = platform.release()

        return {
            "cpuName": cpu_name,
            "operatingSystem": platform_name + " " + os_version,
            "kernel": os_kernel
        }
