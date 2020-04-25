#!/usr/bin/env python3

import click
import subprocess
import build
import os


def run():
    """ Run the back0xff client gstreamer piepline and ui. """
    #TODO: This should all become part of a pipeline object with python docker lib. Planned for later commit.
    build.virtualcam_linux()

    print('\n[+] Running docker image\n')
    volume_mounts = '-v /home/t4l3r/repoz/back0xff:/code/src/'
    options = '--privileged'
    command = 'gst-launch-1.0 v4l2src device=/dev/video0 ! v4l2sink device=/dev/video3'
    image = 'back0xff:latest'
    run_image = f'docker run --rm {volume_mounts} {options} {image} {command}'
    proc = subprocess.Popen(run_image.split())
    try:
        proc.communicate()
    except KeyboardInterrupt as e:
        print("\nShut it down...")
        proc.kill()
        pid = subprocess.run("docker ps --filter ancestor=back0xff:latest -q".split(), 
                              check=True, 
                              encoding="utf-8", 
                              stdout=subprocess.PIPE)
        subprocess.run(f"docker kill {pid.stdout}".split())
        print("DONE.")
        raise


@click.command()
@click.option('--build-new', type=click.Choice(['image','plugin']))
def main(build_new):
    if build_new:
        getattr(build, build_new)()
    else:
        run()



if __name__=='__main__':
    main()
