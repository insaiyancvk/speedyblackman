# TODO: Cut down train test split to 50:50
# Process: move 37.5% of train data from both classes to test data
import shutil, os
from math import floor

SPLIT_FOLDERS = {
    'TRAIN': os.path.join("data","set2","train"),
    'center': os.path.join("data","set2","center"),
    'TRAIN_center': os.path.join("data","set2","train","center"),
    'TEST': os.path.join("data","set2","test"),
    'TEST_center': os.path.join("data","set2","test","center"),
}

for key in SPLIT_FOLDERS:
  if not os.path.isdir(SPLIT_FOLDERS[key]):
    os.mkdir(SPLIT_FOLDERS[key])
    print(f"{SPLIT_FOLDERS[key]} created")

center = os.listdir(SPLIT_FOLDERS['center'])
# s = os.listdir(SPLIT_FOLDERS['s'])

dalen = len(center)

for path in center[floor(0.8*dalen):]:
  print(f"Moving {SPLIT_FOLDERS['center']}/{path}")
  shutil.move(f"{SPLIT_FOLDERS['center']}/{path}",SPLIT_FOLDERS['TRAIN_center'])
c = os.listdir(SPLIT_FOLDERS['center'])
for path in c:
  print(f"Moving {SPLIT_FOLDERS['center']}/{path}")
  shutil.move(f"{SPLIT_FOLDERS['center']}/{path}",SPLIT_FOLDERS['TEST_center'])

# for path in s[floor(0.8*dalen):]:
#   print(f"Moving {SPLIT_FOLDERS['s']}/{path}")
#   shutil.move(f"{SPLIT_FOLDERS['s']}/{path}",SPLIT_FOLDERS['TRAIN_s'])
# s = os.listdir(SPLIT_FOLDERS['s'])
# for path in s:
#   print(f"Moving {SPLIT_FOLDERS['s']}/{path}")
#   shutil.move(f"{SPLIT_FOLDERS['s']}/{path}",SPLIT_FOLDERS['TEST_s'])