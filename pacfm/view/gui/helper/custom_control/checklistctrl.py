import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, size=(300,200), style=wx.LC_REPORT)
        CheckListCtrlMixin.__init__(self)
        
        self.checked_items= {}
        self.unchecked_items= {}
        self.SetLevel(1)
        #self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        #def OnItemActivated(self, evt):
        #    print self.ToggleItem(evt.m_itemIndex)
    
    def SetLevel(self, level):
        self.current_level = level
        if level not in self.unchecked_items:
            self.unchecked_items[level] = []

        if level not in self.checked_items:
            self.checked_items[level] = []


    # this is called by the base class when an item is checked/unchecked
    def OnCheckItem(self, index, flag):
        data = self.GetItemData(index)
        #title = musicdata[data][1]
        unchecked= self.unchecked_items[self.current_level]
        checked= self.checked_items[self.current_level]
        
        if flag:
            #print data
            what = "checked"
            if index in unchecked:
                checked.append(index)
                unchecked.remove(index)
        
        else:
            what = "unchecked"
           
            message= "You are about to remove this pathway from the analyses! Are you sure to proceed?"
            dlg = wx.MessageDialog(self, message,
                               'PACFM Warning!',
                               wx.YES_NO | wx.ICON_EXCLAMATION
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            response= dlg.ShowModal()
            if response == wx.ID_YES:
                unchecked.append(index)
                if index in checked:
                    checked.remove(index)
            
            else:
                self.ToggleItem(index)


