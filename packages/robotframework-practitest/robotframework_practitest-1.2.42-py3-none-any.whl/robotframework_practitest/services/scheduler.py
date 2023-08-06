import logging
from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from queue import Queue, Empty
from threading import Thread, Event
from time import sleep
from typing import Callable

from robotframework_practitest.utils import get_error_info, logger
from robotframework_practitest.utils.singleton import Singleton


logging.basicConfig(format='[%(asctime)s][%(threadName)s : %(filename)s: %(lineno)d] %(levelname)s - %(message)s')

logger = logger.LOGGER


class TaskType(Enum):
    Synchron = 'Synchron'
    Asynchron = 'Asynchron'
    Foreground = 'Foreground'


class Task:
    def __init__(self, callback: Callable, *args, **kwargs):
        self._callback = callback
        self._args = args
        self._kwargs = kwargs

    def __str__(self):
        return "{} ({}, {})".format(
            self._callback.__name__,
            ', '.join(f'{a}' for a in self._args),
            ', '.join([f'{k}={v}' for k, v in self._kwargs.items()])
        )

    def __call__(self):
        return self._callback(*self._args, **self._kwargs)

    def run(self, type_: TaskType):
        if type_ == TaskType.Foreground:
            return self()

        if type_ == TaskType.Asynchron:
            _BackgroundAsyncService(self.__class__.__name__).schedule_task(self)
        elif type_ == TaskType.Synchron:
            _BackgroundSyncService(self.__class__.__name__).schedule_task(self)
        else:
            raise TypeError(f"Task '{self}' have unknown type")

    @staticmethod
    def shutdown():
        _BackgroundSyncService().join()
        _BackgroundAsyncService().join()


class _BackGroundAbstract:
    def __init__(self, name=None):
        self.name = name or self.__class__.__name__

    @abstractmethod
    def schedule_task(self, task: Task):
        pass

    def join(self):
        pass


@Singleton
class _BackgroundSyncService(_BackGroundAbstract):
    def __init__(self, name=None, maxsize=0, thread_interval=0.2):
        self._event = Event()
        self._active = Event()
        self._queue = Queue(maxsize)
        self._thread_interval = thread_interval
        name = name or self.__class__.__name__
        _BackGroundAbstract.__init__(self, "Sync " + name)
        self._thread = Thread(target=self._worker, name=self.name, daemon=True)
        # logger.register_thread_to_logger(self.name)
        logger.info(f"Starting {self.name}...")
        self._thread.start()

    def _worker(self):
        logger.info(f"{self.__class__.__name__}::_worker started")
        while not self._event.is_set():
            try:
                task_obj = self._queue.get()
                logger.debug(f"{self.__class__.__name__}::Task '{task_obj}' start")
                task_obj()
                logger.debug(f"{self.__class__.__name__}::Task '{task_obj}' done")
            except Empty:
                pass
            except Exception as e:
                f, li = get_error_info()
                logger.info(f"Error: {e}; File: {f}:{li}")
            finally:
                sleep(self._thread_interval)
        logger.info(f"{self.__class__.__name__}::_worker ended")

    def schedule_task(self, item: Task):
        if not self._active.is_set():
            self._queue.put(item)
            logger.debug(f"Task '{item}' added")
        else:
            logger.warn("Service ending awaiting; New task adding not possible now")

    def join(self, timeout=None):
        sleep(5)
        self._active.set()
        logger.debug(f'Join; Remains {self._queue.qsize()} tasks')
        while not self._queue.empty():
            sleep(0.2)
        logger.debug(f'All tasks completed')
        self._event.set()
        logger.info(f"Stopped {self.name}...")


@Singleton
class _BackgroundAsyncService(_BackGroundAbstract):
    def __init__(self, name=None):
        name = name or self.__class__.__name__
        super().__init__("Async " + name)
        self.executor = ThreadPoolExecutor(thread_name_prefix=self.name)
        # logger.register_thread_to_logger(self.name)
        self.active = True

    def schedule_task(self, task: Task):
        if not self.active:
            logger.warn("Service ending awaiting; New task adding not possible now")
            return
        self.executor.submit(task)

    def join(self):
        self.executor.shutdown(wait=True)


def run_task(task_type: TaskType, callback: Callable, *args, **kwargs):
    Task(callback, *args, **kwargs).run(task_type)


__all__ = [
    'TaskType',
    'Task',
    'run_task'
]
