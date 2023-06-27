# Init
import turtle
wn = turtle.Screen()
wn.title("Pong")
wn.bgcolor("black")
wn.setup(width=800,height=600)
wn.tracer(0)

# Score
sa = 0
sb = 0

# Paddle A
pa = turtle.Turtle()
pa.speed(0)
pa.shape("square")
pa.shapesize(stretch_wid=5, stretch_len=1)
pa.color("white")
pa.penup()
pa.goto(-350, 0)

# Paddle B
pb = turtle.Turtle()
pb.speed(0)
pb.shape("square")
pb.shapesize(stretch_wid=5, stretch_len=1)
pb.color("white")
pb.penup()
pb.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.15
ball.dy = 0.15

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0    Player B: 0", align="center", font=("Courier", 24, "normal"))

# Function
def pa_up():
    y = pa.ycor()
    if y < 240:
        y += 20
    pa.sety(y)

def pa_down():
    y = pa.ycor()
    if y > -240:
        y -= 20
    pa.sety(y)

def pb_up():
    y = pb.ycor()
    if y < 240:
        y += 20
    pb.sety(y)

def pb_down():
    y = pb.ycor()
    if y > -240:
        y -= 20
    pb.sety(y)

# Input
wn.listen()
wn.onkeypress(pa_up, "w")
wn.onkeypress(pa_down, "s")
wn.onkeypress(pb_up, "Up")
wn.onkeypress(pb_down, "Down")

# Main
while True:
    wn.update()

    # Move the Ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border Checking
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        sa += 1
    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        sb += 1

    # Paddle and Ball Collisions
    if (ball.xcor() > 330 and ball.xcor() < 350) and (ball.ycor() < pb.ycor() + 50 and ball.ycor() > pb.ycor() - 50):
        ball.dx *= -1
    if (ball.xcor() < -330 and ball.xcor() > -350) and (ball.ycor() < pa.ycor() + 50 and ball.ycor() > pa.ycor() - 50):
        ball.dx *= -1

    # Score
    pen.clear()
    pen.write("Player A: {}    Player B: {}".format(sa, sb), align="center", font=("Courier", 24, "normal"))

