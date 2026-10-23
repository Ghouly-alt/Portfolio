import bpy, bmesh, math
from mathutils import Vector

K = 0.684      # rayon de surface / rayon metaball (rigidité 4, seuil 0.6)
STIFF = 4.0
COLN = "WFT_HD"

# --- Collection propre -------------------------------------------------------
lc = bpy.context.view_layer.layer_collection.children
if "WiiFitTrainer" in lc: lc["WiiFitTrainer"].hide_viewport = True
if COLN in bpy.data.collections:
    col = bpy.data.collections[COLN]
    for o in list(col.objects):
        if o.type == 'CAMERA': continue
        d = o.data; bpy.data.objects.remove(o, do_unlink=True)
        if d and d.users == 0:
            if isinstance(d, bpy.types.Mesh): bpy.data.meshes.remove(d)
            elif isinstance(d, bpy.types.MetaBall): bpy.data.metaballs.remove(d)
else:
    col = bpy.data.collections.new(COLN); bpy.context.scene.collection.children.link(col)

def mat(n, rgb, rough=0.6):
    m = bpy.data.materials.get(n) or bpy.data.materials.new(n)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    m.diffuse_color = (*rgb, 1); m.roughness = rough
    return m
SKIN  = mat("HD_skin",  (0.80, 0.79, 0.78), 0.5)
SHIRT = mat("HD_shirt", (0.33, 0.34, 0.36), 0.7)
RAGL  = mat("HD_raglan",(0.21, 0.22, 0.24), 0.7)
BLUE  = mat("HD_blue",  (0.05, 0.58, 0.88), 0.55)
SHORT = mat("HD_shorts",(0.065,0.065,0.075),0.75)
HAIR  = mat("HD_hair",  (0.20, 0.13, 0.08), 0.8)
SCLE  = mat("HD_sclera",(0.97, 0.97, 0.96), 0.25)
IRIS  = mat("HD_iris",  (0.36, 0.38, 0.42), 0.3)
PUPIL = mat("HD_pupil", (0.06, 0.06, 0.07), 0.2)

# --- Metaballs ---------------------------------------------------------------
def mball(name, res):
    mb = bpy.data.metaballs.new(name); mb.resolution = res; mb.render_resolution = res; mb.threshold = 0.6
    o = bpy.data.objects.new(name, mb); col.objects.link(o); return o, mb

def ell(mb, c, r, s=(1,1,1), axis=None, neg=False, stiff=STIFF):
    e = mb.elements.new(type='ELLIPSOID'); e.co = c; e.radius = r / {1:0.394, 2:0.574, 4:0.684, 8:0.76}.get(stiff, K)
    e.size_x, e.size_y, e.size_z = s; e.stiffness = stiff; e.use_negative = neg
    if axis is not None:
        e.rotation = Vector((0,0,1)).rotation_difference(Vector(axis).normalized())
    return e

def cap(mb, a, b, r, stiff=STIFF):
    a, b = Vector(a), Vector(b); d = b - a
    e = mb.elements.new(type='CAPSULE'); e.co = (a+b)/2; e.radius = r / K
    e.size_x = d.length/2; e.stiffness = stiff
    e.rotation = Vector((1,0,0)).rotation_difference(d.normalized())
    return e

def lerp(a, b, t): return tuple(a[i]+(b[i]-a[i])*t for i in range(3))
def mx(p): return (-p[0], p[1], p[2])

# Convention : Z vers le haut, le personnage regarde -Y, taille 1,80 m
body_o, B = mball("HD_Body", 0.007)

