# Window-based-Lane-Detection
Requirements: 
* Python 3.7 or above
* CARLA 0.9.15
* GPU with 8 GB of RAM recommended

## EDGE DETECTION ALGORITHM

For edge detection on an alternate picture, pass the filename into the function pipeline(), which returns the
midlane value if it is not in an error state. 
For generation of figures in paper, run cvbased-window.py as is.

## PID LANE FOLLOWING CONTROLLER

Please ensure that CARLA is running on your computer and serving from port 2000 (these should be default settings). Once confirmed that the CARLA client is active,
you may proceed with executing the notebook's cells sequentially to recreate the experiment(s)s.

Note the directories for saving images using the camera sensor in CARLA. Without the proper file system structure set up, this will cause the program to error.
This can be edited on the line directly below the comment `# Start camera` in the cell responsible for executing the experiment.

All helper methods are not necessary to run for the purpose of viewing the experiments. They were simply helpful for debugging and design.

## VISION LANE FOLLOWING CONTROLLER

Like the PID controller, this notebook's cells can be run sequentially to reproduce the experiment(s). Again, note the choice to save the images captured by the
camera sensor in CARLA. In the cell denoted `LANE FOLLOWING` and in the function named `compute_direction`, the first line of code determines the directory to
save the images to. If this directory does not exist, the experiment will fail.

In the cell captions `# Label the images`, you will find a method to label the images with their corresponding action as determined by the method. This will
use the location of where the images were saved, if they were saved, so again please make sure that the directories match up, otherwise this will fail to work.
It will not, however, impact the running of the experiment(s). 

All helper methods are not necessary to run for the purpose of viewing the experiments. They were simply helpful for debugging and design.
