

class Scene(object):


    def __init__(self):
        self.objects = []

    def addObject(self, o):
        o.model.loadToVRAM()
        self.objects.append(o)

    def removeObject(self, o):
        if o in self.objects:
            self.objects.remove(o)
        else:
            raise TypeError("Not in the list.")

    def update(self, dtime):
        for i in self.objects:
            i.update(dtime)

    def render(self):
        for i in self.objects:
            i.render()
