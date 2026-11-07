#!/usr/bin/env bash
# Copies the Crazyflie files into the laser_uav_system packages.
#
# The files go to ~/git/laser_uav_system/ros_packages/<package> (the link
# targets), never to the workspace, so the symbolic links stay intact.
#
# Usage: ./install_crazyflie.sh
# Other location of the repository: LASER_UAV_SYSTEM=/path ./install_crazyflie.sh

set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGES_DIR="${LASER_UAV_SYSTEM:-$HOME/git/laser_uav_system}/ros_packages"

PACKAGES=(
  laser_gazebo_resources
  laser_uav_controllers
  laser_uav_managers
  laser_uav_simulation
)

if [ ! -d "$PACKAGES_DIR" ]; then
  echo "[ERROR] laser_uav_system is not installed ($PACKAGES_DIR does not exist)." >&2
  exit 1
fi

for pkg in "${PACKAGES[@]}"; do
  cp -r "$SRC_DIR/$pkg/." "$PACKAGES_DIR/$pkg/"
  echo "[ OK ] $pkg"
done

# Planner limits: in the new LUS they live in the pmm_planner package, inside
# laser_uav_planners (ros_packages/pmm_planner/params).
cp -r "$SRC_DIR/laser_uav_planners/ros_packages/pmm_planner/." \
  "$PACKAGES_DIR/laser_uav_planners/ros_packages/pmm_planner/"
echo "[ OK ] laser_uav_planners/ros_packages/pmm_planner"

echo "Done. If the workspace was not built with --symlink-install, run:"
echo "  cd ~/laser_uav_system_ws && colcon build --symlink-install"