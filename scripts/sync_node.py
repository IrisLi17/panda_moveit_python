#!/usr/bin/env python

import rospy
import pickle, sys
import geometry_msgs.msg
import std_msgs.msg
import math
# variable: ready_1, ready_2, ...
# if all ready flags are true, pub a message to move to the next step, clear ready flags

# in each control node, pub ready flag before the first move; subscribe to ``move to next'' message, and call execution in its callback function
    
def main():
    ready_flags = [False, False]
    file_name = sys.argv[1]
    with open(file_name, "rb") as f:
        data = pickle.load(f)
    panda0_traj_ee = data["panda0_ee"]
    panda0_traj_gripper = data["panda0_finger"]
    panda1_traj_ee = data["panda1_ee"]
    panda1_traj_gripper = data["panda1_finger"]
    assert len(panda0_traj_ee) == len(panda1_traj_ee) and len(panda0_traj_ee) == len(panda0_traj_gripper) and len(panda0_traj_gripper) == len(panda1_traj_gripper)
    arm0_pose_pub = rospy.Publisher('/robot1/arm_target_pose', geometry_msgs.msg.Pose, queue_size=1)
    gripper0_pub = rospy.Publisher('/robot1/gripper_target', std_msgs.msg.Float64, queue_size=1)
    arm1_pose_pub = rospy.Publisher('/robot2/arm_target_pose', geometry_msgs.msg.Pose, queue_size=1)
    gripper1_pub = rospy.Publisher('/robot2/gripper_target', std_msgs.msg.Float64, queue_size=1)
    
    def callback0(data):
        print "robot1 ready"
        ready_flags[0] = data

    def callback1(data):
        print "robot2 ready"
        ready_flags[1] = data
    
    rospy.Subscriber('/robot1/ready', std_msgs.msg.Bool, callback0)
    rospy.Subscriber('/robot2/ready', std_msgs.msg.Bool, callback1)

    step = 0
    while not rospy.is_shutdown() and step < len(panda0_traj_ee):
        if ready_flags[0] and ready_flags[1]:
            # command the next move
            pose0 = geometry_msgs.msg.Pose()
            pose0.position.x = panda0_traj_ee[step][0]
            pose0.position.y = panda0_traj_ee[step][1]
            pose0.position.z = panda0_traj_ee[step][2]
            pose0.orientation.x = math.sqrt(2) / 2.0
            pose0.orientation.y = math.sqrt(2) / 2.0
            pose1 = geometry_msgs.msg.Pose()
            pose1.position.x = panda1_traj_ee[step][0]
            pose1.position.y = panda1_traj_ee[step][1]
            pose1.position.z = panda1_traj_ee[step][2]
            pose1.orientation.x = math.sqrt(2) / 2.0
            pose1.orientation.y = math.sqrt(2) / 2.0
            arm0_pose_pub.publish(pose0)    
            arm1_pose_pub.publish(pose1)
            gripper0_pub.publish(panda0_traj_gripper[step])
            gripper1_pub.publish(panda1_traj_gripper[step])

            ready_flags = [False, False]
            step += 1


if __name__ == "__main__":
    main()
