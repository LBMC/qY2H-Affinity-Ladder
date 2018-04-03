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
        """Constructor method."""
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

        self._GFPslice = self.RFPchannel
        self._GFPslice += ' slice (' + str(self._RFPlimits[0])
        self._GFPslice += ', ' + str(self._RFPlimits[1]) + ')\n'
        self._GFPslice += self.GFPchannel
        self._GFPslice += ' slice (' + str(self._GFPlimits[0])
        self._GFPslice += ', ' + str(self._GFPlimits[1]) + ')'
        self._nBinlin = 100

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

        self._nsteps = 1 + 2  # Only one slice of GFP

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

        # Perform Titration.
        self._Titration(config)

        # Perform cumulative histogram for BFP
        self._CumulHisto(self._GFPlimits[0], self._GFPlimits[1])

        # update progressbar 2
        self._step += 1
        config._UpdateCK2(self._step)

        # print self._BFP

        # Initiate attribute to Fitting.
        self._BFPf1 = np.array([])  # fitted BFP.
        self._popt1 = np.array([])  # optimal parameters for the current fit.
        self._pcov1 = np.array([])  # covariance optimal parameters.
        self._r21 = 0  # R2 correlation coefficient.
        self._Equation = ''  # Equation of the current fit model.
        self._param = []  # Name of the parameters of the fit model.

        del self._sample  # to remove when more RAM available!!!!

        # END OF CONSTRUCTOR

    def _CumulHisto(self,
                    Min,
                    Max):
        """Creation of cumulative mean histogram."""
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

        # Creating histogram
        val = gsample.data[self.BFPchannel].values

        (self._BFPlin,
         self._BFPbin) = np.histogram(val,
                                      bins=self._nBinlin,
                                      range=(0.01, 25000)
                                      )

        self.mBFP = gsample[self.BFPchannel].mean()

        # To have same dim that _BFPlin
        self._BFPbin = self._BFPbin[:-1]

        # Contribution to the mean
        self._BFPlin = self._BFPlin * self._BFPbin / float(len(val))

        # Cumulative sum with correction for % and axis display (1000)
        self._BFPlin = np.cumsum(self._BFPlin)

    def _RemoveBubbles(self
                       ):
        """Remove bubble from MacsquantVYB."""
        # Remove bubbles and keep the wanted channels.
        self._sample.data = self._sample.data[self._C
                                              ][10000:
                                                10000+self._NbC
                                                ]
        # Get the number of cells remaining after treatment.
        self._NbC = self._sample.data.shape[0]

        # END OF REMOVE BUBBLES

    def _Titration(self,
                   config):
        """Titrate the BFP as a function of Cst RFP and Variable GFP."""
        # Red Gate.
        rgate = FlowCytometryTools.IntervalGate((self._RFPlimits[0],
                                                 self._RFPlimits[1]),
                                                self.RFPchannel,
                                                region='in'
                                                )

        # Defining the gates.
        ggate = FlowCytometryTools.IntervalGate((self._GFPlimits[0],
                                                 self._GFPlimits[1]),
                                                self.GFPchannel,
                                                region='in'
                                                )
        Gate = rgate & ggate

        # Gating.
        gsample = self._sample.gate(Gate)

        # Update BFP and GFP arrays.
        self._GFP = np.append(self._GFP,
                              (self._GFPlimits[0] + self._GFPlimits[1])/2
                              )

        self._BFP = np.append(self._BFP,
                              gsample[self.BFPchannel].mean()
                              )

        # Delete temp sample to accelerate reattribution.
        del gsample

        # update progressbar 2
        self._step += 1
        config._UpdateCK2(self._step)

        self._BFP = np.nan_to_num(self._BFP)

        # END OF TITRATION

    def _report(self,
                reportfile
                ):
        """Write the BFP values in the csv report file."""
        reportfile.write(self._Couple)
        for b in self._BFP:
            reportfile.write(","+str(b))
        reportfile.write('\n')
