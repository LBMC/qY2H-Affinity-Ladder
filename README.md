Analysis of QY2H Data
===

Authors
--

![Simbio Logo](src/Logo.jpg) ||
-----------------------------|------------|
CLUET David | david.cluet@ens-lyon.fr|
SPICHTY Martin | martin.spichty@ens-lyon.fr|


License
--

Copyright CNRS 2013


>This software is a computer program whose purpose is to automatically analyze QY2H data (`.fcs` files)
and generate in cellulo affinity ladder.
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
>The fact that you are presently reading this means that you have had knowledge
of the CeCILL license and that you accept its terms.

Requirements
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
