"""Droste Draw
By Al Sweigart al@inventwithpython.com

A Python module for making recursive drawings (aka Droste effect) with the built-in turtle module."""

__version__ = '0.2.1'


import turtle, math

MAX_FUNCTION_CALLS = 10000  # Stop recursion after this many function calls.
MAX_ITERATION = 400  # Stop recursion after this iteration.
MIN_SIZE = 1  # Stop recursion if size is less than this.

# NOTE: In general, don't use absolute coordinate functions (like turtle.goto(), turtle.xcor(), turtle.ycor(),
# turtle.setheading()) in your draw functions because they might not work when the heading angle is not 0.

def drawSquare(size, extraData=None):
    """Draw a square where `size` is the length of each side."""

    # Move the turtle to the top-right corner before drawing:
    turtle.penup()
    turtle.forward(size // 2)  # Move to the right edge.
    turtle.left(90)  # Turn to face upwards.
    turtle.forward(size // 2)  # Move to the top-right corner.
    turtle.left(180)  # Turn around to face downwards.
    turtle.pendown()

    # Draw the four sides of a square:
    for i in range(4):
        turtle.forward(size)
        turtle.right(90)


def drawTriangle(size, extraData=None):
    """Draw an equilateral triangle where `size` is the length of
    each side."""

    # Move the turtle to the top of the equilateral triangle:
    height = (size * math.sqrt(3)) / 2
    turtle.penup()
    turtle.left(90)  # Turn to face upwards.
    turtle.forward(height * (2/3))  # Move to the top corner.
    turtle.right(150)  # Turn to face the bottom-right corner.
    turtle.pendown()

    # Draw the three sides of the triangle:
    for i in range(3):
        turtle.forward(size)
        turtle.right(120)


def drawFilledSquare(size, extraData=None):
    """Draw a solid, filled-in square where `size` is the length of each
    side. The extraData dictionary can have a key 'colors' whose value
    is a list of "color strings" that the turtle module recognizes, e.g.
    'red', 'black', etc. The first color string in the list is used
    for the first iteration, the second for the second, and so on. When
    you run out of colors for later iterations, the first color is used
    again."""

    # Move the turtle to the top-right corner before drawing:
    turtle.penup()
    turtle.forward(size // 2)  # Move to the right edge.
    turtle.left(90)  # Turn to face upwards.
    turtle.forward(size // 2)  # Move to the top-right corner.
    turtle.left(180)  # Turn around to face downwards.
    turtle.pendown()

    # The extra data is a tuple of (fillcolor, pencolor) values:
    if extraData is not None:
        iteration = extraData['_iteration'] - 1  # -1 because iteration starts at 1, not 0.
        turtle.fillcolor(extraData['colors'][iteration % len(extraData['colors'])])
        turtle.pencolor(extraData['colors'][iteration % len(extraData['colors'])])

    # Draw the four sides of a square:
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


def drosteDraw(drawFunction, size, recursiveDrawings, extraData=None):
    # NOTE: The current heading of the turtle is considered to be the
    # rightward or positive-x direction.

    # Provide default values for extraData:
    if extraData is None:
        extraData = {}
    if '_iteration' not in extraData:
        extraData['_iteration'] = 1  # The first iteration is 1, not 0.
    if '_maxIteration' not in extraData:
        extraData['_maxIteration'] = MAX_ITERATION
    if '_maxFunctionCalls' not in extraData:
        extraData['_maxFunctionCalls'] = MAX_FUNCTION_CALLS
    if '_minSize' not in extraData:
        extraData['_minSize'] = MIN_SIZE

    requiredNumCalls = len(recursiveDrawings) ** extraData['_iteration']
    if extraData['_iteration'] > extraData['_maxIteration'] or \
       requiredNumCalls > extraData['_maxFunctionCalls'] or \
       size < extraData['_minSize']:
        return  # BASE CASE

    # Remember the original starting coordinates and heading.
    origX = turtle.xcor()
    origY = turtle.ycor()
    origHeading = turtle.heading()

    turtle.pendown()
    drawFunction(size, extraData)
    turtle.penup()

    # RECURSIVE CASE
    # Do each of the recursive drawings:
    for i, recursiveDrawing in enumerate(recursiveDrawings):
        # Provide default values for the recursiveDrawing dictionary:
        if 'x' not in recursiveDrawing:
            recursiveDrawing['x'] = 0
        if 'y' not in recursiveDrawing:
            recursiveDrawing['y'] = 0
        if 'size' not in recursiveDrawing:
            recursiveDrawing['size'] = 1.0
        if 'angle' not in recursiveDrawing:
            recursiveDrawing['angle'] = 0

        # Move the turtle into position for the next recursive drawing:
        turtle.goto(origX, origY)
        turtle.setheading(origHeading + recursiveDrawing['angle'])
        turtle.forward(size * recursiveDrawing['x'])
        turtle.left(90)
        turtle.forward(size * recursiveDrawing['y'])
        turtle.right(90)
        # Increment the iteration count for the next level of recursion:
        extraData['_iteration'] += 1
        drosteDraw(drawFunction, int(size * recursiveDrawing['size']), recursiveDrawings, extraData)
        # Decrement the iteration count when done with that recursion:
        extraData['_iteration'] -= 1

    # Display any buffered drawing commands on the screen:
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

