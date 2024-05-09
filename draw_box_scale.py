import cv2
import os


# load image
def load_image(path):
    return cv2.imread(path)


def draw_colored_border(image, rect, color='blue', thickness=2):
    colors = {'red': (0, 0, 255),
              'orange': (0, 165, 255),
              'blue': (255, 0, 0)}
    
    chosen_color = colors.get(color.lower(), (0, 0, 255))  # default 'red'

    # draw box
    x, y, w, h = rect
    cv2.rectangle(image, (x, y), (x + w, y + h), chosen_color, thickness, cv2.LINE_AA)


# magnify region
def magnify_region(image, rect, scale_factor):
    x, y, w, h = rect
    selected_region = image[y:y+h, x:x+w]
    magnified_region = cv2.resize(selected_region, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

    draw_colored_border(magnified_region, (0, 0, magnified_region.shape[1], magnified_region.shape[0]))

    return magnified_region


def place_magnified_on_image(original_image, magnified_image, loacte):
    oh, ow = original_image.shape[:2]
    mh, mw = magnified_image.shape[:2]

    # Ensure enlarged image are smaller than original images.
    mh, mw = min(mh, oh), min(mw, ow)
    magnified_image = cv2.resize(magnified_image, (mw, mh))

    if loacte == 'left_up':
        original_image[0:mh, 0:mw] = magnified_image # left up
    elif loacte == 'left_down':
        original_image[oh - mh:oh, 0:mw] = magnified_image # left down
    elif loacte == 'right_up':
        original_image[0:mh, ow - mw:ow] = magnified_image # right up
    elif loacte == 'right_down':
        original_image[oh - mh:oh, ow - mw:ow] = magnified_image # right down
    else:
        print(f'<locate> is not supported !')

    return original_image


# Processing single image
def process_image(image_path, rect, scale_factor, loacte):
    image = load_image(image_path)

    # Draw a box
    draw_colored_border(image, rect)

    magnified_region = magnify_region(image, rect, scale_factor)
    result_image = place_magnified_on_image(image, magnified_region, loacte)

    return result_image


def main(directory, save_subdir="box", scale_factor=3, loacte='right_down'):
    assert loacte in ['left_up', 'left_down', 'right_up', 'right_down']

    # Create the directory
    save_dir = os.path.join(directory, save_subdir)
    try: 
        os.makedirs(save_dir)
    except OSError:
        print ("Creation of the directory %s failed" % save_dir)
    else:
        print ("Successfully created the directory %s " % save_dir)

    # dir
    images = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not images:
        print("Directory contains no image files.")
        return

    # Get ROI 
    first_image = load_image(images[0])
    roi = cv2.selectROI("Image", first_image, False, False)
    cv2.destroyAllWindows()

    # draw boxes for every image
    for image_path in images:
        result_image = process_image(image_path, roi, scale_factor, loacte)

        # generate file name
        base_name = os.path.basename(image_path)
        name, ext = os.path.splitext(base_name)
        new_name = f"{name}_box{ext}"
        result_path = os.path.join(save_dir, new_name)
        
        cv2.imwrite(result_path, result_image)
        print(f"Processed and saved: {result_path}")


if __name__ == "__main__":
    """
    Enlarge images locally.
    * Synchronous processing of multiple images
    * arbitrary zoom ratios 
    * placement of the magnified area in any corner of the image

    Args:
        directory (str): The directory containing the images.
        save_subdir (str, optional): The directory where the enlarged images will be saved. Defaults to "box".
        scale_factor (float, optional): The scaling factor. Defaults to 3..
        locate (str, optional): The location of the magnified area. Supports 'left_up', 'left_down', 'right_up', 'right_down'. Defaults to 'right_down'.
    """

    directory = './data1/'
    main(directory, save_subdir='left_up', scale_factor=5, loacte='left_up')


