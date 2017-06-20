import numpy as np

L = 64

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
  return reduce(f_or, voxels)

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
