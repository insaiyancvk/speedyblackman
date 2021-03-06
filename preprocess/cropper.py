from PIL import Image
import os, json, telegram

def cropper(path):
  im = Image.open(path)
  im = im.crop((0,0,1920,920))
  im.save(path)
  del im

paths = {
    'center':[]
    }

paths['center'] += os.listdir('./data/set2/center')
# paths['d'] += os.listdir('./data/set1/w')

base_path_center = './data/set2/center/'
# base_path_d = './data/set1/w/'

class send(): 

  def __init__(self):
    f = open ('D:/Coding/tel.json', 'r')
    self.tel = json.load(f)
    f.close()
    self.bot = telegram.Bot(token=self.tel['token']) 

  def msg(self, mesg):
    self.bot.sendMessage(chat_id=self.tel['nnboiid'], text=mesg)

  def pic(self, path):
    self.bot.sendPhoto(chat_id=self.tel['nnboiid'], photo=open(path, 'rb'))

bot = send()

for value in paths['center']:
  print(f'cropping {value}')
  cropper(base_path_center+value)
bot.msg('Completed cropping in a')
# for value in paths['d']:
#   print(f'cropping {value}')
#   cropper(base_path_d+value)
bot.msg('Completed cropping in d')