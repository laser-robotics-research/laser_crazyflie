# Crazyflie 2.1+ for laser_uav_system

Files to add the **Crazyflie 2.1+** (with an optional **AI-deck camera**) and the **`crazyflie_map`** world to [laser_uav_system](https://github.com/LASER-Robotics/laser_uav_system), running on PX4 SITL + Gazebo Classic + ROS2.

Each folder in this repository is named after a package of `laser_uav_system` and already has the same internal paths as that package. So the idea is simple: **copy each folder over the package with the same name** (the install script does this for you).

## Requirements

- `laser_uav_system` already installed and working with another drone (x500 or lr7pro).
- Packages located in `~/git/laser_uav_system/ros_packages/` (the workspace `~/laser_uav_system_ws/src/` points there).
- LUS version **2026-10-29 or newer** (with the planning and control split, i.e. with the `planning_manager`). These files do not work with older LUS versions. They were checked against the `stable` branches of [LASER-Robotics](https://github.com/LASER-Robotics):

| Package | Version used |
|---|---|
| [laser_uav_simulation](https://github.com/LASER-Robotics/laser_uav_simulation) | [`d9f1be8`](https://github.com/LASER-Robotics/laser_uav_simulation/tree/d9f1be869a32104d0cfd855b468d2c10c0116771) (2026-10-29) |
| [laser_uav_managers](https://github.com/LASER-Robotics/laser_uav_managers) | [`277a3c9`](https://github.com/LASER-Robotics/laser_uav_managers/tree/277a3c9f7d161d8335afa72df75a6cd869491680) (2026-11-03) |
| [laser_uav_planners](https://github.com/LASER-Robotics/laser_uav_planners) | [`8aa841c`](https://github.com/LASER-Robotics/laser_uav_planners/tree/8aa841c1676601d73cfaa1873685dd6947a4204c) (2026-10-29) |
| [pmm_uav_planner](https://github.com/LASER-Robotics/pmm_uav_planner) | [`98ecebd`](https://github.com/LASER-Robotics/pmm_uav_planner/tree/98ecebd784d874ddbf3e28ffff606e0ba2d39f1d) (2026-10-29) |
| [laser_uav_controllers](https://github.com/LASER-Robotics/laser_uav_controllers) | [`fca756a`](https://github.com/LASER-Robotics/laser_uav_controllers/tree/fca756ad4c2113077ca4000b3103af787b92eeeb) (2026-10-29) |

## Quick start

### 1. Install the files

From the root of this repository:

```bash
chmod +x install_crazyflie.sh
./install_crazyflie.sh
```

If `laser_uav_system` is somewhere else:

```bash
LASER_UAV_SYSTEM=/path/to/laser_uav_system ./install_crazyflie.sh
```

The script copies the files into `ros_packages/<package>` (the real folders, so the workspace symlinks stay intact).

<details>
<summary>Prefer to copy by hand?</summary>

Copy each folder over the package with the same name, keeping the internal paths:

```bash
cp -r laser_gazebo_resources/.   ~/git/laser_uav_system/ros_packages/laser_gazebo_resources/
cp -r laser_uav_controllers/.    ~/git/laser_uav_system/ros_packages/laser_uav_controllers/
cp -r laser_uav_managers/.       ~/git/laser_uav_system/ros_packages/laser_uav_managers/
cp -r laser_uav_planners/ros_packages/pmm_planner/. ~/git/laser_uav_system/ros_packages/laser_uav_planners/ros_packages/pmm_planner/
cp -r laser_uav_simulation/.     ~/git/laser_uav_system/ros_packages/laser_uav_simulation/
```
</details>

### 2. Build

Always rebuild after installing. New files (yaml, launch files, meshes) are only linked into the workspace by a build:

```bash
cd ~/laser_uav_system_ws && colcon build --symlink-install
source install/setup.bash
```

### 3. Choose the drone

In `laser_uav_simulation/tmux/one_drone_px4/configs/spawn.yaml` (installed by the script, already set to the Crazyflie):

```yaml
ros__parameters:
  - id: 1
    type: "crazyflie"
    fcu: "px4"
    pose_spawn: [0.0, 0.0, 0.2, 0.0]  # x y z yaw
    sensors: "--enable_ground_truth"
```

### 4. Start the simulation

Start your usual tmux session (`laser_uav_simulation/tmux/one_drone_px4`). The installed `session.yml` already uses the Crazyflie and the `crazyflie_map` world, and starts the planning manager. Close and reopen Gazebo if it was already running.

## Camera module (AI-deck)

To spawn the drone with the AI-deck (Himax HM01B0 camera), add `--enable_ai_deck` to the `sensors` line of `spawn.yaml`:

```yaml
sensors: "--enable_ground_truth --enable_ai_deck"
```

The camera is monochrome (mono8), 324 x 244, 30 Hz. To check that it is running:

```bash
ros2 topic list | grep ai_deck
```

It should show topics like `/uav1/camera/ai_deck/image_raw`. To see the image: `ros2 run rqt_image_view rqt_image_view`.

## What is in each folder

| Folder | What it adds |
|---|---|
| `laser_uav_simulation` | Drone model (SDF template, meshes), PX4 airframe, spawn launch file, `jinja_gen.py` (with the `--enable_ai_deck` flag), tmux session and `spawn.yaml` |
| `laser_uav_managers` | Drone parameters (mass, inertia, motors) and `control_manager.launch.py` |
| `laser_uav_controllers` | Controller weights (NMPC) |
| `laser_uav_planners` | Planner limits (max acceleration and velocity) for the PMM planner |
| `laser_gazebo_resources` | The map: ground (`base_crazyrun`), obstacles (`obstacles_crazyrun`) and the world `crazyflie_map` |

### File by file

Destinations are relative to `ros_packages/`.

| File | Destination | What it does |
|---|---|---|
| `crazyflie.sdf.jinja` | `laser_uav_simulation/models/laser_uavs_description/sdf/` | Drone model template (body, propellers, sensors, AI-deck macro) |
| `jinja_gen.py` | `laser_uav_simulation/scripts/` | Turns the template into an SDF using the sensor flags |
| `crazyflie.dae`, `crazyflie_prop.dae` | `laser_uav_simulation/models/laser_uavs_description/meshes/crazyflie/` | Body and propeller 3D meshes |
| `ai_deck_1_1.stl` | `laser_uav_simulation/models/laser_uavs_description/meshes/sensors/` | AI-deck 3D mesh |
| `22002_crazyflie` | `laser_uav_simulation/ROMFS/etc/init.d-posix/airframes/` | PX4 airframe (rotor geometry, rate gains) |
| `spawn_drones.launch.py` | `laser_uav_simulation/launch/` | Spawns the drones listed in `spawn.yaml` (already accepts `crazyflie`) |
| `spawn.yaml` | `laser_uav_simulation/tmux/one_drone_px4/configs/` | Drone list for the simulation (`crazyflie`) |
| `session.yml` | `laser_uav_simulation/tmux/one_drone_px4/` | Tmux session with `UAV_TYPE=crazyflie`, the `crazyflie_map` world and the planning manager |
| `crazyflie.yaml` (mass, inertia, G1, motor curve) | `laser_uav_managers/params/laser_uavs/` | Drone parameters |
| `control_manager.launch.py` | `laser_uav_managers/launch/` | Starts the control manager (already accepts `crazyflie`) |
| `crazyflie.yaml` (NMPC weights) | `laser_uav_controllers/params/nmpc_controller/` | Controller tuning |
| `crazyflie.yaml` (max acceleration/velocity) | `laser_uav_planners/ros_packages/pmm_planner/params/` | Planner limits |
| `base_crazyrun/`, `obstacles_crazyrun/` | `laser_gazebo_resources/models/` | Map models |
| `crazyflie_map.world` | `laser_gazebo_resources/worlds/` | Map world |

## Things to know

1. The `crazyflie` type must be in the drone list of `spawn_drones.launch.py` (`uavs_available`) and `control_manager.launch.py` (`defaults_uavs`). Both files here already include it.
2. PX4 reads the airframe directly from the ROMFS of `laser_uav_simulation`.
3. The Crazyflie has no Livox, RealSense or VIO (payload of about 15 g). Only the ground truth and the AI-deck camera are optional.