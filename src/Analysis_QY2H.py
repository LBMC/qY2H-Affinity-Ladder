#!/usr/bin/python
# coding: utf-8
"""MAIN PROGRAM."""

# Python libraries.
from __future__ import division
from os.path import join

# Own libraries.
from utils.Object_Echantillon import Echantillon
from utils.Functions import Conditions, FCStoCSV
from utils.Functions import CreatePDF, CreateTXT, Draw_Cumulative
from utils.Opening_window import Start
from utils.Configuration import configuration
from utils.Ending_Window import Result
from utils.Colors import CreateMyColors


def main():
    """Execute main program."""
    """
    ALL ._Functions are those I developped.
    The _ is only there to indicate a non Python native object/functions.
    """
    # GIT commit considered as functional.
    GC = '9fe4e5d4a613f0f651ec5402eaf74b93545afc72'

    # Create colors
    CreateMyColors()

    # Configuration
    WinStart = Start()
    # Waiting for command
    WinStart.mainloop()

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
    RFile = Config.control

    # Norm file
    NFile = Config.MAX

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
                       GC,
                       Config
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

    # Removing Noise for all kind of dimension BFP.
    if Config.noise == 1:

        Zero = Samples[(RFile)]._BFP
        Zerolin = Samples[(RFile)]._BFPlin
        Zerolins = Samples[(RFile)]._BFPlins

        for C in Config.fileList:
            lt = len(Samples[(C)]._BFP)
            Samples[(C)]._BFP = Samples[(C)]._BFP - Zero[:lt]

            lt = len(Samples[(C)]._BFPlins)
            Samples[(C)]._BFPlins = Samples[(C)]._BFPlins - Zerolins[:lt]
            lt = len(Samples[(C)]._BFPlin)
            Samples[(C)]._BFPlin = Samples[(C)]._BFPlin - Zerolin[:lt]

    if Config.stand == 1:

        Standard = Samples[(NFile)]._BFP[-1]
        Standardlin = Samples[(NFile)]._BFPlin[-1]
        Standardlins = Samples[(NFile)]._BFPlins[-1]

        for C in Config.fileList:
            lt = len(Samples[(C)]._BFP)
            Samples[(C)]._BFP = 100 * Samples[(C)]._BFP / Standard

            lt = len(Samples[(C)]._BFPlins)
            Samples[(C)]._BFPlins = 100 * Samples[(C)]._BFPlins / Standardlins
            lt = len(Samples[(C)]._BFPlin)
            Samples[(C)]._BFPlin = 100 * Samples[(C)]._BFPlin / Standardlin

    # Draw the graph with all curves.
    Draw_Cumulative(Config.fileList,
                    Samples,
                    RFile,
                    NFile,
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


if __name__ == "__main__":
    # execute only if run as a script
    main()
