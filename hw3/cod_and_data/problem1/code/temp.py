import numpy as np
import os
# imposrt pymesh
# import pywavefront
from utils import *

# return OBJ

# verbose print


def vprint(*val):
    if verbose:
        print(*val)

fullfilename=os.path.join(os.getcwd(), 'problem1/data/100chairs/100.obj',)


def read_wobj(fullfilename):

    verbose=True

    # read file, assert existence
    assert(os.path.isfile(fullfilename))
    filefolder=os.path.dirname(fullfilename)
    vprint('Reading Object file : []'.format(fullfilename))

    # fixlines
    #


    # Read the DI3D OBJ textfile to a cell array
    # Remove empty cells, merge lines split by "\" and convert strings with
    # values to double
    ftype, fdata=readfile(fullfilename)
    vprint("Finished reading ftype, fdata")

    # Vertex data
    vertices=None
    nv=0
    vertices_texture=None
    nvt=0
    vertices_point=None
    nvp=0
    vertices_normal=None
    nvn=0
    material=None
    v_ct=0
    vt_ct=0
    vp_ct=0
    vn_ct=0
    objects=[]
    nobjects=0

    # Surface data
    no=0

    def extend_array(arr, datalen, num=10000):
        if arr is None:
            return np.zeros((num, datalen))
        return np.stack(arr, np.zeros((num, datalen)))

    seen_types=set([])
    # Loop through the Wavefront object file
    print("Looping through Wavefront object file")
    # decrement everything by 1
    for iline in range(len(ftype)):
        if(iline % 10000==0):
            vprint(['Lines processed : []'.format(iline)])

        itype=ftype[iline]
        data=fdata[iline]
        seen_types.add(itype)

        # Switch on data type line
        if (itype is 'mtllib'):
            datanew=[]
            for i in range(len(data)):
                datanew+=[data[i], ' ']
            # verbose
            material=[]
            for d in datanew[:-1]:
                fp=os.path.join(filefolder, d)
                vprint(fp)
                material.append(pywavefront.Wavefront(fp))
        elif(itype is 'v'):  # vertices
            # 3 or 4
            datalen=len(data)
            if v_ct is 0:
                v_ct=datalen
            assert(v_ct==datalen)

            # Extend size
            if(nv % 10000==0):
                vertices=extend_array(vertices, v_ct)

            # Add to vertices list X Y Z or X Y Z W
            vertices[nv, :datalen]=data
            nv=nv + 1
        elif(itype is 'vp'):
            # Specifies a point in the parameter space of curve or surface
            #  1, 2, or 3
            datalen=len(data)
            if vp_ct is 0:
                vp_ct=datalen
            assert(vp_ct==datalen)

            # Extend
            if(mod(nvp, 10000)==0):
                vertices_point=extend_array(vertices_point, vp_ct)

            # Add to vertices point list U or U V or U V W
            vertices_point[nvp, 0:datalen]=data

            nvp=nvp + 1
        elif(itype is 'vn'):
            # A normal vector
            vn_ct=3
            if(nvn % 10000==0):
                vertices_normal=extend_array(vertices_normal, vn_ct)

            # Add to vertices list I J K
            vertices_normal[nvn]=data
            nvn=nvn + 1

        elif(itype is 'vt'):
            # Vertices Texture Coordinate in photo
            # U V W
            datalen=len(data)
            if vt_ct is 0:
                vt_ct=datalen
            assert(vt_ct==datalen)
            if(mod(nvt, 10000)==1):
                vertices_texture=extend_array(vertices_texture, vt_ct)
    #             vt_ct=extend_array(vt_ct, 1)

            # Add to vertices texture list U or U V or U V W
            vertices_texture[nvt]=data
            nvt +=1

        elif(itype is 'l'):
            datalen=len(data)
            if(no % 10000 is 1):
                objects(no + 10001).data=0
            array_vertices=np.zeros(datalen)
            array_texture=[]
            if type(data)is not list:
                data=[data]

            for i in range(len(data)):
                if type(data)is list:
                    tvals=[float(x) for x in data[i].split('/')]
                else:
                    tvals=data[i].item()
                    
                if type(tvals) is not list:
                    tvals=[tvals]
                val=tvals[0]
                val=val+nv if(val<0)else val
                array_vertices[i]=val
                if(len(tvals)> 1):
                    val=tvals[1]
                    val=val + nvt if (val<0)else val
                    array_texture[i]=val

            # tuples in objects
            objects.append(object())
            objects[no].type='l'
            objects[no].data.vertices=array_vertices
            objects[no].data.texture=array_texture
            no+=1

        elif itype is'f':
            # TODO
            datalen=len(data)
            array_vertices=np.zeros(datalen)
            array_texture=[]
            array_normal=[]
            
            if type(data)is str:
                data=[data]
            for i in range(len(data)):
                tvals=[]
                if type(data)is list:
                    tvals=[float(x) for x in data[i].split('/')]
                else:
                    tvals=data[i].item()
                    
                if type(tvals) is not list:
                    tvals=[tvals]
                    
                val=tvals[0]                
                val=val+nv+1 if val<0 else val
                array_vertices[i]=val
                if(len(tvals)>1) and (tvals[1] is not 'inf'):
                    val=tvals[1]
                    val=val+nvt if(val<0)else val
                    array_texture[i]=val
                if(len(tvals)>2):
                    val=tvals(2)
                    val=val+nvn if(val<0)else val
                    array_normal[i]=val

            # A face of more than 3 indices is always split into
            # multiple faces of only 3 indices.
            objects.append(object())
            objects[no].type='f'
            nvert=min(3,len(array_vertices))
            
            objects[no].data.vertices=array_vertices[:nvert]
            if(len(array_texture)>0):
                objects[no].data.texture=array_texture[:nvert]
            if(len(array_normal)>0):
                objects[no].data.normal=array_normal[:nvert]
            no+=1

            for i in range(len(array_vertices)-3):
                findex=np.array([1, 2+i, 3+i])
                indices=np.where(findex>len(array_vertices))
                findex[indices]-=len(array_vertices)
                objects.append(object())
                objects[no].type='f'
                objects[no].data.vertices=array_vertices[findex]
                if(len(array_texture)>0):
                    objects[no].data.texture=array_texture[findex]
                if(len(array_normal)>0):
                    objects[no].data.normal=array_normal[findex]
                no+=1
        elif itype is '#' or itype is'$':
            # Comment
            if type(data)is not list:
                data=[data]
            tline=['  #'] 
            for i in range(len(data)):
                tline+=[' ', data[i]]
            vprint(tline)
        elif itype is '':
            pass
        else:
            objects.append(object())
            objects[no].type=itype
            objects[no].data=data
            no+=1

    # Initialize new object list, which will contain the "collapsed" objects
    objects2=[]
    index=0
    i=0
    while(i<no):
        itype=objects[i].type

        # First face found
        if(itype is 'f'):
            # Get number of faces
            for j in range(i,no):            
                itype=objects[j].type
                if(itype is not 'f'):
                    break
            numfaces=(j-i+1)
            print("numfaces is: {}".format(numfaces))
            
            objects2.append(object())
            objects2[index].type='f'
            # Process last face first to allocate memory        
            objects2[index].data.vertices=np.zeros((numfaces,v_ct))
            objects2[index].data.vertices[numfaces-1]=objects[i].data.vertices
            
            # if nonzero vertex textures
            if(nvt>0):
                objects2[index].data.texture=np.zeros((numfaces,vt_ct))
                objects2[index].data.texture[numfaces]=objects[i].data.texture
            else:
                objects2[index].data.texture=[]
            # if nonzero vertex normals
            if(nvn>0):
                objects2[index].data.normal=np.zeros((numfaces,vt_ct))
                objects2[index].data.normal[numfaces]=objects[i].data.normal
            else:
                objects2[index].data.normal=[]

    #         index+=1
            # All faces to arrays
            for k in range(numfaces):
                objects2.append(object())
                objects2[index].data.vertices[k]=objects[i+k].data.vertices
                if(nvt>0):
                    objects2[index].data.texture[k]=objects[i+k].data.texture
                if(nvn>0):
                    objects2[index].data.normal[k]=objects[i+k].data.normal
            index+=1
            i=j
        else:
            objects2.append(object())
            objects2[index].type=objects[i].type
            objects2[index].data=objects[i].data
            index+=1
        i+=1
    print("Finished looping through Object file")

    # Add all data to output struct
    OBJ=obj()
    OBJ.objects=objects2[:index]
    OBJ.material=[] if material is None else material
    OBJ.vertices=vertices[:nv]
    OBJ.vertices_point=vertices_point[:nvp] if nvp>0 else []
    OBJ.vertices_normal=vertices_normal[:nvn] if nvn>0 else []
    OBJ.vertices_texture=vertices_texture[:nvt] if nvt>0 else []
    vprint('Finished Reading Object file')
    print("num vertices: ", nv)
    print("num vert points: ", nvp)
    print("num vert normal: ", nvn)
    print("num vert texture: ", nvt)
    print("num objects: ", no)
    print("vct is:", v_ct)
    print("seen types are: ", seen_types)
    return OBJ