# Tronc
ell(B, (0, 0.0, 1.33), 0.135, (1.12, 0.84, 1.25))            # cage thoracique
ell(B, (0, 0.035, 1.37), 0.12, (1.15, 0.75, 1.05))           # haut du dos
ell(B, (0, 0.005, 1.14), 0.114, (1.1, 0.80, 1.05))          # abdomen / taille
ell(B, (0, 0.012, 0.94), 0.135, (1.30, 0.85, 0.80))          # bassin
ell(B, (0, -0.055, 1.19), 0.058, (1.15, 0.4, 1.6))          # grand droit (abdos)
for z in (1.25, 1.19, 1.13):
    for sx in (1, -1): ell(B, (sx*0.03, -0.08, z), 0.014, (1.2, 0.45, 0.8))   # tablettes
cap(B, (0, -0.035, 0.97), (0, -0.025, 0.86), 0.034)           # bas-ventre / pubis

for sx in (1, -1):
    m = lambda p: (sx*p[0], p[1], p[2])
    ell(B, m((0.076, -0.065, 1.38)), 0.072, (1.18, 0.5, 0.75))      # pectoraux
    ell(B, m((0.118, 0.03, 1.31)), 0.075, (0.72, 0.85, 1.4))         # dorsaux
    cap(B, m((0.04, 0.03, 1.545)), m((0.15, 0.02, 1.475)), 0.018)
    ell(B, m((0.125, 0.005, 1.455)), 0.058, (1.45, 0.95, 0.6))       # haut d'épaule          # trapèzes (pente cou-épaule)
    ell(B, m((0.06, 0.085, 1.30)), 0.05, (0.8, 0.5, 2.2))             # érecteurs
    ell(B, m((0.078, 0.055, 0.885)), 0.082, (1.0, 0.85, 1.0))           # fessiers

    # Bras (pendants, légèrement écartés, paumes vers les cuisses)
    S, E, W = m((0.205, 0.005, 1.45)), m((0.278, 0.03, 1.13)), m((0.30, 0.0, 0.895))
    ell(B, m((0.205, 0.005, 1.432)), 0.051, (1.0, 1.1, 1.22))        # deltoïde
    cap(B, S, E, 0.043)
    up = Vector(E) - Vector(S)
    ell(B, lerp(S, E, .52)[:1] + (lerp(S, E, .52)[1]-0.022,) + lerp(S, E, .52)[2:], 0.042, (0.95, 0.85, 2.0), axis=up)  # biceps
    ell(B, lerp(S, E, .42)[:1] + (lerp(S, E, .42)[1]+0.025,) + lerp(S, E, .42)[2:], 0.044, (0.95, 0.9, 2.1), axis=up)  # triceps
    Mf = lerp(E, W, 0.4)
    cap(B, E, Mf, 0.039); cap(B, Mf, W, 0.029)
    ell(B, (Mf[0]+sx*0.006, Mf[1]-0.012, Mf[2]+0.04), 0.036, (0.95, 0.9, 2.0), axis=Vector(W)-Vector(E))  # brachioradial
    ell(B, E, 0.034)                                                   # coude

    # Jambes
    Hj, Kn, An = m((0.093, 0.0, 0.90)), m((0.112, -0.005, 0.475)), m((0.128, 0.035, 0.085))
    cap(B, Hj, Kn, 0.074)
    cap(B, Kn, An, 0.041)
    th = Vector(Kn) - Vector(Hj)
    ell(B, m((0.108, -0.035, 0.70)), 0.068, (1.0, 0.8, 2.3), axis=th)  # quadriceps
    ell(B, m((0.087, -0.028, 0.545)), 0.034, (1.0, 0.9, 1.3))          # vaste interne
    ell(B, m((0.148, -0.0, 0.66)), 0.046, (0.7, 1.0, 2.2), axis=th)    # vaste externe
    ell(B, m((0.10, 0.04, 0.68)), 0.06, (1.0, 0.8, 2.2), axis=th)      # ischios
    ell(B, m((0.055, 0.0, 0.79)), 0.05, (1.0, 1.0, 1.8))              # adducteurs
    ell(B, m((0.113, -0.038, 0.478)), 0.021, (1.0, 0.6, 1.1))         # rotule
    ell(B, Kn, 0.044, (1.0, 1.0, 1.0))                                  # genou
    ell(B, m((0.12, 0.03, 0.355)), 0.052, (1.0, 0.9, 2.0))          # mollet
    ell(B, m((0.11, 0.02, 0.33)), 0.03, (0.9, 0.85, 1.7))           # mollet interne
    ell(B, m((0.128, -0.012, 0.27)), 0.022, (1.0, 1.0, 3.0))           # tibial

