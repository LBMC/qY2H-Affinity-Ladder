"""Ending window displaying the mean experiment."""

# Python library
from PIL import Image, ImageTk

# WARNING PIL IS NO MORE MAINTAINED.
# REQUIRE TO INSTALL PILLOW
# FOR WINDOWS ON ADMIN SESSION: pip install Pillow


import Tkinter as tk
import sys
from os.path import join


class Result(tk.Tk):
    """Configuration GUI."""

    def __init__(self, Config):
        """Create the window."""
        tk.Tk.__init__(self)
        self.wm_title('RESULT')

        image = Image.open(join(Config.OUTpath, 'RESULT.png'))
        photo = ImageTk.PhotoImage(image)

        W = image.size[0]
        H = image.size[1] + 100

        # Defining window dimension (pixels)
        self.geometry('' + str(W) +
                      'x' +
                      str(H) +
                      '+10+10')

        # Create canvas to display the picture
        canvas = tk.Canvas(self,
                           width=image.size[0],
                           height=image.size[1]
                           )
        canvas.create_image(0,
                            0,
                            anchor=tk.NW,
                            image=photo
                            )
        canvas.pack()

        # Exit button
        self.NO = tk.Button(text="ABORT",
                            font=('Courier', 16),
                            command=self._close,
                            bg='#ff6600'
                            )
        self.NO.place(x=25,
                      y=H-75,
                      width=100,
                      height=50)

        self.mainloop()

    def _close(self):
        """Kill the job."""
        self.destroy()
        sys.exit("Manual abort")
