import googlemaps
import shutil
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail import delete as sorl_delete
from django.conf import settings

gmaps = googlemaps.Client(key=settings.GOOGLE_CLIENT_KEY)

def delete_file_thumbnail(obj):
    path=get_thumbnail(obj,'100x100', quality=90)
    folder_to_delete=settings.THUMBNAIL_PATH+str(path).split("/")[-3]
    sorl_delete(obj) #delete thumbnail file, thumbnail k-v, image file
    shutil.rmtree(folder_to_delete) # delete thumbnail folder
    return

