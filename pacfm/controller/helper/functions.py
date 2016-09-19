import wx
### refer to the source

def PilImageToWxImage( myPilImage) :
    myWxImage = wx.EmptyImage( *myPilImage.size )
    myPilImageCopy = myPilImage.copy()
    myPilImageCopyRGB = myPilImageCopy.convert( 'RGB' )    # Discard any alpha from the PIL image.
    myPilImageRgbData =myPilImageCopyRGB.tobytes()
    myWxImage.SetData( myPilImageRgbData )
    return myWxImage

