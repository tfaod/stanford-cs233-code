'''
 Read the objects from a Wavefront OBJ file

 OBJ=read_wobj(filename);

 OBJ struct containing:

 OBJ.vertices : Vertices coordinates
 OBJ.vertices_texture: Texture coordinates
 OBJ.vertices_normal : Normal vectors
 OBJ.vertices_point  : Vertice data used for points and lines
 OBJ.material : Parameters from external .MTL file, will contain parameters like
           newmtl, Ka, Kd, Ks, illum, Ns, map_Ka, map_Kd, map_Ks,
           example of an entry from the material object:
       OBJ.material(i).type = newmtl
       OBJ.material(i).data = 'vase_tex'
 OBJ.objects  : Cell object with all objects in the OBJ file,
           example of a mesh object:
       OBJ.objects(i).type='f'
       OBJ.objects(i).data.vertices: [n x 3 double]
       OBJ.objects(i).data.texture:  [n x 3 double]
       OBJ.objects(i).data.normal:   [n x 3 double]

 Example,
   OBJ=read_wobj('examples\example10.obj');
   FV.vertices=OBJ.vertices;
   FV.faces=OBJ.objects(3).data.vertices;
   figure, patch(FV,'facecolor',[1 0 0]); camlight

 Function is written by D.Kroon University of Twente (June 2010)