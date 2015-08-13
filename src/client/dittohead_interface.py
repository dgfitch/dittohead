import wx
import gettext
import os.path
import sys, traceback
from datetime import *
from threading import *
import time

from copy import copy_files, AuthenticationException


FONT_SIZE = (8,20)


# Long-running worker thread stuff borrowed from http://wiki.wxpython.org/LongRunningTasks

EVT_RESULT_ID = wx.NewId()
EVT_PROGRESS_ID = wx.NewId()

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)

def EVT_PROGRESS(win, func):
    """Define Progress Event."""
    win.Connect(-1, -1, EVT_PROGRESS_ID, func)


class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data

class ProgressEvent(wx.PyEvent):
    """Simple event to carry progress data, like index of file and local path we're at so far"""
    def __init__(self, number, path):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_PROGRESS_ID)
        self.number = number
        self.path = path


class WorkerThread(Thread):
    def __init__(self, notify_window):
        Thread.__init__(self)
        self._handler = notify_window.GetEventHandler()
        self._want_abort = False

    def run(self):
        """
        # Here's a way to test progress and cancelling easily without doing actual SSH somewhere:
        for i in range(1,100):
            wx.PostEvent(self._handler, ProgressEvent(i, "TESTING"))
            time.sleep(1.0)
            if self._want_abort:
                wx.PostEvent(self._handler, ResultEvent(None))
                return
        """

        try:
            copy_files(
                thread=self,
                user=self.username,
                password=self.password, 
                files=self.files,
                study=self.study,
            )

            if self._want_abort:
                wx.PostEvent(self._handler, ResultEvent(None))
                return

        except AuthenticationException:
            wx.PostEvent(self._handler, ResultEvent(False))
            return

        wx.PostEvent(self._handler, ResultEvent(True))

    def progress(self, index, path):
        wx.PostEvent(self._handler, ProgressEvent(index, path))


    def should_abort(self):
        return self._want_abort

    def abort(self):
        self._want_abort = True



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
    """
    The frame for editing study file locations and metadata.
    """
    def __init__(self, *args, **kwds):
        DittoheadFrame.__init__(self, *args, **kwds)

        self.callback = None
        self.original_name = None

        LABEL_WIDTH = 300
        TEXTBOX_WIDTH = 300

        self.panel = wx.Panel(self, wx.ID_ANY)
        l1 = wx.StaticText(self.panel, -1, 'Study Name:', (-1, -1), (-1, -1), wx.ALIGN_RIGHT)
        l2 = wx.StaticText(self.panel, -1, 'Extra Contact Emails (use commas):', (-1, -1), (-1, -1), wx.ALIGN_RIGHT)
        l3 = wx.StaticText(self.panel, -1, 'Local Directory:', (-1, -1), (-1, -1), wx.ALIGN_RIGHT)
        l4 = wx.StaticText(self.panel, -1, 'Remote Directory:', (-1, -1), (-1, -1), wx.ALIGN_RIGHT)
        self.text_name = wx.TextCtrl(self.panel, -1, '', (-1, -1), (TEXTBOX_WIDTH, -1))
        self.text_extra_contacts = wx.TextCtrl(self.panel, -1, '', (-1, -1), (TEXTBOX_WIDTH, -1))
        self.local_directory = wx.DirPickerCtrl(self.panel, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE)
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
        hsizer3.Add(self.local_directory, 1, wx.GROW, b)
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
        self.text_remote_directory.SetValue("/home/inbox/dittohead")


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
        if "local_directory" in s: self.local_directory.SetPath(s["local_directory"])
        if "remote_directory" in s: self.text_remote_directory.SetValue(s["remote_directory"])
        

    def OkClick(self, event):
        new_name = self.text_name.GetValue()

        if new_name == "":
            raise Exception("Trying to save changes to a nonexistent or blank study {0} in hash {1}".format(self.original_name, self.studies))

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
        s["local_directory"] = self.local_directory.GetPath()
        s["remote_directory"] = self.text_remote_directory.GetValue()

        if self.callback: self.callback()
        
        self.Destroy()

    def CancelClick(self, event):
        self.Destroy()


