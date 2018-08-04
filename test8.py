import os


path = 'uploads'
for i in os.listdir(path):
    if os.path.isfile(os.path.join(path,i)) and 'test' in i:
        print(i)