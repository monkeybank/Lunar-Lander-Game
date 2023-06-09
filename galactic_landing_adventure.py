# Galactic Landing Adventure
# This is a program designed to simulate the physics of lading on the moon 
# or some other celestial object.

# Imports the turtle, random, and the program reset modules
import turtle # Original design credit to Wally Feurzig and Seymour Papert https://docs.python.org/3/library/turtle.html
import random # Credit to Guido van Rossum https://docs.python.org/3/library/random.html
import os, sys, subprocess # Credit to Guido van Rossum https://docs.python.org/3/library/os.html, https://docs.python.org/3/library/sys.html, https://docs.python.org/3/library/subprocess.html 

# ---------- Variable definitions ----------

# Creates the screen object
wn = turtle.Screen()
wn.title("Galactic Landing Adventure")

# Register the lunar lander turtle shapes
turtle.register_shape('lander',((25,-25), (40,-50),(45,-50),(45,-52),(30,-52),(30,-50),(35,-50),(20,-30),(10,-30),(15,-40),(-15,-40),(-10,-30),(-20,-30),(-35,-50),(-30,-50),(-30,-52),(-45,-52),(-45,-50),(-40,-50),(-25,-25),(-35,-15),(-35,15),(-25,25),(-29,26),(-32,29),(-32,32),(-29,35),(-26,35),(-23,32),(-23,29),(-25,25),(-15,35),(15,35),(25,25),(35,15),(35,-15)))
turtle.register_shape('flames',((14,-40),(20,-62),(10,-50),(6,-58),(0,-50),(-4,-60),(-6,-50),(-18,-58),(-14,-40)))
turtle.register_shape('meteor',((25,-25),(30,15),(25,25),(5,35),(-25,25),(-30,0),(-25,-25),(-15,-30)))

# Timer configuration
counter_interval = 30 # in milliseconds

# Changes to true if the lander crashes
crashed = False

# Changes to true if the lander lands
landed = False

# Defines how close the lander needs to be to an obstacle to collide
collision_margin = 25

# Defines how upright the lander needs to be to land without crashing
land_orientaion_margin = 30

# Defines the speed the lander can land without crashing
vertical_speed_margin = 2.35
horizontal_speed_margin = 3

# The lander's starting location
starting_location = (-200,300)
lander_start_orientation = 150

# Lander specs
lander_scale = 0.5
lander_color = 'blue'
lander_flame_color = 'red'
engine_thrust = 0
max_engine_thrust = 0.025
start_fuel_level = 100
fuel_level = 0
fuel_level += start_fuel_level
fuel_use_rate = 0.8
turn_speed = 10
max_turn_speed = 10
precise_turn_speed = 5

# Defines the downward acceleration due to gravity
gravity = 0.01

# Creates variables for the lander's velocity
# This is the starting velocity
vertical_speed = -1
horizontal_speed = 2

# Defines the number, speed, and possible locations of obstacles
num_obstacles = 6
obstacle_speed_range = (10,30)
obstacle_colors = ['steelblue','lightgray','skyblue','slategray','navy']
obstacle_area_top = 200
obstacle_area_bottom = -200
obstacle_area_left = -425
obstacle_area_right = 425

# Defines the edges of the screen
screen_top = 350
screen_bottom = -350
screen_left = -450
screen_right = 450
wn.setup(screen_right*2 + 50,screen_top*2 + 50)

# Defines the planetary attributes
planet_surface = -300
background_color = 'gray10'
surface_color = 'silver'
num_stars = 50

# Defines the attributes of the information display
end_message_written = False
font_setup = ("Arial", 30, "normal")
smaller_font_setup = ("Arial", 15, "normal")
display_color = 'gold'
left_padding = 25
vertical_padding = 15


# ----------- Function definitions -----------

