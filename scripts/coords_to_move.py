from move_cartesian import move
import rospy

rospy.loginfo("-1")
ready_state = [0.307015690168, -0.000254705662673, 0.590184127074]
left_corner = [0.388173755816, 0.268323682215, 0.131660533427]
right_corner = [0.388173755816, -0.268323682215, 0.131660533427]


def get_coords():
    rospy.loginfo("1")
    move(left_corner[0], left_corner[1], left_corner[2])
    rospy.loginfo("2")
    move(ready_state[0], ready_state[1], ready_state[2])
    rospy.loginfo("3")


rospy.loginfo("0")
get_coords()
