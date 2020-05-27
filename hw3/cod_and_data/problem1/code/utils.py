
'''
structs for storing objects class
'''
verbose=True
class obj:
    def __init__(self):
        self.vertices=None
        self.vertices_texture=None
        self.vertices_normal=None
        self.vertices_point=None 
        self.material=None
        self.objects=None

class material:
    def __init__(self):
        self.type=None
        self.data=None

class object:
    def __init__(self):
        self.type=None
        self.data=obj_data()

class obj_data:
    def __init__(self):
        self.vertices=None  
        self.texture=None
        self.normal=None



'''
    Remove empty cells, merge lines split by "\" and convert strings with values to double
 '''
def readfile(filename):
# return (ftype, fdata)
    file_words = []
    ftype = []
    fdata = []
    with open(filename, 'r') as f:
        lines = f.readlines() + [""]
        i = 0 
        print("tot lines: {}".format(len(lines)))
        while(i < len(lines)):            
            curr_line = lines[i].strip()
            i += 1
            # remove empty lines
            if len(curr_line) is 0:
                continue
            # print comments
            if(curr_line[0] in ['#','$']):
                print(curr_line)
                continue

            line = curr_line
            # merge split lines
            while(line[-1] is '/'):
                curr_line = lines[i].strip()
                line = line[:-1] + ' ' + curr_line
                i+=1
            # remove empty lines
            # split into ftype, fdata
            splitline = line.split()
            itype = splitline[0]
            # fixlines
            data = np.array(splitline[1:],dtype="float64")

            ftype.append(itype) 
            fdata.append(data)
    return (ftype, fdata)


# return concatenated filefolder and each name in data
def fullfile(filefolder,data):
    if type(data) is str:
        return os.path.join(filefolder,data)    

    filename_mtl=[]
    for d in data:
        filename_mtl.append(os.path.join(filefolder,d))
    return filename_mtl


# return 
# read Wavefront OBJ file, return list of objects
def readmtl(filename_mtl,verbose):
    vprint('Reading Material file : {}'.format(filename_mtl))

    # Remove empty cells, merge lines split by "\" and convert strings with values to double
    (ftype, fdata)= fixlines(filename_mtl)

    # Surface data
    objects=[]
    no=0

    # Loop through the Wavefront object file
    for iline in range(len(ftype)):
        itype=ftype[iline]
        data=fdata[iline]
        
        # Switch on data type line
        if itype in ['#','$']:
            # Comment
            tline=['  #']
            if type(data) is not list:
                data = [data]
            for i in range(len(data)):
                tline+=[' ', data[i]]                
            vprint(tline)
        elif itype is '':
                pass
        else:
            objects.append(object())
            obj[no].type=itype
            obj[no].data=data
            no+=1
            vprint('Finished Reading Material file')
    return objects


'''
WRITE FUNCTION HELPERS
'''

def write_MTL_file(f,material):
    comments=[None for i in range(2)]
    comments[1]=' Produced by Matlab Write Wobj exporter '
    comments[2]=''
    write_comment(f,comments)
    assert(len(material) is 0)

'''
    write comment
'''
def write_comment(f,comments):
    for comment in comments:
        line='# {}\n'.format(comment)
        f.write(line)

        
'''
    write vertices into file
'''
def write_vertices(f,V,itype):
    # V: (shape: (n,nv))
    nv,vert=V.shape
    if vert==1:
        for i in range(nv):
            line='{0} {1:5}\n'.format(itype,V[i,0])
            f.write(line)
        end
    elif vert==2:
        for i in range(nv):
            line='{0} {1:5} {2:5}\n'.format(itype,V[i,0],V[i,1])
            f.write(line)
        end
    elif vert==3:
        for i in range(nv):
            line='{0} {1:5} {2:5} {3:5}\n'.format(
                itype,V[i,0],V[i,1],V[i,2])
            f.write(line)
    else:
        pass

    if itype is 'v':
        line='# {} vertices \n'.format(nv)
        f.write(line)
    elif itype is 'vt':
        line='# {} texture vertices \n'.format(nv)
        f.write(line)
    elif itype is 'vn':
        line='# {} normals \n'.format(nv)
        f.write(line)
    else:
        line='# {}\n'.format(nv)
        f.write(line)
#UTILSS