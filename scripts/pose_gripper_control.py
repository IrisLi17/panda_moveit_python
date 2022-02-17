#!/usr/bin/env python

from move_group_python_interface_tutorial import MoveGroupPythonIntefaceTutorial
import sys
import rospy
import std_msgs.msg
import geometry_msgs.msg
import copy


def main():
    fake = sys.argv[1] == "true"
    ns = sys.argv[2]
    ready_pub = rospy.Publisher("ready", std_msgs.msg.Bool, queue_size=1)
    client = MoveGroupPythonIntefaceTutorial(fake)
    arm_ready = True
    gripper_ready = True
    initial_pose = client.get_pose()

    def arm_callback(data):
        rospy.loginfo(rospy.get_caller_id() + " arm got target")
        print data
        client.go_to_pose_goal(data)
    
    def gripper_callback(data):
        rospy.loginfo(rospy.get_caller_id() + " gripper got target %f" % data.data)
        client.move_gripper_to(data)

    rospy.Subscriber("arm_target_pose", geometry_msgs.msg.Pose, arm_callback)
    rospy.Subscriber("gripper_target", std_msgs.msg.Float64, gripper_callback)

    while not rospy.is_shutdown():
        if arm_ready and gripper_ready:
            rospy.loginfo(rospy.get_caller_id() + " publish ready message")
            msg = std_msgs.msg.Bool()
            msg.data = True
            ready_pub.publish(msg)
            # Comment only for debugging
            arm_ready = False
            gripper_ready = False
        # rospy.sleep(0.01)



if __name__ == "__main__":
    main()
