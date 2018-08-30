**<span style="color:teal">Analysis of QY2H Data</span>**
===

**<span style="color:teal">Introduction</span>**
--
This program permits to easily generate *in cellulo* affinity ladders from `quantitative Yeast Two Hybrid` experiments [Ref]. The program requires linear flowcytometry data `.fcs` files, and generates a `.csv` table file associated with a `.pdf` report enclosing the affinity ladder graph.

**<span style="color:teal">Authors</span>**
--

![Simbio Logo](doc/Logo.jpg) |![LBMC Logo](doc/Logo_LBMC.jpg) ![CNRS Logo](doc/Logo_cnrs.jpg) ![ENS Logo](doc/Logo_ens.jpg) |
-----------------------------|------------|
**CLUET David** | david.cluet@ens-lyon.fr|
**SPICHTY Martin** | martin.spichty@ens-lyon.fr|


**<span style="color:teal">License</span>**
--

Copyright CNRS 2013


>This software is a computer program whose purpose is to automatically analyze QY2H data (`.fcs` files)
and generate *in cellulo* affinity ladder.
>
>This software is governed by the CeCILL  license under French law and abiding
by the rules of distribution of free software. You can use, modify and/ or
redistribute the software under the terms of the CeCILL license as circulated
by CEA, CNRS and INRIA at the following URL:
http://www.cecill.info/index.en.html
>
>As a counterpart to the access to the source code and  rights to copy, modify
and redistribute granted by the license, users are provided only with a limited
warranty  and the software's author,the holder of the economic rights, and the
successive licensors have only limited liability.
>
>In this respect, the user's attention is drawn to the risks associated with
loading, using, modifying and/or developing or reproducing the software by the
user in light of its specific status of free software, that may mean  that it
is complicated to manipulate, and that also therefore means  that it is
reserved for developers  and  experienced professionals having in-depth
computer knowledge. Users are therefore encouraged to load and test the
software's suitability as regards their requirements in conditions enabling
the security of their systems and/or data to be ensured and, more generally,
to use and operate it in the same conditions as regards security.
>
>The fact that you are presently reading this means that--delete the_remote_branch you have had knowledge
of the CeCILL license and that you accept its terms.

**<span style="color:teal">Requirements</span>**
--
This program is optimized for `Python 2.7` with the following libraries:

* `datetime`: To generate unique Analysis ID and file name.

* `FlowCytometryTools`: To open `.fcs` files and manipulate flowcytometry data. http://eyurtsev.github.io/FlowCytometryTools/

* `glob`: To identify the `.fcs` files in the Input folder.

* `matplotlib`: To generate the curves.

* `numpy`: To generate and manipulate arrays.

* `os`: To handle paths of the raw data and generated files.

* `Pillow / PIL`: To display images within the GUI of the program.

* `sys`: To permit manual abortion of the program.

* `Tkinter`: To generate the GUI of the program.

**<span style="color:teal">Files</span>**
--

- README.md
- LICENSE.txt

- [] **src**
    - `Analysis_QY2H.py`

    - [] **utils**
        - `__init__.py`
        - `channels.config`
        - `Colors.py`
        - `Configuration.py`
        - `Configure_Channels.py`
        - `Ending_Window.py`
        - `Functions.py`
        - `Logo.jpg`
        - `Object_Echantillon.py`
        - `Opening_window.py`
        - `Variables.py`

- [] **doc**
    - Analysis_Configuration.png
    - Analysis_Progress.png
    - Logo_cnrs.jpg
    - Logo_ens.jpg
    - Logo_LBMC.jpg
    - Logo.jpg
    - Main_Menu.jpg
    - Results.png
    - Select_Channels.png
    - Select_File.png
    - Select_Input.png
    - Select_Output.png



**<span style="color:teal">User Guide</span>**
--

*<span style="color:teal">1 Recommendation for acquisition</span>*
-
Our program requires `linear` values for all fluorescence channels. Thus, be vigilant that your acquisition program is saving data as linear (even if your acquisition display is `log` or `hyper log`).

Yeasts are small cells, so we recommend to use the `Height (H)` of your channels instead of the `Area (A)` [Ref]. Moreover, some flowcytometer can apply internal corrections on specific channels. For example, the MacsquantVYB (that we used for our experiment) is correcting the `Area A` of each channels.
>Area is the sum of a defined number of adjacent samples at the trigger time point devided by a scaling factor. This factor is chosen in a way that for "normal" events H=A to obtain a diagonal. The scaling factor is pressure dependent.

