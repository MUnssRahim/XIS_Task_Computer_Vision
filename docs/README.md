# XIS Task: Vision Metrology & Instance Segmentation

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?logo=PyTorch&logoColor=white)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?logo=opencv&logoColor=white)
![Deep Learning](https://img.shields.io/badge/segmentation-Mask_R--CNN-FF6F00.svg)

## 📌 Project Overview
This repository implements an end-to-end computer vision pipeline for instance segmentation and metrology of a target object (the **TeaBox**). By combining camera intrinsic calibration, a Mask R-CNN deep learning model, and dynamic scale extraction, the system computes the real-world dimensions of objects directly from 2D photographs.

### 🔗 Datasets , Outputs & Model Weights
Due to file size constraints, the curated image datasets, checkboard images , Final Output **Masked Images**, and trained model weights (`.pth` files) are hosted externally. 
**👉 [Access the Dataset & Models on Google Drive](https://drive.google.com/drive/folders/13S8qHCFh5ukO5oA7mtoIIR17ovi-gmZA?usp=drive_link)**

### How to Test ?
Due to the model not being deployed online , you shall open Final_Inference.py , update the local path of the picture & weights downloaded from the link above . 
The Output will be received when run with correct file paths.
---

## 🏗️ Repository Structure & Documentation
To maintain a clean working directory, all detailed technical reports, limitations, and error analyses have been centralized in the `docs/` folder.

```text
├── docs/                              # 📚 Centralized Documentation
│   ├── CALIBRATION_REPORT.md          # Intrinsic K & D matrices, checkerboard RMS error & hardware limitations
│   ├── DATASET_CARD.md                # Dataset selection, SadaPay anchor strategy, and polygon annotations
│   ├── MEASUREMENT_REPORT.md          # Metrology error analysis, Z-axis parallax evaluation, and final metrics
│   ├── SETUP.md                       # Environment setup and end-to-end execution instructions
│   └── TRAINING_REPORT.md             # Mask R-CNN config, hyperparameters, and model convergence limits
├── Training/                          # Model training scripts, notebooks, and weight outputs
├── calibration/                       # Camera calibration notebook and OpenCV extraction scripts 
├── inference/                         # Inference pipeline and Mask R-CNN segmentation application
├── measurement/                       # Dimension calculation and dynamic PPM mathematical scripts
├── README.md                          # You are here
└── requirements.txt                   # Pipeline dependencies
