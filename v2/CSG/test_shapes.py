from shapes import *

command1 = Command(2, 4, 4, 4)
command2 = Command(2, 4, 4, 4)
command3 = Command(2, 4, 4, 4)
command4 = Command(2, 4, 4, 4)

world = BrickWorld([])

import random

for i in range(100):
  
  random_command = Command(2, 4, random.choice(range(16)), random.choice(range(16)))
  world = run_command(world, random_command)
  print world

# plot( world.to_voxel_field(), "blah.png")
plot_color(world, "world1.png")
