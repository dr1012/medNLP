import os
from shutil import copyfile
from tqdm import tqdm
rootdir = 'C:/Users/David/Desktop/meddoc/text_files2'
newdir = 'C:/Users/David/Desktop/meddoc/text_files'



for subdir, dirs, files in os.walk(rootdir):
    for file in tqdm(files):
        old_path =  os.path.join(subdir, file)
        new_path = os.path.join(newdir, file)
        copyfile(old_path, new_path)
 
