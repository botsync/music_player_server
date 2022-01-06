#!/usr/bin/env python3

import rospy
from music_player_server.srv import MusicServer, MusicServerResponse
from time import sleep
from pygame import mixer
import rospkg
# from sklearn.externals.funcsigs import signature
# from funcsigs import signature


class music_player:

    def __init__(self):

        mixer.init()
        self.sound_running = False
        # Initializing service servers
        self.start_play_music_server()
        self.start_pause_music_server()

        # ROS utility functions
        self.pkg_path = rospkg.RosPack().get_path("music_player_server")
        self.music_file_path = self.pkg_path + "/music_files/"

    # start music callback
    def handle_play_music(self, req):

        if self.sound_running:
            mixer.stop()

        print ("Play music request received!\n")

        # ROS part
        file_name = req.filename
        media_ = self.music_file_path + file_name

        mixer.music.load(media_)
        mixer.music.play(loops=-1)

        self.sound_running = True

        return MusicServerResponse(True, "Music Started Succesfully!\n")

    # pause music callback
    def handle_pause_music(self, req):

        print ("Stop music request received!\n")

        # self.media_player.set_pause(1)
        # if self.sound_running:
        mixer.music.stop()

        # mixer.music.stop()

        self.sound_running = False

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

    # pkg_path = rospack.get_path("music_player_server")
    mps = music_player()

    rospy.spin()