# Cou
cap(B, (0, 0.01, 1.47), (0, 0.0, 1.60), 0.063)
for sx in (1, -1):
    cap(B, (sx*0.045, 0.0, 1.605), (sx*0.02, -0.048, 1.50), 0.017)     # sterno-cléido

# --- Mains et pieds (résolution très fine) ------------------------------------
ext_o, X = mball("HD_Ext", 0.0025)
for sx in (1, -1):
    m = lambda p: (sx*p[0], p[1], p[2])
    W = (0.30, 0.0, 0.895)
    ell(X, m((0.302, 0.0, 0.888)), 0.022, (0.9, 1.2, 1.0))              # poignet
    ell(X, m((0.305, -0.002, 0.85)), 0.04, (0.45, 1.0, 1.15))           # paume
    # doigts : index devant (-Y) -> auriculaire derrière (+Y), légère flexion vers la cuisse
    for dy, L, r in ((-0.027, 0.068, 0.0085), (-0.009, 0.076, 0.0088), (0.009, 0.07, 0.0083), (0.026, 0.056, 0.0072)):
        b0 = (0.305, dy, 0.808); b1 = (0.300, dy*1.05, 0.808 - L*0.55); b2 = (0.288, dy*1.08, 0.808 - L)
        cap(X, m(b0), m(b1), r); cap(X, m(b1), m(b2), r*0.9)
    cap(X, m((0.296, -0.03, 0.865)), m((0.29, -0.055, 0.825)), 0.012)    # pouce
    cap(X, m((0.29, -0.055, 0.825)), m((0.285, -0.064, 0.795)), 0.0095)
    # pied (légèrement tourné vers l'extérieur)
    ell(X, m((0.128, 0.035, 0.085)), 0.033)                             # cheville
    ell(X, m((0.105, 0.035, 0.08)), 0.016); ell(X, m((0.15, 0.04, 0.075)), 0.016)  # malléoles
    ell(X, m((0.13, 0.055, 0.038)), 0.036, (0.9, 1.05, 1.0))            # talon
    cap(X, m((0.13, 0.04, 0.045)), m((0.14, -0.10, 0.026)), 0.035)      # voûte
    ell(X, m((0.14, -0.04, 0.05)), 0.03, (1.1, 1.6, 0.7))               # cou-de-pied
    for tx, L, r in ((0.113, 0.05, 0.013), (0.131, 0.044, 0.0102), (0.145, 0.04, 0.0096), (0.158, 0.035, 0.009), (0.169, 0.029, 0.0085)):
        cap(X, m((tx, -0.092, 0.02)), m((tx+0.003, -0.092-L*0.72, 0.013)), r)  # orteils

