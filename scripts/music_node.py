#!/usr/bin/env python

from fileinput import filename
from genericpath import exists
from tokenize import String
import rospkg
from time import sleep
import vlc
from music_player_server.srv import MusicServer, MusicServerResponse
import time
import os
import rospy
import sys
import os
from std_msgs.msg import String
import threading
import multiprocessing


class music_player:

    def __init__(self):

        # VLC Component
        print("Inside the constructor!")
        self.player = vlc.Instance('--input-repeat=1000')
        self.media_list = self.player.media_list_new()
        self.media_player = self.player.media_list_player_new()
                
        self.pkg_path = rospkg.RosPack().get_path("music_player_server")
        self.music_file_path = self.pkg_path + "/music_files/"

        self.music_file_sub_ = rospy.Subscriber(
            "music_file_name_", String, self.handle_music)
        
        self.last_thread = None
        self.counter = 0  

        print('active_threads inside the music_player constructor: ', threading.active_count())

    
    def handle_music(self, data):
        
        print('Inside the handle_music function')
        print('counter: ', self.counter)

        print('active_threads before: ', threading.active_count())
        
        '''
        t = KillableThread(1, self.handle_play_music, data.data)  
        t.start()
        
        time.sleep(5)
        t.kill()
        '''
            
        if data.data=="":
            self.handle_pause_music()
        else:
            self.handle_play_music(data.data)

        print('active_threads after: ', threading.active_count())
        '''
        if self.last_thread is not None:
            p = self.last_thread
            p.kill()
            print ('Killed last thread')

        if self.counter % 2 == 0:
            t = KillableThread(1, self.handle_play_music, data.data)  
            t.start()
            self.last_thread = t
        
        else:
            self.last_thread.kill()
        
        self.counter = self.counter  + 1
        print('Inside the handle_music function!')
        if data.data == "":
            t = KillableThread(1, self.handle_play_music, data.data)   
        else:
            t = KillableThread(1, self.handle_pause_music)   

        t.start()
        
        self.last_thread = t
        '''
        #handle_play_music(data.data)

    def handle_play_music(self, req):
        
        print("Inside the handle_play_music function!")

        file_name = req

        print("filename: ", file_name)

        media_ = self.music_file_path + file_name
        
        file_exists_ = os.path.exists(media_)
        
        print("file_exists_: ", file_exists_)
        

        if not os.path.exists(media_):
            return MusicServerResponse(False, "Requested Music file not found -- returning False\n")

        self.media_player.stop()
        self.media_list = self.player.media_list_new()
        self.media_player = self.player.media_list_player_new()
        
        self.media = self.player.media_new(media_)
        self.media_list.add_media(self.media)
        self.media_player.set_media_list(self.media_list)
        
        print('Trying to play the song!')
        # vlc part -- playing the song
        self.player.vlm_set_loop("test_var", True)
        self.media_player.play()

        return MusicServerResponse(True, "Music Started Succesfully!\n")

    # pause music callback
    def handle_pause_music(self):

        self.media_player.stop()
        # return MusicServerResponse(True, "Music Paused Successfully!\n")



class KillableThread(threading.Thread):
    
    def __init__(self, sleep_interval, func_, *args):
        
        super(KillableThread, self).__init__()
        self._kill = threading.Event()
        self._interval = sleep_interval
        self.func = func_
        self.func_args = args
        #self.func_args = args
    
    def run(self):  
        
        print('Inside the run function!')
        self.func(*self.func_args)

        pass

    def kill(self):
        self._kill.set()

if __name__ == "__main__":

    rospy.init_node('music_server_node', anonymous=False)

    mps = music_player()
    #global thread    
    #thread.join(3)
    
    

    '''
    t = KillableThread(sleep_interval=1)
    t.start()
    # Every 5 seconds it prints:
    #: Do Something
    #t.kill()
    time.sleep(10)
    t.kill()
    '''
    rospy.spin()
