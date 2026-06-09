

## 1. The Goal
We needed to build a highly accurate instance segmentation model to detect "TeaBox" objects in 2D images. Crucially, simple bounding boxes weren't enough for this project; we needed **pixel-perfect polygon masks** so that we can accurately extract physical dimensions, volume, and orientation downstream. 

## 2. The Challenge: The "Micro-Dataset" Problem
We were working with a very constrained dataset: **only 64 training images and 15 validation images**. 

When we initially trained a standard, heavy neural network (ResNet-50) on this, we hit a wall fast. The model had too much capacity, so it took the lazy route—it just memorized the exact pixel patterns of those 64 specific images. By Epoch 14, the training loss looked great, but it failed completely on new images, capping out at a dismal 22% Recall. It learned the photos, not the objects.

## 3. How We Solved It (Our Architecture & Data Strategy)
To force the model to actually learn what a tea box looks like, we completely overhauled the pipeline with three major changes:

### A. Freezing the Brain (Backbone Lock)
Instead of updating all 23+ million parameters in the **ResNet-50** backbone, we mathematically locked them (`requires_grad = False`). This prevented the model from overwriting the general shape and edge detection it learned from the massive COCO dataset. We only allowed it to train the final prediction heads. 

### B. Safe Polygon Augmentations
To artificially multiply our 64 images into thousands of unique scenarios, we integrated the `Albumentations` library. This was critical because standard augmentations often destroy polygon masks. We applied:
* **Horizontal Flips (50% chance):** To teach the model boxes can face both ways.
* **ShiftScaleRotate (50% chance):** We rotated the boxes up to 15 degrees and scaled them by 10%. Crucially, we used `border_mode=cv2.BORDER_CONSTANT` to pad the empty space with black pixels, ensuring the binary masks rotated perfectly without stretching or tearing.
* **Color Jitter (50% chance):** We tweaked brightness, contrast, and saturation by 20% to simulate different lighting environments.

### C. Stricter Penalties
We increased the optimizer's weight decay to `0.001` to strictly penalize the model if it tried to rely too heavily on specific background noise.

---

## 4. Training Progression
By locking the backbone and spinning the data with Albumentations, the training stabilized beautifully. Instead of plummeting instantly, the loss smoothly decayed, and the model learned to generalize.

```text
Epoch [01/15] | Train Loss: 0.9093
  -> Precision (mAP@0.50): 0.9913 | Recall (mAR@100): 0.7200 | F1-Score: 0.8342

Epoch [05/15] | Train Loss: 0.4102
  -> Precision (mAP@0.50): 1.0000 | Recall (mAR@100): 0.7467 | F1-Score: 0.8550

Epoch [10/15] | Train Loss: 0.2855
  -> Precision (mAP@0.50): 1.0000 | Recall (mAR@100): 0.7600 | F1-Score: 0.8636

Epoch [15/15] | Train Loss: 0.2075
  -> Precision (mAP@0.50): 1.0000 | Recall (mAR@100): 0.7733 | F1-Score: 0.8722
  -> Overall mAP (0.50:0.95): 0.7415 | Strict Mask Align (mAP@0.75): 0.9175
