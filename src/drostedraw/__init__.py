"""Droste Draw
By Al Sweigart al@inventwithpython.com

A Python module for making recursive drawings (aka Droste effect) with the built-in turtle module."""

__version__ = '0.1.0'


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


def drawTriangleOutline(size, extraData=None):
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


def drosteDraw(drawFunction, size, changes, extraData=None):
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
    turtle.update()

_DEMO_NUM = 0
def demo(x=None, y=None):
    global _DEMO_NUM
    turtle.reset()
    turtle.tracer(20000, 0) # Increase the first argument to speed up the drawing.
    turtle.hideturtle()

    if _DEMO_NUM == 0:
        drosteDraw(drawSquare, 350, [{'size': 0.8}])
    elif _DEMO_NUM == 1:
        drosteDraw(drawSquare, 350, [{'size': 0.8, 'x': 0.20}])
    elif _DEMO_NUM == 2:
        drosteDraw(drawSquare, 350, [{'size': 0.5, 'x': -0.5, 'y': 0.5},
                                     {'size': 0.5, 'x': 0.5, 'y': 0.5},
                                     {'size': 0.5, 'x': -0.5, 'y': -0.5},
                                     {'size': 0.5, 'x': 0.5, 'y': -0.5}])


        turtle.exitonclick()

    _DEMO_NUM += 1


def main():


    turtle.onscreenclick(demo)
    demo()
    turtle.mainloop()
    #drosteDraw(drawTriangleOutline, 350, [{'size': 0.8, 'y': 0.20, 'angle': 10}])
    #drosteDraw(drawFilledSquare, 350, [{'size': 0.8, 'y': 0.20, 'angle': 10}], extraData={'colors': ['red', 'black'], 'maxIteration': 20})

    #drosteDraw(drawSquare, 350, [0.5, 0.5, 0.5, 0.5], [-0.5, 0.5, -0.5, 0.5], [0.5, 0.5, -0.5, -0.5], [0,0,0,0], 6,
    #    extraData=(((0.58, 0.77, 0.02), (0.58, 0.77, 0.02)), ((0.98, 0.91, 0.0), (0.98, 0.91, 0.0))))  # TODO Try this with both colors as black.
    #drosteDraw(drawFilledSquare, 350, [0.5, 0.5, 0.5, 0.5], [-0.5, 0.5, -0.5, 0.5], [0.5, 0.5, -0.5, -0.5], [45, 45, 45, 45], 4)
    #drosteDraw(drawFilledSquare, 350, [0.5, 0.5, 0.5, 0.5], [-0.5, 0.5, -0.5, 0.5], [0.5, 0.5, -0.5, -0.5], [30, 30, 30, 30], 5)



if __name__ == '__main__':
    main()

