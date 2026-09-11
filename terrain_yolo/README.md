# YOLOv8 Terrain Traversability Estimation

This folder contains the YOLOv8 segmentation files used for the terrain traversability estimation module in the FYP project.

## Purpose

The YOLOv8 segmentation model was trained to classify golf-course terrain into three traversability classes:

- preferred_traversable
- low_preferred_traversable
- non_traversable

The terrain traversability module was evaluated separately from the Nav2 navigation system. The segmentation output was not directly integrated into the Nav2 costmap in the current implementation.

## Files

- model/best.pt: trained YOLOv8 segmentation model
- config/data.yaml: dataset configuration file used for YOLOv8 training
- results/results.png: training and validation result graph
- results/confusion_matrix.png: confusion matrix result

## Training Information

Model type: YOLOv8n-seg  
Epochs: 30  
Dataset size: 75 images  
Training images: 60  
Validation images: 15  

Validation result:
- Overall precision: 0.889
- Overall recall: 0.791
- Overall mAP50: 0.914
- Overall mAP50-95: 0.664
