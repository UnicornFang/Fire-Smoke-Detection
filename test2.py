import winsound
from threading import Thread
from concurrent import futures
import threading  # python3的threading函数
import time
from concurrent.futures import ThreadPoolExecutor

r = True;


def play_sound():
    # winsound.PlaySound("dank", winsound.SND_ALIAS)
    # winsound.PlaySound(r"dank")
    global r
    if r:
        r = False
        winsound.PlaySound("dank", winsound.SND_ALIAS)
        r = True


def job1():
    print('执行1')


def job2():
    print('执行2')


def job3():
    print('执行3')


if __name__ == '__main__':
    # for i in range(5):
    #     thread = Thread(target=play_sound)
    #     thread.start()

    pool = ThreadPoolExecutor(max_workers=3)  # 线程池大小为3
    future1 = pool.submit(play_sound)
    future2 = pool.submit(play_sound)  # 将任务加到线程池里


    pool.shutdown()  # 关闭线程池
