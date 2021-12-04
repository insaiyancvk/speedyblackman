from torchvision import transforms
# from torchvision.models.resnet import resnet18
import torch.nn as nn
import numpy as np
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
                        transforms.Normalize((0.485, 0.456, 0.406),(0.229, 0.224, 0.225))
                        ])

# resnetTurn = resnet18(pretrained=False)
# resnetTurn.fc = nn.Linear(resnetTurn.fc.in_features, len(turns))
# resnetTurn.load_state_dict(torch.load('data\set2\SpeedyNet18.pth', map_location=torch.device('cpu')))
# resnetTurn.eval()

class AlexNet(nn.Module):
    def __init__(self, num_classes: int = 3, dropout: float = 0.5) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(64, 192, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )
        self.avgpool = nn.AdaptiveAvgPool2d((6, 6))
        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

modelturn = AlexNet()

# modelturn = torch.hub.load('pytorch/vision:v0.10.0', 'mobilenet_v2', pretrained=False, verbose=False)
modelturn.classifier = nn.Sequential(
    nn.Dropout(p=0.2, inplace=False),
    nn.Linear(in_features=1280, out_features = 3)
)
modelturn.load_state_dict(torch.load('data\set2\AlexNetTurnCroppedimgs.pth', map_location=torch.device('cpu')))
modelturn.eval()

def drive():
    global a,d
    iniTurn = [0,0,0]
    ms = mss()
    sc = ms.grab({'left': 0, 'top': 300, 'width': 1920, 'height': 300})
    
    img = transform(Image.frombytes("RGB", sc.size, sc.bgra, 'raw', 'BGRX'))
    img = img.unsqueeze(0)
    
    turnPreds = nn.functional.softmax(modelturn(img)[0], dim=0)
    turnPreds = turnPreds.detach().numpy()
    
    # print(f"Left:{turnPreds[0]:.2f}\tRight:{turnPreds[1]:.2f}")
    iniTurn[np.argmax(turnPreds)] = 1
    print(' '.join(str(x) for x in iniTurn))

    # if turnPreds[0]>0.5:
    #     if d:
    #         keyboard.release('d')
    #         d = False
    #     keyboard.press("a")
    #     a = True

    # elif turnPreds[2]>0.5:
    #     if a:
    #         keyboard.release('a')
    #         a = False
    #     keyboard.press("d")
    #     d = True
    
    # elif turnPreds[1]>0.5:
    #     if a:
    #         keyboard.release('a')
    #         a = False
    #     elif d:
    #         keyboard.release('d')
    #         d = False

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