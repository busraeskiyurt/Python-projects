import turtle
t=turtle.Turtle()
f=turtle.Screen()
f.setup(750,500)
t.shape("turtle")
turtle.bgcolor("red")
t.color("white")
t.speed(7)
t.penup()
t.goto(-113,-125)

t.begin_fill()
t.circle(130)
t.end_fill()
t.penup()

t.goto(-76,-94)
t.begin_fill()
t.color("red")
t.circle(100)
t.end_fill()
t.penup()

t.goto(7,0)
t.color("white")

t.right(15)
t.begin_fill()
for i in range (5):
    t.forward(150)
    t.left(144)
t.end_fill()
t.penup()
t.left(151)
t.hideturtle()


# 
# t.penup()
# t.goto(50, 165)
# t.pendown()
# t.penup()
# t.goto(35, 165)

# t.goto(190, 125)
# t.penup()
# t.color("red")
# t.right(30)
# t.forward(50)
# 
# t.pendown()
# t.goto(190, 80)
# t.begin_fill()
# t.speed(7)
# t.circle(100)
# t.end_fill()
# 

