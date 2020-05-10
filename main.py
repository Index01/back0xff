#!/usr/bin/env python3

import os
import click
import subprocess
import build
import pipelines


def run(mode):
    """ Run the back0xff client gstreamer piepline and ui. """
    build.virtualcam_linux()
    pipelines.set_camera_capabilities()

    print('[+] Running Back0xff image\n')

    proc = getattr(pipelines, mode)()
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
@click.option('--build-new', type=click.Choice(['image','plugin', 'virtualcam_linux']))
@click.option('--mode', type=click.Choice(['segmentation','pass-through']))
def main(build_new, mode):
    if build_new:
        getattr(build, build_new)()
    else:
        run(mode)



if __name__=='__main__':
    main()
