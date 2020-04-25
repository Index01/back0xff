FROM ubuntu:18.04
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    gcc \
    libffi-dev \
    flex \
    bison \
    zlib1g \
    pkg-config \
    ninja-build \
    libmount-dev \
    libgstreamer1.0 \
    gstreamer1.0-x \
    gtk-doc-tools \
    freeglut3 \
    libglib2.0-dev \
    json-glib-1.0 \
    python-gi-dev \
    cmake \
    make 
RUN pip3 install setuptools click

ADD . /lib/modules/

RUN mkdir /code/ && mkdir /code/3rdparty/ 

RUN cd /code/3rdparty/ && git clone https://github.com/mesonbuild/meson.git 

# Sure would be nice to clone and make the virtual cam driver here. Problems installing it as a kernel module.
#RUN git clone https://github.com/umlaeute/v4l2loopback.git 
#    cd v4l2loopback && ls /lib/ && \
#    make && make install && make modprobe

#TODO: Pin to a release branch. The build system changes and this is working currently.
RUN cd /code/3rdparty/ && git clone https://github.com/GStreamer/gst-build.git && \  
    cd /code/3rdparty/gst-build && python3 /code/3rdparty/meson/meson.py -Dgtk_doc=disabled ./builddir && \
    ninja -C ./builddir && ninja -C ./builddir install  

# This is weird. when i run apt install after compiling gst-build things work. moving on.
RUN apt install -y freeglut3-dev && gst-launch-1.0 --version
    
RUN cd /code/3rdparty/ && git clone https://github.com/GStreamer/gst-python.git && \
    cd gst-python && python3 /code/3rdparty/meson/meson.py ./builddir && \
    ninja -C ./builddir && ninja -C ./builddir install

