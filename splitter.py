# TODO: Cut down train test split to 50:50
# Process: move 37.5% of train data from both classes to test data
import shutil, os
from math import floor

SPLIT_FOLDERS = {
    'TRAIN': os.path.join("data","set1","train"),
    'Extra_w': os.path.join("data","set1","extra_w"),
    'TRAIN_w': os.path.join("data","set1","train","w"),
    'TRAIN_s': os.path.join("data","set1","train","s"),
    'TEST': os.path.join("data","set1","test"),
    'TEST_w': os.path.join("data","set1","test","w"),
    'TEST_s': os.path.join("data","set1","test","s"),
    'w': os.path.join("data","set1","w"),
    's': os.path.join("data","set1","s")
}

for key in SPLIT_FOLDERS:
  if not os.path.isdir(SPLIT_FOLDERS[key]):
    os.mkdir(SPLIT_FOLDERS[key])
    print(f"{SPLIT_FOLDERS[key]} created")

w = os.listdir(SPLIT_FOLDERS['w'])
s = os.listdir(SPLIT_FOLDERS['s'])

dalen = len(w)

for path in w[floor(0.8*dalen):]:
  print(f"Moving {SPLIT_FOLDERS['w']}/{path}")
  shutil.move(f"{SPLIT_FOLDERS['w']}/{path}",SPLIT_FOLDERS['TRAIN_w'])
w = os.listdir(SPLIT_FOLDERS['w'])
for path in w:
  print(f"Moving {SPLIT_FOLDERS['w']}/{path}")
  shutil.move(f"{SPLIT_FOLDERS['w']}/{path}",SPLIT_FOLDERS['TEST_w'])

for path in s[floor(0.8*dalen):]:
  print(f"Moving {SPLIT_FOLDERS['s']}/{path}")
  shutil.move(f"{SPLIT_FOLDERS['s']}/{path}",SPLIT_FOLDERS['TRAIN_s'])
s = os.listdir(SPLIT_FOLDERS['s'])
for path in s:
  print(f"Moving {SPLIT_FOLDERS['s']}/{path}")
  shutil.move(f"{SPLIT_FOLDERS['s']}/{path}",SPLIT_FOLDERS['TEST_s'])