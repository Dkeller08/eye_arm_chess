import rospy
import actionlib
from franka_gripper.msg import GraspGoal, GraspAction, GraspEpsilon

rospy.init_node('Franka_gripper_grasp_action')
client = actionlib.SimpleActionClient('/franka_gripper/grasp', GraspAction)
client.wait_for_server()
epsilon = GraspEpsilon(0.05,0.05)
goal = GraspGoal(0.08, epsilon, 0.1, 0.08)
rospy.loginfo(goal)
client.send_goal(goal)
client.wait_for_result(rospy.Duration.from_sec(5.0))