
import sys
import wx
import wx.lib.mixins.listctrl as listmix
import  wx.lib.colourselect as  csel
from collections import OrderedDict

import  wx.lib.scrolledpanel as scrolled



from wx.lib.itemspicker import ItemsPicker,  IP_REMOVE_FROM_CHOICES, IP_SORT_CHOICES, EVT_IP_SELECTION_CHANGED

#from ListCtrl import musicdata

#----------------------------------------------------------------------
ID=wx.ID_ANY



class LinksPanel(wx.Panel):
    def __init__(self, parent, biodb, links=None) :
        
        wx.Panel.__init__(self, parent, -1)


        self.initVariables(biodb, links)

#### init controls  #####
        #self.list = CheckListCtrl(self, ID,
        #                         style=wx.LC_REPORT
        #                         | wx.BORDER_NONE
        #                         | wx.LC_SORT_ASCENDING
        #                         )
        #print sizerLinks.GetCellSize(0,0)
        #self.scroll = wx.ScrolledWindow( self )
        #self.scroll.SetScrollRate(1,1)
        #self.scroll.EnableScrolling(True,True)

        self.scroll = scrolled.ScrolledPanel(self, -1, style = wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER, name="scroll" )

        
        
        self.txtLevel = wx.StaticText(id=ID,
              label=u'Level', parent=self)
        self.cbLevel = wx.Choice(choices=[],
                id=ID, name=u'cbLevel',
                parent=self)
        self.ip = ItemsPicker(self, size= wx.Size(500,200), ipStyle=  IP_REMOVE_FROM_CHOICES | IP_SORT_CHOICES)
        
##### bind events #########
        self.ip.Bind(EVT_IP_SELECTION_CHANGED, self.onSelectionChange)

##### set sizers  #########
        sizerLevel= wx.BoxSizer(wx.HORIZONTAL)
        sizerLevel.Add(self.txtLevel)
        sizerLevel.Add(self.cbLevel)

        self.sizerMain=wx.BoxSizer(wx.VERTICAL)
        
        self.sizerMain.Add(sizerLevel)
        self.sizerMain.Add(self.ip,1, wx.EXPAND)
        self.sizerMain.Add(self.scroll, 1, wx.EXPAND)

        self.initControls()

        self.SetSizerAndFit(self.sizerMain)
    
    def initVariables(self, biodb, links):
        self.biodb= biodb
        self.links= links

    def onSelectionChange(self, e):
        self.links.set_links_by_names(e.GetItems())
        for child in self.scroll.GetChildren(): 
            child.Destroy() 
        self.populateLinks(self.scroll)
        

    def loadLinks(self, links):
        link= links[0]
        self.cbLevel.SetSelection(link.level - 1)
        self.cbLevel.Disable()###
        names= [i.name for i in self.biodb.getFeaturesByLevel(link.level)]
        
        linkNames= [l.name for l in links]
        for name in linkNames:
            try:
                names.remove(name)
            except:
                print name, names

        self.ip.SetItems(names)
        self.ip.SetSelections(linkNames)

    def initControls(self):
        
        dbLevelCount= self.biodb.getLevelCount()
        levels= ["Level %s" %i for i in range(1, dbLevelCount)]
        
        self.cbLevel.SetItems(levels)
       
        self.loadLinks(self.links.items)

        #self.populateLinks(self.scroll, links.links)
        

