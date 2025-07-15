from build123d import *
from ocp_vscode import *
set_port(3939)

fin_w = 35 # 25
fin_h1 = 30 # 15
fin_h2 = 50 # 30
fin_d = 1
muni_w = link_rod_l = 35
muni_h = 140 # 80
cone_h = 30
cone_point_d = 2

fin_poly = Polyline((link_rod_l/2,0), 
                    (link_rod_l/2, fin_h2),
                    (link_rod_l/2 + fin_w, fin_h2),
                    (link_rod_l/2 + fin_w, fin_h1),
                    (link_rod_l/2, 0))
fin = make_face(Plane.XY * fin_poly)
fin = extrude(fin, -fin_d) # Pos(0, 0, -fin_d/2) * 
fin += mirror(fin, Plane.YZ)
fin = Pos(0, -fin_h2, 0) * fin

tol = 1.5
wall_width = 1

drone_tube_edge = 3
muni_tube_od = drone_tube_edge + tol + wall_width
muni_tube_id = drone_tube_edge + tol

body = Plane.XZ * Cylinder(muni_w/2, muni_h, align=(Align.CENTER, Align.CENTER))
body -= Plane.XZ * Pos(0, 0, wall_width) * Cylinder(muni_w/2 - wall_width, muni_h - wall_width, align=(Align.CENTER, Align.CENTER))
body = body + fin

# Add second set of fins
body += Rot(0, 90, 0) * fin

# Add mounting tube 
tube = Plane.YZ * extrude(Rectangle(muni_tube_od, drone_tube_edge + tol + wall_width), muni_w)
tube = Rot(0, 45, 0) * Pos(-muni_w/2, -muni_tube_od/2, 0) * tube
tube_hole = Plane.YZ * extrude(Rectangle(muni_tube_id, drone_tube_edge + tol), muni_w+1) # + 1 is some hack because of non-overlapping surfaces once the cone is added
tube_hole = Rot(0, 45, 0) * Pos(-muni_w/2, -muni_tube_od/2, 0) * tube_hole

body = body + tube - tube_hole

body += Plane.XZ * Pos(0, 0, muni_h) * Cone(muni_w/2, cone_point_d, cone_h, align=(Align.CENTER, Align.CENTER))
body -= Plane.XZ * Pos(0, 0, muni_h) * Cone(muni_w/2 - wall_width, cone_point_d, cone_h - 5, align=(Align.CENTER, Align.CENTER))

body -= Plane.XZ * Pos(muni_w * 0.19, muni_w * 0.19) * Cylinder(muni_w * 0.18, wall_width, align=(Align.CENTER, Align.CENTER))

show((body), reset_camera=Camera.KEEP)
export_stl(Rot(-90, 90, 0) * body, "models/muni.stl")
