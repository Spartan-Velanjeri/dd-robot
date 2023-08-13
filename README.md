
# This branch is about getting this pkg to run on Docker

## In Progress

# dd_robot

`dd_robot` is a differential drive robot simulation for ROS2. This package provides tools to simulate, control, and visualize a differential drive robot in a Gazebo environment.

Currently the robot basically does alternating cyclic motion based on the commands from a YAML file.

![Project Banner](doc/dd.gif)

You can check out the [Video](doc/screenshot_works.webm) of the working.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Note](#note)
- [Credits](#credits)
  
## Features

- Differential drive robot simulation in Gazebo.
- Customizable via ROS2 parameters.
- Integrated command publisher for movement control using YAML file.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- [ROS2](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html) (version `HUMBLE`).
- [Gazebo](https://gazebosim.org/docs/garden/ros_installation#installing-the-default-gazebo-version-for-a-ros-distribution-using-binary-installations) (version `FORTRESS`). Download 
- ROS2 Control and gz_ros2_control (apt or source build). [SEE NOTES](#note)


## Installation

1. **Navigate to your ROS2 workspace**

    ```bash
    cd ~/ros2_ws/src/
    ```

2. **Clone the Repo inside the src file**

    ```bash
    git clone https://github.com/Spartan-Velanjeri/dd_robot.git
    ```

3. **Build the package**

    ```bash
    colcon build --packages-select dd_robot
    ```

4. **Source your ROS2 workspace**

    ```bash
    source install/setup.bash
    ```

## Usage

1. **Launch the Gazebo environment with the robot**

    ```bash
    ros2 launch dd_robot gazebo_robot.launch.py
    ```

You can see that the Differential Drive Robot starts moving based on a cyclic command present inside ```config/commands.yaml``` and is read from the ```scripts/cmd_vel_publisher.py```


This is just a proof of concept code to test out ROS2 Humble and Gazebo Fortress.

## Note

 1. I've built the ROS Control from source, since I had trouble in connecting ROS2 Control and gz_ros2_control and the binary build had failed for Humble. 
 You can build using this link [here](https://control.ros.org/humble/doc/getting_started/getting_started.html) (pretty straightforward!) and make sure to keep all the packages in the src after building.

 2. I'll try to work with the apt version, but this works for now. However, if you can get the APT installation succesffuly, make sure to change the respective controller path in the urdf of the bot. Let me know if you need any help with that

 3. Also if you get an error with running the cmd_vel_publisher, it could be due to your python version. Make sure to NOT run with any virtualenv or conda.

## Credits

Utilised the [differential drive robot](https://github.com/ros-controls/gz_ros2_control/blob/master/gz_ros2_control_demos/urdf/test_diff_drive.xacro.urdf) from the [gz_ros2_control](https://github.com/ros-controls/gz_ros2_control/tree/master) package for this application.

Thank you !

`dd_robot` was developed by `Parthan Manisekaran`. For any questions or feedback, please reach out to `Parthanvelanjeri@Hotmail.com`.