# --- Conversion en maillages --------------------------------------------------
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
def to_mesh(o, name, mat_):
    me = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
    mb = o.data; bpy.data.objects.remove(o, do_unlink=True); bpy.data.metaballs.remove(mb)
    ob = bpy.data.objects.new(name, me); col.objects.link(ob)
    bm_ = bmesh.new(); bm_.from_mesh(me); bmesh.ops.remove_doubles(bm_, verts=bm_.verts, dist=1e-5)
    for _ in range(2): bmesh.ops.smooth_vert(bm_, verts=bm_.verts, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
    bm_.to_mesh(me); bm_.free()
    me.materials.append(mat_); me.shade_smooth()
    return ob
body = to_mesh(body_o, "HD_Body", SKIN)
# --- Tête : loft de sections (profil de la planche) + reliefs sculptés -------
CY = 0.012
#        z      demi-largeur  avant   arrière
PROF = [(1.796, 0.012, 0.012, 0.014), (1.785, 0.05, 0.055, 0.06), (1.77, 0.071, 0.078, 0.086),
        (1.75, 0.085, 0.091, 0.102), (1.725, 0.092, 0.097, 0.111), (1.70, 0.094, 0.099, 0.113),
        (1.675, 0.093, 0.097, 0.110), (1.65, 0.089, 0.099, 0.102), (1.625, 0.079, 0.1, 0.09),
        (1.60, 0.068, 0.099, 0.075), (1.58, 0.057, 0.096, 0.062), (1.563, 0.048, 0.09, 0.05),
        (1.552, 0.03, 0.074, 0.04), (1.546, 0.01, 0.04, 0.02)]
def prof(z):
    if z >= PROF[0][0]: return PROF[0][1:]
    n = len(PROF)
    for k in range(n - 1):
        a, b = PROF[k], PROF[k+1]
        if b[0] <= z <= a[0]:
            p0, p3 = PROF[max(k-1, 0)], PROF[min(k+2, n-1)]
            t = (a[0] - z) / (a[0] - b[0])
            def cr(i):  # Catmull-Rom
                return 0.5*((2*a[i]) + (-p0[i] + b[i])*t + (2*p0[i] - 5*a[i] + 4*b[i] - p3[i])*t*t + (-p0[i] + 3*a[i] - 3*b[i] + p3[i])*t**3)
            return tuple(cr(i) for i in (1, 2, 3))
    return PROF[-1][1:]
NZ, NT, EXP = 140, 112, 2.3
zs = [PROF[0][0] - (PROF[0][0] - PROF[-1][0]) * i/(NZ - 1) for i in range(NZ)]
verts, faces = [(0, CY, 1.799)], []
for z in zs:
    w, f, bk = prof(z)
    for j in range(NT):
        th = 2*math.pi*j/NT; s_, c_ = math.sin(th), math.cos(th)
        px = w * math.copysign(abs(s_)**(2/EXP), s_)
        py = -(f if c_ >= 0 else bk) * math.copysign(abs(c_)**(2/EXP), c_)
        verts.append((px, CY + py, z))
verts.append((0, CY, PROF[-1][0] - 0.004))
for j in range(NT): faces.append((0, 1 + (j+1) % NT, 1 + j))
for i in range(NZ - 1):
    for j in range(NT):
        a = 1 + i*NT + j; b = 1 + i*NT + (j+1) % NT
        faces.append((a, b, b + NT, a + NT))
last = len(verts) - 1
for j in range(NT): faces.append((1 + (NZ-1)*NT + j, 1 + (NZ-1)*NT + (j+1) % NT, last))
hme_ = bpy.data.meshes.new("HD_HeadMesh"); hme_.from_pydata(verts, [], faces)
hme_.validate(); hme_.update()
head = bpy.data.objects.new("HD_HeadMesh", hme_); col.objects.link(head)
bm = bmesh.new(); bm.from_mesh(hme_)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=1, use_grid_fill=True)
for _ in range(6): bmesh.ops.smooth_vert(bm, verts=bm.verts, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
bm.normal_update()
# reliefs : (centre, amplitude en m (négatif = creux), sigmas x/y/z)
FEAT = [((0, -0.10, 1.668), 0.016, (0.0085, 0.03, 0.022)),   # dos du nez
        ((0, -0.104, 1.648), 0.012, (0.0095, 0.03, 0.0105)), # bout du nez
        ((0, -0.10, 1.692), 0.004, (0.007, 0.03, 0.01)),     # racine du nez
        ((0, -0.098, 1.632), -0.004, (0.009, 0.03, 0.004)),  # sous le nez
        ((0, -0.099, 1.614), 0.006, (0.018, 0.03, 0.0065)),  # lèvre sup.
        ((0, -0.099, 1.603), -0.0035, (0.02, 0.03, 0.0022)), # fente de la bouche
        ((0, -0.097, 1.594), 0.006, (0.016, 0.03, 0.006)),   # lèvre inf.
        ((0, -0.096, 1.583), -0.003, (0.013, 0.03, 0.004)),  # sillon menton
        ((0, -0.092, 1.566), 0.006, (0.017, 0.03, 0.01)),    # menton
        ((0, -0.099, 1.71), 0.003, (0.03, 0.03, 0.007))]     # glabelle
for sx in (1, -1):
    FEAT += [((sx*0.036, -0.094, 1.705), 0.004, (0.017, 0.03, 0.005)),   # arcades
             ((sx*0.036, -0.092, 1.682), -0.0135, (0.0165, 0.03, 0.0105)), # orbites
             ((sx*0.012, -0.099, 1.646), 0.0055, (0.006, 0.03, 0.006)),  # ailes du nez
             ((sx*0.036, -0.09, 1.695), 0.003, (0.013, 0.03, 0.003)),  # paupière sup.
             ((sx*0.036, -0.09, 1.669), 0.0015, (0.012, 0.03, 0.0028)),    # paupière inf.
             ((sx*0.055, -0.08, 1.662), 0.004, (0.013, 0.03, 0.012)),    # pommettes
             ((sx*0.045, -0.088, 1.62), -0.002, (0.01, 0.03, 0.02)),     # sillon joue
             ((sx*0.068, -0.02, 1.59), 0.003, (0.012, 0.03, 0.02)),      # angle de la mâchoire
             ((sx*0.024, -0.097, 1.603), -0.0015, (0.004, 0.03, 0.004))] # commissures
def gauss(p, c, sg):
    return math.exp(-0.5*(((p.x-c[0])/sg[0])**2 + ((p.y-c[1])/sg[1])**2 + ((p.z-c[2])/sg[2])**2))
for v in bm.verts:
    d = sum(a*gauss(v.co, c, sg) for c, a, sg in FEAT)
    if d: v.co += v.normal * d
bmesh.ops.smooth_vert(bm, verts=bm.verts, factor=0.3, use_axis_x=True, use_axis_y=True, use_axis_z=True)
bm.to_mesh(hme_); bm.free(); hme_.materials.append(SKIN); hme_.shade_smooth()
# oreilles (inclinées vers l'arrière, creux de conque)
for sx in (1, -1):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, location=(sx*0.094, 0.016, 1.668))
    ea = bpy.context.active_object; ea.name = "HD_Ear"; ea.scale = (0.009, 0.019, 0.03); ea.rotation_euler = (math.radians(-12), 0, math.radians(sx*-18))
    bme = bmesh.new(); bme.from_mesh(ea.data)
    for v in bme.verts:
        if v.co.x*sx > 0.2: v.co.x -= sx*0.55*math.exp(-((v.co.y)**2 + (v.co.z*0.8)**2)/0.35)   # conque
    bme.to_mesh(ea.data); bme.free(); ea.data.materials.append(SKIN); ea.data.shade_smooth()
    for c in ea.users_collection: c.objects.unlink(ea)
    col.objects.link(ea)
