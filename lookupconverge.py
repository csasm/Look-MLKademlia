# Copyright (C) 2010 Sara Dar
# Released under GNU LGPL 2.1
# See LICENSE.txt for more information
import wx
import os
import sys
import decimal
import operator
from copy import copy
import nodeaddr as NodeAddr
import pickle
import Lookupconverge_ext as lucgee
#import queriesgiven as q
#import responsegiven as r
#import matchqandr as qr
#import mappings as map

class LookupConverge(wx.Frame):
    fname=''
    srctxt=''
    infotxt=''
    infohash=''
    #infohashlist=[]
    
    Qrecord=[]
    Rrecord=[]
    newResList=[]
    list=[]
    QueResList=[]
    list3=[]
    
    def __init__(self, parent, mytitle,qrlist, mysize):
        wx.Frame.__init__(self, parent, wx.ID_ANY, mytitle,
            size=(1440,900))
        #self.m=map.Mappings()
        #self.fname=filename
        self.infohash=''
        #self.infohashlist=infohashlist
        self.newResList=[]
        self.QueResList=qrlist
        self.CreateStatusBar()
        self.create_controls()
        if self.QueResList:
            self.load_combo()
        #unpicklefile = open('myfile.txt', 'r')

# now load the list that we pickled into a new object
        #self.list = pickle.load(unpicklefile)

# close the file, just for safety
        #unpicklefile.close()



        self.bindings()

        
    def bindings(self):
        #self.Bind(wx.EVT_BUTTON, self.open_file, id=1)
        self.Bind(wx.EVT_BUTTON, self.close_dlg, id=3)  
        self.Bind(wx.EVT_BUTTON, self.open_lookupconvergee, id=4)
        self.lc.Bind(wx.EVT_LIST_ITEM_SELECTED,self.onSelect)
        self.lc.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.onRightClick)  
              
    def load_combo(self):
            self.list2=[]
            for i in range(len(self.QueResList)):
                if self.QueResList[i][0].query_type == 'get_peers':
                    self.list2.append(self.QueResList[i])
            self.list3=[]
            def times(f,seq):
                number=0
                for i in seq:
                    temp=i[0].src_addr[0],repr(i[0].infohash)
                    if f==temp:
                        number=number+1
                return number
            def find(f, seq):
                for item in seq:
                    if f==item:                        
                        return True
                return False  
            for i in self.list2:
                temp=i[0].src_addr[0],repr(i[0].infohash)
                if not find(temp,self.list3):
                    if times(temp,self.list2)>10:
                        self.list3.append(temp)
            self.combo1.Clear()
            self.lc.DeleteAllItems()
            for i in self.list3:
                self.combo1.Append(i[0]+" : "+i[1])
            self.combo1.SetSelection(0)
            self.collect_values(None)


    def load_list(self):
        self.lc.DeleteAllItems()


        #self.fname=self.filetxt.GetValue()
        #source=self.srctxt.GetValue()
        #infoh=self.infobox.GetValue()


        #a=qr.MatchQandR(self.fname)
        #b=r.ResponseBisector(self.fname,infoh)
        counter=1
        start=0
        previousts=0
        distList=[]
        
        #self.Qrecord = a.get_peers_with_srcaddr_infohash(source,infoh)
        #self.Rrecord = b.get_peers_response()
        #self.list =a.get_peers_query_response_inline_with_src_infohash(source,infoh)
        #self.text.Clear()
        
        counter=1
       
        max_rows=len(self.list)
       
        for i,line in enumerate(self.list):
            #print 'hello'
            index = self.lc.InsertStringItem(max_rows, str(counter))
            counter=counter+1
            if not(line[1]=='bogus'):

        
                self.lc.SetStringItem(index, 1, str(line[0].ts))
                self.lc.SetStringItem(index, 2, str(line[1].ts))
                #d=decimal.Decimal(str(line[1].ts-line[0].ts))
                d=str(line[2])
                decimal.getcontext().prec = 4
                self.lc.SetStringItem(index, 3, str(d*1))
              
                self.lc.SetStringItem(index, 4, str(str(line[1].src_addr[0]))
                                      +':'+str(line[1].src_addr[1]))
                self.lc.SetStringItem(index, 5, str(line[0].hexaTid))
                self.lc.SetStringItem(index,6,
                                      str(str(line[0].dist_from_sender)
                                      +'/'+str(line[1].dist_from_sender)))
                self.lc.SetStringItem(index,7,str(line[1].nodes_distances))
                #print line[1].ts
                #if d < 0:
                    #self.lc.SetItemBackgroundColour(index,wx.RED)
                self.newResList.append(line)
                #self.lc.SetItemBackgroundColour(index,wx.RED)
            else:
                self.lc.SetStringItem(index, 1, str(line[0].ts))
                self.lc.SetStringItem(index, 2, '-')
                self.lc.SetStringItem(index, 3, '-')
                self.lc.SetStringItem(index, 4,str(str(line[0].dst_addr[0])
                                      +':'+str(line[0].dst_addr[1]))) 
                self.lc.SetStringItem(index, 5, str(line[0].hexaTid))
                self.lc.SetItemBackgroundColour(index,'light blue')
                self.newResList.append(line)
                    

    def create_controls(self):
	"""Called when the controls on Window are to be created"""
        # Create the static text widget and set the text
	#self.filelabel = wx.StaticText(self, label="File:")
        self.srclabel = wx.StaticText(self, label="Source Addr : Infohash ")
        self.peerslabel = wx.StaticText(self,label="Peers")
	#Create the Edit Field (or TextCtrl)
	#self.filetxt = wx.TextCtrl(self, size=wx.Size(200, -1),
                                                      #value=self.fname)
