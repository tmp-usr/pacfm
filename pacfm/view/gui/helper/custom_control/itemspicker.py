from wx.lib.itemspicker import ItemsPicker,  IP_REMOVE_FROM_CHOICES,EVT_IP_SELECTION_CHANGED, IP_SORT_CHOICES
import wx

class ItemsPickerPanel(wx.Panel):
    def __init__(self,parent, items):
        wx.Panel.__init__(self,parent)
        sizer =wx.BoxSizer(wx.VERTICAL)
        #b = wx.Button(self, -1, "Add Item")
        #b.Bind(wx.EVT_BUTTON, self.OnAdd)
        self.ip = ItemsPicker(self,-1, 
                        items, '', '',ipStyle =IP_REMOVE_FROM_CHOICES | IP_SORT_CHOICES )
        self.ip.Bind(EVT_IP_SELECTION_CHANGED, self.OnSelectionChange)
        self.ip._source.SetMinSize((-1,100))
        sizer.Add(self.ip, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.itemCount = 3
        #self.Fit()
            
    def OnAdd(self,e):
        items = self.ip.GetItems()
        self.itemCount += 1
        #newItem = "item%d" % self.itemCount
        self.ip.SetItems(items + [newItem])
        
    def OnSelectionChange(self, e):
        print e.GetItems()
        #self.log.write("EVT_IP_SELECTION_CHANGED %s\n" % \
        #                ",".join(e.GetItems()))


