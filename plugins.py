

import gi
gi.require_version('GstBase','1.0')
from gi.repository import GstBase, Gst, GObject



class Back0xffBgSep(GstBase.BaseTransform):
    Gst.init(None)
    FORMATS = "{RGBx,BGRx,xRGB,xBGR,RGBA,BGRA,ARGB,ABGR,RGB,BGR}"
    CAPS = Gst.Caps.from_string(f"video/x-raw,format={FORMATS}")
    __gstmetadata__ = ("Back0xffBgSep",         
                       "BaseTransform",
                       "Background separation plugin",  
                       "Index01")       
       
    src_pad_template = Gst.PadTemplate.new("src",
                        Gst.PadDirection.SRC,
                        Gst.PadPresence.ALWAYS,
                        CAPS)
    sink_pad_template = Gst.PadTemplate.new("sink",
                        Gst.PadDirection.SINK,
                        Gst.PadPresence.ALWAYS,
                        CAPS)
    __gsttemplates__ = (src_pad_template, sink_pad_template)


    def __init__(self):
        GstBase.BaseTransform.__init__(self)
        #self.caps = Gst.Caps.from_string(f"video/x-raw,format={self.formats}")

    def do_transform_ip(self, buffer: Gst.Buffer) -> Gst.FlowReturn:

        return Gst.FlowReturn.OK



GObject.type_register(Back0xffBgSep)
__gstelementfactory__ = ("Back0xffBgSep", Gst.Rank.NONE, Back0xffBgSep)
