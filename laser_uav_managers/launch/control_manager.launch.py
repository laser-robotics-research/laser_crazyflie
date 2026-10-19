import os

import lifecycle_msgs.msg
from launch_ros.actions import LifecycleNode
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
from launch_ros.substitutions import FindPackageShare

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import EmitEvent
from launch.actions import RegisterEventHandler
from launch.event_handlers.on_process_start import OnProcessStart
from launch.events import matches_action
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch.substitutions import PythonExpression


def generate_launch_description():
    uav_name = os.environ['UAV_NAME']
    uav_type = os.environ['UAV_TYPE']

    defaults_uavs = ["x500", "lr7pro", "crazyflie"]

    if uav_name == "":
        print("The uav name dont set up in yours enviroment variables")
        return

    if uav_type == "" or (not uav_type in defaults_uavs):
        print("The uav type dont set up in yours enviroment variables")
        return

    # Declare arguments
    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            'nmpc_controller_file',
            default_value=PathJoinSubstitution(
                [FindPackageShare('laser_uav_controllers'), 'params', 'nmpc_controller', uav_type + '.yaml']),
            description='Full path to the file with the all parameters.'
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            'agile_planner_file',
            default_value=PathJoinSubstitution(
                [FindPackageShare('laser_uav_planners'), 'params', 'agile_planner', uav_type + '.yaml']),
            description='Full path to the file with the all parameters.'
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            'uav_parameters_file',
            default_value=PathJoinSubstitution(
                [FindPackageShare('laser_uav_managers'), 'params', 'laser_uavs', uav_type + '.yaml']),
            description='Full path to the file with the all parameters.'
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            'control_manager_file',
            default_value=PathJoinSubstitution([FindPackageShare('laser_uav_managers'),
                                                'params', 'control_manager.yaml']),
            description='Full path to the file with the all parameters.'
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            'use_sim_time',
            default_value=PythonExpression(['"', os.getenv('REAL_UAV', "true"), '" == "false"']),
            description='Whether use the simulation time.'))

    # Initialize arguments
    nmpc_controller_file = LaunchConfiguration('nmpc_controller_file')
    agile_planner_file = LaunchConfiguration('agile_planner_file')
    uav_parameters_file = LaunchConfiguration('uav_parameters_file')
    control_manager_file = LaunchConfiguration('control_manager_file')

    control_manager_lifecycle_node = LifecycleNode(
        package='laser_uav_managers',
        executable='control_manager',
        name='control_manager',
        namespace=uav_name,
        output='screen',
        parameters=[control_manager_file, uav_parameters_file, agile_planner_file,
                    nmpc_controller_file, {'use_sim_time': LaunchConfiguration('use_sim_time')}],
        remappings=[
            ('/' + uav_name + '/odometry_in', '/' + uav_name + '/estimation_manager/estimation'),
            ('/' + uav_name + '/motor_speed_estimation_in',
             '/' + uav_name + '/hw_api/motor_speed_estimated'),
            ('/' + uav_name + '/imu_in', '/' + uav_name + '/hw_api/imu'),
            ('/' + uav_name + '/motor_speed_reference_out', '/' +
             uav_name + '/control_manager/motor_speed_reference'),
            ('/' + uav_name + '/diagnostics_out', '/' + uav_name + '/control_manager/diagnostics'),
            ('/' + uav_name + '/attitude_rates_thrust_out', '/' +
             uav_name + '/control_manager/attitude_rates_thrust'),
            ('/' + uav_name + '/goto_in', '/' + uav_name + '/control_manager/goto'),
            ('/' + uav_name + '/goto_relative_in', '/' + uav_name + '/control_manager/goto_relative'),
            ('/' + uav_name + '/trajectory_path_in', '/' +
             uav_name + '/control_manager/trajectory_path'),
            ('/' + uav_name + '/takeoff', '/' + uav_name + '/control_manager/takeoff'),
            ('/' + uav_name + '/land', '/' + uav_name + '/control_manager/land'),
            ('/' + uav_name + '/api_diagnostics_in', '/' + uav_name + '/hw_api/diagnostics'),
        ]
    )

    event_handlers = []

    event_handlers.append(
        # Right after the node starts, make it take the 'configure' transition.
        RegisterEventHandler(
            OnProcessStart(
                target_action=control_manager_lifecycle_node,
                on_start=[
                    EmitEvent(event=ChangeState(
                        lifecycle_node_matcher=matches_action(control_manager_lifecycle_node),
                        transition_id=lifecycle_msgs.msg.Transition.TRANSITION_CONFIGURE,
                    )),
                ],
            )
        ),
    )

    event_handlers.append(
        RegisterEventHandler(
            OnStateTransition(
                target_lifecycle_node=control_manager_lifecycle_node,
                start_state='configuring',
                goal_state='inactive',
                entities=[
                    EmitEvent(event=ChangeState(
                        lifecycle_node_matcher=matches_action(control_manager_lifecycle_node),
                        transition_id=lifecycle_msgs.msg.Transition.TRANSITION_ACTIVATE,
                    )),
                ],
            )
        ),
    )

    ld = LaunchDescription()

# Declare the arguments
    for argument in declared_arguments:
        ld.add_action(argument)

# Add client node
    ld.add_action(control_manager_lifecycle_node)

# Add event handlers
    for event_handler in event_handlers:
        ld.add_action(event_handler)

    return ld
