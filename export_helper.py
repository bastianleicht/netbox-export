import io
import requests
from PIL import Image

def get_image_from_url(url):
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    else:
        print(f'Fehler beim Abrufen des Bildes: {response.status_code} [get_image_from_url(url), {url}]')
        return None


# Get connected termination of a cable
def get_connected_termination(device_id, cable):
    for termination in cable['a_terminations']:
        if termination['object']['device']['id'] != device_id:
            return termination
    for termination in cable['b_terminations']:
        if termination['object']['device']['id'] != device_id:
            return termination
    return None