Thus we strongly recommend to use as much as possible **non-manipulated** values.  

*<span style="color:teal">2 Main Menu</span>*
-
To start the program you need to execute the `Analysis_QY2H.py` python script:

```bash
$ python Analysis_QY2H.py
```

The main menu will propose you different functions:
1. **Configure channels** That permit you to specifically identify and attribute the names of the flowcytometer channels.
2. **Start analysis** To generate a `quantitative Yeast Two Hybrid` affinity from a set of `.fcs` files.
3. **Abort** To exit the program.


![Main Menu](/doc/Main_Menu.png)

Before performing any analysis it is recommended to configure your channels so they fit with the names used by your flowcytometer during the acquisition.

*<span style="color:teal">3 Configure the names of the channels</span>*
-

When clicking on `Configure channels`, the program prompts you to choose a `.fcs` file.

![Select File](/doc/Select_File.png)

The program will identify all channels recorded in your file. You can then attribute the correct names to the various channels. They will be saved in the `channels.config` file when clicking on `VALIDATE`

![Select Channels](/doc/Select_Channels.png)

>Note that in our original qY2H system the `BFP` channel corresponds to the `Read-Out` you want to quantify.
>The `RFP` and the `GFP` channels correspond to the `BD-Bait` and `AD-Prey` fusion proteins.



*<span style="color:teal">4 Perform an analysis</span>*
-
When clicking on `Start analysis`, the program prompts you the analysis configuration window. You need first to select the folder where all your files (for one single experiment) are stored.

The program will automatically find all `.fcs` files present in this folder and display them in the analysis settings interface.

![Input](/doc/Select_Input.png)

You need then to specific in which folder you want the output files to be generated. By default, the program is set on the input folder.

![Output](/doc/Select_Output.png)

Once the path of the `ÌNPUT` and `OUTPUT` folders are set, you have access to the analysis settings. The program will generate the `Affinity ladder` by taking a sub-ensemble of cells using thin gating in the `AD-Prey GFP` and `BD-Bait RFP` channels. By default the minimal and maximal values are set to those of the Fig 3 (B and C) of our publication.

![Configuration](/doc/Analysis_Configuration.png)

The maximum in the `Read-out BFP` channel, corresponds to the upper-limit of the generated `Cumulative mean` for each sample. If after one analysis your curves are not reaching a plateau, increase this value. In the reverse situation where the plateau appears to early, decrease this maximum.

The value `BFP bins` corresponds to the number of points you want to be displayed on the final graph. In order to avoid binning effects of the `Cumulative mean` depending on this value, the `Cumulative mean` is first calculated using a hardcoded 5000 bins value that allows an excellent match between the convergence of the calculated `Cumulative mean` and the actual `Mean` of the population. Then, regularly spaced points will be picked to be displayed following the `BFP bins` value that you specified.

You can remove the background of the system by selecting `Remove negative Control`. In this case the negative control will not be displayed (as it becomes equal to 0). Deselect this option could be a good option to monitor the real contribution of the background in your experimental/analyis setup, especially for the weakest interactors.

You need to specify which sample file corresponds to your negative control. In this example, the file `DC2017-06-22_0-0.fcs` corresponds to a qY2H experiment performed with the fluorescent empty (0) bait and prey fusion proteins.

The `Number of cells` value corresponds to the maximum number of cells to be loaded from your file before doing the dual gating in the `AD-Prey GFP` and `BD-Bait RFP` channels.

You have the possibility to display the `Cumulative mean` in log or linear scale.

When clicking `START`, the program proceeds to the analysis (only if a negative control has been specified).

![Progress](/doc/Analysis_Progress.png)

During the analysis the two `Progress Bars` inform you which file (first bar) is currently processed, and which analysis step (second bar) is performed.

Finally, the program displays the result of the analysis, with the main settings in the title.

![Results](/doc/Results.png)

Click on `ABORT` to exit the program.

*<span style="color:teal">5 Output files</span>*
-
The program generates two files. One `.csv` table containing the `mean BFP` value for each file (after substraction of the negative control, if selected), and one `.pdf` report file with the graph. This two files have a common unique prefix based on the date and time of analysis.  