ext  = to_mesh(ext_o, "HD_HandsFeet", SKIN)

# Cheveux : coque prise sur le crâne, plus épaisse sur le dessus, texture de mèches
import random; random.seed(3)
from mathutils import noise
HL = [(-0.12, 1.757), (-0.07, 1.754), (-0.04, 1.735), (-0.01, 1.716), (0.025, 1.70), (0.05, 1.67), (0.08, 1.645), (0.2, 1.64)]
def hairline(p):
    y = p.y
    if y <= HL[0][0]: z = HL[0][1]
    elif y >= HL[-1][0]: z = HL[-1][1]
    else:
        for (y0, z0), (y1, z1) in zip(HL, HL[1:]):
            if y0 <= y <= y1:
                t = (y - y0)/(y1 - y0); t = t*t*(3 - 2*t); z = z0 + (z1 - z0)*t; break
    return z + (0.008*min(1, abs(p.x)/0.07) if y < -0.05 else 0)   # golfes frontaux
bm = bmesh.new(); bm.from_mesh(head.data); bm.normal_update()
for v in bm.verts:
    t = max(0.0, min(1.0, (v.co.z - 1.70) / 0.11))
    u = (v.co.z - hairline(v.co)) / 0.006; u = max(0.0, min(1.0, 0.5 + 0.5*u)); u = u*u*(3 - 2*u)
    if u < 1.0:
        v.co += v.normal * (-0.004 + (0.004 + 0.004 + 0.022*t) * u); continue
    n = (noise.noise(v.co * 55.0) * 0.004 + noise.noise(v.co * 160.0) * 0.0015) * t
    v.co += v.normal * (0.004 + 0.022*t + n)
    if v.co.y < -0.06 and v.co.z > 1.76: v.co.z += 0.006*t           # mèche avant relevée
