# TODO: Implement SpeedyNet
''' 
Steps: 
    1. Import stuff
    2. Take a screenshot for 'left': 0, 'top': 155, 'width': 1920, 'height': 1080
    3. Pass the screenshot to the model
    4. Hold down acceleration and release for 2 secs after every 5 secs
    5. Left/Right drive only if the value is >0.65
'''
# Try mobilenet inceptionv2 SSD300 faster YOLO SSD mobile netv2, v1  tiny yolo 416
from torchvision import transforms
from torchvision.models.resnet import resnet18
import torch.nn as nn
import torch, time, warnings, keyboard, time
warnings.filterwarnings("ignore")
from PIL import Image
from mss import mss

w = False
s = False
a = False
d = False

turns = ['a','d']
acc = ['w','s']

resnetTurn = resnet18(pretrained=False)
resnetTurn.fc = nn.Linear(resnetTurn.fc.in_features, len(turns))
resnetTurn.load_state_dict(torch.load('data\set2\SpeedyNet18.pth', map_location=torch.device('cpu')))

resnetAcc = resnet18(pretrained=False)
resnetAcc.fc = nn.Linear(resnetAcc.fc.in_features, len(acc))
resnetAcc.load_state_dict(torch.load('data\set1\SpeedyNet18acc.pth', map_location=torch.device('cpu')))

transform = transforms.Compose([
                        transforms.Resize([128,128]),
                        transforms.ToTensor(),
                        transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
                        ])

def drive():
    global w,a,s,d
    start = time.time()
    ms = mss()
    sc = ms.grab({'left': 0, 'top': 155, 'width': 1920, 'height': 1080})
    
    img = transform(Image.frombytes("RGB", sc.size, sc.bgra, 'raw', 'BGRX'))
    img = img.unsqueeze(0)
    
    turnPreds = nn.functional.softmax(resnetTurn(img)[0], dim=0)
    turnPreds = turnPreds.detach().numpy()
    
    accPreds = nn.functional.softmax(resnetAcc(img)[0], dim=0)
    accPreds = accPreds.detach().numpy()
    print(f"{time.time()-start}")
    # exit()
    print(f"Left:{turnPreds[0]:.2f}\tRight:{turnPreds[1]:.2f}\tAcceleration:{accPreds[0]:.2f}\tBrake{accPreds[1]:.2f}")

    if turnPreds[0]>0.5 and accPreds[0]>0.5:
        if s:
            keyboard.release("s")
            s = False
        elif d:
            keyboard.release("d")
            d = False
        keyboard.press("a")
        keyboard.press("w")
        a, w = True, True

    elif turnPreds[0]>0.5 and accPreds[1]>0.5:
        if w:
            keyboard.release("w")
            w = False
        elif d:
            keyboard.release("d")
            d = False
        keyboard.press("a")
        keyboard.press("s")
        a, s = True, True

    elif turnPreds[1]>0.5 and accPreds[0]>0.5:
        if a:
            keyboard.release("a")
            a = False
        elif s:
            keyboard.release("s")
            s = False
        keyboard.press("d")
        keyboard.press("w")
        w, d = True, True

    elif turnPreds[1]>0.5 and accPreds[1]>0.5:
        if w:
            keyboard.release("w")
            w = False
        elif a:
            keyboard.release("a")
            a = False
        keyboard.press("d")
        keyboard.press("s")
        s, d = True, True

if __name__ == "__main__":
    t = True
    
    while t:

        try:

            drive()            
        except KeyboardInterrupt:

            print("Pausing the code")
            t = input("Paused")
            if t == "q":
                t == False
            else:
                continue