from torchvision import transforms
import torch.nn as nn
import numpy as np
import torch, warnings, keyboard
warnings.filterwarnings("ignore")
from mss import mss
import cv2

a, d, w, s = False, False, False, False

transform = transforms.Compose([
                        transforms.ToTensor(),                    
                        transforms.Resize([256,256]),
                        transforms.Normalize((0.485, 0.456, 0.406),(0.229, 0.224, 0.225))
                        ])

# Turns model
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
print(modelturn.load_state_dict(torch.load('data\set2\AlexNetTurn.pth', map_location=torch.device('cpu'))))
modelturn.eval()

# Acceleration model
torch.hub._validate_not_a_forked_repo=lambda a,b,c: True
modelacc = torch.hub.load('pytorch/vision:v0.10.0', 'mobilenet_v2', pretrained=False, verbose=False)
modelacc.classifier = nn.Sequential(
    nn.Dropout(p=0.2, inplace=False),
    nn.Linear(in_features=1280, out_features = 2)
)
modelacc.load_state_dict(torch.load('data\set1\MobileNetV2acc.pth', map_location=torch.device('cpu')))
modelacc.eval()


def screen_record(top = 300, left = 0, width = 1920, height = 300):
  
    mon = {"top": top, "left": left, "width": width, "height": height}
    sct = mss()
    img = np.array(sct.grab(mon))
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    sct.close()
    return img


def center_arrow(np_img): # highlight center arrow
    
    np_img = cv2.arrowedLine(np_img, (130, 112), (60, 112), color = (225, 225, 255), thickness= 5, tipLength=.35)
    np_img = cv2.arrowedLine( np_img, (130, 112), (130, 42), color = (0, 0, 255), thickness= 5, tipLength=.35)
    np_img = cv2.arrowedLine( np_img, (130, 112), (205, 112), color = (225, 225, 255), thickness= 5, tipLength=.35)

    return np_img

def left_arrow(np_img): # highlight left arrow
    
    np_img = cv2.arrowedLine(np_img, (130, 112), (60, 112), color = (0, 0, 255), thickness= 5, tipLength=.35)
    np_img = cv2.arrowedLine(np_img, (900, 90), (900, 40), color = (225, 225, 255), thickness= 5, tipLength=.35)
    np_img = cv2.arrowedLine(np_img, (130, 112), (60, 112), color = (225, 225, 255), thickness= 5, tipLength=.35)
    
    return np_img

def right_arrow(np_img): # highlight right arrow
    
    np_img = cv2.arrowedLine(np_img, (130, 112), (60, 112), color = (225, 225, 255), thickness= 5, tipLength=.35)
    np_img = cv2.arrowedLine(np_img, (130, 112), (130, 42), color = (225, 225, 255), thickness= 5, tipLength=.35)
    np_img = cv2.arrowedLine(np_img, (130, 112), (205, 112), color = (0, 0, 255), thickness= 5, tipLength=.35)
    
    return np_img

def acc_arrow(np_img): # highlight acceleration arrow
    
    np_img = cv2.arrowedLine(np_img, (900, 90), (900, 40), color = (0, 0, 255), thickness= 5, tipLength=.35)
    np_img = cv2.arrowedLine(np_img, (900, 90), (900, 140), color = (225, 225, 255), thickness= 5, tipLength=.35)
    
    return np_img

def brake_arrow(np_img): # highlight brake arrow
    
    np_img = cv2.arrowedLine(np_img, (900, 90), (900, 40), color = (225, 225, 255), thickness= 5, tipLength=.35)
    np_img = cv2.arrowedLine(np_img, (900, 90), (900, 140), color = (0, 0, 255), thickness= 5, tipLength=.35)
    
    return np_img

