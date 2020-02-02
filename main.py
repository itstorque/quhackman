"""
    Qu[H]ackMan main python file for game logic, a Quantum PackMan game made for MIT/iQuHack.
"""
import time
from random import choice
from turtle import *
from freegames import floor, vector
import simulate

# Do you want to reveal states after collapse?
revealState = None
while revealState != "y" and revealState != "n":
    revealState = input("Do you want to reveal states after collapse? [y/n] >   ")

# Number of computer players
artificialGhostCount = None
while artificialGhostCount == None:
    try:
        temp = int(input("How many AI ghosts do you want? [Max 8] >   "))
        if temp < 9: artificialGhostCount = temp
    except: pass


past_input_a = None
past_input_b = None
HARDCODE_BOTH = False

player1 = 'player.gif'
register_shape(player1)
player2 = 'turtle'
pacman_mult = 1
pacman2_mult = 1

tgate = 'gateT.gif'
sgate = 'gateS.gif'
zgate = 'gateZ.gif'
measure = 'measure.gif'
register_shape(tgate)
register_shape(sgate)
register_shape(zgate)
register_shape(measure)

winstate = 'win_state.gif'
losestate = 'lose_state.gif'
register_shape(winstate)
register_shape(losestate)

screensize(800, 600)
setworldcoordinates(-190, -170, 150, 170)

simulation = simulate.QuantumSimulation()

resizemode('auto')

state = {'score_a': 0, 'score_b': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)

aim = vector(5, 0)
aim2 = vector(-5, 0)

top = [vector(-40,170),vector(-40,175)]
bottom = [vector(-40,-170),vector(-40,-175),]
right = [vector(110,0),vector(115,0)]
left = [vector(-190,0),vector(-195,0)]

pacman = vector(-40, -80)
pacman2 = vector(-80, -80)

ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
    [vector(-180, 160), vector(0, -5)],
    [vector(-180, -160), vector(5, 0)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(0, 5)],
][:artificialGhostCount-1]

blochFig1 = Turtle()
blochFig2 = Turtle()

if artificialGhostCount == 0: ghosts = []
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 6, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
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
    path.color('white')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 4:
                path.up()
                path.goto(x + 10, y + 10)
                path.shape(tgate)
                path.resizemode('auto')
                path.turtlesize(1)
                path.stamp()

            elif tile == 5:
                path.up()
                path.goto(x + 10, y + 10)
                path.shape(sgate)
                path.resizemode('auto')
                path.turtlesize(1)
                path.stamp()

            elif tile == 6:
                path.up()
                path.goto(x + 10, y + 10)
                path.shape(zgate)
                path.resizemode('auto')
                path.turtlesize(1)
                path.stamp()

            elif tile == 7:
                path.up()
                path.goto(x + 10, y + 10)
                path.shape(measure)
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

def bloch1():
    blochFig1.clear()
    blochFig1.reset()

    blochFig1.penup()
    # blochFig1.color("white")
    # blochFig1.goto(210,80)
    # blochFig1.write("⎪ win 〉", font=("Arial", 16, "normal"))
    # blochFig1.goto(210,-90)
    # blochFig1.write("⎪ lose 〉", font=("Arial", 16, "normal"))
    blochFig1.goto(235,80)
    blochFig1.shape(winstate)
    blochFig1.stamp()

    blochFig1.goto(235,-85)
    blochFig1.shape(losestate)
    blochFig1.stamp()

    blochFig1.goto(235,-70)
    blochFig1.shape("arrow")
    blochFig1.pendown()
    blochFig1.color("blue")
    blochFig1.circle(70, steps=50)

    blochFig1.color("red")

    blochFig1.penup()
    blochFig1.goto(235,0)
    # blochFig1.setheading(90) # Point to the top - towards 0 state
    blochFig1.setheading(0)
    blochFig1.right(-state["score_a"]*360/72)
    blochFig1.pendown()
    blochFig1.forward(60)

    blochFig1.getscreen().update()

def bloch2():
    blochFig2.clear()
    blochFig2.reset()

    blochFig2.penup()
    # blochFig2.color("white")
    # blochFig2.goto(-300,80)
    # blochFig2.write("⎪ win 〉", font=("Arial", 16, "normal"))
    # blochFig2.goto(-300,-90)
    # blochFig2.write("⎪ lose 〉", font=("Arial", 16, "normal"))
    blochFig2.goto(-290, 80)
    blochFig2.shape(winstate)
    blochFig2.stamp()

    blochFig2.goto(-290,-85)
    blochFig2.shape(losestate)
    blochFig2.stamp()

    blochFig2.shape("arrow")
    blochFig2.goto(-290,-70)
    blochFig2.pendown()
    blochFig2.color("blue")
    blochFig2.circle(70, steps=50)

    blochFig2.color("red")

    blochFig2.penup()
    blochFig2.goto(-290,0)
    # blochFig2.setheading(90) # Point to the top - towards 0 state
    blochFig2.setheading(0)
    blochFig2.right(-state["score_b"]*360/72)
    blochFig2.pendown()
    blochFig2.forward(60)

    blochFig2.getscreen().update()