#        self.srctxt = wx.TextCtrl(self, size=wx.Size(100, -1),
#                                  value='192.16.125.181')
#        self.infotxt = wx.TextCtrl(self, size=wx.Size(100, -1),
#                                   value='3ef5cdcbcf57fecf0da0be4cff8d90fee1369649')
        self.combo1 = wx.ComboBox(self,
                              size=(500,wx.DefaultSize.y),
                              choices=self.list3)
        self.combo1.SetEditable(False)
        self.combo1.Bind(wx.wx.EVT_COMBOBOX,self.collect_values)
#28f2e5ea2bf87eae4bcd5e3fc9021844c01a4df9
        #self.browsebtn=wx.Button(self, 1, 'Browse', (50, 130))
        self.Cancelbtn=wx.Button(self, 3, 'Cancel', (50, 130))
        self.GraphicalButton=wx.Button(self, 4, 'Graphical', (50, 130))


        #create list cotrol

        self.lc = wx.ListCtrl(self, wx.ID_ANY,
        style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES)
        self.lc.InsertColumn(0,"No.")
        self.lc.SetColumnWidth(0, 40)
        self.lc.InsertColumn(1,"Query Time")
        self.lc.SetColumnWidth(1, 120)
        self.lc.InsertColumn(2,"Response Time")
        self.lc.SetColumnWidth(2, 120)
        self.lc.InsertColumn(3,"RTT")
        self.lc.SetColumnWidth(3,80 )
        self.lc.InsertColumn(4,"Responder")
        self.lc.SetColumnWidth(4, 160)
        self.lc.InsertColumn(5,"TID")
        self.lc.SetColumnWidth(5, 60)
       
        self.lc.InsertColumn(6,"Log Distance")
        self.lc.SetColumnWidth(6, 100)
        self.lc.InsertColumn(7,"Nodes Distance")
        self.lc.SetColumnWidth(7, 260)

        #self.loadList()
        self.text = wx.TextCtrl(self, wx.ID_ANY,
            value="PEERS",
            style=wx.TE_MULTILINE)




	# Horizontal sizer
        self.h_sizer0 = wx.BoxSizer(wx.HORIZONTAL)
	self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        #vertical sizer
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
	#Add to horizontal sizer
	#add the static text to the sizer, tell it not to resize
	#self.h_sizer1.Add(self.filelabel, 0)
	#Add 5 pixels between the static text and the edit
        #self.h_sizer1.AddSpacer((5,0))
        #self.h_sizer1.Add(self.filetxt,0)
        #self.h_sizer1.AddSpacer((5,0))
        #self.h_sizer1.Add(self.browsebtn, 0)

        self.h_sizer2.AddSpacer((20,0))
        self.h_sizer2.Add(self.srclabel,0)
        self.h_sizer2.AddSpacer((15,0))
        self.h_sizer2.Add(self.combo1,0)

