# Dataset Card: Instance Segmentation & Metrology

## 1. Object Selection & Justification
* **Target Object:** TeaBox
* **Approximate Real-World Dimensions:** 113.0 mm (Height) x 62.0 mm (Width)
* **Justification:** The TeaBox was selected as the primary measurement target due to its rigid, defined geometric boundaries (making it an ideal candidate for polygon masking) and its matte surface texture, which minimizes specular highlights and reflections that can degrade segmentation accuracy during dataset collection. 

## 2. Calibration Hardware & Reference Anchors
To ensure strict metrological accuracy, two separate calibration anchors were used:

### A. Static Lens Calibration (Checkerboard)
* **Grid Specifications:** 13x9 interior vertices (14x10 physical squares).
* **Square Dimensions:** 20.0 mm x 20.0 mm per square.
* **Calibration Set:** 25 raw, distorted checkerboard images were captured. These images were deliberately rotated and positioned at extreme angles, corners, and depths relative to the camera sensor. This maximized the OpenCV `calibrateCamera` algorithm's ability to accurately model and mathematically reverse the inherent radial and tangential lens distortion.

### B. Dynamic Spatial Anchor (SadaPay Card)
* **Standard Dimensions:** 85.60 mm x 53.98 mm
* **Engineering Justification:** The SadaPay card was deliberately chosen because its distinct neon-turquoise profile sits completely isolated in the HSV color space relative to standard background environments. This allows for highly reliable color-space clustering and morphological thresholding via OpenCV, making it incredibly easy to cleanly extract its edges and calculate a dynamic frame-by-frame metric scale.

## 3. Data Collection Strategy
* **Capture Hardware:** OnePlus 7T Smartphone Camera
* **Methodology:** 87 total target images were captured spanning various angles, lighting conditions, and camera-to-object distances to ensure the model generalizes well against spatial variance. 
* **Calibration Dependency:** Prior to any annotation or training, the entire raw target dataset was mathematically flattened using the intrinsic camera matrix (derived from the 25 checkerboard images) to remove lens distortion.

## 4. Labelling Methodology
* **Labelling Tool:** Roboflow
* **Annotation Type:** Polygon Instance Segmentation Masks.Drawn Manually using Roboflow's annotation 

## 5. Dataset Statistics & Splits
The target dataset was split into three strict subsets to ensure rigorous evaluation of the model's ability to segment unseen geometric angles without data leakage.

* **Total Target Images:** 87 
* **Training Set:** 64 images (~73.5%)
* **Validation Set:** 15 images (~17.3%)
* **Testing Set:** 8 images (~9.2%)
* **Class Distribution:** * Class 0: Background
  * Class 1: TeaBox (1 instance per image)