def move_objects():
  global vertical_speed, horizontal_speed, crashed, landed, fuel_level, engine_thrust
  wn.tracer(False)
  # Finds current coordinates
  start_lander_xcor = lander.xcor()
  start_lander_ycor = lander.ycor()
  # Applies the effect of gravity
  vertical_speed -= gravity
  # Calculates new location
  new_lander_xcor = start_lander_xcor + horizontal_speed
  new_lander_ycor = start_lander_ycor + vertical_speed
  # Goes to the new location
  lander.goto(new_lander_xcor,new_lander_ycor)
  if fuel_level > 0 and engine_thrust != 0:
    # Moves based on engine thrust
    lander.fd(engine_thrust)
    # Subsracts from fuel based on engine thrust and fuel usage
    fuel_level -= fuel_use_rate*(engine_thrust/max_engine_thrust)
  else:
    engine_thrust = 0
  # Finds coordinates after engine thrust
  lander_xcor_after_engine = lander.xcor()
  lander_ycor_after_engine = lander.ycor()
  # Calculates total change in position
  # and sets new vertical and horizontal speed
  horizontal_speed = lander_xcor_after_engine - start_lander_xcor
  vertical_speed = lander_ycor_after_engine - start_lander_ycor

  # Moves the flames with the lander
  flames.goto(lander.xcor(),lander.ycor())

  # Hides or shows the flames whether the engine is on or not
  if engine_thrust != 0:
    flames.showturtle()
  else:
    flames.hideturtle()

  # Keeps the lander on screen
  if lander.xcor() < screen_left: 
    lander.setx(screen_left)
    horizontal_speed = 0
  if lander.xcor() > screen_right: 
    lander.setx(screen_right)
    horizontal_speed = 0
  if lander.ycor() > screen_top: 
    lander.sety(screen_top)
    vertical_speed = 0

  # Move the obstacles
  for index,item in enumerate(obstacles):
    if item.xcor() > obstacle_area_right or item.xcor() < obstacle_area_left:
      item.goto(random.choice((obstacle_area_left,obstacle_area_right)),random.randint(obstacle_area_bottom,obstacle_area_top))
    item.fd(obstacle_speeds[index]/10)

  # Check for collision
  for item in obstacles:
    if abs(lander.xcor()-item.xcor()) < collision_margin and abs(lander.ycor()-item.ycor()) < collision_margin:
      wn.bgcolor('red')
      if engine_thrust != 0: engine_thrust = 0
      flames.hideturtle()
      wn.tracer(True)
      explode(lander)
      wn.tracer(False)
      crashed = True

  # Checks if the lander has landed
  if lander.ycor() <= planet_surface:
    if abs(90-lander.heading()) <= land_orientaion_margin and abs(vertical_speed) <= vertical_speed_margin and abs(horizontal_speed) <= horizontal_speed_margin:
      wn.bgcolor('lightblue')
      lander.setheading(90)
      if engine_thrust != 0: engine_thrust = 0
      flames.hideturtle()
      landed = True
    else:
      wn.bgcolor('red')
      if engine_thrust != 0: engine_thrust = 0
      flames.hideturtle()
      wn.tracer(True)
      explode(lander)
      wn.tracer(False)
      crashed = True

  # Updates the text display
  update_display(crashed,landed,engine_thrust,end_message_written)

  wn.tracer(True)

  # Continues as long as the lander has not crashed
  if not crashed and not landed:
    wn.ontimer(move_objects, counter_interval) 

# Turns the lander left by the predefined turn speed
def turn_left():
  if not crashed and not landed:
    wn.tracer(False)
    lander.left(turn_speed)
    flames.left(turn_speed)
    wn.tracer(True)

# Turns the lander right by the predefined turn speed
def turn_right():
  if not crashed and not landed:
    wn.tracer(False)
    lander.right(turn_speed)
    flames.right(turn_speed)
    wn.tracer(True)

# Allows the user to decide whether to turn quickly or precisely
def toggle_precision():
  global turn_speed
  if turn_speed == max_turn_speed:
    turn_speed = precise_turn_speed
  else:
    turn_speed = max_turn_speed

# Increments the engine thrust
def thrust_up():
  global engine_thrust
  if not crashed and not landed and fuel_level > 0:
    engine_thrust += max_engine_thrust/10
    if engine_thrust > max_engine_thrust:
      engine_thrust = max_engine_thrust
  # Updates the text display
  update_display(crashed,landed,engine_thrust,end_message_written)

