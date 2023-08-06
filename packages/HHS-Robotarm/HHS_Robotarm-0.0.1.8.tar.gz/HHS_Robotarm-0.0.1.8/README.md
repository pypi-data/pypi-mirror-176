
!!! ALL OF THIS CODE WILL SOON BE MIGRATED TO A DOCUMENTATION SUBDIRECTORY WITHIN THE LARGER PYTHON LIBRARY UNDER DEVELOPMENT NOW !!!
(What this means is that what is here right now will be used to make a python library for easy installation and use, and will become legacy code/examples)


# ---- Note -----
Readme is in progress, as is the rest of the repository, and so might not be updated with the latest about where code is and what folders are.
Being so warned, here is the somewhat current readme, designed to be quickly read by a student in a computer science class so that they can get right on with making the robot arm do whatever they want it to:




# Robot arm!
Website: https://lparker885.github.io/HHS-robot-arm/

This code is for the robot arm at HHS. 
It has a few folders: maintenence, supersimpledemos, and networked-demos. 

Maintenence should not worried about unless the robot needs retuning or a reflash of the firmware, but feel free to look if you are interested. 

supersimpledemos has simple demos that are run on the pi inside the robot arm. 

networked-demos has three folders: 
- a folder for basic networking stuff, that has the dependancy (network.py) and a basic python network chat app
- a folder for recieve side stuff, which are the python programs that run on the pi inside the robot arm, and are basically just middlemen (sometimes with a bit of calculation for taking one kind of input and feeding it to the arduino like the arduino likes)
- a folder for send side stuff, which are the python programs that run on the pi outside of the robot arm that is connected with an ethernet cable, and send data, commands, input, whatever you want to call it, for super easy interaction. 
