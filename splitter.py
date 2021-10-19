import json, shutil, os

SPLIT_FOLDERS = {
    'TRAIN': os.path.join("data","set2","train"),
    'TRAIN_a': os.path.join("data","set2","train","a"),
    'TRAIN_d': os.path.join("data","set2","train","d"),
    'TEST': os.path.join("data","set2","test"),
    'TEST_a': os.path.join("data","set2","test","a"),
    'TEST_d': os.path.join("data","set2","test","d")
}

for key in SPLIT_FOLDERS:
  if not os.path.isdir(SPLIT_FOLDERS[key]):
    os.mkdir(SPLIT_FOLDERS[key])
    print(f"{SPLIT_FOLDERS[key]} created")

f = open ('data/set2/data.json', 'r')
load_data = json.load(f)
f.close()

try:
  print("Creating train split for 'a' class")
  for path in load_data['train_a']:
    shutil.move("data/"+path, SPLIT_FOLDERS['TRAIN_a'])
except:
  pass
try:  
  print("Creating train split for 'd' class")
  for path in load_data['train_d']:
    shutil.move("data/"+path, SPLIT_FOLDERS['TRAIN_d'])
except:
  pass
try:
  print("Creating test split for 'a' class")
  for path in load_data['test_a']:
    shutil.move("data/"+path, SPLIT_FOLDERS['TEST_a'])
except:
  pass
try:
  print("Creating test split for 'd' class")
  for path in load_data['test_d']:
    shutil.move("data/"+path, SPLIT_FOLDERS['TEST_d'])
except:
  pass
try:
  os.rmdir('set2/a')
except:
  pass
try:
  os.rmdir('set2/d')
except:
  pass