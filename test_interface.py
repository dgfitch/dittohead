import wx
import gettext

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
    def __init__(self, *args, **kwds):
        # begin wxGlade: CopyFrame.__init__
        wx.Frame.__init__(self, *args, **kwds)
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.label_studies = wx.StaticText(self.panel, wx.ID_ANY, "Choose a study:")
        self.list_studies = wx.ListBox(self.panel, wx.ID_ANY, choices=[], style=wx.LB_ALWAYS_SB)
        self.label_username = wx.StaticText(self.panel, wx.ID_ANY, "Username")
        self.label_password = wx.StaticText(self.panel, wx.ID_ANY, "Password")
        self.text_username = wx.TextCtrl(self.panel, wx.ID_ANY, "")
        self.text_password = wx.TextCtrl(self.panel, wx.ID_ANY, "")
        self.copy_button = wx.Button(self.panel, wx.ID_ANY, "Copy")
        self.cancel_button = wx.Button(self.panel, wx.ID_ANY, "Cancel")
        self.edit_study_button = wx.Button(self.panel, wx.ID_ANY, "Edit Study")
        self.add_study_button = wx.Button(self.panel, wx.ID_ANY, "Add Study")
        self.label_preview = wx.StaticText(self.panel, wx.ID_ANY, "Stuff that is about to happen:")
        self.text_preview = wx.TextCtrl(self.panel, wx.ID_ANY, "", style=wx.TE_MULTILINE)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: CopyFrame.__set_properties
        self.SetTitle("dittohead")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: CopyFrame.__do_layout
        action_buttons = wx.BoxSizer(wx.HORIZONTAL)
        action_buttons.Add(self.copy_button, 0, wx.ALL, 0)
        action_buttons.Add((-1, -1), 1)
        action_buttons.Add(self.cancel_button, 0, wx.ALL, 0)

        study_buttons = wx.BoxSizer(wx.HORIZONTAL)
        study_buttons.Add(self.edit_study_button, 0, wx.ALL, 0)
        study_buttons.Add((-1, -1), 1)
        study_buttons.Add(self.add_study_button, 0, wx.ALL, 0)

        left_pane = wx.BoxSizer(wx.VERTICAL)
        left_pane.Add(self.label_studies, 0, wx.EXPAND, 0)
        left_pane.Add(self.list_studies, 1, wx.EXPAND | wx.ALL, 0)

        right_pane = wx.BoxSizer(wx.VERTICAL)
        right_pane.Add(self.label_username, 0, wx.EXPAND)
        right_pane.Add(self.text_username, 0, wx.EXPAND)
        right_pane.Add(self.label_password, 0, wx.EXPAND)
        right_pane.Add(self.text_password, 0, wx.EXPAND)
        right_pane.Add(self.label_preview, 0, wx.EXPAND)
        right_pane.Add(self.text_preview, 1, wx.EXPAND | wx.ALL, 0)
        
        hgap, vgap = 0, 0
        nrows, ncols = 2, 2
        fgs = wx.FlexGridSizer(nrows, ncols, hgap, vgap)

        b = 2
        fgs.AddMany([(left_pane, 1, wx.EXPAND | wx.ALL, b),
                     (right_pane, 1, wx.EXPAND | wx.ALL, b),
                     (study_buttons, 1, wx.EXPAND | wx.ALL, b),
                     (action_buttons, 1, wx.EXPAND | wx.ALL, b),
                    ])

        fgs.AddGrowableRow(0)
        fgs.AddGrowableCol(1)
        self.panel.SetSizer(fgs)

        self.Layout()
        # end wxGlade

    def OnSize(self, evt):
        self.window_1.Fit(self)
        self.Layout()


    def LoadStudies(self, studies, last_users, last_times):
        self.studies = studies
        self.last_users = last_users
        self.last_times = last_times

    
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

