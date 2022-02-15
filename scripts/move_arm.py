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
    group_name = "panda_arm"
    move_group = moveit_commander.MoveGroupCommander(group_name)
    pose_goal = geometry_msgs.msg.Pose()
    pose_goal.orientation.x = 3.0
    pose_goal.orientation.y = 0.0
    pose_goal.orientation.z = 3.0
    pose_goal.position.x = 0.5
    pose_goal.position.y = 0.0
    pose_goal.position.z = 0.58
    pose_list = [0.5,0.4,0.2,3,0,3]

    move_group.set_pose_target(pose_list)
    move_group.go(wait=True)
    move_group.stop()
    rospy.loginfo(move_group.get_current_pose())
    move_group.clear_pose_targets()


move()
