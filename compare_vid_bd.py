from time import sleep
from trace import Trace
from threading import Thread
import cv2
from numpy.ma.core import shape

#import open_door
from crud import *
from simple_facerec import SimpleFacerec
import time
from numba import jit, njit
import numpy as np

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

rojo = (0, 0, 255)
verde = (0, 140, 13)
blanco = (255, 250, 250)

@jit(forceobj=True, looplift=True)
def zoomframe(frame, scale):
    width = int(frame.shape[1] * scale)
    heigth = int(frame.shape[0] * scale)
    dimensions = (width, heigth)
    # cv2.imshow('Zoom',frame)
    # cv2.waitKey(1)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)


@jit(forceobj=True, looplift=True)
def comparar_faces(scale, *args):
    cam_n = 1
    #print(f'frames enviados {len(args)}')
    for frame in args:

        if frame is not None:
            frame = zoomframe(frame, scale)
            face_locations, face_names = sfr.detect_known_faces(frame)
            for face_loc, name in zip(face_locations, face_names):
                name = name[:40]
                # print(face_loc)
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                if name == 'Desconocido':
                    color = rojo
                else:
                    color = verde
                    print(name)

                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 0.7, color=color)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 4)
                insert_face(name)

                key = cv2.waitKey(1)
                if key == 27:
                    break

            if cam_n == 1:
                cv2.imshow("Reconocimiento facial VETA Seguridad- ", frame)
                cv2.waitKey(1)
                cont_frame = +1
            else:
                continue
