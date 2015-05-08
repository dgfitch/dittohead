import wx
import gettext

from copy import copy_files

FONT_SIZE = (8,20)

class StudyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)

        font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPixelSize(FONT_SIZE)
        self.SetFont(font)

        LABEL_WIDTH = 300
        TEXTBOX_WIDTH = 300

        self.panel = wx.Panel(self, wx.ID_ANY)
        l1 = wx.StaticText(self.panel, -1, 'Study Name:', (-1, -1), (-1, -1), wx.ALIGN_RIGHT)
        l2 = wx.StaticText(self.panel, -1, 'Extra Contact Emails (use commas):', (-1, -1), (-1, -1), wx.ALIGN_RIGHT)
        l3 = wx.StaticText(self.panel, -1, 'Local Directory:', (-1, -1), (-1, -1), wx.ALIGN_RIGHT)
        self.text_name = wx.TextCtrl(self.panel, -1, '', (-1, -1), (TEXTBOX_WIDTH, -1))
        self.text_extra_contacts = wx.TextCtrl(self.panel, -1, '', (-1, -1), (TEXTBOX_WIDTH, -1))
        self.text_local_directory = wx.TextCtrl(self.panel, -1, '', (-1, -1), (TEXTBOX_WIDTH, -1))
        b1 = wx.Button(self.panel, wx.NewId(), '&OK', (-1, -1), wx.DefaultSize)
        b2 = wx.Button(self.panel, wx.NewId(), '&Cancel', (-1, -1), wx.DefaultSize)
        staline = wx.StaticLine(self.panel, wx.NewId(), (-1, -1), (-1, 2), wx.LI_HORIZONTAL)

        self.Bind(wx.EVT_BUTTON, self.OkClick, b1)
        self.Bind(wx.EVT_BUTTON, self.CancelClick, b2)

        b = 2
        w = LABEL_WIDTH
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1.Add(l1, 0, wx.RIGHT, b)
        hsizer1.Add(self.text_name, 1, wx.GROW, b)
        hsizer1.SetItemMinSize(l1, (w, -1))

        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2.Add(l2, 0, wx.RIGHT, b)
        hsizer2.Add(self.text_extra_contacts, 1, wx.GROW, b)
        hsizer2.SetItemMinSize(l2, (w, -1))

        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer3.Add(l3, 0, wx.RIGHT, b)
        hsizer3.Add(self.text_local_directory, 1, wx.GROW, b)
        hsizer3.SetItemMinSize(l3, (w, -1))

        hsizer4 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer4.Add(b1, 0)
        hsizer4.Add(b2, 0, wx.LEFT, 10)

        b = 5
        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        vsizer1.Add(hsizer1, 0, wx.EXPAND | wx.ALL, b)
        vsizer1.Add(hsizer2, 0, wx.EXPAND | wx.ALL, b)
        vsizer1.Add(hsizer3, 0, wx.EXPAND | wx.ALL, b)
        vsizer1.Add(staline, 0, wx.GROW | wx.ALL, b)
        vsizer1.Add(hsizer4, 0, wx.ALIGN_RIGHT | wx.ALL, b)

        self.panel.SetSizerAndFit(vsizer1)
        self.SetClientSize(vsizer1.GetSize())

    def AddStudy(self, studies):
        self.isNew = True
        self.studies = studies

    def EditStudy(self, studies, name):
        self.isNew = False
        self.studies = studies
        self.original_name = name
        for s in self.studies:
            if s["name"] == name:
                break
        else:
            raise Exception("Trying to edit a nonexistent study {0} in hash {1}".format(name, studies))
        
        self.text_name.SetValue(s["name"])
        if "extra_contacts" in s: self.text_extra_contacts.SetValue(s["extra_contacts"])
        if "local_directory" in s: self.text_local_directory.SetValue(s["local_directory"])
        

    def OkClick(self, event):
        new_name = self.text_name.GetValue()

        if new_name == "":
            raise Exception("Trying to save changes to a nonexistent study {0} in hash {1}".format(self.original_name, studies))

        if new_name != self.original_name:
            for s in self.studies:
                if s["name"] == new_name:
                    raise Exception("Tried to rename study originally named {0} as {1} when a study with that name already existed.".format(self.original_name, new_name))

        for s in self.studies:
            if s["name"] == self.original_name:
                break
        else:
            raise Exception("Trying to save changes to a nonexistent study {0} in hash {1}".format(self.original_name, studies))

        s["name"] = new_name
        s["extra_contacts"] = self.text_extra_contacts.GetValue()
        s["local_directory"] = self.text_local_directory.GetValue()
        
        self.Destroy()

    def CancelClick(self, event):
        self.Destroy()


class CopyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: CopyFrame.__init__
        wx.Frame.__init__(self, *args, **kwds)

        font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPixelSize(FONT_SIZE)
        self.SetFont(font)

        self.panel = wx.Panel(self, wx.ID_ANY)
        self.label_studies = wx.StaticText(self.panel, wx.ID_ANY, "Choose a study:")
        self.list_studies = wx.ListBox(self.panel, wx.ID_ANY, choices=[], style=wx.LB_ALWAYS_SB)
        self.label_username = wx.StaticText(self.panel, wx.ID_ANY, "Username")
        self.label_password = wx.StaticText(self.panel, wx.ID_ANY, "Password")
        self.combo_username = wx.ComboBox(self.panel, wx.ID_ANY, "")
        self.text_password = wx.TextCtrl(self.panel, wx.ID_ANY, "", style=wx.TE_PASSWORD)
        self.copy_button = wx.Button(self.panel, wx.ID_ANY, "Copy")
        self.cancel_button = wx.Button(self.panel, wx.ID_ANY, "Cancel")
        self.edit_study_button = wx.Button(self.panel, wx.ID_ANY, "Edit Study")
        self.add_study_button = wx.Button(self.panel, wx.ID_ANY, "Add Study")
        self.label_preview = wx.StaticText(self.panel, wx.ID_ANY, "Preview:")
        self.text_preview = wx.TextCtrl(self.panel, wx.ID_ANY, "", style=wx.TE_MULTILINE)

        self.__set_properties()
        self.__bind_events()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: CopyFrame.__set_properties
        self.SetTitle("dittohead")
        self.edit_study_button.Enable(False)
        self.copy_button.Enable(False)
        # end wxGlade

    def __bind_events(self):
        self.Bind(wx.EVT_BUTTON, self.CancelClick, self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.CopyClick, self.copy_button)

        self.Bind(wx.EVT_BUTTON, self.EditStudyClick, self.edit_study_button)
        self.Bind(wx.EVT_BUTTON, self.AddStudyClick, self.add_study_button)

        self.Bind(wx.EVT_LISTBOX, self.StudyClick, self.list_studies)

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
        right_pane.Add(self.combo_username, 0, wx.EXPAND)
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


    def LoadStudies(self, log, studies, last_users, last_times):
        self.studies = studies
        self.last_users = last_users
        self.last_times = last_times

        for s in studies:
            self.list_studies.Append(s["name"])

    
    def CancelClick(self, event):
        self.Destroy()

    def StudyClick(self, event):
        self.selected_study = self.list_studies.GetStringSelection()
        if self.selected_study:
            self.edit_study_button.Enable(True)
            self.copy_button.Enable(True)

        for s in self.studies:
            if s["name"] == self.selected_study:
                if self.selected_study in self.last_times:
                    self.last_time = self.last_times[self.selected_study]
                    self.label_preview.SetValue("Preview: ({0} last ran at {1})".format(self.selected_study, self.last_time))

                users = self.combo_username
                users.Clear()

                if self.selected_study in self.last_users:
                    for u in self.last_users[self.selected_study]:
                        users.Append(u)
                        if self.text_password.GetValue() == "":
                            users.SetSelection(0)


    def AddStudyClick(self, event):
        study_frame = StudyFrame(self, wx.ID_ANY, "Add Study")
        study_frame.AddStudy(self.studies)
        study_frame.Show()

    def EditStudyClick(self, event):
        study_frame = StudyFrame(self, wx.ID_ANY, "Edit Study")
        study_frame.EditStudy(self.studies, self.list_studies.GetStringSelection())
        study_frame.Show()

    def StudiesChanged(self):
        True

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

