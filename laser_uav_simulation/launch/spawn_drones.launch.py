import yaml
from launch_ros.substitutions import FindPackageShare

import launch
from launch.actions import DeclareLaunchArgument
from launch.actions import ExecuteProcess
from launch.actions import IncludeLaunchDescription
from launch.actions import OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch.substitutions import TextSubstitution


def launch_setup(context: launch.LaunchContext, ld):
    # #{ spawn drone config

    config_file_path = LaunchConfiguration('spawn_drones_file').perform(context)

    # #}

    # #{ create the cmd lines with arguments for spawn drones
    process_actions = []

    spawn_script_path = PathJoinSubstitution(
        [FindPackageShare('laser_uav_simulation'), 'scripts', 'spawn_drone.sh']).perform(context)
    uxrce_script_path = PathJoinSubstitution(
        [FindPackageShare('laser_uav_simulation'), 'scripts', 'start_uxrce_protocol.sh']).perform(context)

    try:
        with open(config_file_path, 'r') as file:
            config_data = yaml.safe_load(file)['/**/**']
    except EnvironmentError:
        print(f"Error: Can't find the config file in '{config_file_path}'")
        return None
    except KeyError:
        print(f"Error: The key '/**/**' don't exist in YAML.")
        return None

    uavs = config_data.get('ros__parameters', {})

    uavs_available = ['x500', 'lr7pro', 'crazyflie']

    for uav in uavs:
        id = uav.get('id', 0)
        if id <= 0:
            continue
        namespace = "uav" + str(id)
        uav_type = uav.get('type', '')
        fcu_type = uav.get('fcu', '')
        if not uav_type in uavs_available:
            continue
        pose_spawn = uav.get('pose_spawn', [])
        pose_spawn = [str(i) for i in pose_spawn]
        if len(pose_spawn) != 4:
            continue
        sensors = uav.get('sensors', '')

        cmd_line = ['bash', spawn_script_path, namespace, uav_type, fcu_type]
        for i in pose_spawn:
            cmd_line.append(i)

        cmd_line.append(sensors)

        spawn_script_cmd = ExecuteProcess(
            cmd=cmd_line,
            name="spawn_drone_" + namespace,
            output='screen'
        )

        process_actions.append(spawn_script_cmd)

    # #}

    # #{ start uxrce protocol
    if fcu_type == "px4":
        uxrce_script_cmd = ExecuteProcess(
            cmd=["MicroXRCEAgent", "udp4", "-p", "8888"],
            name="uxrce_protocol",
            output='screen'
        )
        process_actions.append(uxrce_script_cmd)
    # #}

    for action in process_actions:
        ld.add_action(action)


def generate_launch_description():
    ld = launch.LaunchDescription()

    # #{ spawn drone config

    ld.add_action(DeclareLaunchArgument(
        'spawn_drones_file',
        default_value='',
        description='Path to config file for spawn drones.'
    ))

    # #}

    # #{ opaque function

    ld.add_action(
        OpaqueFunction(function=launch_setup, args=[ld])
    )

    # #}

    return ld
