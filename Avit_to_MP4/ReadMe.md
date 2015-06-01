Approach:
=========

1. Run avi_to_mp4.sh as a daemon
2. The shell file will run avi_to_mp4.py file
3. The python file will fetch all the avi format files in swift from 'Avis' container and convert them to MP4 format.
4. The converted files along with the metadata is stored in Videos container.
5. The python script will continue to do this with a 10 second interval in between.

Instruction for running the service:
====================================
1. Copy the avi_to_mp4.py file to /usr/local/bin/avi_to_mp4 directory. Create avi_to_mp4 directory before copying and provide executable permission to the file.
> `sudo mkdir /usr/local/bin/avi_to_mp4; sudo cp ./Avit_to_MP4/avi_to_mp4.py /usr/local/bin/avi_to_mp4/avi_to_mp4.py; sudo chmod 755 /usr/local/bin/avi_to_mp4/avi_to_mp4.py;`

2. Copy the avi_to_mp4.sh file to /etc/init.d directory.
> `sudo cp ./Avit_to_MP4/avi_to_mp4.sh /etc/init.d/; sudo chmod 755 /etc/init.d/avi_to_mp4.sh;`

3. At this point you should be able to start your Python script using the command `sudo /etc/init.d/avi_to_mp4.sh start`, check its status with the `sudo /etc/init.d/avi_to_mp4.sh status` argument and stop it with `sudo /etc/init.d/avi_to_mp4.sh stop`.

Note:
-----
Make sure both the sh and py files are only using UNIX line endings. 
If not you can use dos2unix command line utility to cinvert the line endings 
E.g. - 'dos2unix avi_to_mp4.sh'
To install the utility use 'sudo apt-get install dos2unix' command.
