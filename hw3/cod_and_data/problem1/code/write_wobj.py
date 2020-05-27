import numpy as np
import os
from utils import *


def write_wobj(OBJ,fullfilename):
    # Write objects to a Wavefront OBJ file
    #
    # write_wobj(OBJ,filename);
    #
    # OBJ struct containing:
    #
    # OBJ.vertices : Vertices coordinates
    # OBJ.vertices_texture: Texture coordinates
    # OBJ.vertices_normal : Normal vectors
    # OBJ.vertices_point  : Vertice data used for points and lines
    # OBJ.material : Parameters from external .MTL file,will contain parameters like
    #           newmtl,Ka,Kd,Ks,illum,Ns,map_Ka,map_Kd,map_Ks,
    #           example of an entry from the material object:
    #       OBJ.material(i).type=newmtl
    #       OBJ.material(i).data='vase_tex'
    # OBJ.objects  : Cell object with all objects in the OBJ file,
    #           example of a mesh object:
    #       OBJ.objects(i).type='f'
    #       OBJ.objects(i).data.vertices: [n x 3 double]
    #       OBJ.objects(i).data.texture:  [n x 3 double]
    #       OBJ.objects(i).data.normal:   [n x 3 double]
    #
    # example reading/writing,
    #
    #   OBJ=read_wobj('examples\example10.obj');
    #   write_wobj(OBJ,'test.obj');
    #
    # example isosurface to obj-file,
    #
    #   # Load MRI scan
    #   load('mri','D'); D=smooth3(squeeze(D));
    #   # Make iso-surface (Mesh) of skin
    #   FV=isosurface(D,1);
    #   # Calculate Iso-Normals of the surface
    #   N=isonormals(D,FV.vertices);
    #   L=sqrt(N(:,1).^2+N(:,2).^2+N(:,3).^2)+eps;
    #   N(:,1)=N(:,1)./L; N(:,2)=N(:,2)./L; N(:,3)=N(:,3)./L;
    #   # Display the iso-surface
    #   figure,patch(FV,'facecolor',[1 0 0],'edgecolor','none'); view(3);camlight
    #   # Invert Face rotation
    #   FV.faces=[FV.faces(:,3) FV.faces(:,2) FV.faces(:,1)];
    #
    #   # Make a material structure
    #   material(1).type='newmtl';
    #   material(1).data='skin';
    #   material(2).type='Ka';
    #   material(2).data=[0.8 0.4 0.4];
    #   material(3).type='Kd';
    #   material(3).data=[0.8 0.4 0.4];
    #   material(4).type='Ks';
    #   material(4).data=[1 1 1];
    #   material(5).type='illum';
    #   material(5).data=2;
    #   material(6).type='Ns';
    #   material(6).data=27;
    #
    #   # Make OBJ structure
    #   clear OBJ
    #   OBJ.vertices=FV.vertices;
    #   OBJ.vertices_normal=N;
    #   OBJ.material=material;
    #   OBJ.objects(1).type='g';
    #   OBJ.objects(1).data='skin';
    #   OBJ.objects(2).type='usemtl';
    #   OBJ.objects(2).data='skin';
    #   OBJ.objects(3).type='f';
    #   OBJ.objects(3).data.vertices=FV.faces;
    #   OBJ.objects(3).data.normal=FV.faces;
    #   write_wobj(OBJ,'skinMRI.obj');
    #
    # Function is written by D.Kroon University of Twente (June 2010)

    # assert(not os.path.isfile(fullfilename))
    filefolder,filename=os.path.split(fullfilename)
    vprint('Reading Object file : []'.format(fullfilename))

    comments=['' for i in range(4)]
    comments[1]=' Produced by Matlab Write Wobj exporter '
    comments[2]=''

    vprint("Writing comments")
    f=open(fullfilename,'w')
    write_comment(f,comments)

    vprint("Writing materials")
    if hasattr(OBJ,'material') and (len(OBJ.material)>0):
        filename_mtl=fullfile(filefolder,[filename,'.mtl'])
        line='mtllib {}\n'.format(filename_mtl)
        f.write(line)

    vprint("Writing vertices")
    if hasattr(OBJ,'vertices') and (len(OBJ.vertices)>0):
        print("writing????")
        write_vertices(f,OBJ.vertices,'v')

    vprint("Writing vertices point")
    if hasattr(OBJ,'vertices_point') and (len(OBJ.vertices_point)>0):
        write_vertices(f,OBJ.vertices_point,'vp')

    vprint("Writing vertices normal")
    if hasattr(OBJ,'vertices_normal') and (len(OBJ.vertices_normal)>0):
        write_vertices(f,OBJ.vertices_normal,'vn')

    vprint("Writing vertices texture")
    if hasattr(OBJ,'vertices_texture') and (len(OBJ.vertices_texture)>0):
        write_vertices(f,OBJ.vertices_texture,'vt')

    vprint("Writing objects")
    for i in range(len(OBJ.objects)):
        itype=OBJ.objects[i].type
        data=OBJ.objects[i].data
        if itype is 'usemtl':
            f.write('usemtl {}\n'.format(data))
        elif itype is 'f':
            check1=hasattr(OBJ,'vertices_texture') and len(OBJ.vertices_texture)>0
            check2=hasattr(OBJ,'vertices_normal') and len(OBJ.vertices_normal)>0
            nv,vert=data.vertices.shape
            if(check1 and check2):
                for j in range(nv):
                    f.write('f {}/{}/{}'.format(data.vertices[j,0],
                            data.texture[j,0],data.normal[j,0]))
                    f.write(' {}/{}/{}',data.vertices[j,1],
                            data.texture[j,1],data.normal[j,1])
                    f.write(' {}/{}/{}\n',data.vertices[j,2],
                            data.texture[j,2],data.normal[j,2])
            elif(check1):
                for j in range(nv):
                    f.write('f {}/{}'.format(data.vertices[j,0],
                            data.texture[j,0]))
                    f.write(' {}/{}',data.vertices[j,1],
                            data.texture[j,1])
                    f.write(' {}/{}\n',data.vertices[j,2],
                            data.texture[j,2])
            elif(check2):
                for j in range(nv):
                    f.write('f {}//{}',data.vertices[j,0],
                            data.normal[j,0])
                    f.write(' {}//{}',data.vertices[j,1],
                            data.normal[j,1])
                    f.write(' {}//{}\n',data.vertices[j,2],
                            data.normal[j,2])
            else:
                for j in range(nv):
                    f.write('f {} {} {}\n'.format(int(data.vertices[j,0]),
                            int(data.vertices[j,1]),int(data.vertices[j,2])))

        else:
            f.write('{} ',itype)
            if(type(data) is not list):
                data = [data]
            for j in range(len(data)):
                f.write('{:5} '.format(data[j]))
            f.write('\n')
    f.close()
    vprint("Finished writing")

