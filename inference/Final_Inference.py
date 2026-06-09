import torch
import torchvision
import cv2
import numpy as np
import os
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor
from IPython.display import FileLink, display

PIXELS_PER_MM = 10.157126168224298
CARD_WIDTH_MM = 85.60
CARD_HEIGHT_MM = 53.98
TRUE_DIM_LONG = 113.0
TRUE_DIM_SHORT = 62.0

CAMERA_MATRIX = np.array([
    [6.28627483e+03, 0.00000000e+00, 1.04902659e+03],
    [0.00000000e+00, 5.95750482e+03, 2.69757463e+03],
    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]
], dtype=np.float32)

DISTORTION_COEFFICIENTS = np.array([
    [-0.27477453,  2.58453069,  0.01454981,  0.01631264, -3.94001836]
], dtype=np.float32)

DEFAULT_OUTPUT_DIR = "/kaggle/working/single_annotated_outputs"

def load_segmentation_model(weights_path, device):
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(weights=None)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, 2)
    in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
    model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask, 256, 2)
    model.load_state_dict(torch.load(weights_path, map_location=device))
    model.to(device)
    model.eval()
    return model

def correct_lens_distortion(img, mtx, dist):
    h, w = img.shape[:2]
    new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    dst = cv2.undistort(img, mtx, dist, None, new_camera_mtx)
    x, y, roi_w, roi_h = roi
    return dst[y:y+roi_h, x:x+roi_w]

def measure_baseline_card(img, ppm_ratio):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([80, 70, 50]), np.array([105, 255, 255]))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    valid_contours = [c for c in contours if cv2.contourArea(c) > 500]
    if not valid_contours:
        return None
    largest_contour = max(valid_contours, key=cv2.contourArea)
    _, _, pixel_w, pixel_h = cv2.boundingRect(largest_contour)
    return pixel_w / ppm_ratio, pixel_h / ppm_ratio

def measure_target_ai(img, model, device, ppm_ratio):
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    tensor_img = torchvision.transforms.functional.to_tensor(rgb_img).unsqueeze(0).to(device)
    with torch.no_grad():
        prediction = model(tensor_img)[0]
    scores = prediction['scores'].cpu().numpy()
    if len(scores) == 0 or scores[0] < 0.15:
        return None
    mask = (prediction['masks'][0, 0].cpu().numpy() > 0.5).astype(np.uint8)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    largest_contour = max(contours, key=cv2.contourArea)
    _, _, pixel_w, pixel_h = cv2.boundingRect(largest_contour)
    
    return pixel_w / ppm_ratio, pixel_h / ppm_ratio, scores[0], largest_contour

def run_single_image_pipeline(image_path, weights_path, output_dir=DEFAULT_OUTPUT_DIR):
    if not os.path.exists(image_path):
        print(f"❌ ERROR: Input image path not found: {image_path}")
        return None

    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(image_path)
    output_filepath = os.path.join(output_dir, f"annotated_{filename}")

    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    print(f"Loading model on {device}...")
    model = load_segmentation_model(weights_path, device)

    raw_img = cv2.imread(image_path)
    if raw_img is None:
        print(f"❌ ERROR: Could not read image at {image_path}")
        return None

    print(f"Processing single image: {filename}...")
    img = correct_lens_distortion(raw_img, CAMERA_MATRIX, DISTORTION_COEFFICIENTS)
    annotated_img = img.copy() 

    card_dims = measure_baseline_card(img, PIXELS_PER_MM)
    active_ppm = PIXELS_PER_MM
    
    if card_dims:
        c_w, _ = card_dims
        pixel_width_of_card = c_w * PIXELS_PER_MM
        active_ppm = pixel_width_of_card / CARD_WIDTH_MM
        print(f"   -> Calibration card detected. Dynamic PPM calculated: {active_ppm:.4f}")
    else:
        print(f"   -> No calibration card detected. Using default PPM: {PIXELS_PER_MM:.4f}")
        
    box_result = measure_target_ai(img, model, device, active_ppm)
    
    if box_result:
        b_w, b_h, conf, contour = box_result
        pred_short, pred_long = sorted([b_w, b_h])
        
        err_long = abs(pred_long - TRUE_DIM_LONG)
        err_short = abs(pred_short - TRUE_DIM_SHORT)
        
        pct_long = (err_long / TRUE_DIM_LONG) * 100
        pct_short = (err_short / TRUE_DIM_SHORT) * 100
        avg_pct_err = (pct_long + pct_short) / 2.0
        
        overlay = annotated_img.copy()
        cv2.drawContours(overlay, [contour], -1, (0, 255, 255), -1) 
        cv2.addWeighted(overlay, 0.4, annotated_img, 0.6, 0, annotated_img)
        cv2.drawContours(annotated_img, [contour], -1, (0, 255, 255), 3) 

        text_lines = [
            f"File: {filename}",
            f"Conf: {conf:.2f}",
            f"Dims: {pred_long:.1f} x {pred_short:.1f} mm",
            f"Err(L): {err_long:.1f}mm ({pct_long:.1f}%)",
            f"Err(S): {err_short:.1f}mm ({pct_short:.1f}%)",
            f"Avg Err: {avg_pct_err:.1f}%"
        ]
        
        y_offset = 60
        for line in text_lines:
            cv2.putText(annotated_img, line, (40, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 5, cv2.LINE_AA)
            cv2.putText(annotated_img, line, (40, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
            y_offset += 45

        print(f"✅ Success! Detection metrics:")
        print(f"Conf: {conf:.4f}")
        print(f"   -> Long Dim ({TRUE_DIM_LONG}mm): {pred_long:.2f}mm | Abs: {err_long:.2f}mm | Pct: {pct_long:.2f}%")
        print(f"   -> Short Dim ({TRUE_DIM_SHORT}mm): {pred_short:.2f}mm | Abs: {err_short:.2f}mm | Pct: {pct_short:.2f}%")
        print(f"   -> Average System Error: {avg_pct_err:.2f}%")
        
    else:
        print(f"❌ ERROR: Target localization breach - skipping metrics.")
        cv2.putText(annotated_img, "Target localization breach", (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
        
    cv2.imwrite(output_filepath, annotated_img)
    print(f"💾 Annotated image saved to: {output_filepath}")
    return output_filepath

# Provide your image path here to test on a single image
IMAGE_PATH_TO_TEST = "/kaggle/input/datasets/muhammadunssrahim/teabox/test/IMG_20260609_020946_jpg.rf.BRouITSHw35AfDSGMRAX.jpg" 
MODEL_WEIGHTS_PATH = "teabox_mask_rcnn.pth"

final_annotated_path = run_single_image_pipeline(IMAGE_PATH_TO_TEST, MODEL_WEIGHTS_PATH)

if final_annotated_path and os.path.exists(final_annotated_path):
    print(f"\n👇 Click the link below to download your annotated visual result:")
    display(FileLink(final_annotated_path))
