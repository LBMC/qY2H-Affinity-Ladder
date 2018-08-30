#!/usr/bin/python
"""Function creating the custom color code."""
import matplotlib


def CreateMyColors():
    """Create the custom color code.

    Uses the JET cmap of matplotlib as basis.
    """
    # Message for the user.

    # Colors:
    matplotlib.colors.ColorConverter.colors['mc0'] = (0.00, 0.00, 0.00)
    matplotlib.colors.ColorConverter.colors['mc1'] = (0, 0, 0.498)
    matplotlib.colors.ColorConverter.colors['mc2'] = (0, 0, 0.8)
    matplotlib.colors.ColorConverter.colors['mc3'] = (0, 0.03137, 1)
    matplotlib.colors.ColorConverter.colors['mc4'] = (0, 0.298, 1)
    matplotlib.colors.ColorConverter.colors['mc5'] = (0, 0.5647, 1)
    matplotlib.colors.ColorConverter.colors['mc6'] = (0, 0.8314, 1)
    matplotlib.colors.ColorConverter.colors['mc7'] = (0.1608, 1, 0.8039)
    matplotlib.colors.ColorConverter.colors['mc8'] = (0.3725, 1, 0.5882)
    matplotlib.colors.ColorConverter.colors['mc9'] = (0.5882, 1, 0.3725)
    matplotlib.colors.ColorConverter.colors['mc10'] = (0.8039, 1, 0.1608)
    matplotlib.colors.ColorConverter.colors['mc11'] = (1, 0.898, 0)
    matplotlib.colors.ColorConverter.colors['mc12'] = (1, 0.6392, 0)
    matplotlib.colors.ColorConverter.colors['mc13'] = (1, 0.3922, 0)
    matplotlib.colors.ColorConverter.colors['mc14'] = (1, 0.1451, 0)
    matplotlib.colors.ColorConverter.colors['mc15'] = (0.7843, 0, 0)
