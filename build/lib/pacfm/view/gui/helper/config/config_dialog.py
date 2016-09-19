import wx 
from parser.circos_config_parser import CircosConfigParser, SettingParser 
from StringIO import StringIO
from collections import OrderedDict
import xml.etree.ElementTree as ET


ID= wx.ID_ANY
class TreeCtrlPanel(wx.Panel):
    def __init__(self, parent):
        # Use the WANTS_CHARS style so the panel doesn't eat the Return key.
        wx.Panel.__init__(self, parent, -1,style= wx.WANTS_CHARS |  wx.BORDER_SUNKEN) #style=wx.WANTS_CHARS)
        

        self.tree = wx.TreeCtrl(self, ID, wx.DefaultPosition, wx.DefaultSize,
                               wx.TR_HAS_BUTTONS
                               #| wx.TR_MULTIPLE
                               #| wx.TR_HIDE_ROOT
                               )
        self.SetBackgroundColour('white')
        s=wx.BoxSizer(wx.VERTICAL)
        s.Add(self.tree, 1, wx.EXPAND | wx.ALL, border=5)
        
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        
        self.SetSizer(s)
   
        self.item = self.tree.GetRootItem()

    def OnSelChanged(self, e):
        pass
    
    def OnSelChanged(self, e):
        self.item = e.GetItem()

        if self.item:
            #if self.item == tree.GetRootItem():
            #    props= rootProps
            #else:
            props= self.tree.GetPyData(self.item)
            ### funny coding but inevitable! sorry
            self.GetParent().GetParent().GetParent().buildPropPanel(self.GetParent().propPanel, props)
        
        e.Skip()


class ConfigPanel(wx.SplitterWindow):
    def __init__(self, parent):
        wx.SplitterWindow.__init__(self, parent, ID, style=wx.SP_LIVE_UPDATE | wx.SP_3DSASH )
        self.treePanel = TreeCtrlPanel(self)
        self.propPanel = wx.Panel(self, style=wx.BORDER_SUNKEN)
      
        self.SplitVertically(self.treePanel, self.propPanel,  200)
        
        #self.Layout()

