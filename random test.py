'''import threading, time
from msvcrt import getch

key = "lol"
key2 = "olo"

def thread1():
    global key
    lock = threading.Lock()
    while True:
        with lock:
            key = getch()
            time.sleep(0.1)
            key = '00'
def thread2():
    global key2
    lock = threading.Lock()
    while True:
        with lock:
            key2 = getch()
            time.sleep(0.1)
            key2 = '00'

threading.Thread(target = thread1).start()

while True:
    time.sleep(.1)
    # print(key, type(key), str(key))
    if key=='w':
        print("speed boii")'''





'''import threading
import time
from msvcrt import getch

key = 'lol'
class Job(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event() # The flag used to pause the thread
        self.__flag.set() # Set to True
        self.__running = threading.Event() # Used to stop the thread identification
        self.__running.set() # Set running to True

    def run(self):
        global key
        while self.__running.isSet():
            key = getch().decode('ASCII')
            self.__flag.wait() # return immediately when it is True, block until the internal flag is True when it is False
            # print(time.time())
            time.sleep(.1)
            key = 'lol'

    def pause(self):
        self.__flag.clear() # Set to False to block the thread

    def resume(self):
        self.__flag.set() # Set to True, let the thread stop blocking

    def stop(self):
        self.__flag.set() # Resume the thread from the suspended state, if it is already suspended
        self.__running.clear() # Set to False

a = Job()
a.start()
l = []
start = time.time()

while True:
    print(key)
    time.sleep(.1)

    if key == 'w' or key == 'W':
        print("(W)")
        l.append("w")
        time.sleep(.1)
    
    elif key == 's' or key == 'S':
        print("(S)")
        l.append("S")

    elif key == 'a' or key == 'A':
        l.append("A")
        print("(A)")
    
    elif key == 'd' or key == 'D':
        l.append("D")
        print("(D)")
    
    elif key == 'p' or key == 'P':
        print("Pausing the captures")
        print(l)
        a.pause()
        key = getch().decode('ASCII')

    elif key == 'o' or key == 'O':
        print("Resuming the captures")
        a.resume()
        key = 'lol'

    elif key == 'q' or key == 'Q':
        print("Quitting the captures")
        a.stop()
        break'''


from hook import Hook

def handle_events(args):
    
    if chr(args.key_code) == "W" or chr(args.key_code) == "w":
        print("accelerate")
    elif chr(args.key_code) == "s" or chr(args.key_code) == "S":
        print("front break")
    elif args.key_code == 32:
        print("rear break")


hk = Hook()
hk.handler = handle_events
hk.hook()