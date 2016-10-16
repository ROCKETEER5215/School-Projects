# FILENAME: model.py
# BY: Andrew Holbrook
# DATE: 9/24/2015

import ctypes
from OpenGL import GL
from . import GLWindow, Vector4, Matrix4

class Model(object):
    """Class for representing a Wavefront OBJ object.
    """
    def __init__(self):
        self.parts = []
        self.normals = []
        self.num_indices = 0
    
    def __str__(self):
        return str(self.num_indices)
    
    def getNumParts(self):
        return len(self.parts)
    
    def getNumIndices(self):
        return self.num_indices
    
    def getNumVertices(self):
        num_verts = 0
        for p in self.parts:
            num_verts += len(p.vertices)
        
        return num_verts
    
    def getVertexList(self):
        tmpList = []
        for p in self.parts:
            tmpList += p.vertices
        
        return tmpList
    
    def getIndexList(self):
        tmpList = []
        for p in self.parts:
            tmpList += p.indices
        
        return tmpList
    
    def getNormalList(self):
        return self.normals
    
    def addPart(self, p):
        self.parts.append(p)
        self.num_indices += p.getNumIndices()
    

    def generateNormals(self):
        tmpList = [Vector4(),] * (self.getNumVertices() // 3)
        indexList = self.getIndexList()
        vertexList = self.getVertexList()
        for i in range(0, self.getNumIndices(), 3):
            idx0, idx1, idx2 = indexList[i:i + 3]
            v0 = Vector4(vertexList[idx0 * 3:idx0 * 3 + 3])
            v1 = Vector4(vertexList[idx1 * 3:idx1 * 3 + 3])
            v2 = Vector4(vertexList[idx2 * 3:idx2 * 3 + 3])

            v01 = v1 - v0
            v12 = v2 - v1
            normal = v01.cross(v12)

            tmpList[idx0] += normal
            tmpList[idx1] += normal
            tmpList[idx2] += normal

        for n in tmpList:
            n.normalize()
            self.normals += n.getXYZ()



        # IMPLEMENT ME!
    
    def loadToVRAM(self):
        """Create the OpenGL objects for rendering this model.
        """
        
        # Create vertex array object to encapsulate the state needed to provide
        # vertex information.
        self.vertexArrayObject = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vertexArrayObject)

        self.positionBuffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.positionBuffer)
        c_vertexArray = ctypes.c_float * (3 * self.getNumIndices())
        c_vertexArray = c_vertexArray(*self.getVertexList())
        GL.glBufferData(GL.GL_ARRAY_BUFFER, c_vertexArray, GL.GL_STATIC_DRAW)
        del c_vertexArray

        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 0, None)



        self.normalBuffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.normalBuffer)
        c_normalArray = ctypes.c_float * (3 * self.getNumIndices())
        c_normalArray = c_normalArray(*self.getNormalList())
        GL.glBufferData(GL.GL_ARRAY_BUFFER, c_normalArray, GL.GL_STATIC_DRAW)
        del c_normalArray

        GL.glVertexAttribPointer(2, 3, GL.GL_FLOAT, False, 0, None)

        # postition vertex buffer object
        
        # read and copy vertex data to VRAM


        # position data is associated with location 0
        
        # color vertex buffer object
        self.colorBuffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.colorBuffer)
        
        # load blue color for each vertex and copy data to VRAM
        blue = (0.0, 0.5, 0.5)
        vcolors = ctypes.c_float * (3 * self.getNumIndices())
        vcolors = vcolors(*(blue * self.getNumIndices()))
        
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vcolors, GL.GL_STATIC_DRAW)
        del vcolors
        
        # color data is associated with location 1
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, False, 0, None)

        
        self.indexBuffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.indexBuffer)
        
        c_indexArray = ctypes.c_uint * self.getNumIndices()
        c_indexArray = c_indexArray(*self.getIndexList())
        
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, c_indexArray, GL.GL_STATIC_DRAW)
        del c_indexArray
        
        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)
        GL.glEnableVertexAttribArray(2)
        
        GL.glBindVertexArray(0)
    
    def renderPartByIndex(self, index):
        GL.glBindVertexArray(self.vertexArrayObject)
        
        offset = 0
        for i in range(0, index):
            offset += self.parts[i].getNumIndices()
        
        c_offset = ctypes.c_void_p(offset * ctypes.sizeof(ctypes.c_uint))
        GL.glDrawElements(GL.GL_TRIANGLES, self.parts[index].getNumIndices(), GL.GL_UNSIGNED_INT, c_offset)
        
        GL.glBindVertexArray(0)
        
    def renderPartByName(self, name):
        GL.glBindVertexArray(self.vertexArrayObject)
        
        offset = 0
        for p in self.parts:
            if p.name == name:
                c_offset = ctypes.c_void_p(offset * ctypes.sizeof(ctypes.c_uint))
                GL.glDrawElements(GL.GL_TRIANGLES, p.getNumIndices(), GL.GL_UNSIGNED_INT, c_offset)
                break
            
            offset += p.getNumIndices()
        
        GL.glBindVertexArray(0)
    
    def renderAllParts(self):
        GL.glBindVertexArray(self.vertexArrayObject)
        
        GL.glDrawElements(GL.GL_TRIANGLES, self.getNumIndices(), GL.GL_UNSIGNED_INT, None)
        
        GL.glBindVertexArray(0)

class ModelPart(object):
    """Represents a part (object) from the obj file.
    """
    def __init__(self):
        self.name = None
        self.vertices = []
        self.indices = []
    
    def getNumIndices(self):
        return len(self.indices)
    
    def setName(self, name):
        self.name = name
    
    def addVertex(self, v):
        self.vertices.append(v)
    
    def addIndex(self, i):
        self.indices.append(i)

class OBJReader(object):
    
    @staticmethod
    def readFile(file):
        """Reads an .obj file and returns the data as a Model object.
        """
        model = Model()
        currentPart = None
        
        fp = open(file)
        
        for line in fp:
            if line[0:2] == 'v ':
                verts = line.split()
                for i in range(1, len(verts)):
                    currentPart.addVertex(float(verts[i]))
            elif line[0] == 'f':
                indices = line.split()
                for i in range(1, len(indices)):
                    currentPart.addIndex(int(indices[i]) - 1)
            elif line[0] == 'o':
                if currentPart == None:
                    currentPart = ModelPart()
                else:
                    model.addPart(currentPart)
                    currentPart = ModelPart()
                
                currentPart.setName(line.split()[1])
                
        fp.close()
        
        if currentPart != None:
            model.addPart(currentPart)
        
        model.generateNormals()
        
        return model