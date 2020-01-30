#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import functools
import logging
from crontab import CronTab
from datetime import datetime, timedelta
import math

__author__ = 'Shinichi Nakagawa'


class JobController(object):
    """
    Kontroler wykonywania pracy
    """

    @classmethod
    def run(cls, crontab):
        """
        Przetwarzanie wykonania
        :param crontab: job schedule
        """
        def receive_func(job):
            @functools.wraps(job)
            def wrapper():

                job_settings = JobSettings(CronTab(crontab))
                logging.info("->- Process Start")
                while True:
                    try:
                        logging.info(
                            "-?- next running\tschedule:%s" %
                            job_settings.schedule().strftime("%Y-%m-%d %H:%M:%S")
                        )
                        time.sleep(job_settings.interval())
                        logging.info("->- Job Start")
                        job()
                        logging.info("-<- Job Done")
                    except KeyboardInterrupt:
                        break
                logging.info("-<- Process Done.")
            return wrapper
        return receive_func


class JobSettings(object):
    """
    Ustawienia początkowe
    """

    def __init__(self, crontab):
        """
        :param crontab: crontab.CronTab
        """
        self._crontab = crontab

    def schedule(self):
        """
        Następne wykonanie zadania
        :return: datetime
        """
        crontab = self._crontab
        return datetime.now() + timedelta(seconds=math.ceil(crontab.next()))

    def interval(self):
        """
        Czas do następnego wykonania
        :return: seconds
        """
        crontab = self._crontab
        return math.ceil(crontab.next())