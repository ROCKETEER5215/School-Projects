# FILENAME: glwindow.py
# BY: Andrew Holbrook
# DATE: 9/24/2015

import sdl2
from ctypes import byref, c_int
from OpenGL import GL
from etgg2801.Scene import Scene

class GLWindow(object):
    """A window for use with OpenGL.
    """
    instance = None
    
    @staticmethod
    def getInstance():
        if not GLWindow.instance:
            GLWindow.instance = GLWindow()
        
        return GLWindow.instance
    
    def __init__(self, size=(600, 600), major=4, minor=0):
        if GLWindow.instance:
            raise Exception("Window already created!")
        
        self.size = tuple(size)
        self.major = 4
        self.minor = 0
        
        self.printFPS = False
        self.periodTime = 0
        self.fpsPeriod = 1000
        self.fpsDelay = self.fpsPeriod
        self.numFrames = 0
        
        self.__buildWindow()
        
        GLWindow.instance = self

        #self.setRenderDelegate(GLWindowRenderDelegate())
    
    def setRenderDelegate(self, renderDelegate):
        self.renderDelegate = renderDelegate
    
    def mainLoop(self):
        if not hasattr(self, "renderDelegate"):
            raise Exception("GLWindow's render delegate not set!")
        
        event = sdl2.SDL_Event()
        running = True
        startTime = sdl2.SDL_GetTicks()
        while running:
            stopTime = sdl2.SDL_GetTicks()
            dtime = stopTime - startTime
            startTime = stopTime
            
            if self.printFPS:
                self.periodTime += dtime
                self.fpsDelay -= dtime
                self.numFrames += 1
                if self.fpsDelay <= 0:
                    self.fpsDelay = self.fpsPeriod
                    print("FPS:", (self.numFrames / (self.periodTime / 1000.0)))
                    self.numFrames = 0
                    self.periodTime = 0
                
            
            while sdl2.SDL_PollEvent(byref(event)) != 0:
                if event.type == sdl2.SDL_QUIT:
                    running = False
                else:
                    pass
                    # self.renderDelegate.addEvent(event)
            
            self.renderDelegate.update(dtime)
            self.renderDelegate.render()
            
            sdl2.SDL_GL_SwapWindow(self.window)
            
        self.cleanup()
    
    def cleanup(self):
        self.renderDelegate.cleanup()
        sdl2.SDL_GL_DeleteContext(self.glcontext)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()
    
    def __buildWindow(self):
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
            raise Exception(sdl2.SDL_GetError())
        
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, self.major)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, self.minor)
        
        self.window = sdl2.SDL_CreateWindow(
            b'ETGG2801 Example',
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            self.size[0], self.size[1],
            sdl2.SDL_WINDOW_OPENGL)
        
        self.glcontext = sdl2.SDL_GL_CreateContext(self.window)
        if not self.glcontext:
            sdl2.SDL_DestroyWindow(self.window)
            raise Exception(sdl2.SDL_GetError())
        
        # keep application from receiving text input events
        sdl2.SDL_StopTextInput()

class GLWindowRenderDelegate(object):
    """This class will receive cleanup, update, and render calls from the
    GLWindow.
    """
    def __init__(self):
        pass
        #if type(self) == GLWindowRenderDelegate:
        #    raise Exception("GLWindowRenderDelegate CANNOT BE INSTANTIATED!")
    
    def cleanup(self):
        pass
        #raise Exception("MUST IMPLEMENT 'cleanup' METHOD!")
    
    def update(self, dtime):
        pass
        #raise Exception("MUST IMPLEMENT 'update' METHOD!")
    
    def render(self):
        pass
        #raise Exception("MUST IMPLEMENT 'render' METHOD!")
