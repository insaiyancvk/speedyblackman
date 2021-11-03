from torchvision import transforms
from torchvision.models.resnet import resnet18
import torch.nn as nn
import torch, time, warnings, keyboard, time
warnings.filterwarnings("ignore")
from PIL import Image
from mss import mss

turns = ['a','d']
a = False
d = False

transform = transforms.Compose([
                        transforms.Resize([256,256]),
                        transforms.ToTensor(),
                        transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
                        ])

resnetTurn = resnet18(pretrained=False)
resnetTurn.fc = nn.Linear(resnetTurn.fc.in_features, len(turns))
resnetTurn.load_state_dict(torch.load('data\set2\SpeedyNet18.pth', map_location=torch.device('cpu')))

def drive():
    global a,d
    ms = mss()
    sc = ms.grab({'left': 0, 'top': 155, 'width': 1920, 'height': 1080})
    
    img = transform(Image.frombytes("RGB", sc.size, sc.bgra, 'raw', 'BGRX'))
    img = img.unsqueeze(0)
    
    turnPreds = nn.functional.softmax(resnetTurn(img)[0], dim=0)
    turnPreds = turnPreds.detach().numpy()
    
    print(f"Left:{turnPreds[0]:.2f}\tRight:{turnPreds[1]:.2f}")

    if turnPreds[0]>0.5:
        if d:
            keyboard.release('d')
            d = False
        keyboard.press("a")
        a = True

    elif turnPreds[1]>0.5:
        if a:
            keyboard.release('a')
            a = False
        keyboard.press("d")
        d = True

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