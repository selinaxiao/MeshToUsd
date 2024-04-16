import omni.ext
import omni.ui as ui
import omni.usd
#from .MeshGen.sdf_to_mesh import mc_result

from pxr import Gf, Sdf


# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[mesh.to.usd] some_public_function was called with x: ", x)
    return x ** x


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MeshToUsdExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[mesh.to.usd] mesh to usd startup")

        self._count = 0

        self._window = ui.Window("My Window", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                label = ui.Label("")
                
                def process(path):
                    infile = open(path,'r')
                    lines = infile.readlines()

                    for i in range(len(lines)):
                        lines[i] = lines[i].replace('\n','').split(' ')[1:]

                    if [] in lines:
                        lines.remove([])

                    idx1 = lines.index(['Normals'])
                    verts = lines[1:idx1]
                    float_verts = []
                    for i in range(len(verts)):
                        float_verts.append(Gf.Vec3f(float(verts[i][0]), float(verts[i][1]), float(verts[i][2])))

                    idx2 = lines.index(['Faces'])
                    normals = lines[idx1+1:idx2]
                    float_norms = []
                    print(normals)
                    for i in range(len(normals)):
                        float_norms.append(Gf.Vec3f(float(normals[i][0]), float(normals[i][1]), float(normals[i][2])))
                        float_norms.append(Gf.Vec3f(float(normals[i][0]), float(normals[i][1]), float(normals[i][2])))
                        float_norms.append(Gf.Vec3f(float(normals[i][0]), float(normals[i][1]), float(normals[i][2])))

                    faces = lines[idx2+1:]
                    int_faces = []
                    for i in range(len(faces)):
                        int_faces.append(int(faces[i][0]) - 1)
                        int_faces.append(int(faces[i][1]) - 1)
                        int_faces.append(int(faces[i][2]) - 1)

                    print(type(float_verts))
                    print(float_verts)

                    return float_verts, int_faces, float_norms


                def assemble():
                    stage = omni.usd.get_context().get_stage()

                    if(not stage.GetPrimAtPath(Sdf.Path('/World/Trial')).IsValid()):
                        omni.kit.commands.execute('CreateMeshPrimWithDefaultXform',
                            prim_type='Cube',
                            prim_path=None,
                            select_new_prim=True,
                            prepend_default_prim=True)
                        
                        omni.kit.commands.execute('MovePrim',
                            path_from='/World/Cube',
                            path_to='/World/Trial',
                            destructive=False)

                    cube_prim = stage.GetPrimAtPath('/World/Trial')

                    verts, faces, normals = process('C:/users/labuser/desktop/data transfer/meshtousd/exts/mesh.to.usd/mesh/to/usd/whyyyyyyyareumeaningless.obj')


                    face_vert_count = [3]*(len(faces)//3)

                    primvar = [(0,0)]*len(faces)


                    print(type(cube_prim.GetAttribute('faceVertexIndices').Get()))
                    print(cube_prim.GetAttribute('faceVertexIndices').Get())
                    print(type(face_vert_count))

                    cube_prim.GetAttribute('faceVertexCounts').Set(face_vert_count)
                    cube_prim.GetAttribute('faceVertexIndices').Set(faces)
                    cube_prim.GetAttribute('normals').Set(normals)
                    cube_prim.GetAttribute('points').Set(verts)
                    cube_prim.GetAttribute('primvars:st').Set(primvar)


                with ui.HStack():
                    ui.Button("TRANSFORMERS!!!", clicked_fn=assemble)

        

    def on_shutdown(self):
        print("[mesh.to.usd] mesh to usd shutdown")