class CopyFrame(DittoheadFrame):
    """
    The main window for selecting stuff and copying things
    """
    def __init__(self, *args, **kwds):
        DittoheadFrame.__init__(self, *args, **kwds)

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

        # Some parts of the UI should be hidden before the copy.
        # If I hide them, they don't get a reserved space in the layout.
        # So this is unnecessarily ugly because I don't understand wxPython.
        self.copy_status.SetLabel("")

        self.selected_study = None
        self.last_refreshed_files = None
        self.files = []


        # Set up event handler for any worker thread results
        EVT_RESULT(self,self.OnResult)

        # Set up event handler for any worker thread progress
        EVT_PROGRESS(self,self.OnProgress)

        # And indicate we don't have a worker thread yet
        self.worker = None



    def __set_properties(self):
        # begin wxGlade: CopyFrame.__set_properties
        self.SetTitle("dittohead - The Magic Secure File Copier!")
        self.edit_study_button.Enable(False)
        self.copy_button.Enable(False)
        self.copy_button.SetDefault()

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

        right_pane.Add(self.text_preview, 1, wx.EXPAND | wx.ALL, 0)

        right_pane.Add(self.copy_status, 0, wx.EXPAND, 0)
        right_pane.Add(self.copy_gauge, 0, wx.EXPAND, 0)
        
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


    def showWarningDialog(self, message, caption="Warning"):
        dlg = wx.MessageDialog(self, message, caption, wx.OK | wx.ICON_WARNING)
        dlg.ShowModal()
        dlg.Destroy()

    def __setup_exception_handling(self):
        def handler(*exc_info):
            message = "".join(traceback.format_exception(*exc_info))
            self.log.error(message)
            self.showWarningDialog(message, caption = "Exception")

        None
        sys.excepthook = handler


    def LoadStudies(self, log, studies, last_users):
        self.log = log
        self.__setup_exception_handling()

        self.studies = studies
        self.last_users = last_users
        self.ShowStudies()


    def ShowStudies(self):
        self.list_studies.Clear()
        for s in self.studies:
            self.list_studies.Append(s["name"])

    
    def CancelClick(self, event):
        if self.worker:
            self.log.info("Aborting copy")
            self.worker.abort()
        else:
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
                else:
                    self.label_preview.SetLabel("Preview: ({0} appears to have never ran on this machine yet)".format(self.selected_study))

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

                walk_path = s.get("local_directory") or ""
                if not os.path.isdir(walk_path):
                    return []

                # Iterate over local directory looking for things > last_time

                self.wait = wx.BusyCursor()

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


                del self.wait

                self.files = result
                return result

        return []


    def PrepareUIForCopying(self, files):
        self.copy_gauge.SetRange(len(files))
        self.copy_button.Hide()
        self.Layout()

    def PrepareUIDoneWithCopying(self):
        self.copy_button.Show()
        self.Layout()

        

    def MacReopenApp(self):
        """Called when the dock icon is clicked on OSX"""
        self.GetTopWindow().Raise()

    def CopyClick(self, event):
        study_name = self.list_studies.GetStringSelection()
        username = self.combo_username.GetValue()
        password = self.text_password.GetValue()


        if not study_name: 
            self.showWarningDialog("You didn't select a study.")
            return
        if not username:
            self.showWarningDialog("You didn't enter a user name.")
            return
        if not password: 
            self.showWarningDialog("You didn't enter your password.")
            return

        for s in self.studies:
            if s["name"] == study_name:
                study = s
                break
        else:
            study = None

        if study == None:
            self.showWarningDialog("Could not find information about study {0}".format(study_name))
            return

        if not study["remote_directory"]:
            self.showWarningDialog("No remote directory set for study {0}".format(study_name))
            return


        # We need to store this stuff for the result handler to use
        self.study_name = study_name
        self.study = study
        self.username = username

        self.PrepareUIForCopying(self.files)
        self.wait = wx.BusyCursor()
        self.worker = WorkerThread(self)

        # We also need to pass the stuff into the worker thread state. 
        # Kind of ugly, probably a better way; I couldn't find one.
        self.worker.files = self.files
        self.worker.username = self.username
        self.worker.password = password
        self.worker.study = study
        self.worker.start()


    def OnProgress(self, event):
        self.copy_gauge.SetValue(event.number)
        self.copy_status.SetLabel("Copying " + event.path)


    def OnResult(self, event):
        self.PrepareUIDoneWithCopying()
        del self.wait

        if event.data is None:
            self.worker = None

            self.copy_status.SetLabel("Copy cancelled")
            self.copy_gauge.SetValue(0)

            dlg = wx.MessageDialog(self, "Copy cancelled", "Copy cancelled", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

        elif event.data is False:
            self.copy_status.SetLabel("Authentication failed")
            self.showWarningDialog("Authentication failed for user {0}. Did you mistype your password?".format(self.username))

        elif event.data is True:
            self.copy_status.SetLabel("Copy complete!")

            # Reorder self.last_users or add a new entry if needed
            if self.study_name not in self.last_users:
                self.last_users[self.study_name] = []

            last = self.last_users[self.study_name]
            if self.username in last:
                last.remove(self.username)
            last.insert(0, self.username)

            self.study["last_time"] = self.last_refreshed_files

            dlg = wx.MessageDialog(self, "{0} files were copied.".format(len(self.files)), "Copy successful", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

            self.Destroy()