#        self.h_sizer3.Add(self.infolabel,0)
#        self.h_sizer3.AddSpacer((5,0))
#        self.h_sizer3.Add(self.infotxt,1)
        self.h_sizer4.AddSpacer((20,0))
        self.h_sizer4.Add(self.GraphicalButton,0)
        self.h_sizer4.AddSpacer((20,0))
        self.h_sizer4.Add(self.Cancelbtn,0)
        
        self.h_sizer5.Add(self.lc, 3, flag=wx.ALL|wx.EXPAND, border=10)
        self.h_sizer6.Add(self.peerslabel,0)
        self.h_sizer7.Add(self.text, 3, flag=wx.ALL|wx.EXPAND, border=10)

        self.v_sizer.Add(self.h_sizer0,0,wx.EXPAND|wx.BOTTOM,10)
        self.v_sizer.Add(self.h_sizer1,0,wx.EXPAND|wx.BOTTOM,10)
        self.v_sizer.Add(self.h_sizer2,0,wx.EXPAND|wx.BOTTOM,10)
        self.v_sizer.Add(self.h_sizer4,0,wx.EXPAND|wx.BOTTOM,10)
        self.v_sizer.Add(self.h_sizer5,1,wx.ALL|wx.EXPAND,border=10)
        self.v_sizer.Add(self.h_sizer6,0,wx.EXPAND|wx.BOTTOM,10)
        self.v_sizer.Add(self.h_sizer7,0,wx.ALL|wx.EXPAND,border=10)
	#Set the sizer
	self.SetSizer(self.v_sizer)


    
    def onSelect(self, event):

        ix_selected = self.lc.GetNextItem(item=-1,
            geometry=wx.LIST_NEXT_ALL, state=wx.LIST_STATE_SELECTED)
        self.text.Clear()
        if not self.newResList[ix_selected][1]=='bogus':
            peers = str(self.newResList[ix_selected][1].peers)
        #print peers

            self.text.WriteText(str(peers))

    def onRightClick(self,event):
        ix_selected = self.lc.GetNextItem(item=-1,
            geometry=wx.LIST_NEXT_ALL, state=wx.LIST_STATE_SELECTED)
       
        nodesaddr = (self.newResList[ix_selected][1].nodes_address)
        nodesdist = str(self.newResList[ix_selected][1].nodes_distances)
        #print peers
        width = 1000
        height = 800
        obj=NodeAddr.Nodes(None, 'Nodes Addresses',nodesaddr,nodesdist, 
                               (width, height)).Show()

    def convert_list(self,list):
        def cmc(a):
            b=[]
            for i in a:
                if i.__class__.__name__!="list":
                    b.append(copy(i))
                else:
                    aa=cmc(i)
                    b.append(aa)                        
            return b
        TempA=[]
        ListC=[]
        for i in list:
            if i[1]!='bogus':
                TempA.append(cmc(i))
            else:
                ListC.append(i)
        ListA = cmc(TempA)
        for i in range(len(ListA)):
            for j in range(i+1,len(ListA)):
                if float(ListA[i][0].ts) > float(ListA[j][0].ts):
                    a=ListA[j]
                    ListA[j]=ListA[i]
                    ListA[i]=a
        ListB = cmc(TempA)
        for i in range(len(ListB)):
                for j in range(i+1,len(ListB)):
                        if float(ListB[i][1].ts) > float(ListB[j][1].ts):
                            a=ListB[j]
                            ListB[j]=ListB[i]
                            ListB[i]=a
        i=0
        j=0
        k=0
        ListD=[]
        while(i<len(ListA)):
            if(ListA[i][0].ts<ListB[j][1].ts):
                if(k<len(ListC)):
                    if(ListC[k][0].ts<ListA[i][0].ts):
                        a=cmc(ListC[k])
                        ListD.append(a)
                        k=k+1
                    else:
                        a=cmc(ListA[i])
                        a[1].ts="-"
                        a[1].nodes_distances="-"
                        ListD.append(a)
                        i=i+1
                else:
                    a=cmc(ListA[i])
                    a[1].ts="-"
                    a[1].nodes_distances="-"
                    ListD.append(a)
                    i=i+1
            else:
                if(k<len(ListC)):
                    if(ListC[k][0].ts<ListB[j][1].ts):
                        a=cmc(ListC[k])
                        ListD.append(a)
                        k=k+1
                    else:
                        a=cmc(ListB[j])
                        ListD.append(a)
                        j=j+1
                else:
                    a=cmc(ListB[j])
                    ListD.append(a)
                    j=j+1
        while(j<len(ListB)):
            if(k<len(ListC)):
                if(ListC[k][0].ts<ListB[j][1].ts):
                        a=cmc(ListC[k])
                        ListD.append(a)
                        k=k+1
                else:
                    a=cmc(ListB[j])
                    ListD.append(a)
                    j=j+1
            else:
                a=cmc(ListB[j])
                ListD.append(a)
                j=j+1
        while(k<len(ListC)):
            a=cmc(ListC[k])
            ListD.append(a)
            k=k+1
        return ListD    

    def collect_values(self,event):
        #fname=self.filetxt.GetValue()
        selected=self.combo1.GetCurrentSelection()
        if not selected==-1:
            src_addr=self.list3[selected][0]
            info_hash=self.list3[selected][1]
            self.list1=[]
            for i in self.list2:  
                if str(i[0].src_addr[0])==src_addr:
                    if repr(i[0].infohash)==info_hash:
                        self.list1.append(i)
        self.list=self.convert_list(self.list1)
        self.load_list()
        # import the pickle module


