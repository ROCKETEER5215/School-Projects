import ctypes
import sdl2
from math import *
import random
from OpenGL import GL
from etgg2801 import *
from etgg2801.Scene import Scene

vsrc=b'''
#version 400

layout (location = 0) in vec3 VertexPosition;
layout (location = 1) in vec3 VertexColor;
layout (location = 2) in vec3 VertexNormal;

out vec3 vcolor;
out vec4 eyeVertex;
out vec4 normal;
uniform mat4 modelview;
uniform mat4 projection;

void main()
{
    eyeVertex = modelview * vec4(VertexPosition, 1.0);
    normal = normalize(modelview * vec4(VertexNormal, 0.0));
    vcolor = VertexColor; // pass color info to frag shader
    gl_Position = projection * eyeVertex;
}
'''

fsrc=b'''
#version 400

const vec4 eyePosition = vec4(0.0, 0.0, 0.0, 1.0);
const float shininess = 50.0f;

in vec3 vcolor;
in vec4 eyeVertex;
in vec4 normal;

uniform vec4 lightPosition;

void main() {
    vec4 lv = normalize(lightPosition - eyeVertex);
    vec4 rm = -reflect(lv, normal);
    vec4 ev = normalize(eyePosition - eyeVertex);
    float dotp = 0.1 + max(dot(lv, normal), 0.0) + pow(max(dot(rm, ev), 0.0), shininess);
    gl_FragColor = vec4(clamp(vcolor * dotp, 0.0, 1.0), 1.0);
}

'''

class MyDelegate(GLWindowRenderDelegate):
    def __init__(self):
        super().__init__()

        self.scene = Scene();


        self.lightPosition = Vector4((0.0, 0.5, 3.0, 1.0))

        self.initShaders()
        
        # location of model matrix in shader program
        self.modelview_loc = GL.glGetUniformLocation(self.shaderProgram, b"modelview")
        self.projection_loc = GL.glGetUniformLocation(self.shaderProgram, b"projection")
        self.lightPosition_loc = GL.glGetUniformLocation(self.shaderProgram, b"lightPosition")

        # set background color to green
        GL.glClearColor(0.0, 1.0, 0.0, 1.0)
        
        # enable face culling (backface by default)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glEnable(GL.GL_DEPTH_TEST)
        
        window = GLWindow.getInstance()
        GL.glViewport(0, 0, window.size[0], window.size[1])
        #for o in self.scene.objects:
        #   o.generateNormals()
    
    def initShaders(self):
        
        # build vertex shader object
        self.vertexShader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        GL.glShaderSource(self.vertexShader, vsrc)
        GL.glCompileShader(self.vertexShader)
        result = GL.glGetShaderiv(self.vertexShader, GL.GL_COMPILE_STATUS)
        if result != 1:
            raise Exception("Error compiling vertex shader")
        
        # build fragment shader object
        self.fragmentShader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
        GL.glShaderSource(self.fragmentShader, fsrc)
        GL.glCompileShader(self.fragmentShader)
        result = GL.glGetShaderiv(self.fragmentShader, GL.GL_COMPILE_STATUS)
        if result != 1:
            raise Exception("Error compiling fragment shader")
        
        # build shader program and attach shader objects
        self.shaderProgram = GL.glCreateProgram()
        GL.glAttachShader(self.shaderProgram, self.vertexShader)
        GL.glAttachShader(self.shaderProgram, self.fragmentShader)
        GL.glLinkProgram(self.shaderProgram)
    
    def cleanup(self):
        GL.glDeleteShader(self.vertexShader)
        GL.glDeleteShader(self.fragmentShader)
        GL.glDeleteProgram(self.shaderProgram)
    
    def update(self, dtime):
        self.scene.update(dtime)

    
    def render(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        
        GL.glUseProgram(self.shaderProgram)
        
        # setup the orthographic projection matrix
        projMatrix = Matrix4.getOrthographic(near=1.0,far=10.0)



        GL.glUniformMatrix4fv(self.projection_loc, 1, False, projMatrix.getCType())
        GL.glUniform4fv(self.lightPosition_loc, 1, self.lightPosition.getCType())

        self.scene.render()

        GL.glUseProgram(0)



window = GLWindow((600, 600))

window.setRenderDelegate(MyDelegate())

scara = Scara(OBJReader().readFile("scara.obj"))
scara.position = Vector4((0, -0.75, -3, 1))
scara.orientation = Vector4((45, -45, 0, 1))
window.renderDelegate.scene.addObject(scara)

viper = Viper(OBJReader().readFile("viper.obj"))
viper.position = Vector4((0, 0.20, -3, 1))
viper.orientation = Vector4((45, -45, 0, 1))
window.renderDelegate.scene.addObject(viper)

#scene.addObject(Viper(OBJReader().readFile("viper.obj")))

window.mainLoop()