def move():
    "Move pacman and all ghosts."
    global past_input_a
    global past_input_b
    
    global pacman_mult
    global pacman2_mult
    
    print('mults',pacman_mult,pacman2_mult)
    writer.undo()
    writer.write(str(state['score_a']) + " | " + str(state['score_b']))
    end_time = time.time()
    time_length = end_time - start_time
#    print(time_length)
    clear()

    if valid(pacman + aim):
        if(pacman in top and aim == vector(0,5)):
            pacman.move(bottom[1]-top[1])
        elif(pacman in bottom and aim == vector(0,-5)):
            pacman.move(top[1]-bottom[1])
        elif(pacman in left and aim == vector(-5,0)):
            pacman.move(right[1]-left[1])
        elif(pacman in right and aim == vector(5,0)):
            pacman.move(left[1]-right[1])
        else:
            pacman.move(pacman_mult*aim)

    if valid(pacman2 + aim2):
        if(pacman2 in top and aim2 == vector(0,5)):
            pacman2.move(bottom[1]-top[1])
        elif(pacman2 in bottom and aim2 == vector(0,-5)):
            pacman2.move(top[1]-bottom[1])
        elif(pacman2 in left and aim2 == vector(-5,0)):
            pacman2.move(right[1]-left[1])
        elif(pacman2 in right and aim2 == vector(5,0)):
            pacman2.move(left[1]-right[1])
        else:
            pacman2.move(pacman2_mult*aim2)

    if past_input_a != None:
        change(*past_input_a, "a", save=False)

    if past_input_b != None:
        change(*past_input_b, "b", save=False)

    index = offset(pacman)
    index2 = offset(pacman2)
    
    if(pacman_mult != 1 or pacman2_mult != 1):
        check_collision(index, {1: lambda: inc_score('a'),
                                4: lambda: simulation.add_gate(1, "t"),
                                5: lambda: simulation.add_gate(1, "s"),
                                6: lambda: simulation.add_gate(1, "z")})

        check_collision(index2, {1: lambda: inc_score('b'),
                                 4: lambda: simulation.add_gate(2, "t"),
                                 5: lambda: simulation.add_gate(2, "s"),
                                 6: lambda: simulation.add_gate(2, "z")})
    else:
        check_collision(index, {4: lambda: simulation.add_gate(1, "t"),
                                5: lambda: simulation.add_gate(1, "s"),
                                6: lambda: simulation.add_gate(1, "z")})

        check_collision(index2, {4: lambda: simulation.add_gate(2, "t"),
                                 5: lambda: simulation.add_gate(2, "s"),
                                 6: lambda: simulation.add_gate(2, "z")})    

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
            if(point == top and course == vector(0,5)):
                point.move(bottom-top)
            elif(point == bottom and course == vector(0,-5)):
                point.move(top-bottom)
            elif(point == left and course == vector(-5,0)):
                point.move(right-left)
            elif(point == right and course == vector(5,0)):
                point.move(left-right)
            else:
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

#    for point, course in ghosts:
#        if abs(pacman - point) < 20:
#            return
#        if abs(pacman2 - point) < 20:
#            return
        
    print(time_length)
    gate_collect_time = 5.
        
    if time_length > gate_collect_time and time_length < gate_collect_time + .2:
        
        simulation.run()
        output_sim = simulation.output
#        print(output_sim['00'])
        if output_sim.get('00',0) == 1:
            pacman_mult = 1.
            pacman2_mult = 2.
            
        if output_sim.get('11',0) == 1:
            pacman_mult = 2.
            pacman2_mult = 1.
            
        for index in range(len(tiles)):
            tile = tiles[index]
            if tile > 0:
                x = (index % 20) * 20 - 200
                y = 180 - (index // 20) * 20
                square(x, y)
                if tile == 1:
                    path.up()
                    path.goto(x + 10, y + 10)
                    path.dot(5, 'purple')

    bloch1()
    bloch2()

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
start_time = time.time()
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(str(state['score_a']) + " | " + str(state['score_b']), font=("Arial", 16, "normal"))
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
