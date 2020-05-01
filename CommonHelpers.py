import pyglet


def configure_resources():
    pyglet.resource.path = ['resources']
    pyglet.resource.reindex()


def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


def scale_image(image, width, height):
    image.scale = min(image.height, height) / max(image.height, height), \
                        min(width, image.width) / max(width, image.width)
    image.width = width
    image.height = height
