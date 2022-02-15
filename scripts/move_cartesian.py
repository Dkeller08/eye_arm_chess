#!/usr/bin/env python2.7

from __future__ import print_function
from six.moves import input

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

ready_state = [0.307015690168, -0.000254705662673, 0.590184127074]
left_corner = [0.388173755816, 0.268323682215, 0.131660533427]


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
#move(left_corner[0], left_corner[1], left_corner[2])
#move(ready_state[0], ready_state[1], ready_state[2])
