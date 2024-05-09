import cv2
import os


# load image
def load_image(path):
    return cv2.imread(path)


def draw_colored_border(image, rect, color='blue', thickness=4):
    colors = {'red': (0, 0, 255),
              'orange': (0, 165, 255),
              'blue': (255, 0, 0)}
    
    chosen_color = colors.get(color.lower(), (0, 0, 255))  # default 'red'

    # draw box
    x, y, w, h = rect
    cv2.rectangle(image, (x, y), (x + w, y + h), chosen_color, thickness, cv2.LINE_AA)


# Processing single image
def process_image(image_path, rect):
    image = load_image(image_path)
    draw_colored_border(image, rect)
    return image


def main(directory, save_subdir="box"):
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
        result_image = process_image(image_path, roi)

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

    Args:
        directory (str): The directory containing the images.
        save_subdir (str, optional): The directory where the enlarged images will be saved. Defaults to "box".
    """

    directory = './data1/'
    main(directory, save_subdir='box')


