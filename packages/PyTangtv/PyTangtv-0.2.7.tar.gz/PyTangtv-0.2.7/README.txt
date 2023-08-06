PyTangtv is a set of tools used to work with data from LLNL Tangential viewing camera diagnostics from the DIII-D experiment.

Picker - program to select features from the loaded image and output the pixel coordinates. If a calibration board module is provided then the program can output x,y,z coordinates as well.

PyAlign - program to do simple, rigid, image plane transformations of the loaded image. A background image can be loaded and then the two layered to facilitate aligning the two.

PyMorph - used to determine the foreground->background control points to do polynomial spatial warping of the foreground to match the background. 
