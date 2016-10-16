# FILENAME: robot.py
# BY: Andrew Holbrook
# DATE: 9/24/2015

from OpenGL import GL
from . import GLWindow, Vector4, Matrix4
import sdl2

class Joint(object):
    """Base class for all joint types (prismatic, revolute, etc).
    """
    def __init__(self, partA, partB, axis=(0,1,0), offset=(0,0,0)):
        """Creates a joint linking parts A and B. The axis of motion can be
        specified, along with the offset between parts A and B.
        """
        self.partA = partA
        self.partB = partB
        self.value = 0.0
        self.velocity = 0.0
        self.axis = axis
        self.offset = offset
        self.valueMin = 0.0
        self.valueMax = 0.0
        
        self.offsetMatrix = Matrix4.getTranslation(*offset)
    
    def increaseValue(self, dtime):
        """Increase the value (angle or distance) of the joint with respect to
        the elapsed time (dtime)--the maximum joint value is observed.
        """
        self.value = min(self.valueMax, self.value + self.velocity * dtime)
    
    def decreaseValue(self, dtime):
        """Decrease the value (angle or distance) of the joint with respect to
        the elapsed time (dtime)--the minimum joint value is observed.
        """
        self.value = max(self.valueMin, self.value - self.velocity * dtime)
    
    def setLimits(self, min, max):
        """Sets the minimum/maximum joint limits.
        """
        self.valueMin = min
        self.valueMax = max

class RevoluteJoint(Joint):
    """Class for representing a rotating joint with one degree of freedom.
    """
    def __init__(self, partA, partB, axis=(0,1,0), offset=(0,0,0)):
        """See Joint class.
        """
        super().__init__(partA, partB, axis, offset)
    
    def getTransformation(self):
        """Return the transformation matrix representing partB relative to partA.
        """
        angleList = [a * self.value for a in self.axis]
        return self.offsetMatrix * Matrix4.getRotation(*angleList)

class PrismaticJoint(Joint):
    def __init__(self, partA, partB, axis=(0,1,0), offset=(0,0,0)):
        """See Joint class.
        """
        super().__init__(partA, partB, axis, offset)
    
    def getTransformation(self):
        """Return the transformation matrix representing partB relative to partA.
        """
        dList = [a * self.value for a in self.axis]
        return self.offsetMatrix * Matrix4.getTranslation(*dList)

class Robot(object):
    def __init__(self, model):
        self.model = model
        self.joints = []
        self.position = Vector4()
        self.orientation = Vector4()
        
        renderDelegate = GLWindow.getInstance().renderDelegate
        self.modelview_loc = renderDelegate.modelview_loc
    
    def addJoint(self, joint):
        self.joints.append(joint)
    
    def render(self):
        
        # create object to world matrix
        rotMatrix_ow = Matrix4.getRotation(*self.orientation.getXYZ())
        tranMatrix_ow = Matrix4.getTranslation(*self.position.getXYZ())
        matrix_ow = tranMatrix_ow * rotMatrix_ow
        
        # set the object to world matrix in the shader
        GL.glUniformMatrix4fv(self.modelview_loc, 1, False, matrix_ow.getCType())
        
        # render the robot's first joint
        self.model.renderPartByName(self.joints[0].partA)
        
        # render the remaining joints
        for j in self.joints:
            matrix_ow *= j.getTransformation()
            GL.glUniformMatrix4fv(self.modelview_loc, 1, False, matrix_ow.getCType())
            self.model.renderPartByName(j.partB)

    def update(self, dtime):
        pass

# Scara Controls
class Scara(Robot):
    def __init__(self, model):
        super().__init__(model)
        
        self.addJoint(RevoluteJoint("L0", "L1"))
        self.addJoint(RevoluteJoint("L1", "L2", offset=(-0.325,0.0)))
        self.addJoint(PrismaticJoint("L2", "d3"))
        
        self.joints[0].velocity = 360.0 / 2000.0
        self.joints[0].setLimits(-115, 115)
        self.joints[1].velocity = 360.0 / 500.0
        self.joints[1].setLimits(-135, 135)
        self.joints[2].velocity = .01
        self.joints[2].setLimits(-.2, .2)

    def update(self, dtime):
        keyStates = sdl2.SDL_GetKeyboardState(None)
        if keyStates[sdl2.SDL_SCANCODE_A]:
            self.joints[0].increaseValue(dtime)
        if keyStates[sdl2.SDL_SCANCODE_D]:
            self.joints[0].decreaseValue(dtime)
        if keyStates[sdl2.SDL_SCANCODE_Q]:
            self.joints[1].increaseValue(dtime)
        if keyStates[sdl2.SDL_SCANCODE_E]:
            self.joints[1].decreaseValue(dtime)
        if keyStates[sdl2.SDL_SCANCODE_Z]:
            self.joints[2].increaseValue(dtime)
        if keyStates[sdl2.SDL_SCANCODE_C]:
            self.joints[2].decreaseValue(dtime)

# Viper Controls
class Viper(Robot):
    def __init__(self, model):
        super().__init__(model)
        
        self.addJoint(RevoluteJoint('L0', 'L1'))
        self.addJoint(RevoluteJoint('L1', 'L2', (0, 0, 1), (-0.075, 0.335, 0.0)))
        self.addJoint(RevoluteJoint('L2', 'L3', (0, 0, 1), (-0.365, 0, 0)))
        self.addJoint(RevoluteJoint('L3', 'L4', (0, 1, 0), (0.09, 0, 0)))
        self.addJoint(RevoluteJoint('L4', 'L5', (0, 0, 1), (0, 0.4, 0)))

        self.joints[4].velocity = 300.0/1000.0
        self.joints[4].setLimits(-190, 45)
        self.joints[3].velocity = 300.0/1000.0
        self.joints[3].setLimits(-190, 45)
        self.joints[2].velocity = 300.0/1000.0
        self.joints[2].setLimits(-190, 45)
        self.joints[1].velocity = 300.0/1000.0
        self.joints[1].setLimits(-190, 45)
        self.joints[0].velocity = 400.0/1000.0
        self.joints[0].setLimits(-360, 360)

    def update(self, dtime):
        keyStates = sdl2.SDL_GetKeyboardState(None)
        if keyStates[sdl2.SDL_SCANCODE_V]:
            self.joints[0].increaseValue(dtime)
        if keyStates[sdl2.SDL_SCANCODE_N]:
            self.joints[0].decreaseValue(dtime)
        if keyStates[sdl2.SDL_SCANCODE_F]:
            self.joints[1].increaseValue(dtime)
        if keyStates[sdl2.SDL_SCANCODE_H]:
            self.joints[1].decreaseValue(dtime)
        if keyStates[sdl2.SDL_SCANCODE_R]:
            self.joints[2].increaseValue(dtime)
        if keyStates[sdl2.SDL_SCANCODE_Y]:
            self.joints[2].decreaseValue(dtime)
        if keyStates[sdl2.SDL_SCANCODE_G]:
            self.joints[3].increaseValue(dtime)
        if keyStates[sdl2.SDL_SCANCODE_J]:
            self.joints[3].decreaseValue(dtime)
        if keyStates[sdl2.SDL_SCANCODE_T]:
            self.joints[4].increaseValue(dtime)
        if keyStates[sdl2.SDL_SCANCODE_U]:
            self.joints[4].decreaseValue(dtime)