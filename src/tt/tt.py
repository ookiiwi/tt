from .core import *
from .gui import *
import pyglet

factor = 2

pyglet.gl.glEnable(pyglet.gl.GL_LINE_SMOOTH)
pyglet.gl.glHint(pyglet.gl.GL_LINE_SMOOTH_HINT, pyglet.gl.GL_NICEST)

window = pyglet.window.Window(caption='TT')
batch = pyglet.graphics.Batch()

shape = RegularPolygon(3, 200, subdivision=60, batch=batch)
shape.drawShape(window, batch)
shape.linkPoints(window, factor, batch)

def onShapeChange(value, flag):
    global shape
    global factor

    if ((flag & GUI_FACTOR) != 0):
        assert(type(value) is int)
        factor = value

    # Everything needs to be rebuilt
    elif ((flag & (GUI_SHAPE | GUI_NGON | GUI_RADIUS)) != 0):
        if ((flag & (GUI_SHAPE | GUI_NGON)) != 0):
            shape.delete()

            if ((flag & (GUI_SHAPE)) != 0):
                shape = value

        shape.drawShape(window, batch)

    shape.linkPoints(window, factor, batch)

gui = GUI(window, onShapeChange, shape, factor)

@window.event
def on_draw():
    gui.update()
    
    window.clear()
    batch.draw()
    gui.render()

def main():
    pyglet.app.run()
    gui.destroy()