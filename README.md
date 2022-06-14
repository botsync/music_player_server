The `music_player_package` server provides two services - `/start_music` and `/stop music`

It has a `music_files` folder that contains the list of music files that can be accessed by the server.

To call the `/start_music` service, one can use `rosservice call /start_music "filename:'sample_music.mp3'"`

To call the `/stop_music`, one can use `rosservice call /stop music "filename:''"`


We also need the following package to enable thread killing  - https://github.com/munawarb/Python-Kill-Thread-Extension ( it has already been 
cloned in music_player_server/ so follow the instructions in the link to install it )

We also need to configure the following in /etc/pulse/default.pa
#this module will switch the default sink/source to be the new sink/source as it is plugged in
load-module module-switch-on-connect
#Automatically switches the card profile and/or device port when a port changes its availablility status
load-module module-switch-on-port-available
#set the default sink to the speaker 
set-default-sink alsa_output.usb-Dell_DELL_Slim_Soundbar_SB521A_SB521A-00.analog-stereo
