from CSG import shapes

prog, vox = shapes.gen_data1(10)

print prog

shapes.plot(vox, "drawings/demo_data.png")

# draw prefix of the program 1 at a time
# consistently sort the prog first
prog = sorted(prog)
for i in range(len(prog)+1):
  prefix = prog[:i]
  print prefix
  vox_prefix = shapes.render_prog1(prefix)
  shapes.plot(vox_prefix, "drawings/demo_data_prefix{0}.png".format(i))
  
