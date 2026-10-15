# Crazyflie – onde colocar cada arquivo

Este modelo foi feito para o [laser_uav_system](https://github.com/LASER-Robotics/laser_uav_system).
Cada subpasta desta pasta tem o nome do pacote de destino e já reproduz o caminho interno dele. Basta copiar o conteúdo de cada subpasta por cima do pacote de mesmo nome.

**Raiz dos pacotes no sistema:** `~/git/laser_uav_system/ros_packages/`
(o workspace `~/laser_uav_system_ws/src/` aponta para cá)

> [!NOTE]
> A pasta `laser_gazebo_resources` **(ignorar)** não deve ser copiada: ela está no zip só como referência.

## Arquivos e destinos

Todos os destinos abaixo são relativos a `ros_packages/`.

| Arquivo (nesta pasta) | Destino |
|---|---|
| `crazyflie.sdf.jinja` | `laser_uav_simulation/models/laser_uavs_description/sdf/` |
| `component_snippets.sdf.jinja` (atualizado; inclui o macro da AI-deck) | `laser_uav_simulation/models/laser_uavs_description/sdf/` |
| 2 malhas: `crazyflie.dae`, `crazyflie_prop.dae` | `laser_uav_simulation/models/laser_uavs_description/meshes/crazyflie/` |
| `ai_deck_1_1.stl` | `laser_uav_simulation/models/laser_uavs_description/meshes/sensors/` |
| `22002_crazyflie` (airframe PX4) | `laser_uav_simulation/ROMFS/etc/init.d-posix/airframes/` |
| `crazyflie.yaml` (massa, inércia, G1, curva a/b) | `laser_uav_managers/params/laser_uavs/` |
| `crazyflie.yaml` (pesos do NMPC) | `laser_uav_controllers/params/nmpc_controller/` |
| `crazyflie.yaml` (aceleração/velocidade máx.) | `laser_uav_planners/params/agile_planner/` |

## Instalação

Comando único (rodar de dentro desta pasta):

```bash
cp -r laser_uav_simulation laser_uav_managers laser_uav_controllers laser_uav_planners \
  ~/git/laser_uav_system/ros_packages/
```

## Depois de copiar

1. Os três `crazyflie.yaml` têm o mesmo nome: cada um vai para o pacote da sua subpasta, **não misturar**.
2. Não trocar `component_snippets.sdf.jinja`, ele envolve uma atualização futura, atualmente não se faz necessário.
3. Se o sistema foi compilado com `colcon build --symlink-install`, não precisa recompilar (os parâmetros e o SDF são lidos da fonte). Em instalação nova:

   ```bash
   cd ~/laser_uav_system_ws && colcon build --symlink-install
   ```

4. O Gazebo acha as malhas pelo `GAZEBO_MODEL_PATH` (já inclui `laser_uav_simulation/models`); o PX4 lê o airframe direto do ROMFS do pacote. Confira apenas se `crazyflie` está na lista de spawn de `spawn_drones.launch.py` e no `control_manager.launch.py`.
5. Para usar, em `configs/spawn.yaml` da sessão tmux, defina:

   ```yaml
   type: "crazyflie"
   fcu: "px4"
   ```

   O modelo do Crazyflie não tem Livox, RealSense nem VIO (carga útil de ~15 g); só o ground truth é opcional.
