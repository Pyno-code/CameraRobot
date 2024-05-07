from statistics import mean
import time
import threading

def foo():
    pass


class Timer:


    def __init__(self, func_: callable, time_: float, default_function_=foo):
        self.start_time = 0
        self.func = func_
        self.time = time_
        self.default_function = default_function_


    def __call__(self, *args, **kwargs):
        res = None
        if time.time() - self.start_time > self.time:
            res = self.func(*args, **kwargs)
            self.start_time = time.time()
        else:
            res = self.default_function()
        return res



class TimeCounter:
    

    def __init__(self, func_: callable, mean_lenght = 60) -> None:
        self.func = func_
        self.list_time = [0]*mean_lenght

    def __call__(self, *args, **kwargs):
        start_time = time.time()
        res = self.func(*args, **kwargs)
        time_elapsed = time.time() - start_time

        self.list_time = [time_elapsed] + self.list_time.copy()[0:len(self.list_time)-1]        

        return res
    
    def get_mean(self) -> float:
        return mean(self.list_time)


class TimerThread:


    def __init__(self, func_: callable, time_: float):
        self.start_time = 0
        self.func = func_
        self.time = time_
        self.task = threading.Thread(target=self.func)


    def __call__(self):
        if time.time() - self.start_time > self.time and not self.task.is_alive():
            self.task = threading.Thread(target=self.func)
            self.task.start()
            self.start_time = time.time()
