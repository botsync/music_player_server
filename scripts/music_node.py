#!/usr/bin/env python3

import rospy
import os
import time
from genpy import message
import rospy
import threading
import signal
from subprocess import call
from enum import Enum
# from music_player_server.srv import *
#from std_srvs.srv import SetBool, SetBoolResponse
from music_player_server.srv import MusicServer, MusicServerResponse
import vlc
from time import sleep
import rospkg
# from sklearn.externals.funcsigs import signature
# from funcsigs import signature


class music_player:

    def __init__(self):

        # VLC Component
        self.player = vlc.Instance('--input-repeat=1000')
        self.media_list = self.player.media_list_new()
        self.media_player = self.player.media_list_player_new()
        #self.media_list = self.player.media_list_new()
        #self.media_player = self.player.media_list_player_new()

        # Initializing service servers
        self.start_play_music_server()
        self.start_pause_music_server()

        # ROS utility functions
        self.pkg_path = rospkg.RosPack().get_path("music_player_server")
        self.music_file_path = self.pkg_path + "/music_files/"

    # start music callback
    def handle_play_music(self, req):

        print ("Play music request received!\n")

        # ROS part
        file_name = req.filename
        media_ = self.music_file_path + file_name

        # vlc part -- setting the playlist
        self.media_player.stop()
        self.media_list = self.player.media_list_new()
        self.media_player = self.player.media_list_player_new()
        self.media = self.player.media_new(media_)
        self.media_list.add_media(self.media)
        self.media_player.set_media_list(self.media_list)

        # vlc part -- playing the song
        self.player.vlm_set_loop("test_var", True)
        self.media_player.play()

        print("self.media_player.get_state(): {}\n".format(
            self.media_player.get_state()))

        return MusicServerResponse(True, "Music Started Succesfully!\n")

    # pause music callback
    def handle_pause_music(self, req):

        print ("Pause music request received!\n")

        # self.media_player.set_pause(1)

        self.media_player.stop()
        return MusicServerResponse(True, "Music Paused Successfully!\n")

    # play_music_server
    def start_play_music_server(self):

        self.s1 = rospy.Service(
            'start_music', MusicServer, self.handle_play_music)
        print ("Play Music Service Available!\n")

    # pause_music_server
    def start_pause_music_server(self):

        self.s2 = rospy.Service(
            'stop_music', MusicServer, self.handle_pause_music)
        print ("Pause Music Service Available!\n")


if __name__ == "__main__":

    rospy.init_node('music_server_node', anonymous=False)

    rospack = rospkg.RosPack()

    #pkg_path = rospack.get_path("music_player_server")

    mps = music_player()

    rospy.spin()
