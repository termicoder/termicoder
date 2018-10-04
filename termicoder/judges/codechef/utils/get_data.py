from datetime import datetime
from ....utils.logging import logger


def transpose_running_oauth(x):
    return {
        'code': x['code'],
        'endDate': datetime.strptime(x['endDate'], '%Y-%m-%d %H:%M:%S'),
        'startDate': datetime.strptime(x['endDate'], '%Y-%m-%d %H:%M:%S'),
        'name': x['name']
    }


def running_contests(self):
    path = 'contests'
    url = self._make_url(self.api_url, path)
    r = self._request_api(url)

    data = r['result']['data']['content']
    contest_list = map(transpose_running_oauth, data['contestList'])
    current_time = datetime.fromtimestamp(data['currentTime'])

    def check_current(contest):
        contest_time = contest['endDate']
        return contest_time >= current_time

    running = list(filter(check_current, contest_list))
    logger.debug("got running")

    return running
