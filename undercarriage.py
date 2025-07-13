from build123d import *
from ocp_vscode import *
set_port(3939)

l = 92
h = 10
rod_edge = 3

# Add link rod
arcd = 7.2
l1 = Line((0, 0), (1, 0))
l2 = JernArc(start=l1 @ 1, tangent=l1 % 1, radius=arcd / 2, arc_size=180)
l3 = PolarLine(start=l2 @ 1, length=l, direction=l2 % 1)
l4 = JernArc(start=l3 @ 1, tangent=l3 % 1, radius=arcd / 2, arc_size=90)
l5 = PolarLine(start=l4 @ 1, length=h, direction=l4 % 1)
l6 = JernArc(start=l5 @ 1, tangent=l5 % 1, radius=arcd / 2, arc_size=90)
# l7 = PolarLine(start=l6 @ 1, length=1, direction=l6 % 1)
# l8 = JernArc(start=l7 @ 1, tangent=l7 % 1, radius=arcd / 2, arc_size=-90)
# l9 = PolarLine(start=l8 @ 1, length=.5, direction=l8 % 1)

lprof = Curve() + (l1, l2, l3, l4, l5, l6) #, l8, l9) + 
wire = Wire(lprof.edges())  #  TODO sprof.wires() fails
sweep_rect = Rectangle(rod_edge, rod_edge)
mainp = sweep(Plane.YZ * sweep_rect, path=wire)

s1 = Line((0, 0), (0, 8))
s2 = JernArc(start=s1 @ 1, tangent=s1 % 1, radius=arcd / 2, arc_size=80)
s3 = PolarLine(start=s2 @ 1, length=80, direction=s2 % 1)

#s3 = Line((0, 12), (30, 12))
sprof = Curve() + (s1, s2, s3)
hook = sweep(Plane.XZ * sweep_rect, path=sprof)
mainp += Pos(-10, 8) * hook
fin = Pos(10, 20) *mainp


cyl_len = 60
tol = 1.5
wall_width = 1.2


cyl = extrude(Rectangle(rod_edge + tol + wall_width, rod_edge + tol + wall_width), cyl_len)
cyl -= extrude(Pos(0, 0, 0) * Rectangle(rod_edge + tol, rod_edge + tol), cyl_len)

cyl2 = Plane.XZ * Rectangle(100, cyl_len, align=(Align.MAX, Align.MIN))
cyl2 = extrude(Pos((rod_edge + tol + wall_width)/2, (rod_edge + tol)/2, 0) * cyl2, -1)
cyl = cyl + cyl2

# splits help keep the object 3d printable by reducing overhang
# splitz = rod_r * 0.7
# fin = split(fin, Plane(origin=(0, 0, -splitz)))
# fin = split(fin, Plane(origin=(0, 0, splitz)), keep=Keep.BOTTOM)
show((fin, cyl), reset_camera=Camera.KEEP)
#show(hook)

export_stl(fin, "models/undercarriage.stl")
export_stl(cyl, "models/muni.stl")

