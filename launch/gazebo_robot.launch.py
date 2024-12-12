
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription, ExecuteProcess, RegisterEventHandler, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node
import xacro
def generate_launch_description():

	gz_args = LaunchConfiguration('gz_args',default=' -r -v 4 empty.sdf')
	use_sim_time = LaunchConfiguration('use_sim_time',default=True)
	# command_params_file = os.path.join(get_package_share_directory('cmd_publisher'), 'config', 'commands.yaml')
	# gz_ros2_control_demos_path = os.path.join(
	# 	get_package_share_directory('gz_ros2_control_demos'))
	
	# xacro_file = os.path.join(gz_ros2_control_demos_path,'urdf','test_diff_drive.xacro.urdf')

	dd_robot_path = os.path.join(
		get_package_share_directory('dd_robot'))
	# config = os.path.join(dd_robot_path, 'config', 'commands.yaml')
	xacro_file = os.path.join(dd_robot_path,'urdf','test_diff_drive.xacro.urdf')	
	doc = xacro.parse(open(xacro_file))
	xacro.process_doc(doc)
	params = {'robot_description':doc.toxml(),'use_sim_time':use_sim_time}
	
	print(params)
	
	node_robot_state_publisher = Node(
		package='robot_state_publisher',
		executable='robot_state_publisher',
		output='screen',
		parameters=[params],
	)
	
	
	gz_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=['-string', doc.toxml(),
                   '-name', 'cartpole',
                   '-allow_renaming', 'true'],
    )
	
	load_joint_state_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )
	
	load_joint_trajectory_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'diff_drive_base_controller'],
        output='screen'
    )

    # Bridge
	# 
	bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock','/camera@sensor_msgs/msg/Image@ignition.msgs.Image'],
        output='screen',
    )

	# Command Publisher
	command_publisher_node = Node(
    	package='dd_robot',
    	executable='cmd_vel_publisher.py',
    	name='command_publisher',
    	output='screen',
    )
	
	
	return LaunchDescription([
        bridge,
        # Launch gazebo environment
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [os.path.join(get_package_share_directory('ros_gz_sim'),
                              'launch', 'gz_sim.launch.py')]),
            launch_arguments=[('gz_args', [' -r -v 4 empty.sdf'])]),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=gz_spawn_entity,
                on_exit=[load_joint_state_controller],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=load_joint_state_controller,
                on_exit=[load_joint_trajectory_controller],
            )
        ),
        node_robot_state_publisher,
        gz_spawn_entity,
        command_publisher_node, # disabling cyclic command publisher
        # Launch Arguments
        DeclareLaunchArgument(
            'use_sim_time',
            default_value=use_sim_time,
            description='If true, use simulated clock'),
    ])
