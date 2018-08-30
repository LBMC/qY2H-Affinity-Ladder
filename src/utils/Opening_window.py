"""Opening window displaying initial options."""

# Python library
from PIL import Image, ImageTk

# WARNING PIL IS NO MORE MAINTAINED.
# REQUIRE TO INSTALL PILLOW
# FOR WINDOWS ON ADMIN SESSION: pip install Pillow

import Tkinter as tk
import os
import sys

from Configure_Channels import get_FilePath, Channels


class Start(tk.Tk):
    """Configuration GUI."""

    def __init__(self):
        """Create the window."""
        # Test get script path
        PathLog = os.path.dirname(os.path.abspath(__file__))
        PathL = PathLog + os.sep + 'Logo.jpg'

        tk.Tk.__init__(self)
        self.wm_title('START')

        image = Image.open(PathL)
        self.photo = ImageTk.PhotoImage(image)

        # width x height + x_offset + y_offset:
        Ww = 400
        Hw = 125
        self.geometry(''+str(Ww)+'x'+str(Hw)+'+10+10')

        margin = 10
        (Y, H) = ((Hw - (3*25+2*margin))/2, 25)

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
                     y=(Hw-image.size[1])/2,
                     width=image.size[0],
                     height=image.size[1]
                     )

        self.BrowseI = tk.Button(text='Configure channels',
                                 font=('Courier', 16),
                                 command=lambda: self._browse1(PathLog),
                                 bg='#ffcc66'
                                 )
        self.BrowseI.place(x=image.size[0] + 2*margin,
                           y=Y,
                           width=250,
                           height=H)

        Y += H + margin

        self.OK = tk.Button(text="Start analysis",
                            font=('Courier', 16),
                            command=self._start,
                            bg='#009999'
                            )
        self.OK.place(x=image.size[0] + 2*margin,
                      y=Y,
                      width=250,
                      height=H)

        Y += H + margin

        self.KO = tk.Button(text="Abort",
                            font=('Courier', 16),
                            command=self._close,
                            bg='#ff6600'
                            )
        self.KO.place(x=image.size[0] + 2*margin,
                      y=Y,
                      width=250,
                      height=H)

    def _browse1(self,
                 pathf  # Path of the folder containing the program
                 ):
        """Identify a file to configure the channels."""
        # Quit the active window
        P = get_FilePath()
        Channels(P)

    def _close(self):
        """Kill the job."""
        self.destroy()
        sys.exit("Manual abort")

    def _start(self):
        """Retrieve the configuration values."""
        self.destroy()
