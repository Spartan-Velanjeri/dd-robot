import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
	gz_args = LaunchConfiguration('gz_args',default=' -r -v 4 empty.sdf')
	
	return LaunchDescription([
	# Launch gazebo environment
	IncludeLaunchDescription(
		PythonLaunchDescriptionSource(
			[os.path.join(get_package_share_directory('ros_gz_sim'),'launch','gz_sim.launch.py')]),
		launch_arguments=[('gz_args',gz_args)],
	),
])
