"""Configuration GUI."""

import sys
import Tkinter as tk
import ttk
import tkFileDialog as tkFD
import glob
import os
import numpy as np
from PIL import Image, ImageTk

from Variables import limitsGFP, limitsRFP, RemoveNoise, NbC, NormalizeSignal


class configuration(tk.Tk):
    """Configuration GUI."""

    def __init__(self):
        """Create the window."""
        # Test get script path
        PathLog = os.path.dirname(os.path.abspath(__file__))
        PathL = PathLog + os.sep + 'Logo.jpg'

        PathChannels = PathLog + os.sep + 'channels.config'

        myChannels = open(PathChannels, 'r').readlines()
        for i in range(0, len(myChannels), 1):
            myChannels[i] = myChannels[i].rstrip()

        tk.Tk.__init__(self)
        self.wm_title('CONFIGURATION')

        image = Image.open(PathL)
        self.photo = ImageTk.PhotoImage(image)

        # width x height + x_offset + y_offset:
        Ww = 690
        Hw = 800
        self.geometry(''+str(Ww)+'x'+str(Hw)+'+10+10')

        # default configuration
        self.gup = limitsGFP[0]
        self.glow = limitsGFP[1]
        self.rup = limitsRFP[0]
        self.rlow = limitsRFP[1]
        self.noise = RemoveNoise
        self.stand = NormalizeSignal
        self.NbC = NbC
        self.equation = ''
        self.control = ''
        self.op = ''
        self.semilog = 1
        self.maxBFP = 25000
        self.nbins = 25

        margin = 10
        (Y, H) = (margin, 25)

        # Create canvas to display the logo
        canvas = tk.Canvas(self,
                           width=image.size[0],
                           height=image.size[1]
                           )
        canvas.create_image(0,
                            0,
                            anchor=tk.NW,
                            image=self.photo
                            )
        canvas.place(x=10,
                     y=Y,
                     width=image.size[0],
                     height=image.size[1]
                     )

        # Input
        self.labelInput = tk.Label(self,
                                   text='INPUT:',
                                   anchor='w',
                                   font=('Courier', 16)
                                   )
        self.labelInput.place(x=20 + image.size[0],
                              y=Y,
                              width=100,
                              height=H)

        self.Input = tk.Label(self,
                              text='',
                              anchor='w',
                              font=('Courier', 12),
                              wraplength=450,
                              justify='left'
                              )
        self.Input.place(x=20 + image.size[0] + 100,
                         y=Y,
                         width=450,
                         height=H+10
                         )
        self.BrowseI = tk.Button(text='BROWSE',
                                 font=('Courier', 16),
                                 command=self._browse1(),
                                 bg='#009999'
                                 )
        # self.BrowseI.place(x=Ww-110, y=Y, width=100, height=H)

        # Output
        Y += H + margin + 25
        self.labelOutput = tk.Label(self,
                                    text='OUTPUT:',
                                    anchor='w',
                                    font=('Courier', 16)
                                    )
        self.labelOutput.place(x=20 + image.size[0],
                               y=Y,
                               width=100,
                               height=H
                               )

        self.Output = tk.Label(self,
                               text='',
                               anchor='w',
                               font=('Courier', 12),
                               wraplength=450,
                               justify='left'
                               )
        self.Output.place(x=20 + image.size[0] + 100,
                          y=Y,
                          width=450,
                          height=H+10
                          )
        self.BrowseO = tk.Button(text='BROWSE',
                                 font=('Courier', 16),
                                 command=self._browse2(),
                                 bg='#009999'
                                 )
        # self.BrowseO.place(x=Ww-110, y=Y, width=100, height=H)

        # GFP
        Y += H + margin + 25
        self.labelGFP = tk.Label(self,
                                 text=myChannels[3]+' values:',
                                 anchor='w',
                                 font=('Courier', 16)
                                 )
        self.labelGFP.place(x=20, y=Y, width=250, height=H)

        self.GFPlo = tk.Entry(self,
                              font=('Courier', 16),
                              bg='#99ff99'
                              )
        self.GFPlo.insert(0, str(limitsGFP[0]))
        self.GFPlo.place(x=250, y=Y, width=100, height=H)

        self.labelGFP2 = tk.Label(self,
                                  text=' to ',
                                  anchor='w',
                                  font=('Courier', 16)
                                  )
        self.labelGFP2.place(x=350, y=Y, width=50, height=H)

        self.GFPup = tk.Entry(self,
                              font=('Courier', 16),
                              bg='#99ff99'
                              )
        self.GFPup.insert(0, str(limitsGFP[1]))
        self.GFPup.place(x=400, y=Y, width=100, height=H)

        # RFP
        Y += H + margin
        self.labelRFP = tk.Label(self,
                                 text=myChannels[4]+' values:',
                                 anchor='w',
                                 font=('Courier', 16)
                                 )
        self.labelRFP.place(x=20, y=Y, width=250, height=H)

        self.RFPlo = tk.Entry(self,
                              font=('Courier', 16),
                              bg='#ff9999'
                              )
        self.RFPlo.insert(0, str(limitsRFP[0]))
        self.RFPlo.place(x=250, y=Y, width=100, height=H)

        self.labelRFP2 = tk.Label(self,
                                  text=' to ',
                                  anchor='w',
                                  font=('Courier', 16)
                                  )
        self.labelRFP2.place(x=350, y=Y, width=50, height=H)

        self.RFPup = tk.Entry(self,
                              font=('Courier', 16),
                              bg='#ff9999'
                              )
        self.RFPup.insert(0, str(limitsRFP[1]))
        self.RFPup.place(x=400, y=Y, width=100, height=H)

        # BFP
        Y += H + margin
        self.labelBFP = tk.Label(self,
                                 text=myChannels[2]+' max:',
                                 anchor='w',
                                 font=('Courier', 16)
                                 )
        self.labelBFP.place(x=20, y=Y, width=250, height=H)

        self.BFPin = tk.Entry(self,
                              font=('Courier', 16),
                              bg='#99ccff'
                              )
        self.BFPin.insert(0, str(self.maxBFP))
        self.BFPin.place(x=250, y=Y, width=100, height=H)

        self.labelBFP2 = tk.Label(self,
                                  text=' bins: ',
                                  anchor='w',
                                  font=('Courier', 16)
                                  )
        self.labelBFP2.place(x=350, y=Y, width=100, height=H)

        self.BFPbi = tk.Entry(self,
                              font=('Courier', 16),
                              bg='#99ccff'
                              )
        self.BFPbi.insert(0, str(self.nbins))
        self.BFPbi.place(x=500, y=Y, width=100, height=H)

        # Checkbutton for negative control
        Y += H + margin
        self.RN = tk.IntVar(value=RemoveNoise)
        self.Remove = tk.Checkbutton(self,
                                     text=('Remove negative Control in ' +
                                           myChannels[2]),
                                     variable=self.RN,
                                     font=('Courier', 16),
                                     bg='#99ccff'
                                     )
        self.Remove.place(x=20, y=Y, width=500, height=H)

        # Checkbutton for normalisation control
        Y += H + margin
        self.Nor = tk.IntVar(value=NormalizeSignal)
        self.Norm = tk.Checkbutton(self,
                                   text=('Normalize results'),
                                   variable=self.Nor,
                                   font=('Courier', 16),
                                   bg='#99ccff'
                                   )
        self.Norm.place(x=20, y=Y, width=250, height=H)

        Y += H + margin

        # Files1 & 2
        self.labelFile1 = tk.Label(self,
                                   text='Negative Control:',
                                   anchor='w',
                                   font=('Courier', 16)
                                   )
        self.labelFile1.place(x=20, y=Y, width=300, height=H)

        self.labelFile2 = tk.Label(self,
                                   text='Normalization Control:',
                                   anchor='w',
                                   font=('Courier', 16)
                                   )
        self.labelFile2.place(x=370, y=Y, width=300, height=H)

        Y += H + margin
        self.F = tk.Listbox(self,
                            font=('Courier', 12),
                            exportselection=0
                            )
        self.F.place(x=20, y=Y, width=300, height=200)

        self.N = tk.Listbox(self,
                            font=('Courier', 12),
                            exportselection=0
                            )
        self.N.place(x=370, y=Y, width=300, height=200)

        self.Nfiles = 0
        self.fileList = np.array([])
        os.chdir(self.Input['text'])
        for f in glob.glob('*.fcs'):
            self.fileList = np.append(self.fileList, f)
            self.Nfiles += 1
        self.fileList = np.sort(self.fileList)

        for f in self.fileList:
            self.F.insert(tk.END, f)
            self.N.insert(tk.END, f)

        # NbC
        Y += 200 + margin
        self.labelNbc = tk.Label(self,
                                 text='Number of cells:',
                                 anchor='w',
                                 font=('Courier', 16)
                                 )
        self.labelNbc.place(x=20, y=Y, width=250, height=H)

        self.EntNbc = tk.Entry(self,
                               font=('Courier', 16)
                               )
        self.EntNbc.insert(0, str(self.NbC))
        self.EntNbc.place(x=250, y=Y, width=200, height=H)

        # Representation
        Y += H + margin
        self.RP = tk.IntVar(value=self.semilog)
        self.Repres = tk.Checkbutton(self,
                                     text=('Y axis in log scale'),
                                     variable=self.RP,
                                     font=('Courier', 16)
                                     )
        self.Repres.place(x=20, y=Y, width=280, height=H)

        # Progressbar
        Y += H
        self.labelCK = tk.Label(self,
                                text='',
                                anchor='w',
                                font=('Courier', 16),
                                )
        self.labelCK.place(x=20, y=Y, width=650, height=H)
        self.progressCK = ttk.Progressbar(self,
                                          orient='horizontal',
                                          length=300,
                                          mode='determinate')
        Y += H + margin
        self.progressCK.place(x=20, y=Y, width=650, height=H)

        self.progressCK2 = ttk.Progressbar(self,
                                           orient='horizontal',
                                           length=300,
                                           mode='determinate')
        Y += H
        self.progressCK2.place(x=20, y=Y, width=650, height=H)

        # Buttons
        Y += H + margin
        self.OK = tk.Button(text="START",
                            font=('Courier', 16),
                            command=self._start,
                            bg='#009999'
                            )
        self.OK.place(x=Ww-110, y=Hw-(H+margin), width=100, height=H)

        self.NO = tk.Button(text="ABORT",
                            font=('Courier', 16),
                            command=self._close,
                            bg='#ff6600'
                            )
        self.NO.place(x=margin, y=Hw-(H+margin), width=100, height=H)

        self.INpath = self.Input['text']
        self.OUTpath = self.Output['text']

    def _browse1(self):
        """Choose INPUT Folder."""
        # Quit the active window
        self.quit()
        self.Input['text'] = tkFD.askdirectory(title='CHOOSE A FOLDER')
        self.update()

    def _browse2(self):
        """Choose OUTPUT Folder."""
        self.Output['text'] = tkFD.askdirectory(title='CHOOSE A FOLDER')
        self.update()

    def _setProgress2(self,
                      Min,
                      Max):
        """Initialize progress bar."""
        self.progressCK2['value'] = Min
        self.progressCK2['maximum'] = Max
        self.update_idletasks()
        self.update()

    def _UpdateCK2(self,
                   v):
        """Update Checking file bar."""
        self.progressCK2['value'] = v
        self.update_idletasks()
        self.update()

    def _setProgress(self,
                     Min,
                     Max,
                     operation):
        """Initialize progress bar."""
        self.progressCK['value'] = Min
        self.progressCK['maximum'] = Max
        self.op = operation
        self.labelCK['text'] = self.op
        self.update_idletasks()
        self.update()

    def _UpdateCK(self,
                  v,
                  File):
        """Update Checking file bar."""
        self.progressCK['value'] = v
        self.labelCK['text'] = self.op + File
        self.update_idletasks()
        self.update()

    def _close(self):
        """Kill the job."""
        self.destroy()
        sys.exit("Manual abort")

    def _start(self):
        """Retrieve the configuration values."""
        # GFP
        self.glow = int(self.GFPlo.get())
        self.gup = int(self.GFPup.get())

        # RFP
        self.rlow = int(self.RFPlo.get())
        self.rup = int(self.RFPup.get())

        # BFP
        self.maxBFP = int(self.BFPin.get())
        self.nbins = int(self.BFPbi.get())

        # Remove noise
        self.noise = int(self.RN.get())

        # Normalization
        self.stand = int(self.Nor.get())

        # Equation
        self.control = self.F.get(self.F.curselection())

        # Equation
        self.Ref = self.F.get(self.F.curselection())

        # File for normalisation
        self.B112 = self.N.get(self.N.curselection())

        # Number of cells
        self.NbC = int(self.EntNbc.get())

        # Axis
        self.semilog = int(self.RP.get())

        # Remove the Button
        self.OK.place_forget()

        # Quit the active window
        self.quit()