# lets create something to be pickled
# How about a list?
        #picklelist = ['one',2,'three','four',5,'can you count?']

# now create a file
# replace filename with the file you want to create
#        file = open('myfile.txt', 'w')

# now let's pickle picklelist
#        pickle.dump(self.list,file)

# close the file, and your pickling is complete
#        file.close()

    def list_with_src_infohash(self,source,infoh):
        self.list=[]
        for i in range(len(self.QueResList)):
            if self.QueResList[i][0].query_type == 'get_peers':
                if self.QueResList[i][0].src_addr[0]==source:
                    if repr(self.QueResList[i][0].infohash)==infoh:
                        self.list.append(self.QueResList[i])
         
        #self.load_list()

    def close_dlg(self,event):
        self.Destroy()

    def show_message(self):
        dlg = wx.MessageDialog(self,'Check src address and infohash',
                                   'Error', wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def match_nodeaddr_responder(self):
        pass
    def open_lookupconvergee(self,event):
        obj=lucgee.Lookupconverge_ext(None,"Lookup@Kademlia Visualization",self.list,(1440,900)).Show()

#app = wx.App(0)
#set title and size for the MyFrame instance
#mytitle = "Lookup Overview for...."
#width = 580
#height = 36
#LookupConverge(None, mytitle, (width, height)).Show()

#app.MainLoop()
