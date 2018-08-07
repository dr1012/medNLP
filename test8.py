import os

myfile = open('uploads/pirate.txt')
os.remove('uploads/pirate.txt')

print('done')