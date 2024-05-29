# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 16:30:24 2024

@author: David
"""

from PIL import Image
import os


# Mapa kjer so shranjene slike
def generate_gif(mapa, trajanje_slike, ime_animacije):
    images = [img for img in os.listdir(mapa) if img.endswith(".png")]  # Naredi seznam slik/datotek v mapi

    images.sort(key=lambda x: int(x.split('.')[0]))  # Razvrsti slike

    # Odpre prvo sliko in izmeri njene dimenzije
    first_image = Image.open(os.path.join(mapa, images[0]))
    image_size = first_image.size

    # Ustvari seznam za slikovne objekte
    frames = []

    # Gre skozi slike in jih doda seznam "frame"-ov
    for image in images:
        image_path = os.path.join(mapa, image)
        frame = Image.open(image_path)
        frames.append(frame)

    # Shrani v GIF datoteko
    frames[0].save(ime_animacije, format='GIF', append_images=frames[1:], save_all=True, duration=trajanje_slike,
                   loop=0)
