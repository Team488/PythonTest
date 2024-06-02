from robot import MyRobot

def test_robot_builds(robot: MyRobot):
    # This is a hack to call robotInit directly, the fixture cleanup code is looking for this function to have been added by the Control fixture
    robot._TestRobot__robotInitialized = lambda: None
    robot.robotInit()