

# Back0xff build module. 
# Use a docker image to run the core stuff with lots of dev extras currently, virtual webcam
# requires a driver on the host.

import glob
import subprocess

def image(verbose=True):
    """ Create an image with all the dependencies from the dockerfile. """
    build_tag = 'back0xff:latest'
    build_exec = f'docker build . -t {build_tag}' 
    print("\n[+] Building new image")
    try:
        # NOTE: Hackidy hack hack. One day python3.8 will rule the world and this will get easier.
        if verbose:
            proc = subprocess.run(build_exec.split(), 
                                       stderr=subprocess.STDOUT,
                                       encoding='utf-8')
        else:
            proc = subprocess.check_output(build_exec.split(), 
                                       stderr=subprocess.STDOUT,
                                       encoding='utf-8')
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[-] Unable to execute the build. Exception: {e}"
              f"\nDo you even docker, brah? plz sudo apt install docker docker-compose."
              f"\nConfirm user is in the docker group")
        proc = None
        
    if proc is None or verbose is False:
        print('\nExiting...')
        return
    else:
        print(f'{proc}')


def plugin():
    """ TODO: Build the gstreamer python plugin """
    pass


def virtualcam_linux():
    """ Creating a virtual webcam currently requires installing a kernel module on the host. """
    dev = glob.glob('/dev/*')
    print("\n[+] Initializing virtualcam\n")
    if '/dev/video3' in dev:
        return
    else:
        subprocess.run('git clone https://github.com/umlaeute/v4l2loopback.git'.split())
        subprocess.run('make '.split(), cwd='./v4l2loopback')
        subprocess.run('make modprobe'.split(), cwd='./v4l2loopback')
        subprocess.run('rm -rf ./v4l2loopback'.split(), cwd='./')
    try:
        assert '/dev/video3' in dev
    except AssertionError as e:
        print('[-] Unable to create virtualcam. Are you root? Try sudo modprobe v4l2loopback')
        raise
