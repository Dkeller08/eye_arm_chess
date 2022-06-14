from __future__ import print_function
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import actionlib
from franka_gripper.msg import GraspGoal, GraspAction, GraspEpsilon, MoveGoal, MoveAction

ready_state = [0.307015690168, -0.000254705662673, 0.590184127074]
up_state = [0.31, 0, 0.87]
left_corner = [0.30, 0.205, 0.39]
left_upcorner = [0.70, 0.205, 0.39]
high_state = 0.49
horse_hight = 0.405
closed_width = 0


def gripper(width):
    client = actionlib.SimpleActionClient('/franka_gripper/grasp', GraspAction)
    client.wait_for_server()
    epsilon = GraspEpsilon(0.1, 0.1)
    goal = GraspGoal(width, epsilon, 0.1, 0.08)
    rospy.loginfo(goal)
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(5.0))


def gripper_move():
    client = actionlib.SimpleActionClient('/franka_gripper/move', MoveAction)
    client.wait_for_server()
    goal = MoveGoal(width=0.04, speed=0.08)
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(5.0))


def move(x, y, z):
    wpose = move_group.get_current_pose().pose
    waypoints = []
    wpose.position.z = z  # First move up (z)
    wpose.position.y = y  # and sideways (y)
    wpose.position.x = x  # Second move forward/backwards in (x)
    waypoints.append(copy.deepcopy(wpose))

    (plan, fraction) = move_group.compute_cartesian_path(
        waypoints, 0.01, 0.0  # waypoints to follow  # eef_step
    )  # jump_threshold
    display_trajectory = moveit_msgs.msg.DisplayTrajectory()
    display_trajectory.trajectory_start = robot.get_current_state()
    display_trajectory.trajectory.append(plan)
    # Publish
    display_trajectory_publisher.publish(display_trajectory)
    move_group.execute(plan, wait=True)


def move_readystate():
    # move(0.3, 0, 0.7)
    # We get the joint values from the group and change some of the values:
    joint_goal = [-6.571155563683817e-06, -0.7850979563272178, 1.4132255206966704e-05, -2.355953352448032,
                  5.718449604152909e-05, 1.5709416773256253, 0.7849234744254199]

    # The go command can be called with joint values, poses, or without any
    # parameters if you have already set the pose or joint target for the group
    move_group.set_max_velocity_scaling_factor(1)
    move_group.set_max_acceleration_scaling_factor(1)
    move_group.go(joint_goal, wait=True)

    # Calling ``stop()`` ensures that there is no residual movement
    move_group.stop()


def input_move(chess_move):
    h = left_corner[2]
    if 'b' in chess_move:
        bin_x = 0.57
    elif 'w' in chess_move:
        bin_x = 0.47
    squares = ''.join(char for char in chess_move if char.isdigit())
    letter_move_1 = left_corner[1] - int(squares[0]) * ((2 * left_corner[1]) / 7)
    number_move_1 = left_corner[0] + int(squares[1]) * ((left_upcorner[0] - left_corner[0]) / 7)
    letter_move_2 = left_corner[1] - int(squares[2]) * ((2 * left_corner[1]) / 7)
    number_move_2 = left_corner[0] + int(squares[3]) * ((left_upcorner[0] - left_corner[0]) / 7)
    gripper_move()
    if 'x' in chess_move:
        h_1 =h
        h_2 = h
        if 'H' is chess_move[0]:
            h_1 = horse_hight
        elif 'H' in chess_move:
            h_2 = horse_hight
        # we need to hit a piece
        #move(number_move_2, letter_move_2, high_state)
        move(number_move_2, letter_move_2, h_2)
        gripper(closed_width)
        move(number_move_2, letter_move_2, high_state)
        move(bin_x, -0.3, high_state)
        gripper_move()
        move(number_move_1, letter_move_1, high_state)
        move(number_move_1, letter_move_1, h_1)
        gripper(closed_width)
        move(number_move_1, letter_move_1, high_state)
        move(number_move_2, letter_move_2, high_state)
        move(number_move_2, letter_move_2, h_1+0.003)
        gripper_move()
        #move(number_move_2, letter_move_2, high_state)
        move_readystate()
    elif 'OK' in chess_move:
        if '7' in squares[2]:
            rook_move = letter_move_1 - ((2 * left_corner[1]) / 7)
            king_move = letter_move_1 - 2 * ((2 * left_corner[1]) / 7)
        else:
            rook_move = letter_move_1 + ((2 * left_corner[1]) / 7)
            king_move = letter_move_1 + 2 * ((2 * left_corner[1]) / 7)
        #move(number_move_1, letter_move_1, high_state)
        move(number_move_1, letter_move_1, h)
        gripper(closed_width)
        move(number_move_1, letter_move_1, high_state)
        move(number_move_2, king_move, high_state)
        move(number_move_2, king_move, h+0.003)
        gripper_move()
        move(number_move_2, king_move, high_state)
        move(number_move_2, letter_move_2, high_state)
        move(number_move_2, letter_move_2, left_corner[2])
        gripper(closed_width)
        move(number_move_2, letter_move_2, high_state)
        move(number_move_1, rook_move, high_state)
        move(number_move_1, rook_move, left_corner[2]+0.003)
        gripper_move()
        #move(number_move_1, rook_move, high_state)


    else:
        if "H" in chess_move:
            h = horse_hight
        #move(number_move_1, letter_move_1, high_state)
        move(number_move_1, letter_move_1, h)
        gripper(closed_width)
        move(number_move_1, letter_move_1, high_state)
        move(number_move_2, letter_move_2, high_state)
        move(number_move_2, letter_move_2, h+0.003)
        gripper_move()
        #move(number_move_2, letter_move_2, high_state)
        h = left_corner[2]

    move_up()

def move_up():
    joint_goal = [0.0003318882895201948, -0.284279482700614, -0.00037862229923995433, -1.1254750879020021, 0.0016921628054822192, 0.8419186478455859, 0.7855230086561859]
    # The go command can be called with joint values, poses, or without any
    # parameters if you have already set the pose or joint target for the group
    move_group.set_max_velocity_scaling_factor(1)
    move_group.set_max_acceleration_scaling_factor(1)
    move_group.go(joint_goal, wait=True)

    # Calling ``stop()`` ensures that there is no residual movement
    move_group.stop()



moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node("move_arm", anonymous=True)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
display_trajectory_publisher = rospy.Publisher(
    "/move_group/display_planned_path",
    moveit_msgs.msg.DisplayTrajectory,
    queue_size=20,
)
group_name = "panda_arm"
move_group = moveit_commander.MoveGroupCommander(group_name)

