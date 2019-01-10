"""Accessory functions."""

# Python Llibraries
import datetime
import os
from os.path import join
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# Own libraries
from Variables import Dimension, Bottom, Left, W, H


def CreatePDF(Config):
    """Create PDF report."""
    # Name of the file with unique date-time tag.
    now = datetime.datetime.now()
    NomPdf = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '_'
    NomPdf += str(now.hour) + '-' + str(now.minute) + '_'
    NomPdf += 'Titration_TF'
    NomPdf += '.pdf'

    # Create the matplotlib pdf report.
    Pdf = PdfPages(join(Config.OUTpath,
                        NomPdf))
    return Pdf


def CreateTXT(Samples,  # Dictionnary of Echantillons.
              CR,
              Config
              ):
    """Create the txt report file."""
    # Name of the file with unique date-time tag.
    now = datetime.datetime.now()
    NomTxt = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '_'
    NomTxt += str(now.hour) + '-' + str(now.minute) + '_'
    NomTxt += 'Mean' + '.csv'

    # Retrieve all channels names
    PathLog = os.path.dirname(os.path.abspath(__file__))
    PathChannels = PathLog + os.sep + 'channels.config'
    myChannels = open(PathChannels, 'r').readlines()
    for i in range(0, len(myChannels), 1):
        myChannels[i] = myChannels[i].rstrip()

    BFPchannel = myChannels[2]
    GFPchannel = myChannels[3]
    RFPchannel = myChannels[4]

    # Path of the file.
    MyFile = join(Config.OUTpath,
                  NomTxt)

    # Create the file and allow writing.
    f = open(str(MyFile), "w+")

    # Calculate the mean RFP value of the Gate currently used.
    R = '(' + str(Samples[(CR)]._RFPlimits[0]) + ' - '
    R += str(Samples[(CR)]._RFPlimits[1]) + ')'

    # Update the csv file.
    f.write(RFPchannel + ' = ' + R + '\n')

    # Create the GFP scale using the reference Manip/couple file.
    f.write(GFPchannel)
    for g in Samples[(CR)]._GFP:
        f.write(","+str(g))
    f.write('\n')
    f.write('\n' + BFPchannel + '\n')
    return f


def Conditions(myPdf,  # pdf File to transfert the graph.
               C,  # one couple.
               dict_Echantillon,  # dictionnary of all Echantillon.
               Commit  # current version of the program.
               ):
    """Display the parameters of the analysis."""
    fig = plt.figure(figsize=Dimension)

    # Key parameters to be displayed on the first page of the report.
    Text = 'PARAMATERS\n\n'
    Text += 'RFP limits (' + str(dict_Echantillon[(C)]._RFPlimits[0])
    Text += ', ' + str(dict_Echantillon[(C)]._RFPlimits[1]) + ')\n'
    Text += '\n'
    Text += 'GFP limits (' + str(dict_Echantillon[(C)]._GFPlimits[0])
    Text += ', ' + str(dict_Echantillon[(C)]._GFPlimits[1]) + ')\n'
    Text += '\n\n'
    Text += 'Commit: ' + Commit

    # Display the text and transfert the figure in the pdf.
    fig.text(Left, Bottom, Text)
    plt.savefig(myPdf, format='pdf', dpi=300)


def Draw_Cumulative(Couples_M,
                    Sample,
                    Ref,
                    Standard,
                    Config,
                    pdf
                    ):
    """Draw the cumulative mean BFP curves."""
    # Retrieve all channels names
    PathLog = os.path.dirname(os.path.abspath(__file__))
    PathChannels = PathLog + os.sep + 'channels.config'
    myChannels = open(PathChannels, 'r').readlines()
    for i in range(0, len(myChannels), 1):
        myChannels[i] = myChannels[i].rstrip()

    BFPchannel = myChannels[2]

    # Initiate graph.
    fig = plt.figure(figsize=Dimension)
    fig.add_axes([Left,
                  Bottom,
                  W,
                  H
                  ])
    index = 5
    ls = '-'
    iteration = 0

    dictMarker = {}
    dictMarker[(0, 1)] = 'o'
    dictMarker[(0, 0)] = '^'
    dictMarker[(1, 1)] = 's'
    dictMarker[(1, 0)] = '*'
    dictMarker[(2, 1)] = 'v'
    dictMarker[(2, 0)] = 'h'
    dictMarker[(3, 1)] = '>'
    dictMarker[(3, 0)] = 'D'

    mymin = 1

    for C in Couples_M:
        mymarker = dictMarker[(iteration, index % 2)]
        ind = Sample[(C)]._BFPlin.shape[0] - 1
        T = C + '\n<' + BFPchannel + '> = '
        T += str(round(Sample[(C)]._BFPlin[ind], 2)) + '\n'

        mypotentialmin = Sample[(C)]._BFPlin[ind]

        if C != Ref and C != Standard:

            if mypotentialmin < mymin:
                mymin = mypotentialmin
                print(C + " " + str(mymin))

            if Config.semilog == 1:
                plt.semilogy(Sample[(C)]._BFPbins,
                             Sample[(C)]._BFPlins,
                             linewidth=1,
                             label=T,
                             color='mc'+str(index),
                             linestyle=ls,
                             marker=mymarker,
                             markersize=5
                             )
                print(T)

            else:
                plt.plot(Sample[(C)]._BFPbins,
                         Sample[(C)]._BFPlins,
                         linewidth=1,
                         label=T,
                         color='mc'+str(index),
                         linestyle=ls,
                         marker=mymarker,
                         markersize=5
                         )
                print(T)

            index += 1
            if index > 15:
                index = 0
                iteration += 1

        elif C == Ref and Config.noise == 0:

            if mypotentialmin < mymin:
                mymin = mypotentialmin
                print(C + " " + str(mymin))

            if Config.semilog == 1:
                T += "Negative CTRL\n"
                plt.semilogy(Sample[(C)]._BFPbins,
                             Sample[(C)]._BFPlins,
                             linewidth=3,
                             label=T,
                             color='mc0',
                             linestyle=':'
                             )
                print(T)

            else:
                T += "Negative CTRL\n"
                plt.plot(Sample[(C)]._BFPbins,
                         Sample[(C)]._BFPlins,
                         linewidth=3,
                         label=T,
                         color='mc0',
                         linestyle=':'
                         )
                print(T)

    if Config.semilog == 1 and Config.stand == 0:
        plt.ylim(ymin=1)
    elif Config.semilog == 1 and Config.stand == 1:
        print(str(mymin))
        plt.ylim(ymin=mymin/2)
        plt.ylim(ymax=2)
    else:
        plt.ylim(ymin=0)

    plt.xlim(xmin=0)

    # Axes label.
    plt.xlabel(BFPchannel,
               fontweight='bold',
               )

    plt.ylabel('Cumulative mean',
               fontweight='bold',
               )

    # Display the legend (labels of the files).
    plt.legend(bbox_to_anchor=(1.2, 1),
               loc=2,
               borderaxespad=0,
               fontsize=6
               )

    # Title of the graph.
    plt.suptitle(Sample[(C)]._GFPslice, fontsize=10)

    # Transfert in the pdf.
    plt.savefig(pdf,
                format='pdf',
                dpi=300)

    plt.savefig(join(Config.OUTpath, 'RESULT.png'),
                bbox_inches='tight',
                dpi=200
                )


def FCStoCSV(Couples,
             Samples,
             txtFile):
    """Create CSV."""
    for C in Couples:
        # Update Report.
        Samples[(C)]._report(txtFile)
