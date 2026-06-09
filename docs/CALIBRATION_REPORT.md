# Camera Calibration & Error Analysis Report

## 1. Intrinsic Calibration Metrics
The camera's internal geometry and lens curvature were mathematically modeled using a 13x9 OpenCV checkerboard calibration process. The following optical constants were extracted to flatten the workspace prior to dimensional measurement:

**Camera Matrix ($K$)**
Maps the focal length and the true optical center of the camera sensor:
$$
K = \begin{bmatrix} 6286.27 & 0.00 & 1049.03 \\ 0.00 & 5957.50 & 2697.57 \\ 0.00 & 0.00 & 1.00 \end{bmatrix}
$$

**Distortion Coefficients ($D$)**
This 5-parameter array maps the radial and tangential lens warping (barrel and pincushion distortion) to allow for mathematical flattening:
$$
D = \begin{bmatrix} -0.2747 & 2.5845 & 0.0145 & 0.0163 & -3.9400 \end{bmatrix}
$$

**Global Scale Factor**
* **Average Scale:** 10.157 Pixels-Per-Millimeter (PPM)
* *Note: While the global average is logged here, the inference pipeline dynamically recalculates this PPM on a frame-by-frame basis using the SadaPay reference anchor to maximize accuracy.*

---

## 2. Checkerboard Detection & RMS Error
* **Total Calibration Frames Scanned:** 25
* **Successful Grid Detections:** 10
* **RMS Reprojection Error:** 2.4709 pixels

**Calibration Limitations:** The pipeline successfully extracted the required parameters from 10 frames, but 15 frames failed grid detection. An RMS reprojection error of 2.47 pixels indicates moderate residual error in the 3D-to-2D mapping. This is primarily attributed to physical limitations during the calibration capture phase, such as the checkerboard paper not being perfectly rigid (bending or flexing), minor focus blurring at extreme angles, or uneven lighting washing out the inner corners of the grid. 

---

## 3. Geometric & Environmental Error Analysis
To understand the variance in the final measurement outputs, it is critical to address the physical and environmental constraints of extracting metrology data from standard 2D photographs.

### A. The "Front Face" & Parallax Constraint
This system is designed to measure the 2D dimensions of the target's **front face** using a dynamic reference scale (the SadaPay card). However, because the TeaBox is a 3D object, its front face sits physically higher (closer to the camera lens) than the reference card lying flat on the table. 
* **The Result:** This Z-axis depth disparity creates a perspective magnification effect. The camera sensor perceives the front face of the box as artificially larger relative to the pixel density of the card. This parallax shift is the primary driver of dimensional overestimation in the metrology logs.

### B. Image Distortion & Perspective Skew
Standard smartphone lenses inherently warp spatial dimensions near the edges of a frame. A physical millimeter at the dead-center of the lens occupies a different number of pixels than a millimeter near the border. 
* **The Result:** While the pipeline actively flattens this mathematically using the `cv2.undistort` function, minor residual distortion (as indicated by the 2.47 RMS error) remains. Furthermore, if the camera is not held perfectly perpendicular to the object, perspective foreshortening occurs. This causes the far edges of the box to converge, skewing the linear pixel measurements.

### C. Lighting and Edge Degradation
Deep learning segmentation relies on sharp gradient contrasts to draw accurate polygon boundaries. 
* **The Result:** Harsh directional lighting creates cast shadows that the Mask R-CNN model may misinterpret as part of the physical box, incorrectly extending the polygon mask and inflating the width and height calculations. Conversely, specular highlights (glare) on the target's edges can wash out the boundaries entirely, reducing the AI's confidence score and leading to localization failures.
