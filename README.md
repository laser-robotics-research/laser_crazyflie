# Crazyflie – where to put each file

This model was made for [laser_uav_system](https://github.com/LASER-Robotics/laser_uav_system).

Each folder here is named after a package and already has the same internal paths as that package. So the idea is simple: **copy each folder over the package with the same name.**

**Packages live in:** `~/git/laser_uav_system/ros_packages/`
(the workspace `~/laser_uav_system_ws/src/` points here)

## Quick start

**1. Copy**:

Place each file in its respective location

**2. Build** (only if you did not build with `--symlink-install` before):

```bash
cd ~/laser_uav_system_ws && colcon build --symlink-install
```

**3. Choose the drone** in `configs/spawn.yaml` of your tmux session:

```yaml
type: "crazyflie"
fcu: "px4"
```

**4. Choose the map:** start the simulation with the world `crazyflie_map`. (Instructions bellow)

## What is in each folder

| Folder | What it adds |
|---|---|
| `laser_uav_simulation` | The drone model (SDF, meshes) and the PX4 airframe |
| `laser_uav_managers` | Drone parameters (mass, inertia, motors) |
| `laser_uav_controllers` | Controller weights (NMPC) |
| `laser_uav_planners` | Planner limits (max acceleration and velocity) |
| `laser_gazebo_resources` | The map: ground (`base_crazyrun`), obstacles (`obstacles_crazyrun`) and the world `crazyflie_map` |

## Details

### File by file

Destinations are relative to `ros_packages/`.

| File (in this folder) | Destination |
|---|---|
| `crazyflie.sdf.jinja` | `laser_uav_simulation/models/laser_uavs_description/sdf/` |
| `component_snippets.sdf.jinja` (adds the AI-deck macro) | `laser_uav_simulation/models/laser_uavs_description/sdf/` |
| `crazyflie.dae`, `crazyflie_prop.dae` | `laser_uav_simulation/models/laser_uavs_description/meshes/crazyflie/` |
| `ai_deck_1_1.stl` | `laser_uav_simulation/models/laser_uavs_description/meshes/sensors/` |
| `22002_crazyflie` (PX4 airframe) | `laser_uav_simulation/ROMFS/etc/init.d-posix/airframes/` |
| `crazyflie.yaml` (mass, inertia, G1, a/b curve) | `laser_uav_managers/params/laser_uavs/` |
| `crazyflie.yaml` (NMPC weights) | `laser_uav_controllers/params/nmpc_controller/` |
| `crazyflie.yaml` (max acceleration/velocity) | `laser_uav_planners/params/agile_planner/` |
| `base_crazyrun/`, `obstacles_crazyrun/` (map models) | `laser_gazebo_resources/models/` |
| `crazyflie_map.world` | `laser_gazebo_resources/worlds/` |

### About the map

1. Choose the map:** in `/laser_uav_simulation/launch/gazebo.launch.py`, inside `generate_launch_description()`, change the `default_value` of `<nome_da_variável>` to `'crazyflie_map'`:

```python
def generate_launch_description():
    ...
    DeclareLaunchArgument(
        'world',
        default_value='crazyflie_map',
        ...
    )
```

### Camera Module

To start the drone with the AI-deck module and access its camera, open `/laser_uav_simulation/tmux/one_drone_px4/configs/spawn.yaml` and add `--enable_ai_deck` to the `sensors` line:

```yaml
ros__parameters:
  - id: 1
    type: "crazyflie"
    fcu: "px4"
    pose_spawn: [0.0, 0.0, 1.0, 3.14]  # x y z yaw
    sensors: "--enable_ground_truth --enable_ai_deck"
```

### Things to watch

1. The three `crazyflie.yaml` files have the same name: each one goes to the package of its own folder, **do not mix them up**.
2. With `--symlink-install` there is no need to rebuild after copying (parameters and SDF are read from the source). Without it, rebuild, then close and reopen Gazebo.
3. Gazebo finds the drone meshes through `GAZEBO_MODEL_PATH` (it already includes `laser_uav_simulation/models`). PX4 reads the airframe directly from the ROMFS of the package.
4. Check that `crazyflie` is in the spawn list of `spawn_drones.launch.py` and in `control_manager.launch.py`.
   
```bash
uavs_available = ['x500', 'lr7pro', 'crazyflie']
```
5. If Gazebo cannot find `base_crazyrun` or `obstacles_crazyrun`, check that `laser_gazebo_resources/models` is in `GAZEBO_MODEL_PATH`. The folder name must match the name used in `model://`.
6. The Crazyflie has no Livox, RealSense or VIO (payload of ~15 g). Only the ground truth and the AI-deck camera are optional.