# Decrements the engine thrust
def thrust_down():
  global engine_thrust
  if not crashed and not landed and fuel_level > 0:
    engine_thrust -= max_engine_thrust/10
  if engine_thrust <= 0:
    engine_thrust = 0
  # Updates the text display
  update_display(crashed,landed,engine_thrust,end_message_written)

# Toggles the engine thrust between maximum and minimum
# also changes the sprite to show if the engine is on or not
def toggle_engine():
  global engine_thrust
  if not crashed and not landed and fuel_level > 0:
    if engine_thrust != max_engine_thrust:
      engine_thrust = 0
      engine_thrust += max_engine_thrust
    else:
      engine_thrust = 0
  # Updates the text display
  if not crashed and not landed:
    update_display(crashed,landed,engine_thrust,end_message_written)

# This is a function to animate the explosion of the lander
def explode(turt):
  turt.shape('circle')
  turt.color('red')
  for i in range(10):
    turt.turtlesize(i+1)
  turt.hideturtle()

# Updates the display
def update_display(is_crashed,is_landed,current_engine_thrust,is_end_message_written):
  wn.tracer(False)
  # Updates the displays if the lander has not landed or crashed 
  if not is_crashed and not is_landed:
    fuel_display.clear()
    fuel_display.write('Fuel: '+str(int(fuel_level))+'%',font=font_setup)

    thrust_display.clear()
    thrust_display.write('Thrust: '+str(int((current_engine_thrust/max_engine_thrust)*100))+'%',font=font_setup)
    if int((current_engine_thrust/max_engine_thrust)*100) == 0:
      current_engine_thrust = 0
  # Displays the score if the lander has landed or crashed
  elif not is_end_message_written:
    # Hides the obstacles
    for obstacle in obstacles: 
      obstacle.hideturtle()
    # Calculates score
    score = 1000
    if is_landed:
      score -= abs(lander.xcor())
      if score >= 900:
        score = 1000
    else:
      score = 250 - abs(lander.ycor()-planet_surface)
    score = int(score)
    if score <= 0:
      score = 0
    # Displays the end messages
    if is_crashed:
      result_message = 'You crashed!'
    if is_landed:
      result_message = 'You landed!'
    end_writer.write(result_message,align='center',font=font_setup)
    end_writer.sety(-50)
    end_writer.write('Score: '+str(score),align='center',font=font_setup)
    end_writer.sety(-100)
    end_writer.write('Press enter to restart.',align='center',font=font_setup)
    global end_message_written
    end_message_written = True
  wn.tracer(True)

# Traces the border of the screen with a turtle
def trace_border(turt):
  turt.goto(screen_right,screen_top)
  turt.goto(screen_right,screen_bottom)
  turt.goto(screen_left,screen_bottom)
  turt.goto(screen_left,screen_top)

# Draws the emviroment
def draw_environment():
  wn.tracer(False)

  # Creates and configures the drawer turtle
  drawer = turtle.Turtle()
  drawer.hideturtle()
  drawer.penup()

  # Sets the background color
  drawer.goto(screen_left,screen_top)
  drawer.color(background_color)
  drawer.pendown()
  drawer.begin_fill()
  trace_border(drawer)
  drawer.end_fill()
  drawer.penup()

  # Draws the stars
  drawer.penup()
  drawer.pensize(1)
  drawer.color('white')
  for i in range(num_stars):
    star_size = random.randint(1,5)
    drawer.goto(random.randint(screen_left, screen_right), random.randint(planet_surface, screen_top))
    drawer.right(72)
    drawer.pendown()
    drawer.begin_fill()
    for j in range(5):
      drawer.fd(star_size)
      drawer.left(108)
      drawer.fd(star_size)
      drawer.right(324)
    drawer.end_fill()
    drawer.penup()

  # Draws the planetary surface
  drawer.goto(screen_left,planet_surface)
  drawer.pensize(1)
  drawer.color(surface_color)
  drawer.pendown()
  drawer.begin_fill()
  drawer.setx(screen_right)
  drawer.sety(screen_bottom)
  drawer.setx(screen_left)
  drawer.sety(planet_surface)
  drawer.end_fill()
  drawer.penup()

  # Draws the screen border
  drawer.goto(screen_left,screen_top)
  drawer.pensize(5)
  drawer.color('black')
  drawer.pendown()
  trace_border(drawer)
  drawer.penup()

  wn.tracer(True)

