import wx
import gettext
import os.path
from datetime import *

from copy import copy_files

# Hack so icon works right on windows, see http://stackoverflow.com/questions/15223952/wxpython-icon-for-task-bar
"""
import ctypes
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
"""

FONT_SIZE = (8,20)

class DittoheadFrame(wx.Frame):
    """
    Some shared font and icon settings for windows in this app.
    """
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)

        font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPixelSize(FONT_SIZE)
        self.SetFont(font)

        if os.path.isfile('dittohead.ico'):
            icon = wx.Icon('dittohead.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(icon)


class StudyFrame(DittoheadFrame):
    def __init__(self, *args, **kwds):
        DittoheadFrame.__init__(self, *args, **kwds)

        self.callback = None

        LABEL_WIDTH = 300
        TEXTBOX_WIDTH = 300

        self.panel = wx.Panel(self, wx.ID_ANY)
        l1 = wx.StaticText(self.panel, -1, 'Study Name:', (-1, -1), (-1, -1), wx.ALIGN_RIGHT)
        l2 = wx.StaticText(self.panel, -1, 'Extra Contact Emails (use commas):', (-1, -1), (-1, -1), wx.ALIGN_RIGHT)
        l3 = wx.StaticText(self.panel, -1, 'Local Directory:', (-1, -1), (-1, -1), wx.ALIGN_RIGHT)
        l4 = wx.StaticText(self.panel, -1, 'Remote Directory:', (-1, -1), (-1, -1), wx.ALIGN_RIGHT)
        self.text_name = wx.TextCtrl(self.panel, -1, '', (-1, -1), (TEXTBOX_WIDTH, -1))
        self.text_extra_contacts = wx.TextCtrl(self.panel, -1, '', (-1, -1), (TEXTBOX_WIDTH, -1))
        self.text_local_directory = wx.TextCtrl(self.panel, -1, '', (-1, -1), (TEXTBOX_WIDTH, -1))
        self.text_remote_directory = wx.TextCtrl(self.panel, -1, '', (-1, -1), (TEXTBOX_WIDTH, -1))
        b1 = wx.Button(self.panel, wx.NewId(), '&OK', (-1, -1), wx.DefaultSize)
        b2 = wx.Button(self.panel, wx.NewId(), '&Cancel', (-1, -1), wx.DefaultSize)
        staline = wx.StaticLine(self.panel, wx.NewId(), (-1, -1), (-1, 2), wx.LI_HORIZONTAL)

        b1.SetDefault()

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
        hsizer4.Add(l4, 0, wx.RIGHT, b)
        hsizer4.Add(self.text_remote_directory, 1, wx.GROW, b)
        hsizer4.SetItemMinSize(l4, (w, -1))

        hsizerLast = wx.BoxSizer(wx.HORIZONTAL)
        hsizerLast.Add(b1, 0)
        hsizerLast.Add(b2, 0, wx.LEFT, 10)

        b = 6
        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        vsizer1.Add(hsizer1, 0, wx.EXPAND | wx.ALL, b)
        vsizer1.Add(hsizer2, 0, wx.EXPAND | wx.ALL, b)
        vsizer1.Add(hsizer3, 0, wx.EXPAND | wx.ALL, b)
        vsizer1.Add(hsizer4, 0, wx.EXPAND | wx.ALL, b)
        vsizer1.Add(staline, 0, wx.GROW | wx.ALL, b)
        vsizer1.Add(hsizerLast, 0, wx.ALIGN_RIGHT | wx.ALL, b)

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
        if "remote_directory" in s: self.text_remote_directory.SetValue(s["remote_directory"])
        

    def OkClick(self, event):
        new_name = self.text_name.GetValue()

        if new_name == "":
            raise Exception("Trying to save changes to a nonexistent study {0} in hash {1}".format(self.original_name, studies))

        if self.isNew:
            s = {}
            self.studies.append(s)
        else:
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
        s["remote_directory"] = self.text_remote_directory.GetValue()

        if self.callback: self.callback()
        
        self.Destroy()

    def CancelClick(self, event):
        self.Destroy()


class CopyFrame(DittoheadFrame):
    def __init__(self, *args, **kwds):
        DittoheadFrame.__init__(self, *args, **kwds)

        self.selected_study = None
        self.last_refreshed_files = None
        self.files = []

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

        self.copy_status = wx.StaticText(self.panel, wx.ID_ANY, "Copying:")
        self.copy_gauge = wx.Gauge(self.panel, wx.ID_ANY)

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
        self.copy_button.SetDefault()

        self.copy_status.Hide()
        self.copy_gauge.Hide()
        # end wxGlade

    def __bind_events(self):
        self.Bind(wx.EVT_BUTTON, self.CancelClick, self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.CopyClick, self.copy_button)

        self.Bind(wx.EVT_BUTTON, self.EditStudyClick, self.edit_study_button)
        self.Bind(wx.EVT_BUTTON, self.AddStudyClick, self.add_study_button)

        self.Bind(wx.EVT_LISTBOX, self.StudyClick, self.list_studies)
        self.Bind(wx.EVT_TEXT, self.UserChanged, self.combo_username)
        self.Bind(wx.EVT_COMBOBOX, self.UserChanged, self.combo_username)
        self.Bind(wx.EVT_TEXT, self.PasswordChanged, self.text_password)

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

        right_pane.Add(self.copy_status, 0, wx.EXPAND)
        right_pane.Add(self.copy_gauge, 0, wx.EXPAND)

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


    def LoadStudies(self, log, studies, last_users):
        self.log = log
        self.studies = studies
        self.last_users = last_users
        self.ShowStudies()


    def ShowStudies(self):
        self.list_studies.Clear()
        for s in self.studies:
            self.list_studies.Append(s["name"])

    
    def CancelClick(self, event):
        self.Destroy()

    def EnableEditStudy(self):
        if self.selected_study:
            self.edit_study_button.Enable(True)
        else:
            self.edit_study_button.Enable(False)

    def EnableCopy(self):
        value = self.selected_study != None and self.combo_username.GetValue() != "" and self.text_password.GetValue() != ""
        self.copy_button.Enable(value)

    def UserChanged(self, event):
        self.EnableCopy()

    def PasswordChanged(self, event):
        self.EnableCopy()

    def StudyClick(self, event):
        selection = self.list_studies.GetStringSelection()
        if selection == self.selected_study:
            return

        self.selected_study = self.list_studies.GetStringSelection()

        for s in self.studies:
            if s["name"] == self.selected_study:
                if "last_time" in s:
                    self.label_preview.SetLabel("Preview: ({0} last ran at {1})".format(self.selected_study, s["last_time"]))
                    self.Layout()

                users = self.combo_username
                previous_user_value = users.GetValue()
                users.Clear()

                if self.selected_study in self.last_users:
                    for u in self.last_users[self.selected_study]:
                        users.Append(u)

                if self.text_password.GetValue() == "" and users.GetCount() > 0:
                    users.SetSelection(0)
                else:
                    users.SetValue(previous_user_value)

                self.UpdatePreview()
                break

        self.EnableEditStudy()
        self.EnableCopy()


    def AddStudyClick(self, event):
        study_frame = StudyFrame(self, wx.ID_ANY, "Add Study")
        study_frame.AddStudy(self.studies)
        study_frame.callback = self.ShowStudies
        study_frame.Show()

    def EditStudyClick(self, event):
        study_frame = StudyFrame(self, wx.ID_ANY, "Edit Study")
        study_frame.EditStudy(self.studies, self.list_studies.GetStringSelection())
        study_frame.callback = self.ShowStudies
        study_frame.Show()


    def UpdatePreview(self):
        files = self.FilesToCopy()
        if len(files) == 0:
            p = "No new data files found."
        else:
            p = "New files found:\n\n"
            for f in files:
                p += "Path: '{0}', {1}, modified at {2}\n => {3}\n\n".format(f['local_path'], f['size'], f['mtime'], f['remote_path'])

        self.text_preview.SetValue(p)

    def FilesToCopy(self):
        if not self.selected_study: return []

        # Nicked from http://stackoverflow.com/questions/1094841/
        def sizeof_fmt(num, suffix='B'):
            for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
                if abs(num) < 1024.0:
                    return "%3.1f%s%s" % (num, unit, suffix)
                num /= 1024.0
            return "%.1f%s%s" % (num, 'Yi', suffix)

        self.last_refreshed_files = datetime.now()

        for s in self.studies:
            if s["name"] == self.selected_study:
                if "last_time" in s:
                    last_time = s["last_time"]
                else:
                    last_time = datetime(1969,8,8)

                result = []

                walk_path = s["local_directory"]
                if not os.path.isdir(walk_path):
                    return []

                # Iterate over local directory looking for things > last_time

                wait = wx.BusyCursor()

                for root, dirs, files in os.walk(walk_path):
                    for name in files:
                        full_file_path = os.path.join(root,name)
                        remote_path = os.path.relpath(full_file_path, walk_path).replace("\\", "/")

                        epoch = os.path.getmtime(full_file_path)
                        mtime = datetime.fromtimestamp(epoch)

                        if mtime > last_time:
                            size = sizeof_fmt(os.path.getsize(full_file_path))
                            result.append(dict(local_path = full_file_path, remote_path = remote_path, size = size, mtime = mtime, will_copy = True))

                    if '.git' in dirs:
                        dirs.remove('.git')


                del wait

                self.files = result
                return result

        return []


    def PrepareUIForCopying(self, files):
        self.copy_status.Show()
        self.copy_gauge.Show()
        self.copy_button.Hide()
        self.Layout()

    def CopyingFile(self, num, total, local_path):
        self.copy_gauge.SetRange(total)
        self.copy_gauge.SetValue(num)
        self.copy_status.SetLabel("Copying " + local_path)
        self.Layout()
        

    def CopyClick(self, event):
        study_name = self.list_studies.GetStringSelection()
        username = self.combo_username.GetValue()
        password = self.text_password.GetValue()

        if not study_name: raise Exception("You didn't select a study.")
        if not username: raise Exception("You didn't enter a user name.")
        if not password: raise Exception("You didn't enter your password.")

        for s in self.studies:
            if s["name"] == study_name:
                study = s
                break
        else:
            study = None

        if study == None: raise Exception("Could not find information about study {0}".format(study_name))
        if not study["remote_directory"]: raise Exception("No remote directory set for study {0}".format(study_name))


        def remove_keys(h):
            for k in ["will_copy", "size"]:
                h.pop(k, None)
            return h

        files = filter(lambda x: x["will_copy"], self.files)
        files = map(remove_keys, files)

        self.PrepareUIForCopying(files)

        copy_files(
            window_owner=self,
            user=username,
            password=password, 
            files=files,
            study=study,
        )

        self.copy_status.SetLabel("Copy complete")
        self.Layout()

        # Reorder self.last_users or add a new entry if needed
        if study_name not in self.last_users:
            self.last_users[study_name] = []

        last = self.last_users[study_name]
        if username in last:
            last.remove(username)
        last.insert(0, username)

        study["last_time"] = self.last_refreshed_files

        dlg = wx.MessageDialog(self, "{0} files were copied.".format(len(files)), "Copy successful", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

        self.Destroy()

