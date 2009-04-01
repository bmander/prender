import os
import struct
import time
import subprocess

class BaseRenderer:

    commands = {"LINE":0,
                "DRAW":1,
                "BACKGROUND":2,
                "SMOOTH":3,
                "STOP":4,
                "STROKEWEIGHT":5,
                "TEST":6,
                "START":7,
                "STROKE":8,
                "SCALE":9,
                "TRANSLATE":10,
                "POINT":11,
                "ELLIPSE":12,
                "NOFILL":13,
                "FILL":14}

    def __init__(self, engine="/usr/bin/prender/renderer"):
        self.engine = engine
        
    def execute(self, width, height, func):
        self.start(width,height)
        try:
            func(self)
        except Exception, ex:
            raise ex
        finally:
            self.stop()
        
    def start(self, width, height):
        self.fp = subprocess.Popen(self.engine, stdin=subprocess.PIPE)
        message = struct.pack(">ii", width, height)
        self._sendMessage( "START", message )

    def smooth(self):
        self._sendMessage( "SMOOTH" )

    def background(self, r, g, b):
        message = struct.pack("BBB",r,g,b);
        self._sendMessage( "BACKGROUND", message )

    def line(self, x1, y1, x2, y2):
        message = struct.pack(">ffff", x1, y1, x2, y2)
        self._sendMessage( "LINE", message )
        
    def point(self, x, y):
        message = struct.pack(">ff", x, y)
        self._sendMessage( "POINT", message )
        
    def ellipse(self, x, y, width, height):
        message = struct.pack(">ffff", x, y, width, height)
        self._sendMessage( "ELLIPSE", message )

    def save(self, filename):
        message = filename.encode('ascii')+b"\n"
        self._sendMessage( "DRAW", message )
        
    def saveLocal(self, filename):
        self.save( os.path.join( os.getcwd(), filename ) )
        
    def strokeWeight(self, weight):
        message = struct.pack(">f",weight)
        self._sendMessage( "STROKEWEIGHT", message )
        
    def stroke(self,r,g,b,a=255):
        message = struct.pack("BBBB",r,g,b,a)
        self._sendMessage( "STROKE", message )
        
    def fill(self,r,g,b,a=255):
        message = struct.pack("BBBB",r,g,b,a)
        self._sendMessage( "FILL", message )
        
    def noFill(self):
        self._sendMessage( "NOFILL" )
    
    def _sendMessage( self, messagetype, contents=None ):
        message = struct.pack("B",self.commands[messagetype])
        if contents:
            message += contents
        self.fp.stdin.write( message )
    
    def stop(self):
        self._sendMessage( "STOP" )
        
    def scale(self, x, y):
        message = struct.pack(">ff", x, y)
        self._sendMessage( "SCALE", message )
        
    def translate(self, x, y):
        message = struct.pack(">ff", x, y)
        self._sendMessage( "TRANSLATE", message )
        
    def test(self):
        message = struct.pack(">if",42, 3.14159265358)
        self._sendMessage( "TEST", message )
        
class MapRenderer(BaseRenderer):
    def start(self, l, b, r, t, width):
        """start drawing an image 'width' wide with lower-left corner coordinates (l,b) and upper-right (r,t)"""
        
        if r < l:
            raise Exception( "l must be smaller than r" )
        if t < b:
            raise Exception( "b must be smaller than t" )
        
        # if the window specified by (l,b,r,t) is small, some things (like circles) can render wierd
        # We want everything to render into a window about 1000 Processing units wide
        self.reshelp = 1000/float(r-l)
        
        l *= self.reshelp
        b *= self.reshelp
        r *= self.reshelp
        t *= self.reshelp
        
        resolution = width/float(r-l) #pixels/meters
        height = int((t-b)*resolution) #meters * (pixels/meters) = pixels
        
        BaseRenderer.start(self, width, height)
        self.scale(resolution,resolution)
        self.translate( -l, t )
        
    def execute(self, l, b, r, t, width, func):
        self.start(l, b, r, t, width)
        try:
            func(self)
        except Exception, ex:
            raise ex
        finally:
            self.stop()
        
    def line(self, x1, y1, x2, y2):
        x1 *= self.reshelp
        y1 *= self.reshelp
        x2 *= self.reshelp
        y2 *= self.reshelp
        
        BaseRenderer.line(self,x1,-y1,x2,-y2)
        
    def point(self, x, y):
        x *= self.reshelp
        y *= self.reshelp
        
        BaseRenderer.point(self, x,-y)
        
    def ellipse(self, x, y, width, height):
        x *= self.reshelp
        y *= self.reshelp
        width *= self.reshelp
        height *= self.reshelp
        
        BaseRenderer.ellipse(self, x,-y,width,height)
        
    def strokeWeight(self, weight):
        weight *= self.reshelp
        
        BaseRenderer.strokeWeight( self, weight )

def selftest():
    pp = BaseRenderer("/usr/bin/prender/renderer")
    pp.start(200,200)
    pp.smooth()
    pp.background( 255, 255, 255 )
    pp.scale(0.5,0.5)
    pp.translate(10,10)
    pp.line( 0, 0, 100, 100 )
    pp.line( 0, 50, 100, 50 )
    pp.stroke(255,0,0)
    pp.line( 100, 0, 0, 100 )
    pp.save( os.path.join( os.getcwd(), "thickyddd.png" ) )
    pp.background(255,255,255)
    pp.strokeWeight(0.25)
    pp.line(0,0,100,100)
    pp.save( os.path.join( os.getcwd(), "thicknext.png" ) )
    pp.test()
    pp.stop()
    pp.start(100,100)
    pp.background(128,128,128)
    pp.saveLocal( "gray.png" )
    pp.stop()
    pp.start( 100, 100 )
    pp.background( 255, 255, 255 )
    pp.strokeWeight( 2 )
    pp.ellipse( 50, 50, 10, 10 )
    pp.point(50,50)
    pp.saveLocal( "point.png" )
    pp.stop()
    
    mr = MapRenderer("/usr/bin/prender/renderer")
    mr.start(-500, -500, 500, 500, 500)
    mr.smooth()
    mr.background( 255, 255, 255 )
    mr.line(-500,-500, 500, 500)
    mr.saveLocal("map.png")
    mr.stop()

if __name__=='__main__':
    selftest()