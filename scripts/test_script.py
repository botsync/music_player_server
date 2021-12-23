#!/usr/bin/env python3

import os
import time
from genpy import message
import rospy
import threading
import signal
from subprocess import call
#from music_player_server.srv import *
from std_srvs.srv import SetBool, SetBoolResponse
import vlc
from time import sleep


class music_player:

    def __init__(self, media_source):

        # VLC Component
        self.player = vlc.Instance('--input-repeat=1000')
        self.media_list = self.player.media_list_new()
        self.media_player = self.player.media_list_player_new()
        self.media = self.player.media_new(media_source)
        self.media_list.add_media(self.media)
        self.media_player.set_media_list(self.media_list)

        # Initializing service servers
        self.start_play_music_server()
        self.start_pause_music_server()

    def handle_play_music(self, req):

        print ("Play music request received!\n")

        self.player.vlm_set_loop("test_var", True)
        self.media_player.play()

        print("self.media_player.get_state(): %s\n",
              self.media_player.get_state())

        return SetBoolResponse(success=True, message="Music Started Successfully!\n")

    def handle_pause_music(self, req):

        print ("Pause music request received!\n")

        self.media_player.set_pause(1)

        return SetBoolResponse(success=True, message="Music Paused Successfully!\n")

    # play_music_server
    def start_play_music_server(self):

        self.s1 = rospy.Service(
            '/start_music', SetBool, self.handle_play_music)
        print ("Play Music Service Available!\n")

    # pause_music_server
    def start_pause_music_server(self):

        self.s2 = rospy.Service(
            '/stop_music', SetBool, self.handle_pause_music)
        print ("Pause Music Service Available!\n")


if __name__ == "__main__":

    rospy.init_node('music_server_node')

    music_file = "sample_music.mp3"

    mps = music_player(music_file)

    rospy.spin()
