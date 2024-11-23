# Getting Started

Install python 3.12: https://www.python.org/downloads/release/python-3127/

In a terminal from this repository's folder, run the following commands:

```
pip install robotpy
```

```
python -m robotpy init
```

```
python -m robotpy sync
```

Now everything should be installed and ready to go. You can verify this by running the automated tests:

```
python -m robotpy test
```

## Running in the simulator

```
python -m robotpy sim
```

# Archive / notes

Following instructions here
https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/python-setup.html

Install python 3.12

## robotpy
this lib is the basic core stuff
`pip install robotpy`
`python -m robotpy init`
`python -m robotpy sync`

To run all tests (done with pytest under the covers and a bunch of fixtures to make it easy to write robot tests):
`python -m robotpy test`

To run a single test:
`python -m robotpy test -- -k robot_builds_test`

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

https://robotpy.github.io/community/

## Magicbot style robots (as opposed to Command)

### Dropbears
https://github.com/thedropbears/pycrescendo/blob/main/robot.py
They have some vscode examples working

https://github.com/thedropbears/pycrescendo/blob/main/components/chassis.py
Here's the swerve drive code


## Command Bot

### 1757 WestwoodRobotics

https://github.com/1757WestwoodRobotics/2024-Crescendo


### 1721
They are using yaml files for config in an interesting way

https://github.com/FRC-1721/1721-RapidReact/blob/main/rio/subsystems/drivetrain.py