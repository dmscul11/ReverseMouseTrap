# ReverseMouseTrap

### Loading an image
    from loader.ImageLoader import *
    original_image, new_image, binary_image, color_matrix = load_image(Difficulty.TEST)

###### Showing an image
    from loader.ImageLoader import show_image
    show_image(image)
    
### Detecting objects & Retrieving them
    from loader.ImageLoader import *
    from detector.ObjectDetector import ObjectDetector
    original, new, binary, color_matrix = load_image(Difficulty.TEST_SMALL_2)

    obj_detector = ObjectDetector(new, binary, color_matrix)
    obj_detector.scan_image()

    objects = obj_detector.get_objects()
    
###### To see a label plane in terminal
    obj_detector.print_label_plane()
