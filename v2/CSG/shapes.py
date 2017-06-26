import numpy as np
import copy

L = 16

class Command:
  
  def __init__(self, w, h, dx, dy):
    self.w, self.h, self.dx, self.dy = w, h, dx, dy
    self.points_2d = set([(dx+x, dy+y) for x in range(w) for y in range(h)])

  def __str__(self):
    return "{0} {1} {2} {3}".format(self.w, self.h, self.dx, self.dy)

class Brick:

  def __init__(self, w, h, dx, dy, dz):
    self.w, self.h, self.dx, self.dy, self.dz = w, h, dx, dy, dz
    self.points_2d = set([(dx+x, dy+y) for x in range(w) for y in range(h)])
    self.points_3d = set([(dx+x, dy+y, dz+z) for x in range(w)\
                                             for y in range(h)\
                                             for z in range(2)])

  def __str__(self):
    return "{0} {1} {2} {3} {4}".format(self.w, self.h, self.dx, self.dy, self.dz)

class BrickWorld:

  def __init__(self, bricks):
    self.bricks = bricks

  def __str__(self):
    return str([str(x) for x in self.bricks])

  def to_voxel_field(self):
    ret = np.zeros([L,L,L], np.int32)
    for X in range(L):
      for Y in range(L):
        for Z in range(L):
          for b in self.bricks:
            if (X,Y,Z) in b.points_3d:
              ret[X,Y,Z] = 1
    return ret
    

# takes in a brick world and a command
# get the next brick world
def run_command(brick_world, command):
  z = max([ 2 + b.dz for b in brick_world.bricks if len(b.points_2d & command.points_2d) > 0] + [0])
  
  new_brick = Brick(command.w, command.h, command.dx, command.dy, z)
  new_bricks = copy.deepcopy(brick_world.bricks) + [new_brick]
  return BrickWorld(new_bricks)

    
    

# generate a shape program consists of unions of 
# N circles and squares only
def gen_prog1(N):
  shapes = []
  for i in range(N):
    position = np.random.randint(64, size=3)
    if np.random.random() < 0.5:
      radius = [10]
      s_params = list(position) + radius
      shapes.append(['s'] + s_params)
    else:
      lwh = [15, 15, 15]
      c_params = list(position) + lwh
      shapes.append(['c'] + c_params)
  return shapes

# takes in a union of circles and squares render into
# a voxel field
def render_prog1(shapes):
  # in case we have no shapes to speak of
  if shapes == []:
    return np.zeros((L,L,L), dtype=bool)
  voxels = []
  for s in shapes:
    typo, params = s[0], s[1:]
    if typo == 's':
      voxels.append(sphere(*params))
    if typo == 'c':
      voxels.append(cube(*params))

  ret = np.zeros((L,L,L), dtype=bool)
  for voxel_field in voxels:
    ret = f_or(ret, voxel_field)

  if str(ret) == "False": return np.zeros((L,L,L), dtype=bool)
  return ret

  
  

# generate the data pair of high-level shapes
# and the voxel field representation
# of N shapes of circle and cube
def gen_data1(N):
  prog = gen_prog1(N)
  voxels = render_prog1(prog)
  return prog, voxels

def sphere(x,y,z,r):
  gridx,gridy,gridz = np.ogrid[0:L, 0:L, 0:L]
  mask = (gridx-x)**2+(gridy-y)**2+(gridz-z)**2 <= r**2
  field = np.zeros([L,L,L], dtype=bool)
  field[mask] = True
  return field

def cube(x,y,z,w,h,d):
  mask = np.zeros((L,L,L), dtype=bool)
  mask[x-w/2:x+w/2, y-h/2:y+h/2, z-d/2:z+d/2] = True
  hl = ['c', x,y,z,w,h,d]
  return mask

def f_or(f1, f2):
  return np.ma.mask_or(f1,f2)

def f_and(f1, f2):
  return f1 * f2

def f_not(f1):
  return ~f1

def f_sub(f1, f2):
  return f_and(f1, f_not(f2))

def plot(field, name):
  field = np.transpose(field, [2,0,1])
  import matplotlib.pyplot as plt
  from mpl_toolkits.mplot3d import Axes3D

  z,x,y = field.nonzero()
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  ax.set_xlim(0,L)
  ax.set_ylim(0,L)
  ax.set_zlim(0,L)
  ax.scatter(x, y, z, zdir='z', c= 'red')
  plt.savefig(name)

def plot_color(world, name):
  import matplotlib.pyplot as plt
  from mpl_toolkits.mplot3d import Axes3D
  from matplotlib import colors as mcolors

  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  ax.set_xlim(0,L)
  ax.set_ylim(0,L)
  ax.set_zlim(0,L)
  
  for b in world.bricks:
    x, y, z = [], [], []
    for point in b.points_3d:
      x.append(point[0])
      y.append(point[1])
      z.append(point[2])

    import random
    ax.scatter(x, y, z, zdir='z', c= random.choice(mcolors.cnames.keys()))

  plt.savefig(name)







