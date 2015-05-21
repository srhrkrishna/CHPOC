Installing ffmpeg:
==================

Get the dependencies:
---------------------
>`sudo apt-get update`<br />
>`sudo apt-get -y --force-yes install autoconf automake build-essential libass-dev libfreetype6-dev libgpac-dev \`<br />
>`  libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev \`<br />
>`  libxcb-xfixes0-dev pkg-config texi2html zlib1g-dev`<br />
>`mkdir ~/ffmpeg_sources`

libx264:
--------
>`sudo apt-get install libx264-dev`

libx265:
--------
>`sudo apt-get install cmake mercurial`<br />
>`cd ~/ffmpeg_sources`<br />
>`hg clone https://bitbucket.org/multicoreware/x265`<br />
>`cd ~/ffmpeg_sources/x265/build/linux`<br />
>`PATH="$HOME/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$HOME/ffmpeg_build" -DENABLE_SHARED:bool=off ../../source`<br />
>`make`<br />
>`make install`<br />
>`make distclean`<br />

libfdk-aac
----------
>`sudo apt-get install unzip`<br />
>`cd ~/ffmpeg_sources`<br />
>`wget -O fdk-aac.zip https://github.com/mstorsjo/fdk-aac/zipball/master`<br />
>`unzip fdk-aac.zip`<br />
>`cd mstorsjo-fdk-aac*`<br />
>`autoreconf -fiv`<br />
>`./configure --prefix="$HOME/ffmpeg_build" --disable-shared`<br />
>`make`<br />
>`make install`<br />
>`make distclean`<br />

libmp3lame
----------
>`sudo apt-get install libmp3lame-dev`

libopus
-------
>`sudo apt-get install libopus-dev`

ffmpeg
------
>`cd ~/ffmpeg_sources`<br />
>`wget http://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2`<br />
>`tar xjvf ffmpeg-snapshot.tar.bz2`<br />
>`cd ffmpeg`<br />
>`PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure \`<br />
>`  --prefix="$HOME/ffmpeg_build" \`<br />
>`  --pkg-config-flags="--static" \`<br />
>`  --extra-cflags="-I$HOME/ffmpeg_build/include" \`<br />
>`  --extra-ldflags="-L$HOME/ffmpeg_build/lib" \`<br />
>`  --bindir="$HOME/bin" \`<br />
>`  --enable-gpl \`<br />
>`  --enable-libass \`<br />
>`  --enable-libfdk-aac \`<br />
>`  --enable-libfreetype \`<br />
>`  --enable-libmp3lame \`<br />
>`  --enable-libopus \`<br />
>`  --enable-libtheora \`<br />
>`  --enable-libvorbis \`<br />
>`  --enable-libx264 \`<br />
>`  --enable-libx265 \`<br />
>`  --enable-nonfree`<br />
>`  --disable-yasm`<br />
>`PATH="$HOME/bin:$PATH" make`<br />
>`make install`<br />
>`make distclean`<br />
>`hash -r`<br />

libfaac
-------
>`sudo apt-get install libfaac-dev`

If you want `ffmpeg` to work from anywhere:

-	Login and Logout
-	Or run `source ~/.profile`

Using in Web Application:
-------------------------
When running Django API application note that the ffmpeg command can fail. So find where the ffmpeg is installed on server machine by running

>`find /usr -name "ffmpeg"`

Then in the code where we are using ffmpeg replace it with full path like -

>`command = '/home/krishna/bin/ffmpeg -y -itsoffset -2  -i %s -vcodec mjpeg -vframes 1 -an -f rawvideo -s 320x240 %s' % \`<br />
>`                      (video_path, thumbnail_path)`

Reference:
[ffmpeg guide](https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu)