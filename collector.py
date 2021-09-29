# For collecting the data
import uuid, os, threading
from mss import mss
from PIL import Image
from hook import Hook, KeyboardEvent


'''           !!!!!!!!!!!  IMPORTANT  !!!!!!!!!!!!
              PLAY THE GAME IN FIRST PERSON PERSPECTIVE WITH BONET VISIBLE      '''

class capture_all():

    def __init__(self):

        self.set1_dirs()
        # self.set2_dirs()
        # self.set3_dirs()

    def set1_dirs(self):
        ''' Checks the directories of set1 '''

        print("checking for set1, w, s and space directories")
        
        if not (os.path.isdir("./set1") and os.path.isdir("./set1/w") and os.path.isdir("./set1/s") and os.path.isdir("./set1/space")):
            
            try:
                os.mkdir("./set1")
                print("set1 directory not found, creating one")
            except: pass

            try:
                os.mkdir("./set1/w")
                print("w directory not found, creating one")
            except: pass

            try:
                os.mkdir("./set1/s")
                print("s directory not found, creating one")
            except: pass

            try:
                os.mkdir("./set1/space")
                print("space directory not found, creating one")
            except: pass
    
    def set2_dirs(self):
        ''' Checks the directories of Set2 '''

        print("checking for set2, a and d directories")
        
        if not (os.path.isdir("./set2") and os.path.isdir("./set2/a") and os.path.isdir("./set2/d")):
            
            try:
                os.mkdir("./set2")
                print("set2 directory not found, creating one")
            except: pass

            try:
                os.mkdir("./set2/a")
                print("a directory not found, creating one")
            except: pass

            try:
                os.mkdir("./set2/d")
                print("d directory not found, creating one")
            except: pass

    def set3_dirs(self):
        ''' Checks the directories of Set3 '''

        print("checking for set3, N20 and No20 directories")
        
        if not (os.path.isdir("./set3") and os.path.isdir("./set3/N20") and os.path.isdir("./set3/No20")):
            
            try:
                os.mkdir("./set3")
                print("set3 directory not found, creating one")
            except: pass

            try:
                os.mkdir("./set3/N20")
                print("N20 directory not found, creating one")
            except: pass

            try:
                os.mkdir("./set3/No20")
                print("No20 directory not found, creating one")
            except: pass

    def set1_events(self, args):
        ''' Function that takes care of capturing the frames when acceleration or front/rear break is used '''
        
        if isinstance(args, KeyboardEvent):
            
            if 'Up' in args.pressed_key:
                # pyscreenshot.grab(bbox=(0, 155, 1920, 1080)).save(f"./set1/w/{uuid.uuid1().hex}.png")
                ms = mss()
                ms.compression_level = 9
                sc = ms.grab({'left': 0, 'top': 155, 'width': 1920, 'height': 1080})
                Image.frombytes("RGB", sc.size, sc.bgra, 'raw', 'BGRX').save(f"./set1/w/{uuid.uuid1().hex}.jpg","JPEG")

                print(f"Saved to set1/w/")
            
            elif 'Down' in args.pressed_key:
                # pyscreenshot.grab(bbox=(0, 155, 1920, 1080)).save(f"./set1/s/{uuid.uuid1().hex}.png")
                ms = mss()
                ms.compression_level = 9
                sc = ms.grab({'left': 0, 'top': 155, 'width': 1920, 'height': 1080})
                Image.frombytes("RGB", sc.size, sc.bgra, 'raw', 'BGRX').save(f"./set1/s/{uuid.uuid1().hex}.jpg","JPEG")
                
                print(f"Saved to set1/s/")

            elif 'Space' in args.pressed_key:
                # pyscreenshot.grab(bbox=(0, 155, 1920, 1080)).save(f"./set1/space/{uuid.uuid1().hex}.png")
                ms = mss()
                ms.compression_level = 9
                sc = ms.grab({'left': 0, 'top': 155, 'width': 1920, 'height': 1080})
                Image.frombytes("RGB", sc.size, sc.bgra, 'raw', 'BGRX').save(f"./set1/space/{uuid.uuid1().hex}.jpg","JPEG")

                print("Saved to set1/space")

    def set2_events(self, args):
        ''' Function that takes care of capturing the frames for left or right turns '''
        
        if isinstance(args, KeyboardEvent):
            
            if 'Left' in args.pressed_key:
                # pyscreenshot.grab(bbox=(0, 155, 1920, 1080)).save(f"./set2/a/{uuid.uuid1().hex}.png")
                ms = mss()
                ms.compression_level = 9
                sc = ms.grab({'left': 0, 'top': 155, 'width': 1920, 'height': 1080})
                Image.frombytes("RGB", sc.size, sc.bgra, 'raw', 'BGRX').save(f"./set2/a/{uuid.uuid1().hex}.jpg","JPEG")
                print(f"Saved to set2/a/")
            
            elif 'Right' in args.pressed_key:
                # pyscreenshot.grab(bbox=(0, 155, 1920, 1080)).save(f"./set2/d/{uuid.uuid1().hex}.png")
                ms = mss()
                ms.compression_level = 9
                sc = ms.grab({'left': 0, 'top': 155, 'width': 1920, 'height': 1080})
                Image.frombytes("RGB", sc.size, sc.bgra, 'raw', 'BGRX').save(f"./set2/d/{uuid.uuid1().hex}.jpg","JPEG")
                print(f"Saved to set2/d/")

    def set3_events(self, args):
        ''' Function that takes care of capturing the frames when nitro is used '''
        
        if isinstance(args, KeyboardEvent):
            
            if 'F' in args.pressed_key:
                # pyscreenshot.grab(bbox=( 1434, 662, 1920, 1080)).save(f"./set3/N20/{uuid.uuid1().hex}.png")
                ms = mss()
                ms.compression_level = 9
                sc = ms.grab({'left': 1434, 'top': 662, 'width': 1920, 'height': 1080})
                Image.frombytes("RGB", sc.size, sc.bgra, 'raw', 'BGRX').save(f"./set3/N20/{uuid.uuid1().hex}.jpg","JPEG")
                print(f"Saved to set3/N20/")

    def start_threads(self):

        hk1 = Hook()
        hk1.handler = self.set1_events
        thread1 = threading.Thread(target=hk1.hook)
        thread1.start()


if __name__ == '__main__':

    print("Checking for \"data\" directory")

    try:
        os.chdir("./data/")
        print("\"data\" directory found")
    except:
        print("\"data\" directory not found, creating one")
        os.mkdir("./data/")
        os.chdir("./data")

    starter = capture_all()
    starter.start_threads()


'''
the road cords:
x1,y1,x2,y2 ==> (0, 155, 1920, 1080)

nitro cords:
(1434, 662, 1920, 1080)
'''