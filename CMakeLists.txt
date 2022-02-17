install(PROGRAMS
  scripts/move_group_python_interface_tutorial.py
  scripts/replay_trajectory.py
  scripts/pose_gripper_control.py
  scripts/sync_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})