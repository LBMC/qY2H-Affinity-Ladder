"""Object Echantillon."""
# Python library
import FlowCytometryTools
import os
from FlowCytometryTools import FCMeasurement
import numpy as np


class Echantillon:
    """Sample of FCStools with downstream actions.

    1)   Opening using FCSTools
    2)   Selection using pandas properties
    3)   Titration of BFP/RFP = f (GFP) for a RFP value
    4)   Fitting to new complex Model from Martin
    """

    def __init__(self,  # Current instance.
                 C,  # Name of the couple.
                 path,  # Path of the .fcs file.
                 nom,  # Name of the Echantillon.
                 config  # configuration.
                 ):
        """Construct Object."""
        # Retrieve all channels names
        PathLog = os.path.dirname(os.path.abspath(__file__))
        PathChannels = PathLog + os.sep + 'channels.config'
        myChannels = open(PathChannels, 'r').readlines()
        for i in range(0, len(myChannels), 1):
            myChannels[i] = myChannels[i].rstrip()

        self.FSCchannel = myChannels[0]
        self.SSCchannel = myChannels[1]
        self.BFPchannel = myChannels[2]
        self.GFPchannel = myChannels[3]
        self.RFPchannel = myChannels[4]

        # RFP and GFP limits for Titration.
        self._RFPlimits = [config.rlow, config.rup]
        self._GFPlimits = [config.glow, config.gup]
        self._maxBFP = config.maxBFP

        self._GFPslice = self.RFPchannel
        self._GFPslice += ' slice (' + str(self._RFPlimits[0])
        self._GFPslice += ', ' + str(self._RFPlimits[1]) + ')\n'
        self._GFPslice += self.GFPchannel
        self._GFPslice += ' slice (' + str(self._GFPlimits[0])
        self._GFPslice += ', ' + str(self._GFPlimits[1]) + ')'
        self._nBinlin = 5000
        self._binjump = int(self._nBinlin/config.nbins)

        self._Couple = C
        self._NbC = config.NbC
        self._name = nom

        # Retrieve Cells data.
        self._sample = FCMeasurement(ID='Test Sample',
                                     datafile=path
                                     )

        # Channels to be conserved.
        self._C = [self.FSCchannel,
                   self.SSCchannel,
                   self.BFPchannel,
                   self.GFPchannel,
                   self.RFPchannel
                   ]

        # Remove bubbles.
        self._RemoveBubbles()

        # Calculating GFP concentration
        # self._Conc()

        self._nsteps = 1 + 1  # Only one slice of GFP

        self._step = 0

        # initiate secondary progressbar
        config._setProgress2(self._step, self._nsteps)

        # Reduce size of the sample for memory gain.
        igate = FlowCytometryTools.IntervalGate((self._GFPlimits[0],
                                                 self._GFPlimits[1]),
                                                self.GFPchannel,
                                                region='in'
                                                )
        fgate = FlowCytometryTools.IntervalGate((-5000,
                                                 250000),
                                                self.FSCchannel,
                                                region='in'
                                                )
        mygate = fgate & igate
        self._sample = self._sample.gate(mygate)

        # update progressbar 2
        self._step += 1
        config._UpdateCK2(self._step)

        # Titration values to be called.
        self._BFP = np.array([])
        self._BFPlin = np.array([])
        self._BFPbin = np.array([])
        self._GFP = np.array([])

        self._BFPlins = np.array([])
        self._BFPbins = np.array([])

        # Perform cumulative histogram for BFP
        self._CumulHisto(self._GFPlimits[0], self._GFPlimits[1])

        # take only one point over 10
        self._Simplify()

        # update progressbar 2
        self._step += 1
        config._UpdateCK2(self._step)

        del self._sample  # to remove when more RAM available!!!!

        # END OF CONSTRUCTOR

    def _Simplify(self):
        for i in range(0, self._nBinlin, self._binjump):
            self._BFPlins = np.append(self._BFPlins,
                                      self._BFPlin[i])
            self._BFPbins = np.append(self._BFPbins,
                                      self._BFPbin[i])

    def _CumulHisto(self,
                    Min,
                    Max):
        """Create a cumulative mean histogram."""
        # Red Gate.
        rgate = FlowCytometryTools.IntervalGate((self._RFPlimits[0],
                                                 self._RFPlimits[1]),
                                                self.RFPchannel,
                                                region='in'
                                                )

        # Green Gate
        ggate = FlowCytometryTools.IntervalGate((Min,
                                                 Max),
                                                self.GFPchannel,
                                                region='in'
                                                )

        # Composite gate
        Gate = rgate & ggate

        # Gating.
        gsample = self._sample.gate(Gate)

        # Obtain real mean
        self._BFP = np.append(self._BFP,
                              gsample[self.BFPchannel].mean()
                              )

        # Creating histogram
        val = gsample.data[self.BFPchannel].values

        (self._BFPlin,
         self._BFPbin) = np.histogram(val,
                                      bins=self._nBinlin,
                                      range=(0.01, self._maxBFP)
                                      )

        self.mBFP = gsample[self.BFPchannel].mean()
        print(self.mBFP)

        # To have same dim that _BFPlin
        self._BFPbin = self._BFPbin[1:]

        # Contribution to the mean
        self._BFPlin = self._BFPlin * self._BFPbin / float(len(val))

        # Cumulative sum with correction for % and axis display (1000)
        self._BFPlin = np.cumsum(self._BFPlin)

    def _RemoveBubbles(self
                       ):
        """Remove bubble from MacsquantVYB."""
        # Remove bubbles and keep the wanted channels.
        self._sample.data = self._sample.data[self._C
                                              ][20000:
                                                20000+self._NbC
                                                ]
        # Get the number of cells remaining after treatment.
        self._NbC = self._sample.data.shape[0]

        # END OF REMOVE BUBBLES

    def _report(self,
                reportfile
                ):
        """Write the BFP values in the csv report file."""
        reportfile.write(self._Couple)
        for b in self._BFPlins:
            reportfile.write(","+str(b))
        reportfile.write('\n')
