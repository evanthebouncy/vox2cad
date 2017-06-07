import numpy as np

L = 64

def dist(i,j,k,x,y,z):
  return (i-x)*(i-x) + (j-y)*(j-y) + (k-z)*(k-z) 

def sphere(x,y,z,r):
  gridx,gridy,gridz = np.ogrid[0:L, 0:L, 0:L]
  mask = (gridx-x)**2+(gridy-y)**2+(gridz-z)**2 <= r**2
  field = np.zeros([L,L,L], dtype=bool)
  field[mask] = True
  return field

def cube(x,y,z,w,h,d):
  mask = np.zeros((L,L,L), dtype=bool)
  mask[x-w/2:x+w/2, y-h/2:y+h/2, z-d/2:z+d/2] = True
  return mask

def f_or(f1, f2):
  return np.ma.mask_or(f1,f2)

def f_and(f1, f2):
  return f1 * f2

def f_not(f1):
  return ~f1

def f_sub(f1, f2):
  return f_and(f1, f_not(f2))

def plot(field):
  import matplotlib.pyplot as plt
  from mpl_toolkits.mplot3d import Axes3D

  z,x,y = field.nonzero()
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  ax.set_xlim(0,L)
  ax.set_ylim(0,L)
  ax.set_zlim(0,L)
  ax.scatter(x, y, z, zdir='z', c= 'red')
  plt.savefig("demo.png")
