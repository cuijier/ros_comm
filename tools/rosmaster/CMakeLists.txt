cmake_minimum_required(VERSION 2.8.3)
project(rosmaster)
find_package(catkin REQUIRED rosthrift)

catkin_python_setup()

thrift_add_service_files(
  FILES
  MasterAPI.thrift
)

thrift_generate_messages(
  DEPENDENCIES
)
catkin_package()

catkin_add_nosetests(test)
