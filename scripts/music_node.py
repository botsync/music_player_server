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

print(sys.argv)


class music_player:

    def __init__(self):

        # VLC Component
        print("Inside the constructor!")
        self.player = vlc.Instance('--input-repeat=1000')
        self.media_list = self.player.media_list_new()
        self.media_player = self.player.media_list_player_new()
        #self.media_list = self.player.media_list_new()
        #self.media_player = self.player.media_list_player_new()

        # Initializing service servers
        # self.start_play_music_server()
        # self.start_pause_music_server()

        # ROS utility functions
        self.pkg_path = rospkg.RosPack().get_path("music_player_server")
        self.music_file_path = self.pkg_path + "/music_files/"

        self.music_file_sub_ = rospy.Subscriber(
            "music_file_name_", String, self.handle_music)

    # start music callback

    def handle_music(self, data):

        print("Inside the callback!")

        cnt = 0

        while True:
            cnt = cnt + 1
            print("cnt: ", cnt)

        if(data.data != ""):
            self.handle_play_music(data.data)

        else:
            self.handle_pause_music()

    def handle_play_music(self, req):

        file_name = req

        print("filename: ", file_name)

        media_ = self.music_file_path + file_name

        if not os.path.exists(media_):
            return MusicServerResponse(False, "Requested Music file not found -- returning False\n")

        self.media_player.stop()
        self.media_list = self.player.media_list_new()
        self.media_player = self.player.media_list_player_new()
        self.media = self.player.media_new(media_)
        self.media_list.add_media(self.media)
        self.media_player.set_media_list(self.media_list)

        # vlc part -- playing the song
        self.player.vlm_set_loop("test_var", True)
        self.media_player.play()

        # return MusicServerResponse(True, "Music Started Succesfully!\n")

    # pause music callback
    def handle_pause_music(self):

        self.media_player.stop()
        # return MusicServerResponse(True, "Music Paused Successfully!\n")

    '''
    # play_music_server
    def start_play_music_server(self):

        self.s1 = rospy.Service(
            'start_music', MusicServer, self.handle_play_music)
        #print ("Play Music Service Available!\n")

    # pause_music_server
    def start_pause_music_server(self):

        self.s2 = rospy.Service(
            'stop_music', MusicServer, self.handle_pause_music)
        #print ("Pause Music Service Available!\n")
    '''


if __name__ == "__main__":

    rospy.init_node('music_server_node', anonymous=False)

    mps = music_player()

    rospy.spin()
