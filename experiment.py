import wx



########################################################################
class MyForm(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Tutorial", size=(500,500))

        layout = wx.BoxSizer(wx.VERTICAL)

        splitter = wx.SplitterWindow(self,style=wx.SP_LIVE_UPDATE)

        tree_panel = wx.Panel(splitter)
        tree_panel.SetBackgroundColour(wx.BLACK)
        entry_panel = wx.Panel(splitter)
        entry_panel.SetBackgroundColour(wx.GREEN)

        splitter.SplitVertically(tree_panel,entry_panel)
        splitter.SetMinimumPaneSize(100)

        layout.Add(splitter,1,wx.EXPAND|wx.ALL,5)
        self.SetSizer(layout)


# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm().Show()
    app.MainLoop()
