import tkinter as tk
from tkinter import *
from tkinter import ttk
import config
import cv2
import numpy as np
from numba import objmode, njit, types, jit
from compare_vid_bd import comparar_faces
from threading import Thread
import crud
import listports

def downl_reporte():
    crud.ult_registros()

class GUI:
    def __init__(self):

        self.root = Tk()
        self.root.title('Pruebas Numba')
        self.root.geometry('960x500')

        self.capture1 = None
        self.ret = False
        self.count_fr = 0
        self.isrunning = False

        self.fr_camara = tk.Frame(self.root, width=600, height=300, borderwidth=2, relief='groove')
        self.fr_camara.grid(row=0, column=0, pady=5)

        self.tx_cam1 = tk.Entry(self.fr_camara, width=45)
        self.tx_cam1.insert(0,"rtsp://hugo:solkaf2008@192.168.1.64:554")
        self.tx_cam1.grid(row=0, column=0, pady=5)

        self.bt_cam1 = tk.Button(self.fr_camara, text='Conectar Camara', command=self.get_ip)
        self.bt_cam1.grid(row=0, column=1, pady=5, padx=5)

        self.bt_unpl_cam1 = tk.Button(self.fr_camara, text='Desconectar Camara', command=self.unplg_cam1)
        self.bt_unpl_cam1.config(state='disabled')
        self.bt_unpl_cam1.grid(row=0, column=2, pady=5, padx=5)

        self.lb_stat_cam1 = tk.Label(self.fr_camara, text='')

        self.zoom = Scale(self.fr_camara, from_=1, to=4, orient=tk.HORIZONTAL, label='Zoom', resolution=0.2)
        self.zoom.set(1.8)
        self.zoom.grid(row=2, column=0, padx=0)

        self.sc_framerate = Scale(self.fr_camara, from_=1, to=30, orient=tk.HORIZONTAL, label='Frames Skip')
        self.sc_framerate.set(10)
        self.sc_framerate.grid(row=2, column=1)

        self.bt_downl_reg = (tk.Button(self.fr_camara, text='Descargar Reporte', command=downl_reporte))
        self.bt_downl_reg.grid(row=2, column=2)

    def get_ip(self):
        ip_camara1 = self.tx_cam1.get()
        self.clear_ip(ip_camara1)

    def clear_ip(self, ip_camara1):
        ip_camara1 = ip_camara1.replace(" ","")
        result = True

        if len(ip_camara1)==1:
            try:
                ip_camara1 = int(ip_camara1)
            except:
                print("No se pudo conectar la camara")
                self.tx_cam1.delete(0, 200)
                self.tx_cam1.insert(0, 'Error conectando la camara.')

        self.plug_cam1(ip_camara1)

    def plug_cam1(self, ip_camara1):
        print(f"Intentando conectar la camara con ip {ip_camara1}")
        self.capture1 = cv2.VideoCapture(ip_camara1)

        self.ret, cap =self.capture1.read()
        if not (self.ret and self.capture1.isOpened()):
            print("No se pudo conectar la camara")
            self.tx_cam1.delete(0,200)
            self.tx_cam1.insert(0, 'Error conectando la camara.')


        if (self.ret):
            print(f'{ip_camara1} conectada con exito')
            self.bt_cam1.config(state='disabled')
            self.tx_cam1.config(state="disabled")
            self.bt_unpl_cam1.config(state='normal')
            self.get_frame()

    @jit(forceobj=True,looplift=True)
    def get_frame(self):
        self.count_fr += 1

        self.ret, frame = self.capture1.read()
        if self.ret is not None and self.capture1.isOpened() and self.count_fr % self.sc_framerate.get() == 0:
            self.show_frame(frame)
        self.lb_stat_cam1.after(1,self.get_frame)

    def show_frame(self, frame):
        frame = cv2.resize(frame,(800,600))
        # cv2.imshow('Frame', frame)
        # cv2.waitKey(1)
        th_showcv2 = Thread(target=comparar_faces, args=(self.zoom.get(),frame,))
        th_showcv2.run()

    def unplg_cam1(self):
        print('Desconectar la camara')
        self.ret = False
        self.bt_cam1.config(state='active')
        self.tx_cam1.config(state="normal")
        self.bt_unpl_cam1.config(state='disabled')
        self.capture1.release()
        cv2.destroyWindow('Frame')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    config.create_direct()
    my_win = GUI()
    my_win.root.mainloop()