#################################################
        
        self.SetSizerAndFit(self.sizerMain)

    def populateLinks(self, parent):
        """
            Links: dict of pathway name as key and (z-index, color) tuple as value
        """
        #if self.scroll:
        #    self.scroll.Destroy()
        
        #self.scroll = wx.ScrolledWindow( self ,size= wx.Size(200,200) )
        #self.scroll.SetScrollRate(1,1)
        #self.scroll.EnableScrolling(True,True)

        #parent=self.scroll
        links=self.links.items
        color=def_color=  (155,155,155)
        sizer= wx.FlexGridSizer(cols=3)
        i=0
        
        font = wx.Font(13, family= wx.FONTFAMILY_DEFAULT, style= wx.FONTSTYLE_NORMAL, weight= wx.FONTWEIGHT_BOLD)
        titlePW= wx.StaticText(parent, -1, "Pathway" )
        titlePW.SetFont(font)
        titleZindex= wx.StaticText(parent, -1, "z-index")

        titleZindex.SetFont(font)
        titleColor= wx.StaticText(parent, -1, "Color" )
        
        titleColor.SetFont(font)
        
        
        sizer.Add(titlePW,  flag=wx.BOTTOM | wx.LEFT | wx.TOP, border=10)
        sizer.Add(titleZindex, flag=wx.BOTTOM | wx.TOP, border=10 )
        sizer.Add(titleColor, flag=wx.BOTTOM | wx.TOP, border=10 )
        
        i+=1
        
        baseID= 1000
        for link in links:
            
            cbID= baseID+ 3*(i-1)+1
            chID= baseID+ 3*(i-1)+2
            cpID= baseID+ 3*(i-1)+3
            
            cb = wx.StaticText(parent, cbID, link.name)
            ch = wx.Choice(parent, chID, (100, 50), choices = map(str,range(1,15)))
            
            
            #cb.SetValue(link.checked)
            
            if link.z_index is not None:
                ch.SetStringSelection(str(link.z_index))
            else:
                ch.SetStringSelection("1")

            if link.color is not None:
                color= link.color
            
            else:
                color=def_color
           

            cp = csel.ColourSelect(parent, cpID, 'Pick', color ,size= wx.DefaultSize)
            
            
            
            ch.Bind(wx.EVT_CHOICE, self.onSelectZindex)
            cp.Bind(csel.EVT_COLOURSELECT, self.onSelectColour)
            
            sizer.Add(cb, 0,wx.LEFT, border= 10)
            sizer.Add(ch)
            sizer.Add(cp)
            
            i+=1
        parent.SetupScrolling() 
        ### below did not make any change
        #parent.SetScrollbars(0,10,0, 50, 0, 0 )
        parent.SetSizer(sizer)
        #self.sizerMain.Add(parent, 1, wx.EXPAND |wx.TOP ,border=5)
        #self.SetSizerAndFit(self.sizerMain)
        #return sizer

    def onSelectZindex(self, e):
        chId= e.GetId() 
        linkIndex= (chId-1000)/3
        z_index= e.GetString()
        
        link= self.links.items[linkIndex]
        link.z_index= int(z_index)
    
    def onSelectColour(self, e):
        cpId= e.GetId() 
        linkIndex= (cpId-1000)/3 -1
        color= e.GetValue()
        link= self.links.get_by_index(linkIndex)
        link.color= color  



class TestFrame(wx.Frame):
    def __init__(self, parent, biodb, links):
        wx.Frame.__init__(self, parent, -1, "Huge (virtual) Table Demo", size=(640,480))
        grid = LinksPanel(self, biodb, links)
        #grid.SetReadOnly(5,5, True)
#---------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    from pacfm import LinkContainer
    from biodb.sqling.selector import Selector
    
    biodb= Selector('kegg_orthology')
    
    app = wx.App()
    l= LinkContainer()
    l.load()

    frame = TestFrame(None, biodb, l)
    frame.Show(True)
    app.MainLoop()
#------------------------------------------------------------------


b="""        self.list = CheckListCtrl(self)
        sizer = wx.BoxSizer()
        
        
        sizer.Add(self.list, 1, wx.EXPAND)
        

        

        self.list.InsertColumn(0, "Pathway")
        self.list.InsertColumn(1, "z-index", wx.LIST_FORMAT_CENTER)

        for key, data in musicdata.iteritems():
            index = self.list.InsertStringItem(sys.maxint, data[0])
            self.list.SetStringItem(index, 1, data[1])
        #    self.list.SetStringItem(index, 2, data[2])
            self.list.SetItemData(index, key)
      
        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(1, 50)
        #self.list.SetColumnWidth(2, 100)

        self.list.CheckItem(0)
        self.list.CheckItem(3)
        #self.list.CheckItem(7)
        checkedIndexes= self.list.GetCheckedList() 
        nItems= self.list.GetItemCount()

        sizerColor = wx.GridBagSizer(nItems, 1)
        colorID= wx.NewId()
        for index in checkedIndexes:
            self.list.SetItemBackgroundColour(index,'green') 
            #sizerColor.Add(csel.ColourSelect(self, colorID+index, 'Color', (65,105,225), size= wx.DefaultSize), pos=(index,0), flag=wx.TOP)
        #sizerColor.Add(lblCutoff, pos=(0, 0),flag=wx.TOP,border=3)

        sizer.Add(sizerColor)

        self.SetSizer(sizer)


        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.list)
        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED , self.onActivated)
    

    def OnItemSelected(self, evt):
        pass
        #self.log.write('item selected: %s\n' % evt.m_itemIndex)
        
    def OnItemDeselected(self, evt):
        pass
        #self.log.write('item deselected: %s\n' % evt.m_itemIndex)
       
    def onActivated(self,evt):
        pass


"""
