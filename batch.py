#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from multiprocessing import Pool
from scheduler.job import JobController

__author__ = 'Shinichi Nakagawa'


# Uwaga: Strefa czasowa Docker Image to UTC!
@JobController.run("20 15 * * 5")
def notice_tmr_club():
    """
    Tamori Club Time (Tokio)
    :return: None
    """
    logging.info("Tamori Club - zaczyna się!")


# Uwaga: Strefa czasowa Docker Image to UTC! (Mówiłem ci dwa razy, bo to ważne)
@JobController.run("00 9 * * *")
def notice_baseball():
    """
    Czas na kopaninkę
    :return: None
    """
    logging.info("Och, czas na kopaninkę!")
    
@JobController.run("40 20 * * *")
def notice_noc():
    """
    Czas na sen
    :return: None
    """
    logging.info("Zmiataj do łóżka!")
    


def main():
    """
    metoda uruchomienia crontab
    :return: None
    """
    # Ustawienia dziennika (poziom informacji, format, znacznik czasu)
    logging.basicConfig(
        level=logging.INFO,
        format="time:%(asctime)s.%(msecs)03d\tprocess:%(process)d" + "\tmessage:%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # zarejestruj zadanie, które chcesz wykonać za pomocą crontab
    jobs = [notice_tmr_club, notice_baseball, notice_noc]

    # multi process running
    p = Pool(len(jobs))
    try:
        for job in jobs:
            p.apply_async(job)
        p.close()
        p.join()
    except KeyboardInterrupt:
        logging.info("exit")


if __name__ == '__main__':
    main()