bmesh.ops.smooth_vert(bm, verts=bm.verts, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
hme = bpy.data.meshes.new("HD_HairMesh"); bm.to_mesh(hme); bm.free()
hair = bpy.data.objects.new("HD_HairMesh", hme); col.objects.link(hair); hme.materials.append(HAIR); hme.shade_smooth()

# Yeux : calés par lancer de rayon sur le visage
from mathutils.bvhtree import BVHTree
bvh = BVHTree.FromObject(head, bpy.context.evaluated_depsgraph_get())
for sx in (1, -1):
    hit = bvh.ray_cast(Vector((sx*0.036, -0.3, 1.682)), Vector((0, 1, 0)))[0]
    fy = hit.y if hit else -0.086
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.0118, location=(sx*0.036, fy + 0.0118 - 0.0045, 1.682))
    e = bpy.context.active_object; e.name = "HD_Eye"; e.data.materials.append(SCLE); e.data.shade_smooth()
    for c in e.users_collection: c.objects.unlink(e)
    col.objects.link(e)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.0056, location=(sx*0.036, fy - 0.0043, 1.682))
    i = bpy.context.active_object; i.name = "HD_Iris"; i.scale = (1, 0.35, 1); i.data.materials.append(IRIS)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.0023, location=(sx*0.036, fy - 0.0051, 1.682))
    pu = bpy.context.active_object; pu.name = "HD_Pupil"; pu.scale = (1, 0.3, 1); pu.data.materials.append(PUPIL)
    for c in pu.users_collection: c.objects.unlink(pu)
    col.objects.link(pu)
    for c in i.users_collection: c.objects.unlink(i)
    col.objects.link(i)

# --- Vêtements : coques décollées du corps -----------------------------------
def shell(src, name, keep, offset, thick, mats, assign, cuts=()):
    bm = bmesh.new(); bm.from_mesh(src.data); bm.normal_update()
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if not keep(f.calc_center_median(), f.normal)], context='FACES')
    for _ in range(3): bmesh.ops.smooth_vert(bm, verts=bm.verts, factor=0.6, use_axis_x=True, use_axis_y=True, use_axis_z=True)
    bm.normal_update()
    for v in bm.verts: v.co += v.normal * offset
    for (sub, co, no) in cuts:
        g = [e for e in bm.edges if sub(e.verts[0].co) and sub(e.verts[1].co)] + [f for f in bm.faces if sub(f.calc_center_median())] + [v for v in bm.verts if sub(v.co)]
        bmesh.ops.bisect_plane(bm, geom=g, plane_co=co, plane_no=no, clear_inner=True)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); col.objects.link(ob)
    for mm in mats: me.materials.append(mm)
    for p in me.polygons: p.material_index = assign(p.center, p.normal)
    me.shade_smooth()
    s = ob.modifiers.new("Epaisseur", 'SOLIDIFY'); s.thickness = thick; s.offset = -1
    return ob

