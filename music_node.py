#!/usr/bin/env python

from tokenize import String
import rospkg
import vlc
import os
import rospy
from std_msgs.msg import String

class music_player:

    def __init__(self):
        #self.media_player.get_media_player().audio_set_volume(500)
        # VLC Component
        #print("Inside the constructor!")
        # self.player = vlc.Instance('--input-repeat=100000', '--verbose=-1')
        self.player = vlc.Instance()
        # self.player.set_playback_mode(vlc.PlaybackMode.loop)
        self.media_list = self.player.media_list_new()
        self.media_player = self.player.media_list_player_new()
                
        self.pkg_path = rospkg.RosPack().get_path("music_player_server")
        self.music_file_path = self.pkg_path + "/music_files/"

        self.music_file_sub_ = rospy.Subscriber(
            "music_file_name_", String, self.handle_music)
        
        self.last_music_file = ''
    
    def handle_music(self, data):        
        if data.data == self.last_music_file:
            rospy.loginfo("Music Player --- player state : ")
            rospy.loginfo(self.media_player.get_state())
            if (self.media_player.get_state() == vlc.State.Ended) :
                rospy.loginfo("Music Player --- restarting")
                self.media_player.play()
            rospy.loginfo("Music Player ---- Playing the same music again, not resetting player.")
            return
        
        if data.data == "":
            rospy.loginfo("Music Player ---- Stopping music player.")
            self.last_music_file = data.data
            self.media_player.stop()
            return

        self.handle_play_music(data.data)

        self.last_music_file = data.data

    def handle_play_music(self, req):
        file_name = req

        media_ = self.music_file_path + file_name
        
        file_exists_ = os.path.exists(media_)

        # del self.player

        if not file_exists_:
            rospy.loginfo("Music Player ---- File does not exist.")
            self.media_player.stop()
            return 
        
        self.media = self.player.media_new(media_)
        self.media_list.add_media(self.media)
        self.media_player.set_media_list(self.media_list)

        print(self.player.vlm_set_loop(media_, True))
        self.media_player.play()

        rospy.loginfo("Music Player ---- Successfully started playing music.")

        return

    def handle_pause_music(self):
        self.media_player.stop()


if __name__ == "__main__":

    rospy.init_node('music_server_node', anonymous=False)

    mps = music_player()
    rospy.spin()
