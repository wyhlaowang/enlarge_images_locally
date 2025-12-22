import cv2
import numpy as np
from color_dict import *


def get_roi(img, title="===== Select Your ROI ! ====="):
    if isinstance(img, str):
        img = cv2.imread(img)
   
    roi = cv2.selectROI(title, img, fromCenter=False, showCrosshair=True)
    cv2.destroyAllWindows()
    
    return roi

def get_multi_roi(img, roi_num, colors, thickness, if_dash, dash_length):
    roi_ls = []
    for idx in range(roi_num):
        roi = get_roi(img, f"===== Select Your <{idx+1} ROI> ! =====")
        roi_ls.append(roi)
        draw_box(img, roi, colors[idx], thickness, if_dash, dash_length)

    return roi_ls

def get_size(img):
    if isinstance(img, str):
        img = cv2.imread(img)

    obj_h = img.shape[0]
    obj_w = img.shape[1]        

    return obj_h, obj_w


def get_img(img, obj_h=None, obj_w=None):
    if isinstance(img, str):
        img = cv2.imread(img)
    
    if (obj_h is not None) and (obj_w is not None):
        img = cv2.resize(img, (obj_w, obj_h))

    return img


def get_patch(img, roi_or_points):
    if isinstance(roi_or_points[0], tuple):
        roi = points_to_roi(roi_or_points)
    else:
        roi = roi_or_points

    x, y, w, h = roi
    patch = img[y:y+h, x:x+w]

    return patch


def roi_to_points(roi):
    x, y, w, h = roi

    top_left = (x, y)
    top_right = (x + w, y)
    bottom_left = (x, y + h)
    bottom_right = (x + w, y + h)    

    points = top_left, top_right, bottom_left, bottom_right

    return points


def points_to_roi(points):
    top_left, top_right, bottom_left, bottom_right = points

    x = top_left[0]
    y = top_left[1]
    w = top_right[0] - top_left[0]
    h = bottom_left[1] - top_left[1]

    roi = (x, y, w, h)

    return roi


def auto_thickness(img_width, beta=0.01):
    return int(img_width * beta)


def dashed_rectangle(img, start_point, end_point, color, thickness=8, dash_length=10):
    x1, y1 = start_point
    x2, y2 = end_point
    
    for x in range(x1, x2, int(dash_length * 2.5)):
        cv2.line(img, (x, y1), (min(x + dash_length, x2), y1), color, thickness, cv2.LINE_AA)
        cv2.line(img, (x, y2), (min(x + dash_length, x2), y2), color, thickness, cv2.LINE_AA)

    for y in range(y1, y2, int(dash_length * 2.5)):
        cv2.line(img, (x1, y), (x1, min(y + dash_length, y2)), color, thickness, cv2.LINE_AA)
        cv2.line(img, (x2, y), (x2, min(y + dash_length, y2)), color, thickness, cv2.LINE_AA)


def draw_box(img, roi, color='orange', thickness=8, if_dash=False, dash_length=10):
    bgr = get_color_bgr(color)

    if if_dash:
        points = roi_to_points(roi)
        dashed_rectangle(img, points[0], points[3], bgr, thickness, dash_length)
    else:
        x, y, w, h = roi
        cv2.rectangle(img, (x, y), (x + w, y + h), bgr, thickness, cv2.LINE_AA)


def compute_entropy(img):
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist /= hist.sum()  
    
    entropy = -np.sum(hist * np.log2(hist + 1e-10)) 

    return entropy


def auto_scale(img, roi=None):
    en = compute_entropy(img)
    scale = 0.5 * en + 0.5
    if roi is not None:
        x, y, w, h = roi
        img_h, img_w = get_size(img)
        scale_max = min(img_h/h, img_w/w)
        return min(scale, scale_max)
    else:
        return scale


def check_scale(img, roi, border, scale):
    ih, iw = get_size(img)
    x, y, w, h = roi
    max_scale = min((iw-border)/w-0.1, (ih-border)/h-0.1)
    return min(scale, max_scale)


def patch_corner(img, patch, corner, roi=None):
    oh, ow = img.shape[:2]
    mh, mw = patch.shape[:2]

    if corner == "auto":
        x, y, w, h = roi
        center_w = x + w //2
        center_h = y + h //2

        delta = [center_w**2 + center_h**2, 
                 (ow-center_w)**2 + center_h**2,
                 center_w**2 + (oh-center_h)**2,
                 (ow-center_w)**2 + (oh-center_h)**2]
        corners = ["top-left", "top-right", "bottom-left", "bottom-right"]
        index = delta.index(max(delta))
        corner = corners[index]

    if corner == "top-left":
        img[0:mh, 0:mw] = patch 
    elif corner == "bottom-left":
        img[oh - mh:oh, 0:mw] = patch 
    elif corner == "top-right":
        img[0:mh, ow - mw:ow] = patch 
    elif corner == "bottom-right":
        img[oh - mh:oh, ow - mw:ow] = patch 
    else:
        print(f'{corner} is Not Supported !')

    return img


