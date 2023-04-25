import omni.ext
import omni.ui as ui
from .MeshGen.sdf_to_mesh import mc_result


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

                def assemble():
                    stage = omni.usd.get_context().get_stage()

                    infile = open('hihihi.obj','r')
                    data = infile.read()
                    print(data)
                
                    omni.kit.commands.execute('CreateMeshPrimWithDefaultXform',
                        prim_type='Cube',
                        prim_path=None,
                        select_new_prim=True,
                        prepend_default_prim=True)
                    
                    omni.kit.commands.execute('MovePrim',
                        path_from='/World/Cube',
                        path_to='/World/Trail',
                        destructive=False)

                    cube_prim = stage.GetPrimAtPath('/World/Trail')


                    face_vert_count = [3]*len(faces)

                    primvar = [(0,0)]*len(faces)

                    attributes = ['faceVertexCounts', 'faceVertexIndices', 'normals', 'points', 'primvars:st']

                    cube_prim.GetAttribute('faceVertexCounts').Set(face_vert_count)
                    cube_prim.GetAttribute('faceVertexIndices').Set(faces)
                    cube_prim.GetAttribute('normals').Set(normals)
                    cube_prim.GetAttribute('points').Set(verts)
                    cube_prim.GetAttribute('primvars:st').Set(primvar)


                with ui.HStack():
                    ui.Button("TRANSFORMERS!!!", clicked_fn=assemble)

        

    def on_shutdown(self):
        print("[mesh.to.usd] mesh to usd shutdown")
