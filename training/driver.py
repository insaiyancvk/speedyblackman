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
# from torchvision.models.resnet import resnet18
import torch.nn as nn
import torch, time, warnings, keyboard, time
import numpy as np
warnings.filterwarnings("ignore")
from PIL import Image
from mss import mss

w = False
s = False
a = False
d = False

turns = ['a','center','d']
acc = ['w','s']

torch.hub._validate_not_a_forked_repo=lambda a,b,c: True

modelturn = torch.hub.load('pytorch/vision:v0.10.0', 'mobilenet_v2', pretrained=False, verbose=False)
modelturn.classifier = nn.Sequential(
    nn.Dropout(p=0.2, inplace=False),
    nn.Linear(in_features=1280, out_features = 3)
)
modelturn.load_state_dict(torch.load('data\set2\MobileNetV2turnsCroppedimgs.pth', map_location=torch.device('cpu')))
modelturn.eval()

# resnetTurn = resnet18(pretrained=False)
# resnetTurn.fc = nn.Linear(resnetTurn.fc.in_features, len(turns))
# resnetTurn.load_state_dict(torch.load('data\set2\SpeedyNet18.pth', map_location=torch.device('cpu')))

modelacc = torch.hub.load('pytorch/vision:v0.10.0', 'mobilenet_v2', pretrained=False, verbose=False)
modelacc.classifier = nn.Sequential(
    nn.Dropout(p=0.2, inplace=False),
    nn.Linear(in_features=1280, out_features = 2)
)
modelacc.load_state_dict(torch.load('data\set1\MobileNetV2acc.pth', map_location=torch.device('cpu')))
modelacc.eval()

# resnetAcc = resnet18(pretrained=False)
# resnetAcc.fc = nn.Linear(resnetAcc.fc.in_features, len(acc))
# resnetAcc.load_state_dict(torch.load('data\set1\SpeedyNet18acc.pth', map_location=torch.device('cpu')))

transform = transforms.Compose([
                        transforms.Resize([256,256]),
                        transforms.ToTensor(),
                        transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
                        ])

def drive():
    global w,a,s,d
    # start = time.time()
    iniTurn = [0,0,0]
    iniAcc = [0,0]
    ms = mss()
    sc = ms.grab({'left': 0, 'top': 155, 'width': 1920, 'height': 500})
    
    img = transform(Image.frombytes("RGB", sc.size, sc.bgra, 'raw', 'BGRX'))
    img = img.unsqueeze(0)
    
    turnPreds = nn.functional.softmax(modelturn(img)[0], dim=0)
    turnPreds = turnPreds.detach().numpy()
    
    accPreds = nn.functional.softmax(modelacc(img)[0], dim=0)
    accPreds = accPreds.detach().numpy()
    # print(f"{time.time()-start}")
    # exit()
    # print(f"Left:{turnPreds[0]:.2f}\tRight:{turnPreds[1]:.2f}\tAcceleration:{accPreds[0]:.2f}\tBrake{accPreds[1]:.2f}")
    # print(sum(accPreds),'\t',sum(turnPreds))
    # iniTurn[turnPreds.index(max(turnPreds))] = 1
    iniTurn[np.argmax(turnPreds)] = 1
    # iniAcc[accPreds.index(max(accPreds))] = 1
    iniAcc[np.argmax(accPreds)] = 1
    print(' '.join(str(x) for x in iniTurn),'\t\t',' '.join(str(x) for x in iniAcc))

    if turnPreds[0]>0.5 and accPreds[0]>0.5:
        print("LEFT \t\t BRAKE")
        if w:
            keyboard.release("w")
            w = False
        elif d:
            keyboard.release("d")
            d = False
        keyboard.press("a")
        keyboard.press("s")
        a, s = True, True
        # time.sleep(1)

    elif turnPreds[0]>0.5 and accPreds[1]>0.5:
        print("LEFT \t\t ACCELERATE")
        if s:
            keyboard.release("s")
            s = False
        elif d:
            keyboard.release("d")
            d = False
        keyboard.press("a")
        keyboard.press("w")
        a, w = True, True
        # time.sleep(1)

    elif turnPreds[2]>0.5 and accPreds[0]>0.5:
        print("RIGHT \t\t BRAKE")
        if a:
            keyboard.release("a")
            a = False
        elif w:
            keyboard.release("w")
            w = False
        keyboard.press("d")
        keyboard.press("s")
        s, d = True, True
        # time.sleep(1)

    elif turnPreds[2]>0.5 and accPreds[1]>0.5:
        print("RIGHT \t\t ACCELERATE")
        if s:
            keyboard.release("s")
            s = False
        elif a:
            keyboard.release("a")
            a = False
        keyboard.press("d")
        keyboard.press("w")
        w, d = True, True
        # time.sleep(1)

    elif turnPreds[1]>0.5 and accPreds[0]>0.5:
        print("CENTER \t\t BRAKE")
        keyboard.release("a")
        keyboard.release("d")
        if w:
            keyboard.release("w")
            w = False
        keyboard.press("s")
        s = True

    elif turnPreds[1]>0.5 and accPreds[1]>0.5:
        print("CENTER \t\t ACCELERATE")
        keyboard.release("a")
        keyboard.release("d")
        a,d = False, False
        if s:
            keyboard.release("s")
            s = False
        keyboard.press("w")
        w = True


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