FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive
ENV GZ_VERSION fortress
ENV ROS_DISTRO humble
ENV ROS_WS /home/docker_ws

# Make sure everything is up to date before building from source
RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get update && apt-get install -q -y --no-install-recommends \
    dirmngr \
    gnupg \
    lsb-release \
    wget \
    curl \
    git \
    ca-certificates \
    build-essential \
    cmake \
    python3-pip \
  && python3 -m pip install -U pip \
  && python3 -m pip install vcstool \
  && apt-get clean

RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null && \
  apt-get update && apt-get install -q -y --no-install-recommends \
    python3-colcon-ros \
    python3-colcon-common-extensions \
    python3-rosdep \
    && apt-get clean


# Create ROS workspace
RUN mkdir -p $ROS_WS/src
WORKDIR $ROS_WS


# Create required directories for rosdep initialization
RUN mkdir -p /etc/ros/rosdep/sources.list.d/

# Initialize rosdep
RUN sh -c 'echo "yaml http://packages.ros.org/ros/ubuntu/$(lsb_release -sc) main" > /etc/ros/rosdep/sources.list.d/20-default.list'
RUN if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then \
        rosdep init; \
    fi && \
    rosdep update
    
# Get ROS2 Control and gz_ros2_control dependencies
RUN wget https://raw.githubusercontent.com/ros-controls/control.ros.org/master/ros_controls.$ROS_DISTRO.repos \
    && vcs import src < ros_controls.$ROS_DISTRO.repos

# Install ROS dependencies
RUN rosdep update --rosdistro=$ROS_DISTRO \
    && rosdep install --from-paths src --ignore-src -r -y

# Set working directory and clone your ROS2 package into the container
WORKDIR $ROS_WS/src
RUN git clone https://github.com/Spartan-Velanjeri/dd_robot.git

# Build the workspace
RUN . /opt/ros/${ROS_DISTRO}/setup.sh \
    && colcon build --symlink-install

# Source ROS2 setup
RUN echo "source $ROS_WS/install/setup.bash" >> ~/.bashrc

# Set the container's entrypoint to run your launch file. Make sure you have Gazebo Fortress installed
ENTRYPOINT ["ros2", "launch", "dd_robot", "gazebo_robot.launch.py"]
