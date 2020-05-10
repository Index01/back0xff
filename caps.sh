#!/bin/bash


#TODO: Parameterize.
device=/dev/video3
caps="video/x-raw, format=(string)YUY2, width=(int)1280, height=(int)720, pixel-aspect-ratio=(fraction)1/1"
framerate="framerate=(fraction)10/1"
fps=`echo "$framerate" | sed -r 's/.*(=|\))//g'`

sysfs=/sys/devices/virtual/video4linux/${device##*/}
echo "@$fps" | tee $sysfs/format >/dev/null || echo "could not set fps attr"

v4l2-ctl -d $device -c keep_format=1 || exit 1
v4l2-ctl -d $device -c sustain_framerate=1 || exit 1
gst-launch-1.0 videotestsrc num-buffers=1 ! "$caps" ! v4l2sink device=$device >> /dev/null 2>&1 || echo "output $device failed"
#v4l2-ctl -d $device --list-ctrls

