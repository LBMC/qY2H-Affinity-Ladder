"""Functions creating a dynamic GUI."""

import Tkinter as tk
import os
from FlowCytometryTools import FCMeasurement
from tkFileDialog import askopenfilename  # Name consistancy!!???
from Variables import FilesTypes


def get_FilePath():
    """Create a dialog window allowing to choose the file to treat."""
    file_path = askopenfilename(title='Select a fcs file:',
                                filetypes=FilesTypes)
    return file_path


class Channels(tk.Tk):
    """Configuration GUI."""

    def __init__(self, path):
        """Create the window."""
        self.PathLog = os.path.dirname(os.path.abspath(__file__))

        # Open the fcs file and retrieve the channels
        self._sample = FCMeasurement(ID='Test Sample',
                                     datafile=path
                                     )
        channelsnames = self._sample.channel_names

        tk.Tk.__init__(self)
        self.wm_title('Channels configuration')

        # width x height + x_offset + y_offset:
        Ww = (25+100) * 5 + 25
        Hw = 500
        self.geometry(''+str(Ww)+'x'+str(Hw)+'+10+10')

        margin = 10
        (Y, H) = (25, 25)
        Y2 = Y+H+margin
        X = 25

        # Channels
        self.labelFSC = tk.Label(self,
                                 text='FSC:',
                                 anchor='w',
                                 font=('Courier', 16)
                                 )
        self.labelFSC.place(x=X, y=Y, width=100, height=H)

        self.FSC = tk.Listbox(self,
                              font=('Courier', 12),
                              exportselection=0,
                              bg='#D3D3D3'
                              )
        self.FSC.place(x=X, y=Y2, width=100, height=300)

        X += 125

        self.labelSSC = tk.Label(self,
                                 text='SSC:',
                                 anchor='w',
                                 font=('Courier', 16)
                                 )
        self.labelSSC.place(x=X, y=Y, width=100, height=H)

        self.SSC = tk.Listbox(self,
                              font=('Courier', 12),
                              exportselection=0,
                              bg='#FFFFFF'
                              )
        self.SSC.place(x=X, y=Y2, width=100, height=300)

        X += 125

        self.labelBFP = tk.Label(self,
                                 text='BFP:',
                                 anchor='w',
                                 font=('Courier', 16)
                                 )
        self.labelBFP.place(x=X, y=Y, width=100, height=H)

        self.BFP = tk.Listbox(self,
                              font=('Courier', 12),
                              exportselection=0,
                              bg='#99ccff'
                              )
        self.BFP.place(x=X, y=Y2, width=100, height=300)

        X += 125

        self.labelGFP = tk.Label(self,
                                 text='GFP:',
                                 anchor='w',
                                 font=('Courier', 16)
                                 )
        self.labelGFP.place(x=X, y=Y, width=100, height=H)

        self.GFP = tk.Listbox(self,
                              font=('Courier', 12),
                              exportselection=0,
                              bg='#99ff99'
                              )
        self.GFP.place(x=X, y=Y2, width=100, height=300)

        X += 125

        self.labelRFP = tk.Label(self,
                                 text='RFP:',
                                 anchor='w',
                                 font=('Courier', 16)
                                 )
        self.labelRFP.place(x=X, y=Y, width=100, height=H)

        self.RFP = tk.Listbox(self,
                              font=('Courier', 12),
                              exportselection=0,
                              bg='#ff9999'
                              )
        self.RFP.place(x=X, y=Y2, width=100, height=300)

        for c in channelsnames:
            self.FSC.insert(tk.END, c)
            self.SSC.insert(tk.END, c)
            self.BFP.insert(tk.END, c)
            self.GFP.insert(tk.END, c)
            self.RFP.insert(tk.END, c)

        self.fsc = ''
        self.ssc = ''
        self.bfp = ''
        self.gfp = ''
        self.rfp = 'self.FSC.get(self.RFP.curselection())'

        # Button
        self.OK = tk.Button(self,
                            text="VALIDATE",
                            font=('Courier', 16),
                            command=lambda: self._validate(),
                            bg='#009999'
                            )
        self.OK.place(x=525, y=450, width=100, height=H)

    def _validate(self):
        """Save the selected channels as default."""
        # FSC
        self.fsc = self.FSC.get(self.FSC.curselection())
        self.ssc = self.SSC.get(self.SSC.curselection())
        self.bfp = self.BFP.get(self.BFP.curselection())
        self.gfp = self.GFP.get(self.GFP.curselection())
        self.rfp = self.FSC.get(self.RFP.curselection())

        # New parameters
        Param = (self.fsc + '\n' +
                 self.ssc + '\n' +
                 self.bfp + '\n' +
                 self.gfp + '\n' +
                 self.rfp)

        # Update channels.config file

        file = open(self.PathLog + os.sep + 'channels.config',
                    'w')
        file.write(Param)
        file.close()
        self.destroy()
