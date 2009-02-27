

public class renderer extends Applet {

  static public void main(String args[]) {
    
    PGraphicsJava2D pg = new PGraphicsJava2D();
    
    while(true) {
       try{
         if( System.in.available() > 0 ) {
           DataInputStream protocol = new DataInputStream( System.in );
           int messageType = protocol.readUnsignedByte();
           if( messageType==0 ) {
             //System.out.println( "LINE" );
             float x1 = protocol.readFloat();
             float y1 = protocol.readFloat();
             float x2 = protocol.readFloat();
             float y2 = protocol.readFloat();
             pg.line(x1,y1,x2,y2);
           } else if( messageType==1 ) {
             //System.out.println( "SAVE" );
             String filename = protocol.readLine();
             pg.endDraw();
             pg.save( filename );
           } else if( messageType==2 ) {
             //System.out.println( "BACKGROUND" );
             int r = protocol.readUnsignedByte();
             int g = protocol.readUnsignedByte();
             int b = protocol.readUnsignedByte();
             pg.background(r,g,b);
           } else if( messageType==3 ) {
             //System.out.println( "SMOOTH" );
             pg.smooth();
           } else if( messageType==4 ) {
             //System.out.println("STOP");
             break;
           } else if( messageType==5 ) {
             //System.out.println( "STROKEWEIGHT" );
             float weight = protocol.readFloat();
             pg.strokeWeight(weight);
           } else if( messageType==6 ) {
             //System.out.println( "TEST" );
             int testint = protocol.readInt();
             float testfloat = protocol.readFloat();
             //System.out.println( testfloat );
           } else if( messageType==7) {
             //System.out.println( "START" );
             int x = protocol.readInt();
             int y = protocol.readInt();
             pg.setSize(x, y);
             pg.beginDraw();
           } else if( messageType==8 ) {
             int r = protocol.readUnsignedByte();
             int g = protocol.readUnsignedByte();
             int b = protocol.readUnsignedByte();
             int a = protocol.readUnsignedByte();
             pg.stroke(r,g,b,a);
           } else if( messageType==9 ) {
             float x = protocol.readFloat();
             float y = protocol.readFloat();
             pg.scale(x,y);
           } else if( messageType==10 ) {
             float x = protocol.readFloat();
             float y = protocol.readFloat();
             pg.translate(x,y);
           } else if( messageType==11 ) {
             float x = protocol.readFloat();
             float y = protocol.readFloat();
             pg.point( x, y );
           } else if( messageType==12 ) {
             float x = protocol.readFloat();
             float y = protocol.readFloat();
             float width = protocol.readFloat();
             float height = protocol.readFloat();
             pg.ellipse( x, y, width, height );
           } else if( messageType==13 ) {
             pg.noFill(); 
           } else if( messageType==14 ) {
             int r = protocol.readUnsignedByte();
             int g = protocol.readUnsignedByte();
             int b = protocol.readUnsignedByte();
             int a = protocol.readUnsignedByte();
             pg.fill(r,g,b,a);
           }
         }
       } catch (IOException e) {
         System.out.println( "ioexception "+e+" "+e.getMessage() );
         break;
       }
    }

  }
}

