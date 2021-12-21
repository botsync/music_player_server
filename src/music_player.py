#!/usr/bin/env python

import os
import time
import rospy
import threading
import signal
from subprocess import call
from music_player_server.srv import *



class music_player():
	def __init__(self):
		self.s1 = rospy.Service('/start_music', start_music, self.handle_start_music)
		self.s2 = rospy.Service('/stop_music', stop_music, self.handle_stop_music)
		self.vlc_command_str = "nvlc"                 
		self.filename_str = "sample_music.mp3"
		self.loop_str = "--loop"                        
		self.volume_str = "--gain="
		self.volume_command = ""
		self.quit_str = "vlc://quit"
		self.stop_thread = False
		self.srv_res = start_musicResponse()
		self.stop_res = stop_musicResponse()

	def handle_start_music(self,req):
		 		
		print("inside callback")
		self.volume_command = self.volume_str + str(req.volume)
	
		x = threading.Thread(target=self.thread_function, args=(req,)) 
		x.start()

		self.srv_res.result = True
		return self.srv_res
	

	def thread_function(self, req):
		print("inside thread")

		start = time.time()
		while(True):
			call([self.vlc_command_str , self.filename_str, self.volume_command , self.quit_str])
			end = time.time()
			elapsed = end - start
			if((elapsed > req.duration)):
				break

		print("exiting thread")
	
	def handle_stop_music(self, stop_req):
		if(stop_req.stop_command == "STOP"):
			self.stop_thread = True
			self.stop_res.result = True
		else:
			self.stop_res.result = False
		return self.stop_res

if __name__ == "__main__":
	rospy.init_node('music_server_node')
	mps = music_player()
	rospy.spin()





'''
https://stackoverflow.com/questions/24374620/python-loop-to-run-for-certain-amount-of-seconds
'''