"""
Collect images
"""
import argparse
import shutil
import os
import time
import logging
from io import BytesIO
import requests
import numpy as np
import cv2
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, ElementNotInteractableException
from image_crawl.src.utils.imageprocessor import ImageProcessor
from PIL import Image

IMG_CLASS = 'rg_i'
BIG_IMG_XPATH = '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img'

def get_param():
    """
    Get parameters
    """
    parser = argparse.ArgumentParser(prog ='bcrawl')
    parser.add_argument('-n', '--number',
                        type=int,
                        required=True,
                        dest='num',
                        help='Number of images')
    parser.add_argument('-k', '--keyword',
                        type=str,
                        required=True,
                        dest='keyword',
                        help='Keyword')
    parser.add_argument('-d', '--dest',
                        type=str,
                        required=True,
                        dest='dest',
                        help='Destination folder')
    parser.add_argument('--xshear',
                        nargs='+',
                        required=False,
                        dest='xshear',
                        help='xshear range')
    parser.add_argument('--yshear',
                        nargs='+',
                        required=False,
                        dest='yshear',
                        help='yshear range')
    parser.add_argument('--rotate',
                        nargs='+',
                        required=False,
                        dest='rotate',
                        help='rotate range')
    parser.add_argument('--flip',
                        type=bool,
                        required=False,
                        default=False,
                        dest='flip',
                        help='flip')
    parser.add_argument('--zoom',
                        nargs='+',
                        required=False,
                        dest='zoom',
                        help='zoom range')
    parser.add_argument('--resize',
                        nargs='+',
                        required=False,
                        dest='resize',
                        help='Resize')
    args = parser.parse_args()
    return args

def save_file(image, filename, image_url, count,
                image_file_path, metadata_file_path, status_file_path):
    """
    Save file
    """
    cv2.imwrite(image_file_path,image)
    with open(metadata_file_path,"a") as metadata_file:
        metadata_file.write("{0}, {1}\n".format(filename, image_url))
    with open(status_file_path,"w") as status_file:
        status_file.write(str(count))

def main():
    """
    Main
    """
    args = get_param()
    status_file_path = os.path.join(args.dest, 'status.txt')
    if os.path.exists(args.dest):
        try:
            with open(status_file_path,'r') as status_file:
                count = int(status_file.read())
        except (FileNotFoundError, ValueError):
            shutil.rmtree(args.dest)
            os.mkdir(args.dest)
            with open(status_file_path,'w') as status_file:
                count = 0
                status_file.write(str(count))
    else:
        os.mkdir(args.dest)
        with open(status_file_path,'w') as status_file:
            count = 0
            status_file.write(str(count))

    url = "https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={0}".format(args.keyword)
    browser = webdriver.Chrome()
    browser.get(url)
    images = browser.find_elements_by_class_name(IMG_CLASS)
    prev_images = images
    while True:
        metadata_file_path = os.path.join(args.dest, "metadata.txt")
        for image in images:
            try:
                image.click()
            except (StaleElementReferenceException, ElementClickInterceptedException, 
                    ElementNotInteractableException):
                continue
            time.sleep(1)
            big_image = browser.find_element_by_xpath(BIG_IMG_XPATH)
            image_url = big_image.get_attribute("src")
            try:
                response = requests.get(image_url)
            except requests.exceptions.InvalidSchema:
                continue

            if response.status_code==200:
                content = Image.open(BytesIO(response.content))
                image = np.array(content)
                if len(image.shape) != 3:
                    continue
                image = image[:,:,[2,1,0]]
                filled = ImageProcessor.fill(image)
                size = None
                if args.resize is not None:
                    size = args.resize
                    size = (int(size[0]),int(size[1]))
                    filled = ImageProcessor.resize(filled,size)
                filename = "{0}.jpg".format(str(count).zfill(len(str(args.num))))
                image_file_path = os.path.join(args.dest,filename)
                save_file(filled, filename, image_url, count, image_file_path, metadata_file_path, status_file_path)
                count += 1
                if count >= args.num:
                    break
                if args.xshear is not None:
                    shear_range = args.xshear
                    if len(shear_range) == 1:
                        shear_range = (0, float(shear_range[0]))
                    else: 
                        shear_range = (float(shear_range[0]), float(shear_range[1]))
                    filename = "{0}.jpg".format(str(count).zfill(len(str(args.num))))
                    image_file_path = os.path.join(args.dest,filename)
                    xsheared = ImageProcessor.random_shear(image, shear_range, size=size)
                    save_file(xsheared, filename, image_url, count, image_file_path, metadata_file_path, status_file_path)
                    count += 1
                    if count >= args.num:
                        break
                if args.yshear is not None:
                    shear_range = args.yshear
                    if len(shear_range) == 1:
                        shear_range = (0, float(shear_range[0]))
                    else: 
                        shear_range = (float(shear_range[0]), float(shear_range[1]))
                    filename = "{0}.jpg".format(str(count).zfill(len(str(args.num))))
                    image_file_path = os.path.join(args.dest,filename)
                    ysheared = ImageProcessor.random_shear(image, shear_range, direction=0, size=size)
                    save_file(ysheared, filename, image_url, count, image_file_path, metadata_file_path, status_file_path)
                    count += 1
                    if count >= args.num:
                        break
                if args.rotate is not None:
                    rotate_range = args.rotate
                    if len(rotate_range) == 1:
                        rotate_range = (0, float(rotate_range[0]))
                    else:
                        rotate_range = (float(rotate_range[0]), float(rotate_range[1]))
                    filename = "{0}.jpg".format(str(count).zfill(len(str(args.num))))
                    image_file_path = os.path.join(args.dest,filename)
                    rotated = ImageProcessor.random_rotate(image, rotate_range, size=size)
                    save_file(rotated, filename, image_url, count, image_file_path, metadata_file_path, status_file_path)
                    count += 1
                    if count >= args.num:
                        break
                if args.flip:
                    filename = "{0}.jpg".format(str(count).zfill(len(str(args.num))))
                    image_file_path = os.path.join(args.dest,filename)
                    flipped = ImageProcessor.random_flip(image, size=size)
                    save_file(flipped, filename, image_url, count, image_file_path, metadata_file_path, status_file_path)
                    count += 1
                    if count >= args.num:
                        break
                if args.zoom is not None:
                    zoom_range = args.zoom
                    if len(zoom_range) == 1:
                        zoom_range = (0, float(zoom_range[0]))
                    else: 
                        zoom_range = (float(zoom_range[0]), float(zoom_range[1]))
                    filename = "{0}.jpg".format(str(count).zfill(len(str(args.num))))
                    image_file_path = os.path.join(args.dest,filename)
                    zoomed = ImageProcessor.random_zoom(image, zoom_range, size=size)
                    save_file(zoomed, filename, image_url, count, image_file_path, metadata_file_path, status_file_path)
                    count += 1
                    if count >= args.num:
                        break

            response.close()
            time.sleep(1)
        if count < args.num:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")   
            new_images = browser.find_elements_by_class_name(IMG_CLASS)
            images = list(set(new_images) - set(prev_images))
            prev_images = new_images
        else:
            break

    logging.info("Done!")

if __name__=="__main__":
    main()
