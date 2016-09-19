import os
import sys

class PacfmD(object):
    """
    Interface manager class. Currently available user interfaces include a wxPython-based GUI and a command-line interface.  
    """
    def __init__(self, **kwargs):
        """
            Initiates PACFM with the selected ui.
        """
        if len(sys.argv) > 1:
            ui= sys.argv[1]
            
            if ui == "-gui" or ui == "1":
                import wx
                from pacfm.bootstrap.pacfm_gui import PacfmGUI
                
                app= wx.App(None)
                frame=  PacfmGUI(app, db_name= "kegg_orthology", calculation_type="sum")
                app.MainLoop()

            elif ui == "-cl" or ui == "2":
                from pacfm.bootstrap.pacfm_cl import PacfmCL
                from pacfm.view.commandline.main_view import MainView
                
                main_ctrl= PacfmCL(kwargs)
                MainView(main_ctrl)

        else:
            import wx
            from pacfm.bootstrap.pacfm_gui import PacfmGUI
            app= wx.App(None)
            frame=  PacfmGUI(app)
            app.MainLoop()


if __name__ == "__main__":
    PacfmD()

