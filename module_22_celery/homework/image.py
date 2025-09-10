"""
Здесь происходит логика обработки изображения
"""

from typing import Optional

from PIL import Image, ImageFilter


def blur_image(img_file_path):
    """
    Функция принимает на вход имя входного и выходного файлов.
    Применяет размытие по Гауссу со значением 5.
    """
    # if not dst_filename:
    #     dst_filename = f'blur_{src_filename}'

    with Image.open(img_file_path) as img:
        img.load()
        new_img = img.filter(ImageFilter.GaussianBlur(5))
        file_path_list = img_file_path.split('/')
        new_img_filename = (f"{file_path_list[0]}/{file_path_list[1]}/{file_path_list[2]}/blur_{file_path_list[3]}")
        new_img.save(new_img_filename)
        return new_img_filename
