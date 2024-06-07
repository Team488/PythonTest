Following instructions here
https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/python-setup.html

Install python 3.12

## robotpy
this lib is the basic core stuff
`pip install robotpy`
`python -m robotpy init`
`python -m robotpy sync`

To deploy to robot:
`python -m robotpy deploy`

Api docs
https://robotpy.readthedocs.io/projects/robotpy/en/stable/


## pyfrc
simulation and testing support
https://robotpy.readthedocs.io/projects/pyfrc/en/stable/

# simulation
python -m robotpy sim

# Teams using python

## Magicbot style robots (as opposed to Command)

### Dropbears
https://github.com/thedropbears/pycrescendo/blob/main/robot.py
They have some vscode examples working

https://github.com/thedropbears/pycrescendo/blob/main/components/chassis.py
Here's the swerve drive code


## Command Bot

### 1757 WestwoodRobotics

https://github.com/1757WestwoodRobotics/2024-Crescendo
