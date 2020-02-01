"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.

"""

from random import choice
from turtle import *
from freegames import floor, vector
import simulate

past_input_a = None
past_input_b = None
HARDCODE_BOTH = False
# shape("turtle")
player1 = 'player.gif'
tgate = 'gateT.gif'
sgate = 'gateS.gif'
register_shape(player1)
register_shape(tgate)
register_shape(sgate)
player2 = 'turtle'

simulation = simulate.quantum_simulation()

resizemode('auto')

state = {'score_a': 0, 'score_b': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
aim2 = vector(5, 0)
pacman = vector(-40, -80)
pacman2 = vector(-80, -80)
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0,
    0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 4, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 5, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

def square(x, y, gate=""):
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

def offset(point):
    "Return offset of point in tiles."
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

def valid(point):
    "Return True if point is valid in tiles."
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 < 5 or point.y % 20 < 5

def world():
    "Draw world using path."
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')

            if tile == 4:
                path.up()
                path.goto(x + 10, y + 10)
                path.shape(tgate)
                path.resizemode('auto')
                path.turtlesize(1)
                path.stamp()

            if tile == 5:
                path.up()
                path.goto(x + 10, y + 10)
                path.shape(sgate)
                path.resizemode('auto')
                path.turtlesize(1)
                path.stamp()

def check_collision(playerIndex, perform):
    # perform is a dictionary of function

    for key in perform.keys():
        if tiles[playerIndex] == key:
            tiles[playerIndex] = 2
            perform[key]()
            x = (playerIndex % 20) * 20 - 200
            y = 180 - (playerIndex // 20) * 20
            square(x, y)

def inc_score(player):
    state['score_' + player.lower()] += 1

def move():
    "Move pacman and all ghosts."

    global past_input_a
    global past_input_b

    writer.undo()
    writer.write(str(state['score_a']) + " | " + str(state['score_b']))

    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    if valid(pacman2 + aim2):
        pacman2.move(aim2)

    if past_input_a != None:
        change(*past_input_a, "a", save=False)

    if past_input_b != None:
        change(*past_input_b, "b", save=False)

    index = offset(pacman)
    index2 = offset(pacman2)

    check_collision(index, {1: lambda: inc_score('a'),
                            4: lambda: simulation.add_gate(1, "t"),
                            5: lambda: simulation.add_gate(1, "s")})

    check_collision(index2, {1: lambda: inc_score('b'),
                             4: lambda: simulation.add_gate(2, "t"),
                             5: lambda: simulation.add_gate(2, "s")})

    up()
    goto(pacman.x + 10, pacman.y + 10)
    shape(player1)
    resizemode('auto')
    penup()
    turtlesize(0.1)
    color('green')
    stamp()

    up()
    goto(pacman2.x + 10, pacman2.y + 10)
    shape(player2)
    resizemode('auto')
    penup()
    turtlesize(1)
    color('green')
    stamp()

    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return
        if abs(pacman2 - point) < 20:
            return

    ontimer(move, 100)

def change(x, y, both=True, save=True):
    "Change pacman aim if valid."

    global past_input_a
    global past_input_b

    a, b = both==True or both=="a" or HARDCODE_BOTH, both==True or both=="b" or HARDCODE_BOTH

    if save and a: past_input_a = (x, y)
    if save and b: past_input_b = (x, y)

    if valid(pacman + vector(x, y)) and a:
        aim.x = x
        aim.y = y
        past_input_a = None
    if valid(pacman2 + vector(x, y)) and b:
        aim2.x = x
        aim2.y = y
        past_input_b = None

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(str(state['score_a']) + " | " + str(state['score_b']))
listen()
onkey(lambda: change(5, 0, "a"), 'Right')
onkey(lambda: change(-5, 0, "a"), 'Left')
onkey(lambda: change(0, 5, "a"), 'Up')
onkey(lambda: change(0, -5, "a"), 'Down')
onkey(lambda: change(5, 0, "b"), 'd')
onkey(lambda: change(-5, 0, "b"), 'a')
onkey(lambda: change(0, 5, "b"), 'w')
onkey(lambda: change(0, -5, "b"), 's')
world()
move()
done()
