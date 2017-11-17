#!/usr/bin/python
"""MAIN PROGRAM."""

# Python libraries.
from os.path import join

# Own libraries.
from Object_Echantillon.py import Echantillon

from Functions import Conditions, FCStoCSV
from Functions import CreatePDF, CreateTXT, Draw_Cumulative
from Configuration import configuration
from Ending_Window import Result
from Colors import CreateMyColors


"""
ALL ._Functions are those I developped.
The _ is only there to indicate a non Python native object/functions.
"""

# GIT commit considered as functional.
GC = '0f2182916ce9b347e7771370d03817ababdb3958'

# Create colors
CreateMyColors()

# Configuration
Config = configuration()
# Waiting until Start is pressed
Config.mainloop()

# Start is pressed
Config.update_idletasks()
Config.update()


# Dictionnary of all Echantillons.
Samples = {}

NFiles = Config.Nfiles

# Ref file
RFile = Config.Ref

# Create pdf file.
BilanPdf = CreatePDF(Config)

# Procesing files.
f = 0

Config._setProgress(f,
                    NFiles,
                    'PROCESSING FILES: '
                    )


for C in Config.fileList:
    f += 1
    # Creating the local object instance.
    NameE = C
    PathE = join(Config.INpath, NameE)

    Config._UpdateCK(f, NameE)
    Samples[(C)] = Echantillon(C,
                               PathE,
                               NameE,
                               Config
                               )

    # Create report first page.
    if f == 1:
        # Use the first couple to generate the txt file.
        Conditions(BilanPdf,
                   C,
                   Samples,
                   GC
                   )

# Initialize the txt report.
F = CreateTXT(Samples,
              C,
              Config
              )

# Creating graph.
m = 0

Config._setProgress(m,
                    len(Config.fileList),
                    'REMOVING NOISE'
                    )

Zero = Samples[(RFile)]._BFP
Zerolin = Samples[(RFile)]._BFPlin
for C in Config.fileList:
    # Removing Noise for all kind of dimension BFP.
    if Config.noise == 1:
        lt = len(Samples[(C)]._BFP)
        Samples[(C)]._BFP = Samples[(C)]._BFP - Zero[:lt]

        lt = len(Samples[(C)]._BFPlin)
        Samples[(C)]._BFPlin = Samples[(C)]._BFPlin - Zerolin[:lt]


# Draw the graph with all curves.
Draw_Cumulative(Config.fileList,
                Samples,
                RFile,
                Config,
                BilanPdf
                )

m += 1
Config._UpdateCK(m, '')

# Create all 'Mean' experiment and Graph.
FCStoCSV(Config.fileList, Samples, F)

# Close the report file.
F.close()

# Close the PDF file.
BilanPdf.close()
Config.destroy()

# Display the result in a window
Result(Config)
