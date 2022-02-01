The `music_player_package` server provides two services - `/start_music` and `/stop music`

It has a `music_files` folder that contains the list of music files that can be accessed by the server.

To call the `/start_music` service, one can use `rosservice call /start_music "filename:'sample_music.mp3'"`

To call the `/stop_music`, one can use `rosservice call /stop music "filename:''"`
