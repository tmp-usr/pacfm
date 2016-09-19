from StringIO import StringIO
import xml.etree.ElementTree as ET
from collections import OrderedDict

from pacfm.helper.config.model.objects import CircosSettingItem
from pacfm.helper.config.parser.parser import CircosConfigParser, SettingParser


confFile='k'
configparser= CircosConfigParser(confFile)
text, blocks = configparser.parse()
for block in blocks:
    #root= ET.fromstring(in_text)
    
    f = StringIO(block)
    depth=0
    for (event, node) in ET.iterparse(f, ['start', 'end', 'start-ns', 'end-ns']):
      
        if depth == 0:
            props= SettingParser(node.text).props
            #parent =  tree.AppendItem(root, node.tag )
            cci= CircosSettingItem(confFile, props, node.tag )
            parent=cci
            depth += 1
            
      

        if event == 'end':
            if depth > 1:
                parent = CircosSettingItem(confFile, props, node.tag )
                depth -= 1


        if event == 'start':
            props= SettingParser(node.text).props
            if props != OrderedDict():
                if node.tag != parent.item_tag: # tree.GetItemText(parent):    
                    child = CircosSettingItem(confFile, props, node.tag )  #tree.AppendItem(parent, node.tag)
                    #print child.item_tag
                    cci.settingList.append(child)
                    parent= child
                    depth += 1
    
    for ci in cci.settingList:
        for c in ci.settingList:
            print c.item_tag


