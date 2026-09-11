# Autonomous Golf Trolley Navigation System

This repository contains the source files used for the Final Year Project titled:

Development and Evaluation of an Autonomous Navigation System for Golf Trolleys in Simulated Golf-Course Environments

## Project Overview

This project develops and evaluates a simulation-based autonomous navigation system for a golf trolley using ROS 2, Gazebo Harmonic and Nav2. The system includes a custom URDF golf trolley model, simulated golf-course environment, Nav2 map-based navigation, DWB, MPPI and RPP controller evaluation, waypoint navigation, dynamic obstacle avoidance and YOLOv8 terrain traversability estimation.

## Repository Contents

- robot_description: URDF/Xacro model of the golf trolley
- gazebo_world: Gazebo golf-course simulation world
- nav2_config: Nav2 parameter files for DWB, MPPI and RPP
- launch: ROS 2 and Gazebo launch files
- waypoint_navigation: Python waypoint navigation script
- terrain_yolo: YOLOv8 terrain traversability model/testing files
- analysis_scripts: Python scripts used for navigation performance analysis

## Software Used

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic
- Nav2
- Python
- YOLOv8
