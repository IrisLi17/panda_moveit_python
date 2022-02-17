#!/usr/bin/env python

from move_group_python_interface_tutorial import MoveGroupPythonIntefaceTutorial
import sys
import rospy
import std_msgs.msg
import geometry_msgs.msg


def main():
    fake = sys.argv[1] == "true"
    ns = sys.argv[2]
    ready_pub = rospy.Publisher(ns + "/ready", std_msgs.msg.Bool, 1)
    client = MoveGroupPythonIntefaceTutorial(fake)
    arm_ready = True
    gripper_ready = True

    def arm_callback(data):
        print ns + " arm got target"
        client.go_to_pose_goal(data)
        arm_ready = True
    
    def gripper_callback(data):
        print(ns + " gripper got target...")
        client.move_gripper_to(data)
        gripper_ready = True

    rospy.Subsriber(ns + "/arm_target_pose", geometry_msgs.msg.Pose, arm_callback)
    rospy.Subscriber(ns + "/gripper_target", std_msgs.msg.Float64, gripper_callback)

    while not rospy.is_shutdown():
        if arm_ready and gripper_ready:
            ready_pub.publish(1)
            arm_ready = False
            gripper_ready = False
        rospy.sleep(0.01)



if __name__ == "__main__":
    main()
