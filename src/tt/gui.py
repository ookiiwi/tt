import imgui 
from imgui.integrations.pyglet import create_renderer
import tt

GUI_SUBDIVISION=0x1
GUI_NGON=0x2
GUI_RADIUS=0x6
GUI_SHAPE=0x8
GUI_FACTOR=0x10

def selectableButton(isSelected, *args):
    if (isSelected):
            imgui.push_style_color(0, 0.0, 0.0, 0.0)
            imgui.push_style_color(21, 255.0, 255.0, 255.0)
    if (imgui.button(*args) and not isSelected):
        return True
    elif (isSelected):
        imgui.pop_style_color()
        imgui.pop_style_color()

class GUI():
    def __init__(self, window, onChange, shape=tt.Circle(), factor=2):
        assert(onChange is not None)
        
        imgui.create_context()

        self.window = window
        self.impl = create_renderer(window)
        self.shape = shape
        self.factor = factor
        self.onChange = onChange

    def update(self):
        def isCircle():
            return type(self.shape) is tt.Circle
        
        def isRegularPolygon():
            return type(self.shape) is tt.RegularPolygon

        self.impl.process_inputs()
        imgui.new_frame()

        imgui.begin("Options")

        imgui.text("Shape: ")
        imgui.same_line()
        imgui.begin_group()

        if (selectableButton(isCircle(), "Circle")):
            self.shape = tt.Circle()
            self.onChange(self.shape, GUI_SHAPE)

        imgui.same_line()

        if (selectableButton(isRegularPolygon(), "Regular polygon")):
            self.shape = tt.RegularPolygon()
            self.onChange(self.shape, GUI_SHAPE)

        # TODO: uncomment when ellipsis implemented
        # if (selectableButton(isEllipsis(), "Ellipsis")):
        #     pass
        
        imgui.end_group()

        rvFactor, self.factor = imgui.slider_int("Factor", self.factor, 2, 10)
        if (rvFactor):
            self.onChange(self.factor, GUI_FACTOR)

        if (isRegularPolygon()):
            rv, self.shape.n_gon = imgui.slider_int("n-gon", self.shape.n_gon, 3, 10)
            if (rv):
                self.onChange(self.shape, GUI_NGON)

        rvSub, self.shape.subdivision = imgui.slider_int("Subdivision", self.shape.subdivision, 0, 100)
        if (rvSub):
            self.onChange(self.shape, GUI_SUBDIVISION)

        imgui.end()

    def render(self):
        imgui.render()
        self.impl.render(imgui.get_draw_data())

    def destroy(self):
        self.impl.shutdown()