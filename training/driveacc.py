from torchvision import transforms
from torchvision.models.resnet import resnet18
import torch.nn as nn
import torch, time, warnings, keyboard, time
warnings.filterwarnings("ignore")
from PIL import Image
from mss import mss

acc = ['w','s']
w, s = False, False
transform = transforms.Compose([
                    transforms.Resize([256,256]),
                    transforms.ToTensor(),
                    transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
                    ])

# resnetAcc = resnet18(pretrained=False)
# resnetAcc.fc = nn.Linear(resnetAcc.fc.in_features, len(acc))
# resnetAcc.load_state_dict(torch.load('data\set1\SpeedyNet18acc.pth', map_location=torch.device('cpu')))

torch.hub._validate_not_a_forked_repo=lambda a,b,c: True
resnetAcc = torch.hub.load('pytorch/vision:v0.10.0', 'mobilenet_v2', pretrained=False, verbose=False)
resnetAcc.classifier = nn.Sequential(
    nn.Dropout(p=0.2, inplace=False),
    nn.Linear(in_features=1280, out_features = 2)
)
resnetAcc.load_state_dict(torch.load('data\set1\MobileNetV2acc_croppedimgs.pth', map_location=torch.device('cpu')))

def drive():
    global w, s
    ms = mss()
    sc = ms.grab({'left': 0, 'top': 155, 'width': 1920, 'height': 1080})
    
    img = transform(Image.frombytes("RGB", sc.size, sc.bgra, 'raw', 'BGRX'))
    img = img.unsqueeze(0)

    
    accPreds = nn.functional.softmax(resnetAcc(img)[0], dim=0)
    accPreds = accPreds.detach().numpy()

    print(f"Acceleration:{accPreds[0]:.2f}\tBrake{accPreds[1]:.2f}")

    if accPreds[0]>0.5:
        if s:
            keyboard.release('s')
            s = False
        keyboard.press("w")
        w = True

    elif accPreds[1]>0.5:
        if w:
            keyboard.release('w')
            w = False
        keyboard.press("s")
        s = True

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