# TODO: Implement SpeedyNet
''' 
Steps: 
    1. Import stuff
    2. Take a screenshot for 'left': 0, 'top': 155, 'width': 1920, 'height': 1080
    3. Pass the screenshot to the model
    4. Hold down acceleration and release for 2 secs after every 5 secs
    5. Left/Right turn only if the value is >0.65
'''

from torchvision import transforms
from torchvision.models.resnet import resnet18
import torch.nn as nn
import torch, time, warnings, keyboard, threading, time
warnings.filterwarnings("ignore")
from PIL import Image
from mss import mss

def turn():
    ms = mss()
    sc = ms.grab({'left': 0, 'top': 155, 'width': 1920, 'height': 1080})
    labels = ['a','d']
    resnet = resnet18(pretrained=False)
    resnet.fc = nn.Linear(resnet.fc.in_features, len(labels))
    resnet.load_state_dict(torch.load('data\set2\SpeedyNet18.pth', map_location=torch.device('cpu')))
    transform = transforms.Compose([
                        transforms.Resize([256,256]),
                        transforms.ToTensor(),
                        transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
                        ])
    img = transform(Image.frombytes("RGB", sc.size, sc.bgra, 'raw', 'BGRX'))
    img = img.unsqueeze(0)
    preds = nn.functional.softmax(resnet(img)[0], dim=0)
    print(preds.detach().numpy()[0],"\t",preds.detach().numpy()[1])
    if preds.detach().numpy()[0]>0.5:
        keyboard.press("a")
        time.sleep(.2)
        keyboard.release("a")
    elif preds.detach().numpy()[1]>0.5:
        keyboard.press("d")
        time.sleep(.2)
        keyboard.release("d")

def acc():
    keyboard.press("w")
    time.sleep(5)
    keyboard.release("w")
    keyboard.press("s")
    time.sleep(2)
    keyboard.release("s")


if __name__ == "__main__":
    t = True
    
    # t = time.time()
    # flag = False
    # keyboard.press("w")
    while t:
        keyboard.press("w")
        try:
            # t1 = threading.Thread(target=turn)
            # t2 = threading.Thread(target=acc)
            # t1.start()
            # t2.start()
            turn()
            # keyboard.release("w")
            # keyboard.press("s")
            # time.sleep(.01)
            # keyboard.release("s")
        except KeyboardInterrupt:
            print("Pausing the code")
            t = input("Paused")
            if t == "q":
                t == False
            else:
                continue