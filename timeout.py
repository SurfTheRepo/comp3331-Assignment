import signal

class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass
 
    def __init__(self, sec):
        self.sec = sec
 
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.setitimer(signal.ITIMER_REAL, self.sec)
 
    def __exit__(self, *args):
        signal.setitimer(signal.ITIMER_REAL, 0)    # disable alarm
 
    def raise_timeout(self, *args):
        raise Timeout.Timeout()