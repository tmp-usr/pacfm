import wx
import wx.lib.scrolledpanel as scroll

from pacfm.controller import Drawer

class CircosPanel( wx.Panel ) :

    """Create a very simple app frame.
    This will be completely filled with the DrawWindow().
    """
    def __init__( self, parent, wx_image ) :
       
        wx.Panel.__init__(self, parent= parent, size= (1000,800) )

        screenSize = wx.DisplaySize()
        screenWidth = screenSize[0]
        screenHeight = screenSize[1]


        self.wxImage=wx_image 
        self.imageSize= self.wxImage.GetSize()
        
        def scale(by):
            size=[0,0]
            size[0] = self.imageSize[0]/by
            size[1] = self.imageSize[1]/by 
            return size 
        
        self.scrolled = scroll.ScrolledPanel( self,  id= -1  , size= scale(3), style= wx.SIMPLE_BORDER )
        
        #self.SetupScrolling()
        #self.drawWindow = DrawWindow( self, -1, imgFilename )   # Instantiate
        #self.imgFilename = imgFilename                          # Only for OnDrawTimer()
        
        # Set the frame size. Discard the opened pilImage afterward reading its size.
        #pilImage = Image.open( imgFilename )
        #imgSizeX, imgSizeY = pilImage.size
        #clientSizeX = int( (1.414 * imgSizeX) + 25 )  # Max axis size necessary to completely show the rotated image
        #clientSizeY = int( (1.414 * imgSizeY) + 25 )  # plus an arbitrary 25 pixel margin.
        #maxSize = clientSizeX
        #if clientSizeY > clientSizeX :    maxSize = clientSizeY
        #self.pnl= wx.Panel(self.scrolled, id=-1) 
        #self.SetClientSize( (maxSize, maxSize) )
        
       
        self.pnl= wx.Panel(self.scrolled, -1, size= scale(3) )
        self.scrolled.SetBackgroundColour('white')

        self.pnl.Bind(wx.EVT_PAINT, self.OnPaint)
        #self.drawOnPanel2(wxImage, self.pnl)    
        
        sizer= wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.scrolled, 1, wx.EXPAND )
        #self.scrolled.SetSizer(sizer)
        #self.SetAutoLayout(1)
        #self.scrolled.SetScrollbars(1, 1, 600, 400)
        #self.scrolled.SetScrollRate(20,20)
        
        #sizerMain= wx.BoxSizer()
        #sizerMain.Add(self.scrolled, 1, wx.EXPAND)
        #self.scrolled.SetupScrolling()
        self.scrolled.SetScrollbars(scale(3)[0]/20, scale(3)[1]/20.2, 20, 20)
        #self.scrolled.SetAutoLayout(1)
        #self.scrolled.SetAutoLayout(1)
        #self.scrolled.SetTargetWindow(self)

        self.SetSizer(sizer)
        self.Layout() 
        
        #sizer= wx.BoxSizer()
        #sizerM= wx.BoxSizer()
        #sizerM.Add(self.scrolled)
        #self.SetSizer(sizerM)
        self.sizer=sizer
            
        #import pdb
        #pdb.set_trace()
        self.Show()                                 # The drawing window  must be shown before drawing.
        
        # Initial unrotated drawing. Subsequent timer events will call self.drawWindow.DrawRotated()
        # Subsequent draws will be incrementally rotated.
        #self.drawWindow.DrawRotated( imgFilename )
        
        #print self.runtimeMessage
                                                    
        #---------------
        
        # Rotate the image and redisplay it every 50 milliseconds.
        #self.drawTimer = wx.Timer( self, id=wx.NewId() )
        #self.Bind( wx.EVT_TIMER, self.OnDrawTimer )
        #self.drawTimer.Start( 50, oneShot=False )

    #end def __init__
   
    def OnPaint2(self, e):
        self.drawOnPanel(self.wxImage, self.pnl)

    #--------------
    def OnPaint(self,e):
        dc = wx.PaintDC(self.pnl)
        client_w, client_h = self.pnl.GetClientSizeTuple()
        #dc.DrawBitmap(self.scale_bitmap(self.wxImage.ConvertToBitmap(), client_w*1.5, client_h*1.5), 0, 0)
        #dc.DrawBitmap(self.wxImage.ConvertToBitmap(), 0, 0)
        
        imageWid, imageHgt = self.wxImage.GetSize()
        dc.DrawBitmap( self.scale_bitmap(self.wxImage.ConvertToBitmap(), imageWid/3, imageHgt/3), 0, 0 )
        #self.drawOnPanel2(self.wxImage, self.pnl)
        
    #def drawOnPanel2(self, wxImage, parent):
    
    def scale_bitmap(self, bitmap, width, height):
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result

    def drawOnPanel(self, wxImage, parent):
        clientWid, clientHgt = parent.GetClientSizeTuple()
        bufferedDC = wx.BufferedDC( wx.ClientDC(parent), wx.EmptyBitmap( clientWid, clientHgt ) )
        bufferedDC.SetBackground( wx.Brush( (220, 220, 240) ) )  
        bufferedDC.Clear()
        #
        # The WX way (angle values are given in degrees).
        # The specified center-of-rotation and offset-after-rotation don't seem to have any effect.
        # Rotation image margins are set to black if .HasAlpha() is False.
        #
        #rotatedImage = wxImage.Rotate( self.angle, rotationCenterDummy, 
        #                               True, offsetAfterRotationDummy )
        # Insert a call to a wx filtering method here.
        
        # Center the rotated image on the client area.
        imageWid, imageHgt = wxImage.GetSize()
        offsetX = (clientWid - imageWid) / 2
        offsetY = (clientHgt - imageHgt) / 2
        # Display the rotated image. Only wxBitmaps can be displayed, not wxImages.
        # .DrawBitmap() autmatically "closes" the dc, meaning it finalizes the bitmap in some way.
        bufferedDC.DrawBitmap( self.scale_bitmap(wxImage.ConvertToBitmap(), imageWid/3, imageHgt/3), 0, 0 )
        #bufferedDC.DrawBitmap( self.scale_bitmap(wxImage.ConvertToBitmap(), clientWid, clientHgt), 0, 0 )
        #bufferedDC.DrawBitmap(wxImage.ConvertToBitmap(), 0, 0 )
        #self.SetSizer(self.sizer)
    
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)


class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Simple Grid Demo", size=(1000,900))
        self.hl = TestPanel(self)


if __name__ == "__main__":
    app= wx.App(None)
    frame= MyFrame(None)
    frame.Show()
    app.MainLoop()


    #def OnDrawTimer( self, event ) :
        #self.drawWindow.DrawRotated( self.imgFilename )             # The file is read in only once !
        #self.drawWindow.angle += self.drawWindow.angleIncrement     # Adjust for the next .DrawRotated()
    #end def                                                        #  on the next timer tick.

#end class TestFrame

