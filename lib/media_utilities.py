import ffmpeg
from PIL import Image, ExifTags

def extract(image):
    try:
        img = Image.open(image)
        exif = img._getexif()
        return exif
    except:
        return None

def get_field(exif,field):
    try:
        for (k,v) in exif.items():
            if ExifTags.TAGS.get(k) == field:
                return v
    except:
        #print("Exif Not Found")
        return None

def extract_vid(video):
    try:
        vid = ffmpeg.probe(video)
        #print(vid['streams'][0]['tags']['creation_time'])
        date = vid['streams'][0]['tags']['creation_time']
        year = date[0]+date[1]+date[2]+date[3]
        month = date[5]+date[6]
        day = date[8]+date[9]
        return year,month,day
    except:
        return None

def no_names(filename):
        if filename[0]+filename[1]+filename[2] == "VID":
            year = filename[4]+filename[5]+filename[6]+filename[7]
            month = filename[8]+filename[9]
            day = filename[10]+filename[11]
        elif filename[0:11] == "Screenshot_":
            year = filename[11:15]
            month = filename[16:18]
            day = filename[19:21]
        else:
            raise Exception
        return year, month, day
'''
def no_names_staging(filename):
        if filename[0]+filename[1]+filename[2] == "VID":
            year = filename[4]+filename[5]+filename[6]+filename[7]
            month = filename[8]+filename[9]
            day = filename[10]+filename[11]
        elif filename[0:11] == "Screenshot_":
            year = filename[11:15]
            month = filename[16:18]
            day = filename[19:21]
        elif filename[0:2] == "IMG":
            if filename[4:5] == "20" 
        else:
            raise Exception
        return year, month, day
'''
