# Crazyflie – where to put each file

This model was made for [laser_uav_system](https://github.com/LASER-Robotics/laser_uav_system).
Each subfolder in this folder is named after its target package and already mirrors the package's internal path. Just copy the contents of each subfolder over the package with the same name.

**Package root on the system:** `~/git/laser_uav_system/ros_packages/`
(the workspace `~/laser_uav_system_ws/src/` points here)

## Files and destinations

All destinations below are relative to `ros_packages/`.

| File (in this folder) | Destination |
|---|---|
| `crazyflie.sdf.jinja` | `laser_uav_simulation/models/laser_uavs_description/sdf/` |
| `component_snippets.sdf.jinja` (updated; includes the AI-deck macro) | `laser_uav_simulation/models/laser_uavs_description/sdf/` |
| 2 meshes: `crazyflie.dae`, `crazyflie_prop.dae` | `laser_uav_simulation/models/laser_uavs_description/meshes/crazyflie/` |
| `ai_deck_1_1.stl` | `laser_uav_simulation/models/laser_uavs_description/meshes/sensors/` |
| `22002_crazyflie` (PX4 airframe) | `laser_uav_simulation/ROMFS/etc/init.d-posix/airframes/` |
| `crazyflie.yaml` (mass, inertia, G1, a/b curve) | `laser_uav_managers/params/laser_uavs/` |
| `crazyflie.yaml` (NMPC weights) | `laser_uav_controllers/params/nmpc_controller/` |
| `crazyflie.yaml` (max acceleration/velocity) | `laser_uav_planners/params/agile_planner/` |

## Installation

Single command (run from inside this folder):

```bash
cp -r laser_uav_simulation laser_uav_managers laser_uav_controllers laser_uav_planners \
  ~/git/laser_uav_system/ros_packages/
```

## After copying

1. The three `crazyflie.yaml` files have the same name: each one goes to the package of its own subfolder, **do not mix them up**.
2. Do not replace `component_snippets.sdf.jinja`; it involves a future update and is not currently necessary.
3. If the system was built with `colcon build --symlink-install`, there is no need to rebuild (the parameters and the SDF are read from the source). For a fresh install:

   ```bash
   cd ~/laser_uav_system_ws && colcon build --symlink-install
   ```

4. Gazebo finds the meshes through `GAZEBO_MODEL_PATH` (which already includes `laser_uav_simulation/models`); PX4 reads the airframe directly from the package's ROMFS. Just check that `crazyflie` is in the spawn list of `spawn_drones.launch.py` and in `control_manager.launch.py`.
5. To use it, in `configs/spawn.yaml` of the tmux session, set:

   ```yaml
   type: "crazyflie"
   fcu: "px4"
   ```

   The Crazyflie model has no Livox, RealSense or VIO (payload of ~15 g); only the ground truth is optional.
