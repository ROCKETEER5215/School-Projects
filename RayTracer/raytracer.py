__author__ = 'Justin Wallace'

from math3d import *
from objects3d import *

#Ray_Tracer Class
class Raytracer(object):
    def __init__(self, surf, ambientColor):
        self.surface = surf
        self.camera_pos = VectorN((0, 0, 0))
        self.camera_up = VectorN((0, 0, 0))
        self.camera_fov = 0
        self.camera_near = VectorN((0, 0, 0))
        self.mObjects = []
        self.mLights = []
        self.ambient_color = ambientColor

    #Set_Camera
    def setCamera(self, campos, camCOI, camUP, camFOV, camNear):
        self.camera_pos = campos
        self.camera_coi = camCOI
        self.camera_up = camUP
        self.camera_fov = camFOV
        self.camera_near = camNear
        # get the Aspect Ratio
        self.aspect_ratio = self.surface.get_width() / self.surface.get_height()
        # get the Camera's coordinates
        self.camera_z = (self.camera_coi - self.camera_pos).normalized_copy()
        self.camera_x = (self.camera_up.cross(self.camera_z)).normalized_copy()
        self.camera_y = (self.camera_z.cross(self.camera_x)).normalized_copy()
        # calculate View Plane Height , Width, and Origin
        self.viewPlane_Height = self.camera_near * math.tan(self.camera_fov/2 * math.pi/180) * 2
        self.viewPlane_Width = self.viewPlane_Height * self.aspect_ratio
        self.viewPlane_Origin = self.camera_pos + (self.camera_near * self.camera_z) + \
            ((self.viewPlane_Height / 2) * self.camera_y) + ((-self.viewPlane_Width / 2) * self.camera_x)

    #Calculate_Pixel_Pos
    def calculatePixelPos(self, ix, iy):
        # calculate the position of the Pixel
        a = (ix / self.surface.get_width()) * self.viewPlane_Width
        b = (iy / self.surface.get_height()) * self.viewPlane_Height
        A = a * self.camera_x
        B = b * (-self.camera_y)
        P = self.viewPlane_Origin + A + B
        return P

    #Ray_Cast
    def rayCast(self, ray):
        hits = []
        hit_distances = []
        # look for Ray Hits and get the distances
        for i in self.mObjects:
            x = i.rayHit(ray)
            if not x == None:
               if len(x.mIntersectionDistances) > 0 and x.mIntersectionDistances[0] > 1:
                 hits.append(x)
                 hit_distances.append(x.mIntersectionDistances[0])
        if len(hits) > 1:
            hit_distances_b = list(hit_distances)
            hit_distances.sort()
            x = hit_distances_b.index(hit_distances[0])
            return hits[x]
        elif len(hits) == 1:
            return hits[0]
        else:
            return None

    #Get_Color_Of_Hit
    def getColorOfHit(self, hitData):
        # get the color of the pixel to display
        #return hitData.mHitObject.mMaterial.getPygameColor()
        light_pw = VectorN((0, 0, 0))
        Shadow = False
        if len(hitData.mIntersectionPoints) > 1:
            Dist_copy = list(hitData.mIntersectionDistances)
            Dist_copy2 = list(Dist_copy)
            Dist_copy2.sort()
            New_Dist = hitData.mIntersectionDistances.index(Dist_copy2[0])

            New_Point = hitData.mIntersectionPoints[New_Dist]

        else:
            New_Dist = 0
            New_Point = hitData.mIntersectionPoints[0]

        ambient_pw = self.ambient_color.pairwise(hitData.mHitObject.mMaterial.mAmbient)
        light_pw += ambient_pw

        for i in self.mLights:
            Shadow = False
            shadow_ray_dist = i.Pos - hitData.mIntersectionPoints[New_Dist]
            shadow_ray = Ray(hitData.mIntersectionPoints[New_Dist], shadow_ray_dist.normalized_copy())
            shadow_ray_hits = self.rayCast(shadow_ray)

            if shadow_ray_hits is not None and len(shadow_ray_hits.mIntersectionPoints) > 0:
                for s in shadow_ray_hits.mIntersectionPoints:
                    dist_to_light = hitData.mIntersectionPoints[New_Dist] - i.Pos
                    numOf_light_dists = dist_to_light.dot(dist_to_light)
                    New_shadow_dist = s - hitData.mIntersectionPoints[New_Dist]
                    numOf_shadow_dists = New_shadow_dist.dot(New_shadow_dist)
                    if numOf_shadow_dists < numOf_light_dists:
                        Shadow = True

            if not Shadow:
                New_Normal = hitData.mIntersectionNormals[New_Dist]
                New_Direction = (i.Pos - New_Point).normalized_copy()
                # diffuse
                New_Diffuse_ray = New_Direction.dot(New_Normal)
                if New_Diffuse_ray > 0:
                    Object_Diffuse = hitData.mHitObject.mMaterial.mDiffuse
                    New_Diffuse = New_Diffuse_ray * i.Diffuse.pairwise(Object_Diffuse)
                else:
                    New_Diffuse = VectorN((0, 0, 0))

                # specular
                Specular_ray = 2 * (New_Direction.dot(New_Normal)) * New_Normal - New_Direction
                Camera_ray = (self.camera_pos - New_Point).normalized_copy()
                New_Specular_ray = Camera_ray.dot(Specular_ray)
                if New_Specular_ray > 0:
                    New_Specular = (New_Specular_ray**hitData.mHitObject.mMaterial.mShininess)*(i.Specular.pairwise(hitData.mHitObject.mMaterial.mSpecular))
                else:
                    New_Specular = VectorN((0, 0, 0))


                light_pw += New_Diffuse + New_Specular

            if light_pw[0] > 1:
                light_pw[0] = 1

            if light_pw[1] > 1:
                light_pw[1] = 1

            if light_pw[2] > 1:
                light_pw[2] = 1

            if light_pw[0] < 0:
                light_pw[0] = 0

            if light_pw[1] < 0:
                light_pw[1] = 0

            if light_pw[2] < 0:
                light_pw[2] = 0

            return light_pw * 255





    #Render_One_Line
    def renderOneLine(self, iy):
        # render the screen one line at a time
        for i in range(self.surface.get_width()):
            direction = (self.calculatePixelPos(i, iy) - self.camera_pos).normalized_copy()
            ray = Ray(self.calculatePixelPos(i, iy), direction)
            hit = self.rayCast(ray)
            if not hit == None:
                self.surface.set_at((i, iy),self.getColorOfHit(hit))