def patch_beside(img, patch, beside, roi, thickness):
    oh, ow = img.shape[:2]
    mh, mw = patch.shape[:2]
    x, y, w, h = roi

    center_h = y + h //2
    center_w = x + w //2

    if beside == "auto":
        delta = [center_h/oh, (oh-center_h)/oh, center_w/ow, (ow-center_w)/ow]
        besides = ["top", "bottom", "left", "right"]
        index = delta.index(max(delta))
        beside = besides[index]

    if beside == "top":
        anchor_h = y + thickness
        anchor_w = x + w//2
        img[anchor_h-mh:anchor_h, anchor_w-mw//2:anchor_w+mw//2] = patch 
    elif beside == "bottom":
        anchor_h = y + h - thickness
        anchor_w = x + w//2
        img[anchor_h:anchor_h+mh, anchor_w-mw//2:anchor_w+mw//2] = patch 
    elif beside == "left":
        anchor_h = y + h//2
        anchor_w = x + thickness   
        img[anchor_h-mh//2:anchor_h+mh//2, anchor_w-mw:anchor_w] = patch
    elif beside == "right":
        anchor_h = y + h//2
        anchor_w = x + w - thickness   
        img[anchor_h-mh//2:anchor_h+mh//2, anchor_w:anchor_w+mw] = patch
    else:
        print(f'{beside} is Not Supported !')

    return img


def multi_patch_outside(img, patch_ls, beside, border, colors):
    oh, ow = img.shape[:2]
    
    if beside in ["top", "bottom"]:
        hs = [p.shape[0] for p in patch_ls]
        scaled_patches = []
        for idx, p in enumerate(patch_ls):
            scale = max(hs) / hs[idx]
            scaled_patch = cv2.resize(p.copy(), None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)            
            scaled_patches.append(scaled_patch)

        scaled_w = [p.shape[1] for p in scaled_patches]
        sum_w = sum(scaled_w)
        scale = (ow - 2*border*len(patch_ls)) / sum_w

        border_patches = []
        for idx, p in enumerate(scaled_patches):
            border_patch = cv2.resize(p.copy(), None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)     
            border_patch = cv2.copyMakeBorder(border_patch, border, border, border, border, cv2.BORDER_CONSTANT, value=get_color_bgr(colors[idx]))
            border_patches.append(border_patch)

        concated_patch = cv2.hconcat(border_patches)[:, :ow]
        concated = cv2.vconcat([concated_patch, img]) if beside == "top" else cv2.vconcat([img, concated_patch])

    elif beside in ["right", "left"]:
        border_patches = []
        for idx, p in enumerate(patch_ls):
            scale = (oh - 2*border) / p.shape[0]
            scaled_patch = cv2.resize(p.copy(), None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)        
            border_patch = cv2.copyMakeBorder(scaled_patch, border, border, border, border, cv2.BORDER_CONSTANT, value=get_color_bgr(colors[idx]))
            border_patches.append(border_patch)

        concated_patch = cv2.hconcat(border_patches)
        concated = cv2.hconcat([concated_patch, img]) if beside == "left" else cv2.hconcat([img, concated_patch])

    else:
        print(f'{beside} is Not Supported !')

    return concated



def multi_patch_inside(img, patch_ls, corner, border, colors, scale):
    im = img.copy()
    oh, ow = im.shape[:2]
    
    hs = [p.shape[0] for p in patch_ls]
    scaled_patches = []
    for idx, p in enumerate(patch_ls):
        scale_align = max(hs) / hs[idx]
        scaled_patch = cv2.resize(p.copy(), None, fx=scale_align, fy=scale_align, interpolation=cv2.INTER_CUBIC)            
        scaled_patches.append(scaled_patch)

    scaled_w = [p.shape[1] for p in scaled_patches]
    sum_w = sum(scaled_w)
    scale_max = (ow - 2*border*len(patch_ls)) / sum_w
    scale = min(scale, scale_max)

    border_patches = []
    for idx, p in enumerate(scaled_patches):
        border_patch = cv2.resize(p.copy(), None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)     
        border_patch = cv2.copyMakeBorder(border_patch, border, border, border, border, cv2.BORDER_CONSTANT, value=get_color_bgr(colors[idx]))
        border_patches.append(border_patch)

    concated_patch = cv2.hconcat(border_patches)

    patch_corner(im, concated_patch, corner)

    return im

