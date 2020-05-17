from src import CommonHelpers, Settings
import pyglet

class ControlPaneUI:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = 50
        space_between = 20
        self.graph_x = self.x + space_between
        self.graph_y = self.y + space_between
        self.graph_width = self.width - 2 * space_between
        self.graph_height = self.height - 1.5 * self.font_size - 2 * space_between
        self.point = self.load_point()

    def draw(self, generation):
        height = self.height - self.graph_height
        # plus five because of graph's last label
        CommonHelpers.draw_colored_rectangle(self.x, self.graph_y + self.graph_height + 5,
                                             self.width, self.height - self.graph_height,
                                             0, 0, 0)
        pyglet.text.Label(text=f"Generation: {generation}",
                          x=(self.x + self.width / 2), y=(self.y + self.height - self.font_size / 2),
                          anchor_x="center", anchor_y="center",
                          font_name="Bangers", font_size=self.font_size
                          ).draw()
        self.draw_graph_skeleton()
        pyglet.gl.glFlush()

    def draw_graph(self, values):
        CommonHelpers.draw_colored_rectangle(self.graph_x, self.y,
                                             self.graph_width, self.graph_height + self.graph_y - self.x,
                                             0, 0, 0)
        space = self.graph_width / (len(values) + 1)
        point_scale = self.graph_height / Settings.max_score
        i = 0
        for v in values:
            self.point.x = self.graph_x + i * space + space
            self.point.y = self.graph_y + v * point_scale
            self.point.draw()
            i += 1
        pyglet.gl.glFlush()

    def draw_graph_skeleton(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_LINES,
                             ("v2f", (self.graph_x, self.graph_y,
                                      self.graph_x, self.graph_y + self.graph_height,
                                      self.graph_x, self.graph_y,
                                      self.graph_x + self.graph_width, self.graph_y)),
                             ("c3B", ((56, 88, 129) * 4)))
        space_between = self.graph_height / (Settings.num_graph_labels - 1)
        difference = Settings.max_score / (Settings.num_graph_labels - 1)
        for i in range(Settings.num_graph_labels):
            pyglet.text.Label(text=f"{round(i * difference)}",
                              x=self.x, y=self.graph_y + i * space_between,
                              anchor_x="center", anchor_y="center",
                              font_size=10).draw()

    def load_point(self):
        point_image = pyglet.resource.image("SimpleUI/point.png")
        CommonHelpers.scale_image(point_image, 10, 10)
        CommonHelpers.center_image(point_image)
        return pyglet.sprite.Sprite(img=point_image)
