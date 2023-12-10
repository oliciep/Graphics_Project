class Material:
    def __init__(self, name=None, Ka=None, Kd=None, Ks=None, Ns=10.0, texture=None):
        if Ks is None:
            Ks = [1, 1, 1]
        if Kd is None:
            Kd = [1, 1, 1]
        if Ka is None:
            Ka = [1, 1, 1]
        self.name = name
        self.Ka = Ka
        self.Kd = Kd
        self.Ks = Ks
        self.Ns = Ns
        self.texture = texture
        self.alpha = 1.0

class MaterialLibrary:
    def __init__(self):
        self.materials = []
        self.names = {}

    def add_material(self, material):
        self.names[material.name] = len(self.materials)
        self.materials.append(material)

