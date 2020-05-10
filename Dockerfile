FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3.6 \
    python3-pip \
    python3.6-dev \
    python-dev \
    python3-dev \
    git \
    gcc \
    libffi-dev \
    flex \
    bison \
    zlib1g \
    pkg-config \
    ninja-build \
    libcairo2-dev \
    libgirepository1.0-dev \
    gobject-introspection \
    libmount-dev \
    libgstreamer1.0 \
    gstreamer1.0-x \
    gstreamer-1.0 \
    python3-gi \
    python-gobject \
    python-gst-1.0 \
    gtk-doc-tools \
    freeglut3 \
    libglib2.0-dev \
    json-glib-1.0 \
    python-gi-dev \
    libssl-dev \
    v4l-utils \
    vim \
    tzdata \
    cmake \
    make 
RUN pip3 install setuptools click pycairo

RUN dpkg-reconfigure --frontend noninteractive tzdata

RUN apt install libopencv-dev -y

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/lib/:/usr/local/lib/x86_64-linux-gnu/:/code/src
ENV PYTHON=/usr/bin/python3.6
ENV PYTHONPATH=/usr/bin/python3.6:/usr/local/lib/python3.6/site-packages
ENV GST_PLUGIN_PATH=/code/src/:/code/3rdparty/gst-build/subprojects/gst-python/examples/plugins/python/:/code/3rdparty/gst-build/subprojects/gst-python/builddir/plugin/:/usr/local/lib/x86_64-linux-gnu/gstreamer-1.0/:/usr/local/lib/gstreamer-1.0/:/usr/local/lib/x86_64-linux-gnu/:/usr/local/lib/

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

ADD . /lib/modules/

RUN mkdir /code/ && mkdir /code/3rdparty/ 

RUN cd /code/3rdparty/ && git clone https://github.com/mesonbuild/meson.git 

RUN cd /code/3rdparty/ && git clone https://github.com/umlaeute/v4l2loopback.git 

# Pinned on release branch 1.16.2
RUN cd /code/3rdparty/ && git clone https://github.com/GStreamer/gst-build.git && \  
    cd /code/3rdparty/gst-build && git checkout tags/1.16.2 -b back0xff && \
    python3 /code/3rdparty/meson/meson.py -Dgtk_doc=disabled ./builddir && \
    ninja -C ./builddir && ninja -C ./builddir install  

# This is weird. when i run apt install after compiling gst-build things work. 
# Cache problems rule everything around me. moving on.
RUN apt install -y freeglut3-dev && gst-launch-1.0 --version
    
