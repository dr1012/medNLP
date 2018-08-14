import os
from shutil import copyfile

apath = r'C:\Users\David\Desktop\meddoc\text_files2'
all_files = []
for filename in os.listdir(apath):
    path = os.path.join(apath, filename)

    for x in os.listdir(path):
        all_files.append(x)

for a in all_files:
    count = 0
    for filename in os.listdir(apath):
        path = os.path.join(apath, filename)

        for x in os.listdir(path):
            if a == x:
                count = count + 1
            if count > 1:
                remove_path = os.path.join(path,x)
                print(x)
                os.remove(remove_path)
                count = count - 1

mycount = 0
for filename in os.listdir(apath):
    path = os.path.join(apath, filename)

    for x in os.listdir(path):
        mycount = mycount + 1

print(mycount)