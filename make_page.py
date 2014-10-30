import os
from html_generator import HtmlGenerator

def make_page(path, name, images, words=None):
    num_images = len(images)
    if not words:
        words = [''] * num_images
    css_ids = ['undetermined'] * num_images
    filename = os.path.join(path, name)
    title = 'Images'
    page = HtmlGenerator(filename)
    page.h1(title)
    page.table(images,  words, css_ids)
    page.close()