import os
import cv2
from utils import *
from color_dict import *



def main(configs):
    images_dir = configs.get("images_dir")
    save_folder = configs.get("save_folder")
    roi_folder = configs.get("roi_folder")
    reference_img = configs.get("reference_img")

    mode = configs.get("mode")
    corner = configs.get("corner")
    beside = configs.get("beside")
    scale = configs.get("scale")

    color = configs.get("color")
    thickness = configs.get("thickness")
    if_dash_box = configs.get("if_dash_box")
    dash_length = configs.get("dash_length")

    os.makedirs(os.path.join(images_dir, save_folder), exist_ok=True)
    os.makedirs(os.path.join(images_dir, roi_folder), exist_ok=True)

    img_ls = [f for f in os.listdir(images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not img_ls:
        print("Directory Contains No Image !")
        return
    
    img_paths = [os.path.join(images_dir, f) for f in img_ls]

    if (reference_img is not None) and (reference_img in img_ls):
        reference_img = get_img(os.path.join(images_dir, reference_img))
    else:
        print(f"Assigned [{img_ls[0]}] as Reference Image !")
        reference_img = get_img(img_paths[0])

    obj_h, obj_w = get_size(reference_img)
    roi = get_roi(reference_img)

    if thickness == "auto":
        thickness = auto_thickness(obj_w)
    else:
        thickness = int(thickness)

    border = int(2*thickness) if mode == "corner" else int(1.5*thickness)

    if scale == "auto":
        scale = auto_scale(reference_img, roi)

    scale = check_scale(reference_img, roi, border, scale)

    # draw boxes for every image
    for p in img_paths:
        img = get_img(p, obj_h, obj_w)
        roi_patch = get_patch(img.copy(), roi)

        draw_box(img, roi, color, thickness, if_dash_box, dash_length)

        if mode == "corner":
            scaled_patch = cv2.resize(roi_patch, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            scaled_patch = cv2.copyMakeBorder(scaled_patch, border, border, border, border, cv2.BORDER_CONSTANT, value=get_color_bgr(color))
            patch_corner(img, scaled_patch, corner, roi)

        elif mode == "beside":
            scaled_patch = cv2.resize(roi_patch, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)            
            scaled_patch = cv2.copyMakeBorder(scaled_patch, border, border, border, border, cv2.BORDER_CONSTANT, value=get_color_bgr(color))
            patch_beside(img, scaled_patch, beside, roi, thickness)

        cv2.imwrite(os.path.join(images_dir, save_folder, os.path.basename(p)), img)
        cv2.imwrite(os.path.join(images_dir, roi_folder, os.path.basename(p)), roi_patch)

        print(f"Processed and Saved: {os.path.basename(p)} !")



if __name__ == "__main__":
    # ===== Parameters without <Need Change> can be Neglected ! =====

    CONFIGS = {
        "images_dir": "./test_data",         # <Need Change> Your Image Directory

        "scale": 3,                          # Recommend: 2-5. zoom factor. 
        "mode": "beside",                    # Recommend: "corner". Choose from ["corner", "beside", "only_roi"]
        "corner": "auto",                    # Recommend: "auto". Choose from ["auto", "top-right", "top-left", "bottom-right", "bottom-left"]
        "beside": "auto",                    # Recommend: "auto". Choose from ["auto", "top", "bottom", "right", "left"]

        "thickness": "auto",                # Recommend: "auto". line thickness. Choose from ["auto", <number>]
        "color": "orange",                  # box color. Choose from <Support Color>
        "if_dash_box": False,               # if need dashed box 
        "dash_length": 8,                   # length of dash line

        "save_folder": "with_box",           # save location
        "roi_folder": "roi",                 # ROI location
        "reference_img": "***.png",          # for marking ROI
    }

    main(CONFIGS)


"""
===== Support Color =====
'blue',  'green', 'red',   'deep_red', 'orange', 'yellow',  'purple', 
'brown', 'gray',  'black', 'white',    'cyan',   'magenta', 'pink', 
"""