def draw_arrows(np_img):
    
    np_img = cv2.arrowedLine(np_img, (900, 90), (900, 40), color = (225, 225, 255), thickness= 5, tipLength=.35)
    np_img = cv2.arrowedLine(np_img, (900, 90), (900, 140),color = (225, 225, 255), thickness= 5, tipLength=.35)
    np_img = cv2.arrowedLine(np_img, (130, 112), (60, 112),color = (225, 225, 255), thickness= 5, tipLength=.35)
    np_img = cv2.arrowedLine(np_img, (130, 112), (130, 42),color = (225, 225, 255), thickness= 5, tipLength=.35)
    np_img = cv2.arrowedLine(np_img, (130, 112), (205, 112),color = (225, 225, 255), thickness= 5, tipLength=.35)
    return np_img


def flex(np_img, turnPreds, accPreds, window_name = "speedyblackman"):

    global a,d,w,s
    
    np_img = cv2.cvtColor(np_img, cv2.COLOR_BGR2RGB)
    np_img = cv2.resize(np_img, (np_img.shape[1]//2,np_img.shape[0]//2), interpolation = cv2.INTER_AREA)
    np_img = draw_arrows(np_img)
    
    if turnPreds[0]>0.75 and accPreds[1]>0.75: # Left and Acc
        if d:
            keyboard.release('d')
            d = False
        if s:
            keyboard.release('s')
            s = False
        
        keyboard.press("a")
        a = True
        keyboard.press("w")
        w = True
        
        np_img = left_arrow(np_img)
        np_img = acc_arrow(np_img)
    
    elif turnPreds[1]>0.5 and accPreds[1]>0.75: # Center and Acc
        if a:
            keyboard.release('a')
            a = False
        if d:
            keyboard.release('d')
            d = False
        if s:
            keyboard.release('s')
            s = False
        
        keyboard.press("w")
        w = True
        
        np_img = center_arrow(np_img)
        np_img = acc_arrow(np_img)
        
    elif turnPreds[2]>0.75 and accPreds[1]>0.75: # Right and Acc
        if a:
            keyboard.release('a')
            a = False
        if s:
            keyboard.release('s')
            s = False
        
        keyboard.press('w')
        w = True
        keyboard.press("d")
        d = True
        
        np_img = right_arrow(np_img)
        np_img = acc_arrow(np_img)
    
    elif turnPreds[0]>0.75 and accPreds[0]>0.75: # Left and Brake
        if d:
            keyboard.release('d')
            d = False
        if w:
            keyboard.release('w')
            w = False
        
        keyboard.press("a")
        a = True
        keyboard.press("s")
        s = True
        
        np_img = left_arrow(np_img)
        np_img = brake_arrow(np_img)
    
    elif turnPreds[1]>0.5 and accPreds[0]>0.75: # Center and Brake
        if a:
            keyboard.release('a')
            a = False
        if d:
            keyboard.release('d')
            d = False
        if w:
            keyboard.release('w')
            w = False
        
        keyboard.press("s")
        s = True
        
        np_img = center_arrow(np_img)
        np_img = brake_arrow(np_img)
        
    elif turnPreds[2]>0.75 and accPreds[0]>0.75: # Right and Brake
        if a:
            keyboard.release('a')
            a = False
        if w:
            keyboard.release('w')
            w = False
        
        keyboard.press('s')
        s = True
        keyboard.press("d")
        d = True
        
        np_img = right_arrow(np_img)
        np_img = brake_arrow(np_img)
    
    elif accPreds[0]<0.75:
        keyboard.release('s')
        s = False
    elif accPreds[1]<0.75:
        keyboard.release('w')
        w = False
    
    cv2.imshow(window_name, np_img)



if __name__ == "__main__":
    t = True
    
    while t:
        
        try:
            foo = screen_record()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            
            transformed_foo = transform(foo)
            transformed_foo = transformed_foo.unsqueeze(0)
            
            turnPreds = nn.functional.softmax(modelturn(transformed_foo)[0], dim=0)
            turnPreds = turnPreds.detach().numpy()
            
            accPreds = nn.functional.softmax(modelacc(transformed_foo)[0], dim=0)
            accPreds = accPreds.detach().numpy()
            
            flex(foo, turnPreds, accPreds,window_name='speedyblackmanCAM')

        except KeyboardInterrupt:

            print("Pausing the code")
            t = input("Paused")
            if t == "q":
                t == False
            else:
                continue