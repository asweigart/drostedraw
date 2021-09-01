"""Droste Draw
By Al Sweigart al@inventwithpython.com

A Python module for making recursive drawings (aka Droste effect) with the built-in turtle module."""

__version__ = '0.2.1'


import turtle, math

MAX_FUNCTION_CALLS = 10000
MAX_ITERATION = 400
MIN_SIZE = 1

# NOTE: In general, don't use absolute coordinate functions (like turtle.goto(), turtle.xcor(), turtle.ycor(),
# turtle.setheading()) in your draw functions because they might not work when the heading angle is not 0.

def drawSquare(size, extraData=None):
    size = int(size)  # Reduce rounding errors by converting this to an int.

    # Move to the top-right corner before drawing:
    turtle.penup()
    turtle.forward(size // 2)
    turtle.left(90)
    turtle.forward(size // 2)
    turtle.left(180)
    turtle.pendown()

    # Draw a square:
    for i in range(4):
        turtle.forward(size)
        turtle.right(90)


def drawTriangle(size, extraData=None):
    # Move the turtle into position at the top of the equilateral triangle:
    height = (size * math.sqrt(3)) / 2
    turtle.penup()
    turtle.left(90)
    turtle.forward(height * (2/3))
    turtle.right(150)
    turtle.pendown()

    # Draw the triangle:
    turtle.forward(size)
    turtle.right(120)
    turtle.forward(size)
    turtle.right(120)
    turtle.forward(size)
    turtle.right(120)



def drawFilledSquare(size, extraData=None):
    # Move to the top-right corner before drawing:
    turtle.penup()
    turtle.forward(size // 2)
    turtle.left(90)
    turtle.forward(size // 2)
    turtle.left(180)
    turtle.pendown()

    # The extra data is a tuple of (fillcolor, pencolor) values:
    if extraData is not None:
        iteration = extraData['_iteration'] - 1  # -1 because iteration starts at 1, not 0.
        turtle.fillcolor(extraData['colors'][iteration % len(extraData['colors'])])
        turtle.pencolor(extraData['colors'][iteration % len(extraData['colors'])])

    # Draw a square:
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(size)
        turtle.right(90)
    turtle.end_fill()


def drawFilledDiamond(size, extraData=None):
    # Move to the right corner before drawing:
    turtle.penup()
    turtle.forward(math.sqrt(size ** 2 / 2))
    turtle.right(135)
    turtle.pendown()

    # The extra data is a tuple of (fillcolor, pencolor) values:
    if extraData is not None:
        iteration = extraData['_iteration'] - 1  # -1 because iteration starts at 1, not 0.
        turtle.fillcolor(extraData['colors'][iteration % len(extraData['colors'])])
        turtle.pencolor(extraData['colors'][iteration % len(extraData['colors'])])

    # Draw a square:
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(size)
        turtle.right(90)
    turtle.end_fill()


def drosteDraw(drawFunction, size, changes, extraData=None):
    # NOTE: The heading of the turtle is considered to be the rightward direction.

    # Provide default values for extraData if they weren't provided by the caller:
    if extraData is None:
        extraData = {}
    if '_iteration' not in extraData:
        extraData['_iteration'] = 1
    if 'maxIteration' not in extraData:
        extraData['maxIteration'] = MAX_ITERATION
    if 'maxFunctionCalls' not in extraData:
        extraData['maxFunctionCalls'] = MAX_FUNCTION_CALLS
    if 'minSize' not in extraData:
        extraData['minSize'] = MIN_SIZE

    if extraData['_iteration'] > extraData['maxIteration'] or \
       len(changes) ** extraData['_iteration'] > extraData['maxFunctionCalls'] or \
       size < extraData['minSize']:
        return  # BASE CASE

    # Remember the original starting coordinates and heading.
    origX = turtle.xcor()
    origY = turtle.ycor()
    origHeading = turtle.heading()

    turtle.pendown()
    drawFunction(size, extraData)
    turtle.penup()

    # RECURSIVE CASE
    for i in range(len(changes)):
        # Provide default values for the dictionaries in `changes`:
        if 'x' not in changes[i]:
            changes[i]['x'] = 0
        if 'y' not in changes[i]:
            changes[i]['y'] = 0
        if 'size' not in changes[i]:
            changes[i]['size'] = 1.0
        if 'angle' not in changes[i]:
            changes[i]['angle'] = 0

        #turtle.goto(origX + (size * changes[i]['x']), origY + (size * changes[i]['y']))
        turtle.goto(origX, origY)
        turtle.setheading(origHeading + changes[i]['angle'])
        turtle.forward(size * changes[i]['x'])
        turtle.left(90)
        turtle.forward(size * changes[i]['y'])
        turtle.right(90)
        extraData['_iteration'] += 1
        drosteDraw(drawFunction, int(size * changes[i]['size']), changes, extraData)
        extraData['_iteration'] -= 1

    # At the end of the first recursive call to drosteDraw(), call
    # update() to display any buffered drawings on the screen:
    if extraData['_iteration'] == 1:
        turtle.update()

_DEMO_NUM = 0
def demo(x=None, y=None):
    global _DEMO_NUM
    turtle.reset()
    turtle.tracer(20000, 0) # Increase the first argument to speed up the drawing.
    turtle.hideturtle()


    if _DEMO_NUM == 0:
        # Recursively draw smaller squares in the center:
        drosteDraw(drawSquare, 350, [{'size': 0.8}])
    elif _DEMO_NUM == 1:
        # Recursively draw smaller squares going off to the right:
        drosteDraw(drawSquare, 350, [{'size': 0.8, 'x': 0.20}])
    elif _DEMO_NUM == 2:
        # Recursively draw smaller squares that go up at an angle:
        drosteDraw(drawSquare, 350, [{'size': 0.8, 'y': 0.20, 'angle': 15}])
    elif _DEMO_NUM == 3:
        # Recursively draw smaller triangle in the center:
        drosteDraw(drawTriangle, 350, [{'size': 0.8}])
    elif _DEMO_NUM == 4:
        # Recursively draw smaller triangle going off to the right:
        drosteDraw(drawTriangle, 350, [{'size': 0.8, 'x': 0.20}])
    elif _DEMO_NUM == 5:
        # Recursively draw smaller triangle that go up at an angle:
        drosteDraw(drawTriangle, 350, [{'size': 0.8, 'y': 0.20, 'angle': 15}])
    elif _DEMO_NUM == 6:
        # Recursively draw a spirograph of squares:
        drosteDraw(drawSquare, 150, [{'angle': 10, 'x': 0.1}])
    elif _DEMO_NUM == 7:
        # Recursively draw a smaller square in each of the four corners of the parent square:
        drosteDraw(drawSquare, 350, [{'size': 0.5, 'x': -0.5, 'y': 0.5},
                                     {'size': 0.5, 'x': 0.5, 'y': 0.5},
                                     {'size': 0.5, 'x': -0.5, 'y': -0.5},
                                     {'size': 0.5, 'x': 0.5, 'y': -0.5}])
    elif _DEMO_NUM == 8:
        # Recursively draw smaller filled squares in the center, alternating red and black:
        drosteDraw(drawFilledSquare, 350, [{'size': 0.8}], {'colors': ['red', 'black']})
    elif _DEMO_NUM == 9:
        # Recursively draw a smaller filled square in each of the four corners of the parent square with red and black:
        drosteDraw(drawFilledSquare, 350, [{'size': 0.5, 'x': -0.5, 'y': 0.5},
                                           {'size': 0.5, 'x': 0.5, 'y': 0.5},
                                           {'size': 0.5, 'x': -0.5, 'y': -0.5},
                                           {'size': 0.5, 'x': 0.5, 'y': -0.5}], {'colors': ['red', 'black']})
    elif _DEMO_NUM == 10:
        # Recursively draw a smaller filled square in each of the four corners of the parent square with white and black:
        drosteDraw(drawFilledSquare, 350, [{'size': 0.5, 'x': -0.5, 'y': 0.5},
                                           {'size': 0.5, 'x': 0.5, 'y': 0.5},
                                           {'size': 0.5, 'x': -0.5, 'y': -0.5},
                                           {'size': 0.5, 'x': 0.5, 'y': -0.5}], {'colors': ['white', 'black']})
    elif _DEMO_NUM == 11:
        # Recursively draw a smaller filled square in each of the four corners of the parent square:
        drosteDraw(drawFilledDiamond, 350, [{'size': 0.5, 'x': -0.45, 'y': 0.45},
                                            {'size': 0.5, 'x': 0.45, 'y': 0.45},
                                            {'size': 0.5, 'x': -0.45, 'y': -0.45},
                                            {'size': 0.5, 'x': 0.45, 'y': -0.45}], {'colors': ['green', 'yellow']})
    elif _DEMO_NUM == 12:
        # Draw the sierpinsky triangle:
        drosteDraw(drawTriangle, 600, [{'size': 0.5, 'x': 0, 'y': math.sqrt(3) / 6, 'angle': 0},
                                       {'size': 0.5, 'x': 0, 'y': math.sqrt(3) / 6, 'angle': 120},
                                       {'size': 0.5, 'x': 0, 'y': math.sqrt(3) / 6, 'angle': 240}])
    elif _DEMO_NUM == 13:
        # Draw a recursive "glider" shape from Conway's Game of Life:
        drosteDraw(drawSquare, 600, [{'size': 0.333, 'x': 0, 'y': 0.333},
                                     {'size': 0.333, 'x': 0.333, 'y': 0},
                                     {'size': 0.333, 'x': 0.333, 'y': -0.333},
                                     {'size': 0.333, 'x': 0, 'y': -0.333},
                                     {'size': 0.333, 'x': -0.333, 'y': -0.333}])

        turtle.exitonclick()
    _DEMO_NUM += 1


def main():
    # Start the demo:
    turtle.onscreenclick(demo)
    demo()
    turtle.mainloop()


if __name__ == '__main__':
    main()

