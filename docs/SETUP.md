# Environment Setup & Execution Guide

This document outlines the complete, end-to-end procedure required to replicate our metrology environment, train the Mask R-CNN model on the cloud, and execute the final inference pipeline to extract real-world millimeter measurements.

## 1. Hardware Architecture & Prerequisites
Instance segmentation, particularly the **Mask R-CNN (ResNet-50-FPN)** architecture used in this project, is highly computationally intensive. Attempting to train this model on a standard CPU is not viable. 

**Compute Recommendations:**
* **Training (Cloud):** Kaggle Notebook with **GPU T4 x2** or **P100** enabled.
* **Inference (Local/Cloud):** A CUDA-enabled local NVIDIA GPU (RTX 3060+ recommended) or Kaggle/Google Colab. CPU inference is possible for final testing, but expect latency (~3-5 seconds per frame).

**Software Stack:**
* Python 3.8+
* `torch` and `torchvision` (compiled with CUDA)
* `opencv-python-headless` (for image un-distortion and contour mapping)
* `numpy` and `matplotlib`

---

## 2. Local Project Initialization
If you are evaluating the final inference pipeline or running the calibration locally, set up the repository:

```bash
# 1. Clone the repository
git clone [https://github.com/MUnssRahim/XIS_Task_Computer_Vision.git](https://github.com/MUnssRahim/XIS_Task_Computer_Vision.git)
cd XIS_Task_Computer_Vision

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
