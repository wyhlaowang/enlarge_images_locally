import os
import cv2
from utils import *
from color_dict import *



def main(configs):
    images_dir = configs.get("images_dir")
    save_folder = configs.get("save_folder")
    roi_folder = configs.get("roi_folder")
    reference_img = configs.get("reference_img")

    roi_number = configs.get("roi_number")
    mode = configs.get("mode")
    outside = configs.get("outside_position")
    inside = configs.get("inside_position")
    scale = configs.get("scale")

    colors = configs.get("colors")
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

    if thickness == "auto":
        thickness = auto_thickness(obj_w)
    else:
        thickness = int(thickness)

    border = int(2 * thickness)

    roi_ls = get_multi_roi(reference_img, roi_number, colors, thickness, if_dash_box, dash_length)
    for ip in img_paths:
        img = get_img(ip, obj_h, obj_w)
        patch_ls = [get_patch(img.copy(), roi) for roi in roi_ls]

        for idx, roi in enumerate(roi_ls):
            draw_box(img, roi, colors[idx], thickness, if_dash_box, dash_length)

        if mode == "inside":
            zoom_im = multi_patch_inside(img, patch_ls, inside, border, colors, scale)
        elif mode == "outside":
            zoom_im = multi_patch_outside(img, patch_ls, outside, border, colors)
        else:
            zoom_im = img

        base_name = os.path.basename(ip)
        cv2.imwrite(os.path.join(images_dir, save_folder, base_name), zoom_im)
        for idx, patch in enumerate(patch_ls):
            name, ext = os.path.splitext(base_name)
            saved_name = f"{name}_{idx}{ext}"
            cv2.imwrite(os.path.join(images_dir, roi_folder, saved_name), patch)

        print(f"Processed and Saved: {base_name} !")


if __name__ == "__main__":
    # ===== Parameters without <Need Change> can be Neglected ! =====

    CONFIGS = {
        "images_dir": "./test_data",         # <Need Change> Your Image Directory
        "roi_number": 1,                     # <Need Change> Choose from 1 - 14

        "mode": "inside",                    # Choose from ["inside", "outside", "only_roi"]
        "outside_position": "right",         # Choose from ["top", "bottom", "right", "left"]
        "inside_position":  "top-right",   # Choose from ["top-right", "top-left", "bottom-right", "bottom-left"]
        "scale": 3,                           # Only for "inside" mode. Recommend: 2-5. zoom factor

        "thickness": "auto",                  # Recommend: "auto". line thickness. Choose from ["auto", <number>]
        "colors": ['orange',  'yellow', 'red',   
                   'purple',  'blue',   'green',  
                   'brown',   'gray',   'deep_red',  
                   'black',   'white',  'cyan',   
                   'magenta', 'pink'],        # box color. Choose from <Support Color>
        "if_dash_box": False,                 # if need dashed box 
        "dash_length": 8,                     # length of dash line

        "save_folder": "with_box",            # save location
        "roi_folder": "roi",                  # ROI location
        "reference_img": "***.png",           # for marking ROI
    }

    main(CONFIGS)




