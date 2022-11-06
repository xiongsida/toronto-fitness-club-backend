import googlemaps
import shutil
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail import delete as sorl_delete

gmaps = googlemaps.Client(key='AIzaSyAz2VJWVsBKb65KyxVWm1exv2-dubWdFdU')

def delete_file_thumbnail(obj):
    path=get_thumbnail(obj,'100x100', quality=90)
    folder_to_delete='media/'+'/'.join(str(path).split("/")[:-2])
    sorl_delete(obj) #delete thumbnail file, thumbnail k-v, image file
    shutil.rmtree(folder_to_delete) # delete thumbnail folder
    return

