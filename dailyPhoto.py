import os, sys
import datetime
import subprocess

# Import global variables
from decouple import config

source
now = datetime.datetime.now()
day = now.strftime('%d')
month = now.strftime('%m')
year = now.strftime('%Y')

path = config('misc_path')
list_for_ffmpeg = []


for yr in range(2000,int(year) + 1):
    for root, d_names, f_names in os.walk(path+"/"+str(yr)+"/"+month+"/"+day):
        for f in f_names:
            list_for_ffmpeg.append(os.path.join(root,f))

print(list_for_ffmpeg)
im_extensions = (".jpeg", ".jpg", ".png", ".gif")
vid_extensions = (".mp4", ".mov", ".avi")
nimage = 0
nvid = 0
imindex = 0

for item in list_for_ffmpeg:
    if item.endswith(im_extensions):
        nimage += 1
with open(config(img_ffmpeg_txt), "w") as img_list:
    with open(config(vid_ffmpeg_txt), "w") as vid_list:
        for entry in list_for_ffmpeg:
            if entry.endswith(im_extensions):
                imindex += 1
                img_list.write("file '"+entry+"'\n")
                img_list.write("duration 3\n")
                if imindex == nimage:
                    img_list.write("file '"+entry+"'\n")
            elif entry.endswith(vid_extensions):
                vid_list.write("file '"+entry+"'\n")

subprocess.run(("echo", "Hello_World")) # Debug step
#subprocess.run(config(ffmpeg_creator_sh))
