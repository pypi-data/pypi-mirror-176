#!python3
#pylint: disable=C0116

"""
This tool can be used to book times into JIRA issues.
This tool uses the internal rest api (v3) of JIRA and
therefore can be subject to change.

Use it on your own risk!
"""

import base64
import datetime
import os
import re
import sys
import time

import requests

from jira_timesheet_cli.arguments import ArgumentError, FileArgumentParser

if not 'JIRA_URL' in os.environ:
    print('Environment variable JIRA_URL must be set')
    sys.exit(1)

if not 'JIRA_USER' in os.environ:
    print('Environment variable JIRA_USER must be set')
    sys.exit(1)

if not 'JIRA_TOKEN' in os.environ:
    print('Environment variable JIRA_TOKEN must be set')
    sys.exit(1)

JIRA_USER = os.environ['JIRA_USER']
JIRA_TOKEN = os.environ['JIRA_TOKEN']
JIRA_URL = os.environ['JIRA_URL']

# Create an authentication object,using
# registered emailID, and, token received.
auth = f'{JIRA_USER}:{JIRA_TOKEN}'.encode('ascii')
auth = base64.b64encode(auth)
auth = auth.decode('ascii')
# The Header parameter, should mention, the
# desired format of data.
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Basic {auth}"
}


def _log_time(ticket: str, log_duration: str, log_at: datetime.datetime, dryrun: bool = False):
    log_at = log_at.strftime('%Y-%m-%dT%T.000')
    log_at += f'{"-" if time.timezone > 0 else "+"}'
    log_at += f'{abs(time.timezone) // 3600:0>2}{abs(time.timezone // 60) % 60:0>2}'

    url = f"{JIRA_URL.rstrip('/')}/rest/internal/3/issue/{ticket}/worklog"

    if dryrun:
        print(f"Dry-running to url {url}")
    else:
        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=f'{{\
                "timeSpent":"{log_duration}",\
                "comment":{{"type":"doc","version":1,"content":[]}},\
                "started":"{log_at}"\
            }}',
            timeout=5
        )
        if not 200 <= response.status_code <= 201:
            raise Exception(f'Unexpected status code: {response.status_code}')

    print(f"Booked {log_duration} at {log_at} on {ticket}")


duration_re = re.compile(r'^((?P<hour>\d+)h)?((?P<minute>\d{1,2})m)?$')

def main():
    dirname = os.path.dirname(__file__)

    if len(sys.argv) > 1 and sys.argv[1] == 'completion':
        with open(os.path.join(dirname, 'register-completion.txt'), 'r', encoding='utf-8') as f:
            print(f.read(), end="")
        sys.exit(0)

    options = FileArgumentParser('book-time.yaml', basepath=dirname).parse()

    duration = options.duration
    match = duration_re.match(duration)

    if not match:
        raise ArgumentError('duration')

    hour = match.group('hour')
    minute = match.group('minute')
    if not hour and not minute:
        raise ArgumentError("The duration is invalid")

    hour = hour if hour else 0
    minute = minute if minute else 0

    duration = f'{hour}h {minute}m'

    # date
    if options.today:
        date = datetime.date.today()
    elif options.yesterday:
        date = datetime.date.today() - datetime.timedelta(days=1)
    elif options.date:
        date = datetime.datetime.strptime(options.date, '%d-%m-%y').date()
    else:
        raise ArgumentError('One of -today, -yesterday or -date must be set')

    # time
    if options.now:
        t = datetime.datetime.now().time()
    elif options.at:
        t = datetime.datetime.strptime(options.at, '%H:%M').time()
    else:
        raise ArgumentError('One of -now or -at must be set')

    moment = datetime.datetime.combine(date, t)

    _log_time(ticket=options.ticket, log_duration=duration, log_at=moment, dryrun=options.dryrun)

if __name__ == '__main__':
    main()
