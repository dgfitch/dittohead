import wx
from copy import copy_files

class DFrame(wx.Frame):
    def __init__(self, parent, title, studies, last_users = {}, last_times = {}):
        self.studies = studies
        self.last_users = last_users
        self.last_times = last_times

        wx.Frame.__init__(self, parent, title=title, size=(200,400))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []

        self.cancel = wx.Button(self, -1, "Cancel")
        self.buttons.append(self.cancel)
        self.buttonSizer.Add(self.cancel, 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.CancelClick, self.cancel)

        self.copy = wx.Button(self, -1, "&Copy")
        self.buttons.append(self.copy)
        self.buttonSizer.Add(self.copy, 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.CopyClick, self.copy)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control, 1, wx.EXPAND)
        self.sizer.Add(self.buttonSizer, 0, wx.EXPAND)

        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show()

    
    def CancelClick(self, event):
        self.Destroy()

    def CopyClick(self, event):
        """
        copy_files(
            user=user, password=password, 
            localfile=r"c:\DanTemp\git\pySketch",
            remotefile="dittohead_copy"
        )
        """

        # Reorder self.last_users or add a new entry if needed
        # self.last_users["TEST"] = "yay"
        self.Destroy()