def restart_prgm():
  # Removes the screen object
  wn.bye()
  # Restarts the program
  subprocess.call(sys.executable + ' "' + os.path.realpath(__file__) + '"')

def close_prgm():
  # Removes the screen object
  wn.bye()
  


# ---------- Main sequence ----------

# Draws the environment
draw_environment()

wn.tracer(False)
# Creates the lander object, configures it, and positions it
lander = turtle.Turtle()
lander.shape('lander')
lander.color(lander_color)
lander.turtlesize(lander_scale)
lander.penup()
lander.setheading(lander_start_orientation)
lander.goto(starting_location)

# Creates the lander's flames, hides them and puts them by the lander
flames = turtle.Turtle()
flames.hideturtle()
flames.shape('flames')
flames.color(lander_flame_color)
flames.turtlesize(lander_scale)
flames.penup()
flames.setheading(lander_start_orientation)
flames.goto(starting_location)

# Creates the turtles for the information displays
fuel_display = turtle.Turtle()
fuel_display.hideturtle()
fuel_display.penup()
fuel_display.color(display_color)
fuel_display.goto(screen_left+left_padding,screen_top-50-vertical_padding)

thrust_display = turtle.Turtle()
thrust_display.hideturtle()
thrust_display.penup()
thrust_display.color(display_color)
thrust_display.goto(screen_left+left_padding,screen_top-(50+vertical_padding)*2)

end_writer = turtle.Turtle()
end_writer.hideturtle()
end_writer.penup()
end_writer.color(display_color)

instruction_writer = turtle.Turtle()
instruction_writer.hideturtle()
instruction_writer.penup()
instruction_writer.color(display_color)
instruction_writer.goto(screen_left+left_padding+250,screen_top-30-vertical_padding)
instruction_writer.write('Your goal is to pilot the lander to a safe touchdown!',font=smaller_font_setup)
instruction_writer.sety(instruction_writer.ycor()-25)
instruction_writer.write('Use a and d keys to turn the lander and space bar to toggle the engine.',font=smaller_font_setup)
instruction_writer.sety(instruction_writer.ycor()-25)
instruction_writer.write('The more fuel you land with and the closer you are to the center',font=smaller_font_setup)
instruction_writer.sety(instruction_writer.ycor()-25)
instruction_writer.write('of the screen, the more points you get. Press enter to restart.',font=smaller_font_setup)


# Creates the obstacles, configures, and positions them
obstacles = [turtle.Turtle() for i in range(num_obstacles)]
obstacle_speeds = [random.randint(obstacle_speed_range[0],obstacle_speed_range[1]) for i in range(num_obstacles)]

for index,item in enumerate(obstacles):
  item.turtlesize(0.5)
  item.color(random.choice(obstacle_colors))
  if random.randint(1,500) == 500:
    item.shape('turtle')
    item.turtlesize(2)
  else:
    item.shape('meteor')
  item.penup()
  if index < num_obstacles/2:
    item.goto(obstacle_area_left,random.randint(obstacle_area_bottom,obstacle_area_top))
  else:
    item.goto(obstacle_area_right,random.randint(obstacle_area_bottom,obstacle_area_top))
    item.setheading(180)
wn.tracer(True)

# Moves the lander and obstacles every certain amount of time
wn.ontimer(move_objects, counter_interval) 

# Accepts different user inputs
wn.onkeypress(turn_left,"a")
wn.onkeypress(turn_right,"d")
wn.onkeypress(thrust_up,'=')
wn.onkeypress(thrust_down,'-')
wn.onkeypress(toggle_precision,'/')
wn.onkeypress(toggle_engine,"space")
wn.onkeypress(restart_prgm,'Return')
wn.onkeypress(close_prgm,'BackSpace')

wn.listen()

wn.mainloop()