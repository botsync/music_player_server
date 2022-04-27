#!/usr/bin/env python

import threader
from fileinput import filename
from genericpath import exists
from tokenize import String
import rospkg
import vlc
from time import sleep
import os
import rospy
import sys
import os
from std_msgs.msg import String
import threading
import atexit

class music_player:

    def __init__(self):

        # VLC Component
        #print("Inside the constructor!")
        self.player = vlc.Instance('--input-repeat=1000')
        self.media_list = self.player.media_list_new()
        self.media_player = self.player.media_list_player_new()
                
        self.pkg_path = rospkg.RosPack().get_path("music_player_server")
        self.music_file_path = self.pkg_path + "/music_files/"

        self.music_file_sub_ = rospy.Subscriber(
            "music_file_name_", String, self.handle_music)
        
        self.last_thread = None

        #self.threading.Timer(2, after_timeout).start()
        #threading.Timer(2, self.after_timeout).start()
    
    def handle_music(self, data):
        
        #print("Callback received!")
        #sleep(5)

        if self.last_thread is not None:
            #print("Trying to kill last thread")
            self.last_thread.end()
       
        #print("data.data: " , data.data)
        
        #print("len(data.data): ", len(data.data))

        if len(data.data) > 0:
            runMe = AThread(self.handle_play_music, data.data)
        else:
            runMe = AThread(self.handle_pause_music, data.data)
        
        runMe.start()
        self.last_thread = runMe 


    def handle_play_music(self, req):
       
        #print("Inside the handle_play_music function")
        file_name = req

        #print("filename: ", file_name)

        media_ = self.music_file_path + file_name
        
        file_exists_ = os.path.exists(media_)
        
       # print("file_exists_: ", file_exists_)
        
        

        if not os.path.exists(media_):
            self.media_player.stop()
            return 

        self.media_player.stop()
        self.media_list = self.player.media_list_new()
        self.media_player = self.player.media_list_player_new()
        
        self.media = self.player.media_new(media_)
        self.media_list.add_media(self.media)
        self.media_player.set_media_list(self.media_list)
        
        #print('Trying to play the song!')
        # vlc part -- playing the song
        self.player.vlm_set_loop("test_var", True)
        self.media_player.play()

        return


    # pause music callback
    def handle_pause_music(self, data):
        
        #print("Inside the pause_music function")
        self.media_player.stop()


class AThread(threading.Thread):
   
    def __init__(self, func_, *args):
        
        threading.Thread.__init__(self)
	    #self.stopped = False
        self.func = func_   
        self.file_name = args

    def run(self):
        
        self.func(*self.file_name)
        self.stopped = False


    def end(self):
        if self.is_alive():
            threader.killThread(self.ident)
            self.stopped = True

if __name__ == "__main__":

    rospy.init_node('music_server_node', anonymous=False)

    mps = music_player()
    rospy.spin()
