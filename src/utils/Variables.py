"""Variables."""

# Equation for fitting.

# limits.
limitsGFP = [5000, 6000]

limitsRFP = [700, 900]
# Removal of Noise.
RemoveNoise = 1

# Normalization
NormalizeSignal = 0

# Number of Cells.
NbC = 10000000

# Figures format
Dimension = (8, 4)  # inches.
Bottom = 0.15  # proportion (0-1).
Left = 0.15  # proportion (0-1).
Square = 3  # inches.

W = 0.375  # Width (0-1) of the figure
H = 0.75  # Height (0-1) of the figure

# Accepted FilesTypes
FilesTypes = FilesTypes = (('Cytometry files', '*.fcs'),
                           ('All files', '*.*')
                           )
