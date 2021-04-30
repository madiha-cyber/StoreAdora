from PIL import Image


def resize_image_square_crop(src_img_stream, required_size=(100, 100)):
    """
    returns (bool, msg, img)
    """
    img = Image.open(src_img_stream)
    if img.format != "JPEG":
        return (False, "File is not JPEG", None)

    # original size is  a tuple
    # tuple of height and width (heigth, width)
    original_size = img.size
    if original_size[0] > 5000 or original_size[0] < 5:
        return (False, "Image size too big or small", None)

    if original_size[1] > 5000 or original_size[1] < 5:
        return (False, "Image size too big or small", None)

    # min of (width, height)
    smallest_side = min(original_size[0], original_size[1])

    # if width is greater than height then crop the width
    if original_size[0] > original_size[1]:
        x = (original_size[0] - smallest_side) / 2
        #
        new_size = (x, 0, x + smallest_side, original_size[1])
    # if heigth is greater than width then crop the heigth
    elif original_size[0] < original_size[1]:
        y = (original_size[1] - smallest_side) / 2
        new_size = (0, y, smallest_side, y + smallest_side)
    # if width is equal to heigth then don't crop
    else:
        new_size = (0, 0, smallest_side, smallest_side)

    # crop the image based on new size
    cropped_image = img.crop(new_size)
    # resize the image based on required size
    resize_image = cropped_image.resize(required_size)
    return (True, "Resized the image", resize_image)


def resize_image(src_img_stream, required_size=(100, 100)):
    """
    returns (bool, msg, img)
    """
    img = Image.open(src_img_stream)
    if img.format != "JPEG":
        return (False, "File is not JPEG", None)

    original_size = img.size
    if original_size[0] > 5000 or original_size[0] < 5:
        return (False, "Image size too big or small", None)

    if original_size[1] > 5000 or original_size[1] < 5:
        return (False, "Image size too big or small", None)

    # smallest_side = min(original_size[0], original_size[1])
    # TODO: Fix this

    # if original_size[0] > original_size[1]:
    #     x = (original_size[0] - smallest_side) / 2
    #     new_size = (x, 0, x + smallest_side, original_size[1])
    # elif original_size[0] < original_size[1]:
    #     y = (original_size[1] - smallest_side) / 2
    #     new_size = (0, y, smallest_side, y + smallest_side)
    # else:
    #     new_size = (0, 0, smallest_side, smallest_side)

    # cropped_image = img.crop(new_size)
    resize_image = img.resize(required_size)
    return (True, "Resized the image", resize_image)
