from ..output_node import UMOGOutputNode
import bpy
import bmesh

class BMeshCurlNode(UMOGOutputNode):
    bl_idname = "umog_BMeshCurlNode"
    bl_label = "BMesh Curl Node"

    mesh_name = bpy.props.StringProperty()
    mesh_dupl_name = bpy.props.StringProperty()

    mesh_name_index = bpy.props.IntProperty()

    mod_list_handle = bpy.props.IntProperty()

    def init(self, context):
        self.inputs.new("TextureSocketType", "Input")
        super().init(context)

    def draw_buttons(self, context, layout):
        # layout.operator("umog.select_mesh", text = "Select Mesh").pnode = self.name
        layout.prop_search(self, "mesh_name", bpy.data, "objects", icon="MESH_CUBE", text="")

    def update(self):
        pass

    def execute(self, refholder):
        try:
            print("sculpt node execution, mesh: " + self.mesh_name)
        except:
            pass
        try:
            fn = self.inputs[0].links[0].to_socket
            texture_handle = fn.texture_index
            # copy the mesh and hid the original
        except:
            print("no texture as input")

        bm = bmesh.new()  # create an empty BMesh
        bm.from_mesh(bpy.data.meshes[bpy.data.objects[self.mesh_name].data.name])

        # bmesh.ops.inset_region(bm, faces=bm.faces, thickness=0.4)
        # bmesh.ops.inset_region(bm, faces=bm.faces, thickness=0, depth=-0.5)
        bmesh.ops.poke(bm, faces=bm.faces)

        cx, cy = 0, 0
        tr = bpy.context.scene.TextureResolution - 1
        for vert in bm.verts:
            # displace along normal by texture
            factor = (refholder.np2dtextures[texture_handle].item(cx, cy, 3)) + 0.1
            # print("factor: " + str(factor) + " x:" + str(cx) + " y:" + str(cy))
            # print("shell factor: " + str(vert.calc_shell_factor()))
            if vert.calc_shell_factor() > 1.01:
                vert.co = vert.co + (factor * vert.normal)
                if cx == tr:
                    cx = 0
                    cy = cy + 1
                else:
                    cx = cx + 1

                if cy == tr:
                    cy = 0

        bm.to_mesh(bpy.data.meshes[bpy.data.objects[self.mesh_name].data.name])
        bm.free()

    def preExecute(self, refholder):
        pass