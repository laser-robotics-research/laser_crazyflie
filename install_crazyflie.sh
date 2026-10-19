#!/usr/bin/env bash
# Copia os arquivos do Crazyflie para os pacotes do laser_uav_system.
#
# Os arquivos vao para ~/git/laser_uav_system/ros_packages/<pacote> (o destino
# dos links), nunca para o workspace, assim os links simbolicos continuam intactos.
#
# Uso: ./install_crazyflie.sh
# Outro local do repositorio: LASER_UAV_SYSTEM=/caminho ./install_crazyflie.sh

set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGES_DIR="${LASER_UAV_SYSTEM:-$HOME/git/laser_uav_system}/ros_packages"

PACKAGES=(
  laser_gazebo_resources
  laser_uav_controllers
  laser_uav_managers
  laser_uav_planners
  laser_uav_simulation
)

if [ ! -d "$PACKAGES_DIR" ]; then
  echo "[ERRO] laser_uav_system nao esta instalado ($PACKAGES_DIR nao existe)." >&2
  exit 1
fi

for pkg in "${PACKAGES[@]}"; do
  cp -r "$SRC_DIR/$pkg/." "$PACKAGES_DIR/$pkg/"
  echo "[ OK ] $pkg"
done

echo "Pronto. Se o workspace nao foi compilado com --symlink-install, rode:"
echo "  cd ~/laser_uav_system_ws && colcon build --symlink-install"
