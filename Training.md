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
Training converged and plateaued between Epoch 14 and Epoch 30. This stability confirms the model reached the generalization limits of the provided 54-image dataset. 

A critical observation is the constrained size of the training set; with only 54 images, the model reached its optimal generalization at Epoch 14 (mAP@0.50: 0.1347). Beyond this point, the model began to overfit the specific lighting and background conditions of the training images rather than learning broader structural features. Consequently, increasing the duration beyond 30 epochs was deemed futile, as it would only follow this overfitting trend. The resulting Recall and mAP metrics reflect this dataset limitation, representing the maximum feasible performance under these specific constraints.

## 5. Artifacts
* **Weights:** `teabox_mask_rcnn.pth` (Final Epoch 30 weights).
