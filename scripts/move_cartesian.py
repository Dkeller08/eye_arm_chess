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

def move():
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
    wpose = move_group.get_current_pose().pose
    waypoints = []
    wpose.position.z -=  0.1  # First move up (z)
    wpose.position.y +=  0.2  # and sideways (y)
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.x +=  0.1  # Second move forward/backwards in (x)
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.y -=  0.1  # Third move sideways (y)
    wpose.orientation.y +=0.2
    waypoints.append(copy.deepcopy(wpose))
    (plan, fraction) = move_group.compute_cartesian_path(
            waypoints, 0.01, 0.0  # waypoints to follow  # eef_step
        )  # jump_threshold
    rospy.loginfo("Planned")
    display_trajectory = moveit_msgs.msg.DisplayTrajectory()
    display_trajectory.trajectory_start = robot.get_current_state()
    display_trajectory.trajectory.append(plan)
    # Publish
    display_trajectory_publisher.publish(display_trajectory)
    rospy.loginfo("published")
    move_group.execute(plan, wait=True)

move()
