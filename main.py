# This is the main module for the program. This module facilitates the rendering of the scene, and the loading of all
# the objects into the scene.

import pygame
# Here we import the scene class from the scene module.
from scene import Scene

# From the light source module we import the light source class to provide illumination.
from lightSource import LightSource

# From the obj module we import the load_obj_file class to allow us to load models into the scene.
from obj import load_obj_file

# From the ShadowMapping module we import all the classes, to allow us to cast shadows upon the land model in the scene.
from ShadowMapping import *

# From skyBox module we import all classes, to allow for the rendering and creation of the surrounding skybox around the
# scene.
from skyBox import *

# From the environentMapping module we import all the classes, to allow the rendering of the cube map upon which we map
# our skybox textures.
from environmentMapping import *


# Here is the main class that we use to create the scene. This class handles encapsulating all the concepts that are
# present within the other modules, and instantiates them with the needed values in order to place the models in the
# correct places in the scene.
class mainScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        # Here the light is instantiated, with coordinates to place the light source to match the skybox.
        lightX = -12
        lightY = 8
        lightZ = 0
        self.light = LightSource(self, position=[lightX, lightY, lightZ])

        self.shaders = 'phong'

        # This code is used to render the shadow map needed to cast shadows. The shadows are cast based upon the light
        # source instantiated above.
        self.shadows = ShadowMap(light=self.light)
        self.show_shadow_map = ShowTexture(self, self.shadows)

        # Here, I load in all the models needed for the scene using the obj module. These models contain variable
        # models, with some obj files containing multiple models rendered.
        island = load_obj_file('models/island.obj')
        trees = load_obj_file('models/trees.obj')
        tigers = load_obj_file('models/tigers.obj')
        shrubs = load_obj_file('models/shrubs.obj')
        cave = load_obj_file('models/cave.obj')
        rocks = load_obj_file('models/rocks.obj')

        translationX = 0
        translationY = -7
        translationZ = 0
        islandScale = 0.5
        modelsScale = 0.75

        # This section of code instantiates instances of each class of model with the relevant parameters. The land
        # module uses the ShadowMappingShader instead of the PhongShader, because instead it is used to render the scene
        # from the light sources perspective, meaning any part which isn't lit is cast in shadow.
        self.island = [
            DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([translationX, translationY, translationZ]),
                                                      scaleMatrix([islandScale, islandScale, islandScale])), mesh=mesh,
                              shader=PhongShader()) for mesh in island]

        self.water = DrawModelFromMesh(scene=self,
                                       M=np.matmul(translationMatrix([translationX, translationY, translationZ]),
                                                   scaleMatrix([modelsScale, modelsScale, modelsScale])),
                                       mesh=island[0], shader=PhongShader())
        self.land = DrawModelFromMesh(scene=self,
                                      M=np.matmul(translationMatrix([translationX, translationY, translationZ]),
                                                  scaleMatrix([modelsScale, modelsScale, modelsScale])),
                                      mesh=island[1], shader=ShadowMappingShader(shadow_map=self.shadows), name='land')
        self.trees = [
            DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([translationX, translationY, translationZ]),
                                                      scaleMatrix([modelsScale, modelsScale, modelsScale])),
                              mesh=mesh, shader=PhongShader()) for mesh in trees]
        self.tigers = [
            DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([translationX, translationY, translationZ]),
                                                      scaleMatrix([modelsScale, modelsScale, modelsScale])),
                              mesh=mesh, shader=PhongShader()) for mesh in tigers]
        self.shrubs = [
            DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([translationX, translationY, translationZ]),
                                                      scaleMatrix([modelsScale, modelsScale, modelsScale])),
                              mesh=mesh, shader=PhongShader()) for mesh in shrubs]
        self.cave = DrawModelFromMesh(scene=self,
                                      M=np.matmul(translationMatrix([translationX, translationY, translationZ]),
                                                  scaleMatrix([modelsScale, modelsScale, modelsScale])),
                                      mesh=cave[0], shader=PhongShader())
        self.rocks = [
            DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([translationX, translationY, translationZ]),
                                                      scaleMatrix([modelsScale, modelsScale, modelsScale])), rotationMatrixX(np.pi/32)),
                              mesh=mesh, shader=PhongShader()) for mesh in rocks]

        # This renders the skybox.
        self.skybox = SkyBox(scene=self)

        # This renders the environment for the skybox, with the skybox texture in the skybox folder.
        self.environment = EnvironmentMappingTexture(width=400, height=400)

    # This function deals with the mapping of shadows. This is done using a shader on the land model, allowing shadows
    # to be cast by calculating which parts of the scene cannot be seen by the perspective of the light source.
    def draw_shadow_map(self):

        # This clear function will clear the scene and the depth buffer, which means that the buffer values will be
        # reset to standard values. This allows for the shadows to be cast when the shader for land is set, without
        # being interfered with by previous buffer values present in other shaders.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Here, all the models are rendered for the shadow map. This allows for the light source to cast a ray,
        # which will cast any of the occluded fragments of the models as shadows.
        self.cave.draw()

        for model in self.trees:
            model.draw()

        for model in self.shrubs:
            model.draw()

        for model in self.tigers:
            model.draw()

        for model in self.rocks:
            model.draw()

    # This draw function is where the models are rendered on to the scene.
    def draw(self, framebuffer=False):
        '''
        Draw all models in the scene
        :return: None
        '''

        # Again, we clear the colour and depth buffer to preset values, allowing for colour and depth to be arbitrarily
        # added when called upon.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # when using a framebuffer, we do not update the camera to allow for arbitrary viewpoint.
        if not framebuffer:
            self.camera.update()

        # Here we draw the skybox.
        self.skybox.draw()

        # Then we render the shadows that have been mapped onto the scene.
        self.shadows.render(self)

        # when rendering the framebuffer we ignore the reflective object
        if not framebuffer:
            # glEnable(GL_BLEND)
            # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            #            self.envbox.draw()
            # self.environment1.update(self)
            # self.envbox.draw()

            self.environment.update(self)

            self.show_shadow_map.draw()

        # This portion of code will now go through each of the separate models, and renders them based upon the amount
        # of models present in each obj file.

        # For trees, I have disabled culling because otherwise they will not render from an underneath perspective. As
        # this is the only model that has this requirement, it is enabled after the trees are rendered.
        glDisable(GL_CULL_FACE)

        for model in self.trees:
            model.draw()

        # Now we enable culling again to render other models.
        glEnable(GL_CULL_FACE)
        for model in self.shrubs:
            model.draw()
        for model in self.tigers:
            model.draw()
        for model in self.rocks:
            model.draw()

        self.cave.draw()

        self.land.draw()

        # Here, I set the alpha of the water to 0.1, in order to create a transparent plane. This allows for models to
        # be visible through the body of the model. The blend function is used in order to allow for the colour to not
        # be solid, meaning that other object colours will be visible at varying intensities.
        self.water.mesh.material.alpha = 0.1
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.water.draw()
        glDisable(GL_BLEND)

        # Finally, the scene is rendered and then displayed.
        # Note that here we use double buffering to avoid artefacts: we draw on a different buffer than the one we
        # display, and flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

    def keyboard(self, event):
        '''
        Process additional keyboard events for this demo.
        '''
        Scene.keyboard(self, event)

        # Code to move the camera up and down on the y axis by increments of 0.5.
        if event.key == pygame.K_o:
            self.camera.center[1] -= 0.5

        if event.key == pygame.K_l:
            self.camera.center[1] += 0.5

# This function instantiates the program, creates an instance of the main class, and then runs the class to being
# creating the scene.
if __name__ == '__main__':
    # This will initialise a new scene.
    scene = mainScene()

    # This then draws the models.
    scene.run()
