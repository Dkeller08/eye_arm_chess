import rospy
import actionlib
from franka_gripper.msg import GraspGoal, GraspAction

rospy.init_node('Franka_gripper_grasp_action')
client = actionlib.SimpleActionClient('/franka_gripper/move', GraspAction)
goal = GraspGoal(width = 0.08, force = 0.08)
client.send_goal(goal)