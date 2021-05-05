	

import gi
import numpy as np
import cv2
from openalpr import Alpr
import sys
import serial
import sqlite3
import subprocess
import os



gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ButtonWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="ALPRS 0.2")
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(250, 350)

        #hbox = Gtk.Box(spacing=100)
        #self.add(hbox)
        
        self.outter_box = Gtk.VBox(False,spacing=10)
        self.add(self.outter_box)
        
        hbox = Gtk.ButtonBox.new(Gtk.Orientation.HORIZONTAL)
        hbox.set_layout(Gtk.ButtonBoxStyle.CENTER) 
        self.outter_box.pack_start(hbox, False, True, 0)
        
        hbox.get_style_context().add_class("linked")

        button = Gtk.Button.new_with_label("Allowed")
        hbox.add(button)
        button.connect("clicked", self.on_click_me_clicked)
        #hbox.pack_start(button, True, True, 0)

        button = Gtk.Button.new_with_mnemonic("_Logs")
        hbox.add(button)
        button.connect("clicked", self.on_open_clicked)
        #hbox.pack_start(button, True, True, 0)

        button = Gtk.Button.new_with_mnemonic("_Close")
        hbox.add(button)
        button.connect("clicked", self.on_close_clicked)
        #hbox.pack_start(button, True, True, 0)
        
        button = Gtk.Button.new_with_mnemonic("Start the Engine")
        hbox.add(button)
        button.connect("clicked", self.on_button_clicked)
        #hbox.pack_start(button, True, True, 0)
        
        hbox = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        self.outter_box.pack_end(hbox, False, True, 0)
        self.label_display = Gtk.Label("Output Log : ")
        hbox.add(self.label_display)
        
        hbox = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        self.outter_box.pack_start(hbox, False, True, 0)
        self.status_log = Gtk.Label("Status : ")
        hbox.add(self.status_log)
        
        hbox = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        self.outter_box.pack_end(hbox, False, True, 0)
        self.source_path = Gtk.Label("Status : ")
        hbox.add(self.source_path)
        
        #label_display.set_text("sdsd")
        
    def on_click_me_clicked(self, button):
		subprocess.Popen(["python", "allowed.py"])

    def on_button_clicked(self, button):
		
		#------
		RTSP_SOURCE  = 'rtsp://192.168.8.109:8080/h264_ulaw.sdp'
		WINDOW_NAME  = 'ALPR System 0.1'
		FRAME_SKIP   = 15
		self.source_path.set_text(str(RTSP_SOURCE))
		


		def open_cam_rtsp(uri):
			gst_str = ('rtspsrc location={} ! rtph264depay ! h264parse ! avdec_h264 ! '
               'videoconvert ! appsink').format(uri)
			return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)


		def main():
			alpr = Alpr('fr', 'fr.conf', '/usr/local/share/openalpr/runtime_data')
			if not alpr.is_loaded():
				print('Error loading OpenALPR')
				sys.exit(1)
			alpr.set_top_n(3)
			#alpr.set_default_region('new')

			cap = open_cam_rtsp(RTSP_SOURCE)
			if not cap.isOpened():
				alpr.unload()
				#sys.exit('Failed to open video file!')
				self.label_display.set_text("Output Log : Failed to open video file")
			#cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
			#cv2.setWindowTitle(WINDOW_NAME, 'Gate Camera test')
			#cv2.resizeWindow(WINDOW_NAME, 256, 256)

			conn = sqlite3.connect('stu3.db')
			c = conn.cursor()
					
			#c.execute('create table pr1 (ID, Name, NP)')
			
			conn.commit()	


			_frame_number = 0
			while True:
				ret_val, frame = cap.read()
				if not ret_val:
					self.label_display.set_text("Output Log : VidepCapture.read() failed. Exiting...")
					break

				_frame_number += 1
				if _frame_number % FRAME_SKIP != 0:
					continue
				#cv2.imshow(WINDOW_NAME, frame)
				#cv2.resizeWindow(WINDOW_NAME, frame, 256, 256)

				

				results = alpr.recognize_ndarray(frame)
				for i, plate in enumerate(results['results']):
					best_candidate = plate['candidates'][0]
					
					J = ('{}'.format(best_candidate['plate'].upper(),best_candidate))
					print J
					
					rows = c.execute("select plate from NP")
					conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
					for row in rows:
						if row[0] == str(J):
							self.status_log.set_text(str(J))
							print("Matched")
							arduino = serial.Serial('/dev/ttyACM0', 9600)
							command = str(85)
							arduino.write(command)
							reachedPos = str(arduino.readline())
								
								
							
								
					else:
						print("Doesn't Match")
						print(type(row[0]))



				if cv2.waitKey(1) == 27:
					break

			cv2.destroyAllWindows()
			cap.release()
			alpr.unload()








		if __name__ == "__main__":
			main()



    def on_open_clicked(self, button):
        print('"Open" button was clicked')

    def on_close_clicked(self, button):
        print("Closing application")
        Gtk.main_quit()


win = ButtonWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
