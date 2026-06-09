# XIS Task Computer Vision

## Project Overview

This repository implements an end-to-end computer vision pipeline for instance segmentation and metrology of a target object called the **TeaBox**. It combines camera calibration, a Mask R-CNN segmentation model, and dynamic scale extraction to compute real-world object dimensions from images.

Key project goals:
- Calibrate smartphone camera lens distortion using checkerboard images.
- Build a small but highly curated dataset of polygon-annotated TeaBox images.
- Train a Mask R-CNN model for instance segmentation of the TeaBox.
- Measure the TeaBox's real-world length and width using a SadaPay card as a reference anchor.
- Evaluate measurement accuracy across validation and unseen test images.

## Repository Structure

- `dataset/` - Dataset documentation and annotated train/valid/test image folders.
- `calibration/` - Camera calibration notebook and calibration report.
- `Training/` - Training notebook and model training report.
- `inference/` - Inference notebook for segmentation and metrology evaluation.
- `measurement/` - Measurement and metrology results report.
- `requirements.txt` - Python dependencies required by the notebooks and pipeline.

## What the Project Does

1. Performs camera intrinsic calibration using a 13x9 checkerboard.
2. Uses a dynamic spatial anchor (SadaPay card) to compute frame-specific pixels-per-millimeter.
3. Trains a Mask R-CNN model to segment the TeaBox in images.
4. Extracts box dimensions from the predicted polygon mask.
5. Computes measurement accuracy versus known ground truth dimensions.

## Data and Calibration

- Target object: **TeaBox** with real-world dimensions of approximately **113.0 mm x 62.0 mm**.
- Calibration anchor:
  - Static checkerboard for camera intrinsics.
  - Dynamic SadaPay card for frame-scale estimation.
- Dataset split:
  - Training: 64 images
  - Validation: 15 images
  - Testing: 8 images

## Training Summary

- Architecture: `Mask R-CNN` with `ResNet-50-FPN` backbone.
- Training epochs: `30`
- Batch size: `2`
- Learning rate: `0.001`
- Augmentations: brightness, contrast, saturation, grayscale conversion.
- Final results:
  - Training loss reduced from `1.3235` to `0.4781`
  - Validation mAP@0.50: `0.1322`
  - Validation mAP@0.50:0.95: `0.0932`
  - Validation recall: `0.2267`

## Inference and Measurement

- The inference pipeline undistorts incoming images using the calibrated camera matrix and distortion coefficients.
- It detects the SadaPay card, computes a dynamic PPM scale, and then segments the TeaBox.
- It predicts TeaBox dimensions and overlays measurements on output images.
- Best achieved measurement error is below **15%** for some images, while the system is most accurate when the camera is perpendicular to the target.

## Important Notes

- The pipeline assumes the TeaBox front face is approximately coplanar with the reference card.
- Measurement accuracy is limited by perspective foreshortening, 3D depth differences, and residual distortion.
- The notebooks use Kaggle-style absolute paths for sample dataset locations; adjust paths for local execution.

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Open the notebooks in `calibration/`, `Training/`, and `inference/` to execute the pipeline step by step.
3. Update dataset paths inside notebooks if running outside the current Kaggle environment.

## Reports and Documentation

- `dataset/DataSet.md` - dataset selection, calibration anchors, and labelling strategy.
- `calibration/Calibration.md` - camera calibration results and error analysis.
- `Training/Training.md` - training configuration, results, and analysis.
- `measurement/Metrics.md` - performance evaluation and metrology error analysis.

## Dependencies

- Python 3.x
- `torch`
- `torchvision`
- `opencv-python`
- `pycocotools`
- `torchmetrics`
- `matplotlib`
- `numpy`

For full details, refer to `requirements.txt`.

## Contact

Use this repository as a reference implementation for vision-based dimensional metrology and object segmentation research.