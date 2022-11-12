import googlemaps
import shutil
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail import delete as sorl_delete
from django.conf import settings
import datetime

gmaps = googlemaps.Client(key=settings.GOOGLE_CLIENT_KEY)

def delete_file_thumbnail(obj):
    path=get_thumbnail(obj,'100x100', quality=90)
    folder_to_delete=settings.THUMBNAIL_PATH+str(path).split("/")[-3]
    sorl_delete(obj) #delete thumbnail file, thumbnail k-v, image file
    shutil.rmtree(folder_to_delete) # delete thumbnail folder
    return


def generate_weekdays(start,end,pattern):
    ans=[]
    initial_offset=(pattern-start.isoweekday()+7)%7
    cur_date=start+datetime.timedelta(days=initial_offset)
    while cur_date <= end:
        ans.append(cur_date)
        cur_date+=datetime.timedelta(days=7)
    return ans

def flatten_list(alist):
    ans=[]
    for a in alist:
        if type(a) is list or type(a) is tuple:
            if len(a)>0:
                ans.extend(flatten_list(a))
        else:
            ans.append(a)
    return ans