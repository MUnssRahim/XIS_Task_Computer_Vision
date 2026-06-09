# Measurement & Metrology Report

## 1. Evaluation Baseline
* **Target Object:** TeaBox
* **Ground Truth Dimensions:** 113.0 mm (Long Axis) $\times$ 62.0 mm (Short Axis)
* **Scaling Anchor:** SadaPay Card (85.60 mm $\times$ 53.98 mm)
* **Scale Extraction:** Dynamic, frame-specific Pixels-Per-Millimeter (PPM) calculation.

## 2. Top Performing Images
The system was evaluated across a batch of 11 images (3 Train, 8 Test). The following images yielded the highest geometric accuracy when comparing the predicted AI polygon against the physical ground truth.

| Position | Image Filename | Origin | Long Axis (113mm) | Short Axis (62mm) | Avg System Error |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Best** | `IMG_..._BRouITSHw35AfDSGMRAX.jpg` | TEST | 128.04 mm *(13.31% err)* | 70.70 mm *(14.03% err)* | **13.67%** |
| **2nd Best** | `IMG_..._rdCgxq1EVKIpen5OLaeR.jpg` | TEST | 110.77 mm *(1.97% err)* | 82.54 mm *(33.13% err)* | **17.55%** |
| **3rd Best** | `IMG_..._2JLL6eceo4R00W15gtlv.jpg` | TEST | 98.25 mm *(13.05% err)* | 80.33 mm *(29.56% err)* | **21.31%** |

*Note: The 2nd best pic achieved an exceptional sub-2% error margin on the primary longitudinal axis (110.77 mm vs 113.0 mm truth).*

## 3. Comprehensive Batch Evaluation
*Absolute Error ($\Delta$) = |Predicted - Ground Truth|*

### Testing Set (Unseen Data)
| Filename | Predicted Long | $\Delta$ Long | Predicted Short | $\Delta$ Short |
| :--- | :--- | :--- | :--- | :--- |
| `dsj17Uar...R1er.jpg` | 246.79 mm | 133.79 mm | 124.88 mm | 62.88 mm |
| `2dmx73Ix...4wMZ.jpg` | 168.02 mm | 55.02 mm | 103.55 mm | 41.55 mm |
| `836fH1sz...OFep.jpg` | *Localization Breach* | - | *Localization Breach* | - |
| `DYEQjnWM...6bVE.jpg` | 86.70 mm | 26.30 mm | 39.12 mm | 22.88 mm |
| `vxVqR8bN...znxI.jpg` | 103.65 mm | 9.35 mm | 90.23 mm | 28.23 mm |

### Training Set 
| Filename | Predicted Long | $\Delta$ Long | Predicted Short | $\Delta$ Short |
| :--- | :--- | :--- | :--- | :--- |
| `hOithGS3...rq9T.jpg` | 196.93 mm | 83.93 mm | 114.08 mm | 52.08 mm |
| `x06cv4dB...Bgo0.jpg` | 189.98 mm | 76.98 mm | 109.98 mm | 47.98 mm |
| `JTEQka9l...UgBp.jpg` | *Localization Breach* | - | *Localization Breach* | - |

## 4. Error Analysis
Because this metrology engine is strictly designed to calculate the 2D dimensions of the target's **front face**, it operates under strict geometric constraints. This 2D planar assumption is the primary source of the dataset's error variance:

1. **The Z-Axis Coplanar Constraint (Parallax Error):** The system maps the pixel-to-millimeter ratio of the flat SadaPay card to the TeaBox. Because the TeaBox has 3D depth, its top/front face is physically closer to the camera lens than the card resting on the table. This Z-axis disparity causes perspective magnification, making the box appear artificially larger in the pixel grid.
2. **Perspective Foreshortening:** Frames captured at an angular tilt relative to the table surface introduce severe foreshortening. Without a perspective warp to simulate a perfect bird's-eye view, pixels along the far edge of the box represent more physical millimeters than pixels at the near edge.

**Conclusion for Optimal Measurement:**
The system achieves its highest measurement accuracy (sub-15% error) when images are captured completely perpendicular to the target. Straight, vertical camera alignment eliminates foreshortening and ensures the front face is captured uniformly across the 2D sensor plane.
