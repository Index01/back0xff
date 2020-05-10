
#TODO: This should all become part of a pipeline object with python docker lib. Planned for later commit.

import subprocess


def set_camera_capabilities():
    """ Virtual camera must have the same settings as the real source. """
    print("[+] Set Caps\n")
    volume_mounts = '-v /home/t4l3r/repoz/back0xff:/code/src/'
    options = '--privileged'
    image = 'back0xff:latest'

    command = 'caps.sh'
    run_image = f'docker run --rm {volume_mounts} {options} {image} {command}'

    proc = subprocess.Popen(run_image.split())
    proc.communicate()


def segmentation():
    print("[+] Starting Segmentation\n")
    volume_mounts = '-v /home/t4l3r/repoz/back0xff:/code/src/'
    options = '--privileged'
    image = 'back0xff:latest'

    caps = "video/x-raw,format=YUY2,width=1280,height=720,framerate=10/1"
    src = "v4l2src device=/dev/video0 " 
    sink = "v4l2sink device=/dev/video3" 
    #bgsep = "segmentation test-mode=true method=2"
    bgsep = "segmentation method=2"

    command = f"gst-launch-1.0  {src} ! {caps} ! videoconvert ! {bgsep} ! videoconvert ! tee ! {sink}"

    run_image = f'docker run --rm {volume_mounts} {options} {image} {command}'
    #proc = subprocess.Popen(run_image.split())
    return subprocess.Popen(run_image.split())


def pass_through():
    volume_mounts = '-v /home/t4l3r/repoz/back0xff:/code/src/'
    options = '--privileged'
    image = 'back0xff:latest'
    
    command = 'gst-launch-1.0 v4l2src device=/dev/video0 ! v4l2sink device=/dev/video3'

    run_image = f'docker run --rm {volume_mounts} {options} {image} {command}'
    #proc = subprocess.Popen(run_image.split())
    return subprocess.Popen(run_image.split())
