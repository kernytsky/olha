from build123d import *
from ocp_vscode import *
set_port(3939)

# Add link rod
# l = 92
# h = 10
# rod_h = 2
# rod_w = 4
arcd = 7.2

# Make front clip

l1 = Line((0, 0), (0.1, 0))
l2 = JernArc(start=l1 @ 1, tangent=l1 % 1, radius=arcd * .18, arc_size=170)
l3 = PolarLine(start=l2 @ 1, length=2, direction=l2 % 1)
# l7 = PolarLine(start=l6 @ 1, length=1, direction=l6 % 1)
# l8 = JernArc(start=l7 @ 1, tangent=l7 % 1, radius=arcd / 2, arc_size=-90)
# l9 = PolarLine(start=l8 @ 1, length=.5, direction=l8 % 1)

lprof = Curve() + (l1, l2, l3) 
wire = Plane.XZ * Wire(lprof.edges())  #  TODO sprof.wires() fails
sweep_rect = Rectangle(14, 1.5)
front_clip = sweep(Plane.YZ * sweep_rect, path=wire)
front_clip = Pos(30, 0, 29.2) * front_clip

# Make rear clip

l1 = PolarLine((0, 10), -44, 57)
l2 = JernArc(start=l1 @ 1, tangent=l1 % 1, radius=arcd / 2, arc_size=-60)
l3 = PolarLine(start=l2 @ 1, length=5, direction=l2 % 1)
l4 = JernArc(start=l3 @ 1, tangent=l3 % 1, radius=arcd / 2, arc_size=-80)

lprof = Curve() + (l1, l2, l3, l4) 
wire = Plane.XZ * Wire(lprof.edges())  #  TODO sprof.wires() fails
sweep_rect = Plane.YZ * Rot(-60, 0, 0) * Pos(0, 0, 0) * Rectangle(7.5, 2)
rear_clip = sweep(sweep_rect, path=wire)
rear_clip = Pos(-33, 0, 14) * Rot(0, 90, 0) * rear_clip
rear_clip = split(rear_clip, Plane(origin=(0, 0, 11), normal=(0, 0, 1)))

# Build undecarriage body
body_l = 60
body_w = 100
body_h = 30
wall_width = 1

body = Box(body_l, body_w, body_h, align=(Align.CENTER, Align.CENTER))
ibody = Box(body_l - wall_width*2, body_w - wall_width*2, body_h - wall_width, align=(Align.CENTER, Align.CENTER, Align.MIN))
body -= Pos(0, 0, wall_width) * ibody
uc = front_clip + Pos(0, 0, -10) * rear_clip + body

# Make servo holder
servo_w = 12
servo_l = 23
servo_h = 24
servo_tol = 0.2
servo_mount_h = 20 # height of the top of the overhang with mounting holes

servo_body = Pos(22, 10) * Box(servo_w + servo_tol, servo_l + servo_tol, 10)
uc -= servo_body
servo_wall = Plane.YZ * Box(servo_l, servo_mount_h, wall_width, 
                            align=(Align.CENTER, Align.MIN, Align.CENTER))

uc += Pos(14.5, 10, 0) * servo_wall

# Add slots for rail mount points
mount_slot = Box(2, 10, 10)
uc -= Pos(5, -3, 0) * mount_slot + Pos(-20, -3, 0) * mount_slot

show((uc), reset_camera=Camera.KEEP)
export_stl(uc, "models/undercarriage.stl")

# # Make hook for muni

# s1 = Line((0, 0), (0, 28))
# s2 = JernArc(start=s1 @ 1, tangent=s1 % 1, radius=arcd / 2, arc_size=80)
# s3 = PolarLine(start=s2 @ 1, length=80, direction=s2 % 1)

# #s3 = Line((0, 12), (30, 12))
# sprof = Curve() + (s1, s2, s3)
# sprof_wire = Plane.XZ * Wire(sprof.edges())
# hook = sweep(Plane.XY * sweep_rect, path=sprof_wire)
# mainp += Pos(-10, 8) * hook