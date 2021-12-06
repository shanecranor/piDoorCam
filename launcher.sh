cd ~
sudo pigpiod -p 8887
cd ~/mjpg-streamer/mjpg-streamer-experimental
./mjpg_streamer -o "output_http.so -p 8090 -w ./www" -i "input_raspicam.so -p 8090" &
cd ~/piDoorCam
python3 RecordAudio.py &
python3 server.py &