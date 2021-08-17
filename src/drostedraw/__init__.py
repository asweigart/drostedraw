"""Droste Draw
By Al Sweigart al@inventwithpython.com

A Python module for making recursive drawings (aka Droste effect) with the built-in turtle module."""

__version__ = '0.1.0'


import turtle, random, time

MAX_ITERATION = 8

turtle.tracer(10000, 0) # Increase the first argument to speed up the drawing.
turtle.hideturtle()


# NOTE: In general, don't use absolute coordinate functions (like turtle.goto(), turtle.xcor(), turtle.ycor(),
# turtle.setheading()) in your draw functions.
def drawSquare(size, iteration):
    size = int(size)  # Reduce rounding errors by converting this to an int.

    # Remember the original starting coordinates:
    origX = turtle.xcor()
    origY = turtle.ycor()

    # Move to the top-right corner before drawing:
    turtle.penup()
    #turtle.goto(turtle.xcor() - (size // 2), turtle.ycor() + (size // 2))
    turtle.forward(size // 2)
    turtle.left(90)
    turtle.forward(size // 2)
    turtle.left(180)
    turtle.pendown()

    # Alternate between two colors:
    if iteration % 2 == 0:
        turtle.fillcolor(0.58, 0.77, 0.02)  # A nice green color.
        turtle.pencolor(0.58, 0.77, 0.02)  # Comment this line out for black outline.
    else:
        turtle.fillcolor(0.98, 0.91, 0.0)  # A nice yellow color.
        turtle.pencolor(0.98, 0.91, 0.0)  # Comment this line out for black outline.

    # Draw a square:
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(size)
        turtle.right(90)
    turtle.end_fill()

    # Move back to the starting coordinates:
    turtle.penup()
    turtle.goto(origX, origY)
    turtle.pendown()

    #time.sleep(0.01)
    #turtle.update()

def drosteDraw(drawFunction, size, changeSize, changeX, changeY, changeAngle, maxIteration=MAX_ITERATION, iteration=0):
    #print('drosteDraw(): size =', size, 'and iteration =', iteration, ')')

    if iteration > maxIteration or size < 1:
        return  # BASE CASE

    # Convert the change arguments to lists if they aren't in lists already:
    if not isinstance(changeSize, list):
        changeSize = [changeSize]
    if not isinstance(changeX, list):
        changeX = [changeX]
    if not isinstance(changeY, list):
        changeY = [changeY]
    if not isinstance(changeAngle, list):
        changeAngle = [changeAngle]
    assert len(changeSize) == len(changeX) == len(changeY) == len(changeAngle)
    for i in range(len(changeSize)):
        assert changeSize[i] >= 0.0

    # Remember the original starting coordinates and heading.
    origX = turtle.xcor()
    origY = turtle.ycor()
    origHeading = turtle.heading()

    turtle.pendown()
    drawFunction(size, iteration)
    turtle.penup()

    # RECURSIVE CASE
    for i in range(len(changeSize)):
        turtle.goto(origX + (size * changeX[i]), origY + (size * changeY[i]))
        turtle.setheading(origHeading + changeAngle[i])
        drosteDraw(drawFunction, size * changeSize[i], changeSize, changeX, changeY, changeAngle, maxIteration, iteration + 1)


def randomDrosteDraw(drawFunction):
    startSize = random.randint(50, 100)
    changeSize = random.randint(-50, 50)
    changeX = random.randint(-100, 100)
    changeY = random.randint(-100, 100)
    changeAngle = random.randint(-30, 30)
    print('Called drosteDraw(FUNC,', startSize, ',', changeSize, ',', changeX, ',', changeY, ',', changeAngle, ')')

    drosteDraw(drawFunction, startSize, changeSize, changeX, changeY, changeAngle)
    turtle.update()

#turtle.penup()
#turtle.goto(0,-200)

#drosteDraw(drawSquare, 600 , [0.8] , [0] , [0] , [-10])
#drosteDraw(drawSquare, 600 , [0.8, 0.5] , [0,0] , [0,0] , [-10, 15])

#while True:
#    turtle.reset()
#    randomDrosteDraw(drawSquare)
#    time.sleep(1)

def main():
    drosteDraw(drawSquare, 350, [0.5, 0.5, 0.5, 0.5], [-0.5, 0.5, -0.5, 0.5], [0.5, 0.5, -0.5, -0.5], [0,0,0,0], 6) # Try this with both colors as black.
    turtle.exitonclick()


if __name__ == '__main__':
    main()

