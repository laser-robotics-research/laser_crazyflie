#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

import jinja2

parser = argparse.ArgumentParser(description='Generate UAV SDF models using Jinja2 templates.')
parser.add_argument('--namespace', type=str, required=True, help='Robot namespace')
parser.add_argument('--uav_model', type=str, required=True, help='UAV model name')
parser.add_argument('--instance', type=int, required=True, help='UAV instance number')
parser.add_argument(
    '--flight_controller',
    type=str,
    required=True,
    choices=['px4', 'ap'],
    help="Flight controller for SITL simulation (choices: 'px4' or 'ap')"
)
parser.add_argument('--enable_ground_truth', action='store_true')
parser.add_argument('--enable_load_pendulum', action='store_true')
parser.add_argument('--enable_d435_front', action='store_true')
parser.add_argument('--enable_d435i_front', action='store_true')
parser.add_argument('--enable_d435i_down', action='store_true')
parser.add_argument('--enable_d435_down', action='store_true')
parser.add_argument('--enable_vio', action='store_true')
parser.add_argument('--enable_garmin', action='store_true')
parser.add_argument('--enable_livox', action='store_true')
parser.add_argument('--enable_livox_45', action='store_true')
parser.add_argument('--enable_livox_down', action='store_true')
parser.add_argument('--enable_ai_deck', action='store_true') # Tentativa de adicionaro módulo da camera para o crazyflie pelo spawn
parser.add_argument('--x', type=float, default=0.0)
parser.add_argument('--y', type=float, default=0.0)
parser.add_argument('--z', type=float, default=0.0)
parser.add_argument('--roll', type=float, default=0.0)
parser.add_argument('--pitch', type=float, default=0.0)
parser.add_argument('--yaw', type=float, default=0.0)

args = parser.parse_args()

base_dir = os.path.dirname(os.path.abspath(__file__))

snippets_dir = os.path.realpath(os.path.join(base_dir, '../models/laser_uavs_description'))
drones_dir = os.path.realpath(os.path.join(snippets_dir, 'sdf'))

# Configure Jinja2 environment loader
env = jinja2.Environment(loader=jinja2.FileSystemLoader([snippets_dir, drones_dir]))

# Load main template
try:
    template = env.get_template(args.uav_model + '.sdf.jinja')
except jinja2.exceptions.TemplateNotFound:
    print(
        f"[ERROR] Template '{args.uav_model}.sdf.jinja' not found in {drones_dir}!", file=sys.stderr)
    sys.exit(1)

# Data dictionary to render the template
data = {
    'namespace': str(args.namespace),
    'model_name': str(args.uav_model),
    'instance': int(args.instance),
    'flight_controller': str(args.flight_controller),
    'enable_load_pendulum': args.enable_load_pendulum,
    'enable_ground_truth': args.enable_ground_truth,
    'enable_d435_front': args.enable_d435_front,
    'enable_d435i_front': args.enable_d435i_front,
    'enable_d435i_down': args.enable_d435i_down,
    'enable_d435_down': args.enable_d435_down,
    'enable_vio': args.enable_vio,
    'enable_livox': args.enable_livox,
    'enable_garmin': args.enable_garmin,
    'enable_livox_45': args.enable_livox_45,
    'enable_livox_down': args.enable_livox_down,
    'enable_ai_deck': args.enable_ai_deck,              # Continuação da tentativa
    'x_offset': -float(args.x),
    'y_offset': -float(args.y),
    'z_offset': -float(args.z),
    'roll_offset': -float(args.roll),
    'pitch_offset': -float(args.pitch),
    'yaw_offset': -float(args.yaw)
}

# Render template
output = template.render(data)

dir_path = '/tmp/laser_uavs_description/sdf'
file_name = f"{args.uav_model}_{args.instance}.sdf"
file_path = os.path.join(dir_path, file_name)

os.makedirs(dir_path, exist_ok=True)

# Save the generated SDF file
with open(file_path, 'w') as file:
    file.write(output)

print(f"[SUCCESS] SDF file successfully generated at: {file_path}")
