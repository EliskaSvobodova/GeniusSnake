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


def mouse_on_button(button: pyglet.sprite.Sprite, x, y):
    if ((button.x - (button.width // 2) < x)
            & (x < button.x + (button.width // 2))
            & (button.y - (button.height // 2) < y)
            & (y < button.y + (button.height // 2))):
        return True
    return False


def draw_colored_rectangle(x, y, width, height, r, g, b):
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ("v2f", (x, y,
                                  x, y + height,
                                  x + width, y + height,
                                  x + width, y)),
                         ("c3B", ((r, g, b) * 4)))
    pyglet.gl.glFlush()
