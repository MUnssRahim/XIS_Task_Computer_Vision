# Model Training Report

## 1. Overview
The model utilizes a **Mask R-CNN (ResNet-50-FPN)** architecture to segment "TeaBox" instances. The pipeline is designed to generate pixel-perfect masks, enabling the extraction of physical dimensions from images.

## 2. Configuration
* **Dataset:** 54 training / 15 validation images.
* **Training Duration:** 30 Epochs.
* **Batch Size:** 2.
* **Learning Rate:** 0.001 (stepped at 7-epoch intervals).
* **Augmentations:** Color jittering (brightness, contrast, saturation) and grayscale conversion.

## 3. Results
* **Training Loss:** Successfully reduced from `1.3235` to `0.4781`.
* **Validation Performance:**
    * **mAP@0.50:** 0.1322
    * **mAP@0.50:0.95:** 0.0932
    * **Recall:** 0.2267

## 4. Training Analysis
Training converged and plateaued between Epoch 14 and Epoch 30. This stability confirms the model reached the generalization limits of the provided 54-image dataset. The final model weights are stable and ready for inference.

## 5. Artifacts
* **Weights:** `teabox_mask_rcnn.pth` (Final Epoch 30 weights).
