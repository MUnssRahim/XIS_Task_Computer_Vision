# XIS Task: Vision Metrology & Instance Segmentation

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?logo=PyTorch&logoColor=white)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?logo=opencv&logoColor=white)
![Deep Learning](https://img.shields.io/badge/segmentation-Mask_R--CNN-FF6F00.svg)

## 📌 Project Overview
This repository implements an end-to-end computer vision pipeline for instance segmentation and metrology of a target object (the **TeaBox**). By combining camera intrinsic calibration, a Mask R-CNN deep learning model, and dynamic scale extraction, the system computes the real-world dimensions of objects directly from 2D photographs.

### 🔗 Dataset & Model Weights
Due to file size constraints, the curated image datasets, polygon annotations, and trained model weights (`.pth` files) are hosted externally. 
**👉 [Access the Dataset & Models on Google Drive](https://drive.google.com/drive/folders/13S8qHCFh5ukO5oA7mtoIIR17ovi-gmZA?usp=drive_link)**

---

## 🏗️ Repository Structure & Documentation
To maintain a clean working directory, all detailed technical reports and error analyses have been centralized in the `docs/` folder.

```text
├── docs/                              # 📚 Centralized Documentation
│   ├── DataSet.md                     # Dataset selection, anchor strategy, and annotations
│   ├── Calibration.md                 # Intrinsic K & D matrices, checkerboard RMS error
│   ├── Training.md                    # Mask R-CNN config, hyperparams, and loss graphs
│   └── Metrics.md                     # Metrology error analysis and performance evaluation
├── calibration/                       # Camera calibration notebooks
├── Training/                          # Model training notebooks
├── inference/                         # Inference and segmentation notebooks
├── measurement/                       # Measurement and metrology evaluation report
├── README.md                          # You are here
└── requirements.txt                   # Pipeline dependencies
