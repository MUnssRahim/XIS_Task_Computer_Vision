
# Camera Calibration & Scale Extraction Report

## 1. System Setup & Methodology
Here is the rundown of how we set up the calibration pipeline to map the camera's lens and extract real-world measurements:
* **Calibration Target:** Standard OpenCV checkerboard. We used a **13x9** grid where each physical square measures exactly **20.0mm**.
* **Scale Reference:** Since we need dynamic scaling, we used a turquoise SadaPay Card as our metrology anchor. Its physical dimensions are **85.60mm x 53.98mm**.
* **Algorithm Pipeline:** We used OpenCV's `cv2.cornerSubPix` for iterative corner refinement on the grid, and basic HSV contour filtering to segment the SadaPay card.

## 2. Pipeline Execution & Detection Logs
When we ran the automated script over our dataset, here is what actually happened:

* **Checkerboard Detection:** We only successfully detected the grid in **10 out of 25** frames (**40%** success rate). The other **15** frames completely failed the OpenCV check.
* **Target Image Scanning:** We scanned **60** training images for the SadaPay card.
* **Reference Detection Rate:** We hit a **60/60** (**100%**) success rate using the HSV bounds of `[80, 70, 50]` to `[105, 255, 255]`. 

## 3. The Math: Intrinsic Calibration Parameters
Using the **10** successful calibration frames, the pipeline extracted the camera's intrinsic parameters. We use these to mathematically "flatten" the curved image plane via `cv2.undistort`.

**Camera Matrix (K)**
This maps the focal length and the true optical center of the camera sensor.
* Focal Lengths (fx, fy): **6286.27483** and **5957.50482**
* Optical Centers (cx, cy): **1049.02659** and **2697.57463**

$$
K = \begin{bmatrix} \textbf{6286.27483} & \textbf{0.00000000} & \textbf{1049.02659} \\ \textbf{0.00000000} & \textbf{5957.50482} & \textbf{2697.57463} \\ \textbf{0.00000000} & \textbf{0.00000000} & \textbf{1.00000000} \end{bmatrix}
$$

**Distortion Coefficients (D)**
This 5-parameter array handles the radial and tangential lens warping (basically fixing the barrel and pincushion distortion).

$$
D = \begin{bmatrix} \textbf{-0.27477453} & \textbf{2.58453069} & \textbf{0.01454981} & \textbf{0.01631264} & \textbf{-3.94001836} \end{bmatrix}
$$

## 4. Scale Extraction (PPM Analysis)
To convert our AI's pixel masks into millimeters, we calculated the Pixels-Per-Millimeter (PPM).

* **Global Average PPM:** **10.157126**
* **The Reality (Dynamic Variance):** During the scan of the **60** images, the actual PPM fluctuated massively—dropping as low as **4.2056** and spiking up to **17.1028**. 
* **Conclusion:** This proves we absolutely cannot rely on a single static Global PPM. If the camera moves closer or further away, the pixel density changes. Our inference engine *must* recalculate the PPM dynamically for every single frame using the SadaPay card, otherwise, our measurements will be entirely wrong.

## 5. Error Analysis (What went wrong and why)
The calibration phase yielded an RMS Reprojection Error of **2.470915 pixels**. In computer vision, anything above 1.0 is generally considered high, so here is the breakdown of why our error is at **~2.47** and why the pipeline dropped so many frames.

### A. The "Page Issue" (Surface Deformation)
Honestly, the biggest source of error was just the physical checkerboard itself. We printed it on standard paper, and it wasn't mounted to a perfectly rigid surface (like glass or wood). 
* **The Effect:** The paper had slight folds, creases, and bends. Because the paper wasn't perfectly flat, the **20.0mm** squares warped in 3D space. OpenCV's sub-pixel algorithm expects mathematically straight lines, so when it tried to map these bent curves to a perfect plane, it threw our RMS error up to **2.470915**.

### B. The 60% Failure Rate & Small Dataset
Because of the paper folds and some extreme capture angles, the algorithm couldn't even recognize the checkerboard in **15** of the **25** images.
* **The Effect:** We had to calculate the camera matrix using only **10** valid frames. **10** frames is barely enough to map the center of the lens, let alone the outer edges. Because of this small sample size, there is still some residual distortion near the borders of our images.

### C. Geometric Realities: Parallax & Masking
Even with a perfect intrinsic calibration, measuring a 3D box from a 2D image has physical constraints:
* **Parallax Disparity:** The SadaPay card is lying flat on the table, but the front face of the TeaBox is physically sitting several inches higher (closer to the camera). Because it's closer to the lens, the TeaBox looks artificially larger than the card. This depth disparity causes dimensional overestimation.
* **Lighting vs. AI Segmentations:** Our Mask R-CNN needs sharp edges to draw its polygons. When we have harsh directional lighting, the TeaBox casts a shadow, and the AI often includes that shadow inside the polygon mask. Or, if there is a bright specular glare on the edge of the box, the AI loses the boundary entirely. Both issues artificially inflate or shrink our pixel counts before we even do the math.

  ## 6. Conclusion & Practical Takeaways
To sum it all up, the high error rates and dropped frames ultimately came down to hardware and environmental limitations during the image capture phase. 

Because we had **no tripod stand available**, all **25** calibration images and the **60** target dataset images were captured completely handheld. 
* **Handheld Instability:** Without a fixed, stable mount, we inadvertently introduced minor motion blur into the dataset. 
* **Distorted Angles:** Trying to manually capture "different angles" to map the lens curvature meant the camera was physically tilted at highly irregular pitch and yaw degrees. This resulted in severely foreshortened, distorted images of the grid that OpenCV simply couldn't read.

**Final Verdict:** The pipeline was a success mathematically—we successfully extracted the intrinsic matrix ($K$) and distortion coefficients ($D$), and we proved beyond a doubt that dynamic PPM scaling is necessary. However, the baseline RMS error of **2.47** is a direct reflection of our handheld, unmounted capture environment. For a true production-grade metrology system, a rigid camera mount (like a tripod) and a perfectly flat calibration board are absolute, non-negotiable necessities.

