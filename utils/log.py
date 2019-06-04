import time

from utils import helpers as clock


def debug(message):
    log_message = 'Debug: {} - {}'.format(clock.date(time.time()), message)
    print(log_message)
    with open('./data/logs/debug.log', 'a') as log:
        log.write(log_message + '\n')

def error(message):
    log_message = 'Error: {}\n{}'.format(clock.date(time.time()), message)
    print(log_message)
    with open('./data/logs/error.log', 'a') as log:
        log.write(log_message + '\n')

def clearlogs():
    open('./data/logs/debug.log', 'w').close()
    open('./data/logs/error.log', 'w').close()