#!/usr/bin/env python2.7

from __future__ import print_function
from six.moves import input

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import actionlib
from franka_gripper.msg import GraspGoal, GraspAction, GraspEpsilon
import geometry_msgs.msg
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

ready_state = [0.307015690168, -0.000254705662673, 0.590184127074]
left_corner = [0.27, 0.25, 0.4]
left_upcorner = [0.73, 0.25, 0.4]
high_state = 0.5
open_width = 0.09
closed_width = 0.08

def gripper(width):
    client = actionlib.SimpleActionClient('/franka_gripper/grasp', GraspAction)
    client.wait_for_server()
    epsilon = GraspEpsilon(0.1, 0.1)
    goal = GraspGoal(width, epsilon, 0.1, 0.08)
    rospy.loginfo(goal)
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
    # We get the joint values from the group and change some of the values:
    joint_goal = [-6.571155563683817e-06, -0.7850979563272178, 1.4132255206966704e-05, -2.355953352448032,
                  5.718449604152909e-05, 1.5709416773256253, 0.7849234744254199]

    # The go command can be called with joint values, poses, or without any
    # parameters if you have already set the pose or joint target for the group
    move_group.go(joint_goal, wait=True)

    # Calling ``stop()`` ensures that there is no residual movement
    move_group.stop()


def input_move(chess_move):
    squares = ''.join(char for char in chess_move if char.isdigit())
    letter_move_1 = left_corner[1] - int(squares[0]) * ((2 * left_corner[1]) / 7)
    number_move_1 = left_corner[0] + int(squares[1]) * ((left_upcorner[0] - left_corner[0]) / 7)
    letter_move_2 = left_corner[1] - int(squares[2]) * ((2 * left_corner[1]) / 7)
    number_move_2 = left_corner[0] + int(squares[3]) * ((left_upcorner[0] - left_corner[0]) / 7)
    # print(letter_move_1, "and number_1 = ", number_move_1, " leeter_2 = ", letter_move_2, "number_2 = ", number_move_2)
    move_readystate()
    gripper(open_width)
    if 'x' in chess_move:
        # we need to hit a piece
        move(number_move_2, letter_move_2, high_state)
        move(number_move_2, letter_move_2, left_corner[2])
        gripper(closed_width)
        move(number_move_2, letter_move_2, high_state)
        move_readystate()
        gripper(open_width)
        move(number_move_1, letter_move_1, high_state)
        move(number_move_1, letter_move_1, left_corner[2])
        gripper(closed_width)
        move(number_move_1, letter_move_1, high_state)
        move(number_move_2, letter_move_2, high_state)
        move(number_move_2, letter_move_2, left_corner[2])
        gripper(open_width)
        move(number_move_2, letter_move_2, high_state)
        move_readystate()
    else:
        move(number_move_1, letter_move_1, high_state)
        move(number_move_1, letter_move_1, left_corner[2])
        gripper(closed_width)
        move(number_move_1, letter_move_1, high_state)
        move(number_move_2, letter_move_2, high_state)
        move(number_move_2, letter_move_2, left_corner[2])
        gripper(open_width)
        move(number_move_2, letter_move_2, high_state)
        move_readystate()



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
move_readystate()
input_move(sys.argv[1])
