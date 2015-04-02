import wx
import wx.lib.scrolledpanel as scrolled

from copy import copy_files

"""
        # File view selection
        self.study_panel = scrolled.ScrolledPanel(self.panel, -1, 
                                 style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER, name="panel1")
        self.study_panel.SetAutoLayout(1)
        self.study_panel.SetupScrolling()

        self.study_sizer = wx.BoxSizer(wx.VERTICAL)
        for study in studies:
            b = wx.Button(self.study_panel, -1, study['name'])
            self.study_sizer.Add(b, 0, wx.EXPAND)

        self.study_panel.SetSizer(self.study_sizer)
"""


class CopyFrame(wx.Frame):
    def __init__(self, parent, title, studies, last_users = {}, last_times = {}):
        self.studies = studies
        self.last_users = last_users
        self.last_times = last_times

        wx.Frame.__init__(self, parent, title=title, size=(300,500))

        newFont = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        newFont.SetPixelSize((10,24))
        self.SetFont(newFont)

        # Add a panel so it looks the same on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)

        # Buttons
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []

        self.cancel = wx.Button(self, -1, "Cancel")
        self.buttons.append(self.cancel)
        self.button_sizer.Add(self.cancel, 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.CancelClick, self.cancel)

        self.copy = wx.Button(self, -1, "&Copy")
        self.copy.Disable()
        self.buttons.append(self.copy)
        self.button_sizer.Add(self.copy, 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.CopyClick, self.copy)


        # Split
        self.split = wx.Panel(self, wx.ID_ANY)
        self.split_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Studies listing
        self.studies = wx.ListBox(self.split, wx.ID_ANY, style=wx.LB_SINGLE)


        # Upload
        self.upload = wx.Panel(self, wx.ID_ANY)
        self.upload_sizer = wx.BoxSizer(wx.VERTICAL)

        # User and password entry
        self.user = wx.Panel(self.upload, wx.ID_ANY)

        # Preview of what's going to be copied
        self.preview = wx.Panel(self.upload, wx.ID_ANY)

        self.upload_sizer.Add(self.user, 3, wx.EXPAND)
        self.upload_sizer.Add(self.preview, 2, wx.EXPAND)
        self.upload.SetSizer(self.upload_sizer)


        self.split_sizer.Add(self.studies, 1, wx.EXPAND)
        self.split_sizer.Add(self.upload, 2, wx.EXPAND)
        self.split.SetSizer(self.split_sizer)


        # Main sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.split, 1, wx.EXPAND)
        self.sizer.Add(self.button_sizer, 0, wx.EXPAND)
        self.panel.SetSizer(self.sizer)

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

