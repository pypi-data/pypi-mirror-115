"""
Image Processing Toolkit
"""
import numpy as np
import cv2
import random

class ImageProcessor():
    """
    Image processing class
    """
    def __init__(self):
        pass

    @staticmethod
    def resize(image, size):
        """
        Image resizing
        """
        return cv2.resize(image, (size[1],size[0]))

    @staticmethod
    def fill(image):
        """
        Image filling
        """
        height, width, _ = image.shape
        max_size = max(height, width)
        filled = np.zeros((max_size,max_size,3),dtype=np.uint8)
        filled[(max_size-height)//2:(max_size+height)//2,
                (max_size-width)//2:(max_size+width)//2,:]= image
        return filled
    
    @staticmethod
    def shear(image, shear_value, direction=1, filled=True, size=None):
        """
        Image shearing
        """
        assert direction in (0,1)
        height, width, _ = image.shape
        if direction == 1:
            width = width + abs(int(height*shear_value))
            translate_vector =(min(0, height*shear_value),0) 
            shear_matrix = np.float32([[1, shear_value, 0],[0, 1, 0],[0, 0, 1]])
        else:
            height = height + abs(int(width*shear_value))
            translate_vector =(0,min(0, width*shear_value)) 
            shear_matrix = np.float32([[1, 0, 0],[shear_value, 1, 0], [0, 0, 1]])
        translate_matrix = np.float32([[1, 0, -translate_vector[0]],
                                        [0, 1, -translate_vector[1]],
                                        [0, 0, 1]])
        transform_matrix = translate_matrix.dot(shear_matrix)
        sheared = cv2.warpPerspective(image, transform_matrix, (width, height))
        if filled:
            sheared = ImageProcessor.fill(sheared)
        if size is not None:
            sheared = ImageProcessor.resize(sheared,size)
        return sheared
    
    @staticmethod
    def random_shear(image, shear_range, direction=1, filled=True, size=None):
        """
        Random shear
        """
        shear_value = random.random()*abs(shear_range[1]-shear_range[0]) + min(shear_range[1],shear_range[0])
        return ImageProcessor.shear(image, shear_value, direction, filled, size)

    @staticmethod
    def rotate(image, angle, filled=True, size=None):
        """
        Image rotating
        """
        assert angle is not None
        angle = np.radians(angle)
        height_prev, width_prev, _ = image.shape
        rotate_matrix = np.float32([[np.cos(angle), -(np.sin(angle)), 0],
                                    [np.sin(angle), np.cos(angle), 0],
                                    [0, 0, 1]])
        top_left = np.zeros(2)
        top_right = np.array([width_prev*np.cos(angle), width_prev*np.sin(angle)])
        bottom_left = np.array([height_prev*np.cos(angle+np.pi/2),
                                height_prev*np.sin(angle+np.pi/2)])
        bottom_right = top_right + bottom_left
        width = int(max(abs((top_left - bottom_right)[0]), abs((top_right - bottom_left)[0])))
        height = int(max(abs((top_left - bottom_right)[1]), abs((top_right - bottom_left)[1])))
        translate_vector = np.min([top_left, top_right, bottom_left, bottom_right],axis=0)
        translate_matrix = np.float32([[1, 0, -translate_vector[0]],
                                        [0, 1, -translate_vector[1]],
                                        [0, 0, 1]])
        transform_matrix = translate_matrix.dot(rotate_matrix)
        rotated = cv2.warpPerspective(image, transform_matrix, (width, height))
        if filled:
            rotated = ImageProcessor.fill(rotated)
        if size is not None:
            rotated = ImageProcessor.resize(rotated,size)
        return rotated
    
    @staticmethod
    def random_rotate(image, angle_range, filled=True, size=None):
        """
        Random rotate
        """
        angle = random.random()*abs(angle_range[1]-angle_range[0]) + min(angle_range[1],angle_range[0])
        return ImageProcessor.rotate(image, angle, filled, size)

    @staticmethod
    def flip(image, direction=1, filled=True, size=None):
        """
        Image flipping
        """
        assert direction in (0,1)
        flipped = cv2.flip(image, direction)
        if filled:
            flipped = ImageProcessor.fill(flipped)
        if size is not None:
            flipped = ImageProcessor.resize(flipped,size)
        return flipped

    @staticmethod
    def random_flip(image, filled=True, size=None):
        """
        Random flip
        """
        direction = round(random.random())
        return ImageProcessor.flip(image, direction, filled, size)

    @staticmethod
    def zoom(image, zoom_factor=1.0, filled=True, size=None):
        """
        Image zooming
        """
        assert zoom_factor > 0
        height, width, _ = image.shape
        if zoom_factor > 1.0:
            dsize = (int(width*zoom_factor),int(height*zoom_factor))
            zoomed = cv2.resize(image, dsize)
            zoomed = zoomed[(int(height*zoom_factor)-height)//2:(int(height*zoom_factor)+height)//2,
                            (int(width*zoom_factor)-width)//2:(int(width*zoom_factor)+width)//2,:]
        else:
            zoomed = np.zeros((int(height*1/zoom_factor),int(width*1/zoom_factor),3),dtype=np.uint8)
            zoomed[(int(height*1/zoom_factor)-height)//2:(int(height*1/zoom_factor)+height)//2,
                (int(width*1/zoom_factor)-width)//2:(int(width*1/zoom_factor)+width)//2,:]= image
            zoomed = cv2.resize(zoomed, (width,height))
        if filled:
            zoomed = ImageProcessor.fill(zoomed)
        if size is not None:
            zoomed = ImageProcessor.resize(zoomed,size)    
        return zoomed

    @staticmethod
    def random_zoom(image, zoom_range, fill=True, size=None):
        """
        Random zoom
        """
        zoom_factor = random.random()*abs(zoom_range[1]-zoom_range[0]) + min(zoom_range[1],zoom_range[0])
        if zoom_factor <= 0:
            zoom_factor = 0.01
        return ImageProcessor.zoom(image, zoom_factor, fill, size)
