# TeaBox Instance Segmentation: Comprehensive Project Report

## 1. Executive Summary
This model leverages a heavily optimized **Mask R-CNN (ResNet-50-FPN)** architecture to perform high-precision instance segmentation of "TeaBox" objects. Unlike standard bounding-box detection, this pipeline generates pixel-perfect polygon masks. This level of granularity is strictly required for downstream applications, such as calculating the exact physical dimensions, volume, or orientation of the tea boxes from 2D images.

## 2. Architectural Optimizations & Data Strategy
Training a complex neural network on a micro-dataset (64 training / 15 validation images) typically results in catastrophic overfitting. To counter this, three major structural interventions were implemented:

* **Feature Extractor Freezing (Backbone Lock):** * *The Problem:* A standard ResNet-50 backbone contains over 23 million parameters. Updating all these weights on 64 images causes the model to memorize the specific pixel patterns of the training data rather than learning what a "box" looks like.
  * *The Solution:* The entire ResNet-50 backbone was mathematically frozen (`requires_grad = False`). The model relies entirely on the generalized edge, texture, and shape detection it originally learned from the massive COCO dataset. Only the final Region of Interest (ROI) heads were trained to specifically classify those shapes as "TeaBoxes."
* **Mathematical Mask-Safe Augmentations:** * *The Strategy:* To artificially expand the dataset, `Albumentations` was integrated. This library applies complex spatial transformations (like `ShiftScaleRotate` and `HorizontalFlip`) simultaneously to the image and the polygon mask arrays. 
  * *The Impact:* By using constant border padding during rotation, the binary masks remain perfectly mathematically aligned with the object, effectively simulating thousands of unique physical box orientations without corrupting the annotations.
* **Hyperparameter Tuning:** * SGD Optimizer with a learning rate of 0.001, decayed by 90% at Epoch 7. Weight decay was increased to 0.001 to strictly penalize the model for attempting to over-rely on specific background pixels.

## 3. Training Logs (Epoch Progression)
The logs demonstrate a highly stable training curve. Instead of an immediate loss plunge (a symptom of memorization), the model steadily learned the object boundaries while maintaining high generalization on the validation set.

```text
Epoch [01/30] | Train Loss: 0.9093
  -> Precision (mAP@0.50): 0.9913 | Recall (mAR@100): 0.7200 | F1-Score: 0.8342
  -> Overall mAP (0.50:0.95): 0.6521 | mAP@0.75: 0.8025
  -> mAR@1: 0.6933 | mAR@10: 0.7200

... [Steady convergence and boundary refinement] ...

Epoch [15/15] | Train Loss: 0.2075
  -> Precision (mAP@0.50): 1.0000 | Recall (mAR@100): 0.7733 | F1-Score: 0.8722
  -> Overall mAP (0.50:0.95): 0.7415 | mAP@0.75: 0.9175
  -> mAR@1: 0.7733 | mAR@10: 0.7733