class ConfigBookDialog(wx.Dialog):
    global configList, normAlgorithmList
    configList=['conf','plots','ideogram']
   
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "Circos Configuration Settings",  size=(640,480) )
        
        self.nb=wx.Notebook(self,  -1, style= wx.NO_BORDER)
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             ##wx.NB_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             
        
        
        self.configParsers={}
        
        self.initPages()

        #nb.AddPage(self.splitter,'1')
        #nb.AddPage(wx.SplitterWindow(nb, -1, style=wx.SP_LIVE_UPDATE | wx.SP_3DSASH ),'2')

        #nb.AddPage(wx.SplitterWindow(nb, -1, style=wx.SP_LIVE_UPDATE | wx.SP_3DSASH ),'3')
        
        sizerPanel= wx.BoxSizer(wx.HORIZONTAL)
        sizerPanel.Add(self.nb, 1, wx.EXPAND |wx.ALL , border=5)
 
        #self.splitter.SetMinimumPaneSize(20)
        

        self.SetSizer(sizerPanel)
        #self.Layout()
        self.Show() 
    
    def initPages(self):
        for configType in configList:
            configParser= CircosConfigParser(configType)
            #rootProps, blocks= configParser.parse()
            #print rootprops
            
            #try:
            #    rootProps= SettingParser(text).props
            #except:
            #    rootProps={}

            
            
            
            #####
            pnlConfig= ConfigPanel(self.nb)

            self.initTree(pnlConfig.treePanel.tree, configParser)
            
            rootItem= pnlConfig.treePanel.tree.GetRootItem()
            rootProps= pnlConfig.treePanel.tree.GetPyData(rootItem)
            
            self.buildPropPanel(pnlConfig.propPanel, rootProps)
            self.nb.AddPage(pnlConfig, configType)
            self.configParsers[configType] = configParser
        
    
    def onValueChanged(self,e):
        #print e.GetString()
        self.changedText= e.GetString()
        self.changedID= e.GetId()
        #c=e.GetClientObject()
        #if c.
    
        #e.Skip()

    def onFocusGone(self,e):
        if e.GetId() == self.changedID:
            #print self.changedText
           # self.changedID =-1
            curTree= self.curTreePanel.tree
            curItem= curTree.GetSelection()
            
            rootItem= curTree.GetRootItem()
            
            #print str(rootItem)
            #print curTree.GetItemText(rootItem)
            root_tag=self.nb.GetPageText(self.nb.GetSelection())
            #print rootItem
            if curItem == rootItem:
                item_tag= root_tag
            else:    
                item_tag= curTree.GetItemText(curItem)
                parent_tag=  curTree.GetItemText(curTree.GetItemParent(curItem))
            data= curTree.GetPyData(curItem)
            label= self.FindWindowById(self.changedID-1)#.GetString()
            prop= label.GetLabel()
            value= self.changedText
           
            #print prop, value
            if 'index' in data: # and item_tag is not root:
                self.configParsers[root_tag].set(prop, value, item_tag, 'index', data['index'] )
            else:
                self.configParsers[root_tag].set(prop, value)
        
        #e.Skip()




    def initTree(self, tree, configParser):
        # NOTE:  For some reason tree items have to have a data object in
        #        order to be sorted.  Since our compare just uses the labels
        #        we don't need any real data, so we'll just use None below for
        #        the item data.
        #isz = (16,16)
        #il = wx.ImageList(isz[0], isz[1])
        #fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        #fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        
        #print configParser.configType
        tree.root= tree.AddRoot("%s.conf" % configParser.configType)
        
        
        #tree.SetPyData(tree.root, None)
        #tree.SetItemImage(tree.root, fldridx, wx.TreeItemIcon_Normal)
        #tree.SetItemImage(tree.root, fldropenidx, wx.TreeItemIcon_Expanded)
        ### TODO: Check if this is required
        #tree.SetImageList(il)
        #self.il = il
        
        self.appendTreeItems(tree, configParser)
        tree.Expand(tree.root)

    def appendTreeItems(self, tree, configParser):
        '''
        ideally we would build a tree object here as an adapter to fill in data. this function does the same job eliminating the tree model.
        '''
        rootProps, blocks = configParser.parse()
        
        if rootProps: 
            rootItem=  tree.GetRootItem()
            tree.SetPyData(rootItem, rootProps)
        
        for block in blocks:
            f = StringIO(block)
            depth=0
            for (event, node) in ET.iterparse(f, ['start', 'end', 'start-ns', 'end-ns']):
                if depth == 0:
                    props= SettingParser(node.text).props
                    parent =  tree.AppendItem(tree.root, node.tag )
                    tree.SetPyData(parent, props)
                    depth += 1
                    
                if event == 'end':
                    if depth > 1:
                        parent= tree.GetItemParent(child)
                        depth -= 1

                if event == 'start':
                    props= SettingParser(node.text).props
                    if props != OrderedDict():
                        if node.tag != tree.GetItemText(parent):    
                            child =  tree.AppendItem(parent, node.tag)
                            tree.SetPyData(child, props)
                            parent= child
                            depth += 1
            
    
    def buildPropPanel(self, propPanel, props):
        # wx.Panel(splitter, style=sty)
        for child in propPanel.GetChildren(): 
            child.Destroy() 
        
        sizerMain= wx.GridBagSizer(5, 5)
        #sizerMain.SetFlexibleDirection(wx.VERTICAL)
        
        #sizerMain.Add((0,10))
        labelID= wx.NewId() #gives consecutive numbers for supposedly randomized ids
        row=0
        if props:
            for k,v in props.iteritems():
                #izer= wx.BoxSizer(wx.HORIZONTAL) 
                #print id(k)
                #if k != 'index':
                label=wx.StaticText(propPanel, id= labelID, label=k ) 
                text= wx.TextCtrl(propPanel, id= labelID+1, value=v )
                
                text.Bind(wx.EVT_TEXT, self.onValueChanged)
                text.Bind(wx.EVT_KILL_FOCUS, self.onFocusGone)
                #sizer.Add((10,0))
                #sizerMain.Add(sizer)
                if k == 'file' :
                    sizerMain.Add(label,pos=(row,0), flag= wx.ALIGN_LEFT | wx.LEFT, border= 20 )
                    sizerMain.Add(text, pos= (row,1), span=(1,10),  flag= wx.EXPAND )
                else:
                    sizerMain.Add(label,pos=(row,0), flag= wx.ALIGN_LEFT | wx.LEFT, border= 20 )
                    sizerMain.Add(text, pos= (row,1), span=(1,1),flag=  wx.EXPAND )
                row+=1
                labelID+=2
            
        sizerPanel= wx.BoxSizer(wx.VERTICAL)
        sizerPanel.Add(sizerMain, 1,  wx.TOP | wx.RIGHT | wx.ALIGN_LEFT | wx.EXPAND , border=10)
        
        self.curConfigPage= self.nb.GetSelection()
        self.curTreePanel= propPanel.GetParent().treePanel
        self.curPropPanel= propPanel

        propPanel.SetSizer(sizerPanel)
        propPanel.Layout() #this was important 

