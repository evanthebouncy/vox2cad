from shapes import *

# s1 = sphere(40,10,20,20)
# c1 = cube(40,30,20,40,30,20)
# x1 = f_sub(s1,c1)
# plot(x1)

prog, vox = gen_data1(10)

print prog

plot(vox, "demo.png")