def in_shirt(c, n):
    x, y, z = abs(c.x), c.y, c.z
    if z < 1.03 or z > 1.575: return False
    if x > 0.19 and z < 1.20: return False           # bas de manche (recoupé ensuite)
    if math.hypot(c.x, c.y - 0.005) < 0.074 and z > 1.47: return False   # col
    return True
def shirt_mat(c, n):
    x, z = abs(c.x), c.z
    if x > 0.185 or (z > 1.30 and x > 0.175 - 0.72*(z - 1.36)): return 1   # raglan foncé
    ang = math.degrees(math.atan2(x, -(c.y - 0.012)))
    if 64 < ang < 116 and z < 1.375 - 0.25*max(0, ang - 95)/27*0.2 and x < 0.2: return 2   # panneau bleu (flancs)
    return 0
arm = (Vector((0.205, 0.005, 1.45)) - Vector((0.278, 0.03, 1.13))).normalized()
def sleeve_cut(sx):
    co = Vector((0.205, 0.005, 1.45)).lerp(Vector((0.278, 0.03, 1.13)), (1.45 - 1.255)/0.32); co.x *= sx
    no = arm.copy(); no.x *= sx
    return (lambda p, sx=sx: p.x*sx > 0.19, co, no)
shirt = shell(body, "HD_Shirt", in_shirt, 0.0035, 0.003, [SHIRT, RAGL, BLUE], shirt_mat, cuts=(sleeve_cut(1), sleeve_cut(-1)))

def in_shorts(c, n):
    return 0.56 < c.z < 1.045 and abs(c.x) < 0.24
def shorts_mat(c, n): return 1 if c.z > 1.022 else 0
shorts = shell(body, "HD_Shorts", in_shorts, 0.0065, 0.004, [SHORT, BLUE], shorts_mat, cuts=((lambda p: p.z < 0.66, Vector((0, 0, 0.595)), Vector((0, 0, 1))),))

# Col côtelé : tube qui suit exactement le bord de l'encolure
sm_ = bmesh.new(); sm_.from_mesh(shirt.data)
ne = [e for e in sm_.edges if e.is_boundary and all(v.co.z > 1.42 and math.hypot(v.co.x, v.co.y) < 0.13 for v in e.verts)]
cme = bpy.data.meshes.new("HD_CollarPath"); idx = {}
vs = []
for e in ne:
    for v in e.verts:
        if v.index not in idx: idx[v.index] = len(vs); vs.append(v.co.copy())
cme.from_pydata(vs, [(idx[e.verts[0].index], idx[e.verts[1].index]) for e in ne], []); sm_.free()
bc = bmesh.new(); bc.from_mesh(cme)
for _ in range(25): bmesh.ops.smooth_vert(bc, verts=bc.verts, factor=0.6, use_axis_x=True, use_axis_y=True, use_axis_z=True)
bc.to_mesh(cme); bc.free()
cl = bpy.data.objects.new("HD_Collar", cme); col.objects.link(cl)
bpy.ops.object.select_all(action='DESELECT'); cl.select_set(True); bpy.context.view_layer.objects.active = cl
bpy.ops.object.convert(target='CURVE')
cl = bpy.context.active_object; cl.data.bevel_depth = 0.0055; cl.data.bevel_resolution = 3
for sp in cl.data.splines: sp.use_smooth = True
cl.data.materials.append(RAGL)

# Vue de face
for w in bpy.context.window_manager.windows:
    for a in w.screen.areas:
        if a.type == 'VIEW_3D':
            sp = a.spaces.active; sp.shading.type = 'SOLID'; sp.shading.color_type = 'MATERIAL'
            r = sp.region_3d; r.view_perspective = 'ORTHO'; r.view_location = (0, 0, 0.92)
            r.view_distance = 2.3; r.view_rotation = (0.7071, 0.7071, 0, 0); a.tag_redraw()
print("OK", {o.name: len(o.data.polygons) for o in col.objects if o.type == 'MESH'})
