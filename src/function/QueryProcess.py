import time
import datetime
import pygetwindow as gw

import psutil

# pids = psutil.pids()
# for pid in pids:
#     print("pid:{} name:{}".format(pid, pid.name))

LOL_PROCESS_NAME = "LeagueClient.exe"

IN_LOL_CHOOSE = "League of Legends"
IN_LOL_GAMING = "League of Legends (TM) Client"


class QueryProcess:
    # 如果在返回开始时间，否则返回空
    def IsPlayingLol_OLD(self):
        process_info = self._find_procs_by_name(LOL_PROCESS_NAME)
        print(process_info)
        if process_info:
            process = process_info[0]
            started_time = self._pprint_secs(process.create_time())
            if process.status() == "running":
                return str(started_time)

        return ""

    def _find_procs_by_name(self, name):
        "Return a list of processes matching 'name'."
        ls = []
        for p in psutil.process_iter(['name']):
            if p.info['name'] == name:
                ls.append(p)
            # print(p.info['name'])
        return ls

    def _pprint_secs(self, secs):
        """Format seconds in a human readable form."""
        now = time.time()
        secs_ago = int(now - secs)
        if secs_ago < 60 * 60 * 24:
            fmt = "%H:%M:%S"
        else:
            fmt = "%Y-%m-%d %H:%M:%S"
        return datetime.datetime.fromtimestamp(secs).strftime(fmt)

    def IsPlayingLol(self):
        active_windows_title = gw.getActiveWindow().title
        if active_windows_title == IN_LOL_GAMING:
            return True
        return False


if __name__ == '__main__':

    while True:
        try:
            print(gw.getActiveWindow().title == IN_LOL_GAMING)
        except Exception as e:
            print(e)
        time.sleep(3)

    # q = QueryProcess()
    # if q.IsPlayingLol():
    #     print(q.IsPlayingLol())
    # else:
    #     print("No")
# [psutil.Process(pid=3852, name='LeagueClientUxRender.exe', status='running', started='20:10:04'), psutil.Process(pid=4452, name='LeagueClientUxRender.exe', status='running', started='20:10:06'), psutil.Process(pid=7032, name='LeagueClientUxRender.exe', status='running', started='20:10:15'), psutil.Process(pid=19692, name='LeagueClientUxRender.exe', status='running', started='20:10:06'), psutil.Process(pid=20212, name='LeagueClientUx.exe', status='running', started='20:10:04'), psutil.Process(pid=23508, name='LeagueClientUxRender.exe', status='running', started='20:10:06'), psutil.Process(pid=25348, name='LeagueClient.exe', status='running', started='20:10:00'), psutil.Process(pid=25760, name='LeagueClientUxRender.exe', status='running', started='20:10:07')]
