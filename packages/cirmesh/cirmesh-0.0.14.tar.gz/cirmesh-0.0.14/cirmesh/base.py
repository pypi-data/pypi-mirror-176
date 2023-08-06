"""
----------------------------
Library for importing, exporting and doing simple operations on triangular meshes.
"""

from hashlib import new
from . import augment
from trimesh import Trimesh
import sys

class CIRmesh(Trimesh):

    def __init__(self):
        sys.setrecursionlimit(1500000000)
        super().__init__()

    def fixNonWatertight(self, mesh):
        """
            fixNonWatertight
        """

        new_mesh = augment.fixNonWatertight(mesh)
        return new_mesh
    
    def fixNonWatertight1Vertex(self, mesh):
        """
            fixNonWatertight
        """
        new_mesh = augment.removeEyeBalls(mesh)
        new_mesh = augment.fixNonWatertight_1vertex(new_mesh)
        return new_mesh

    def increaseMeshVertex(
        self,
        original_mesh,
        max_point,
        step=200,
        mustWatertight=True,
        debug=False):
        """
            increaseMeshVertex
        """

        new_mesh = augment.generalMeshVertexIncreasing(
            original_mesh=original_mesh,
            max_point=max_point,
            step=step,
            debug=debug
        )
        if mustWatertight == True and new_mesh.is_watertight == True:
            return new_mesh
        
        return False

    def createScar(self, mesh, path, directory):
        """
            createScar
        """

        if (augment.scarCreating(
            mesh=mesh,
            path=path,
            directory=directory
        )) == True:
            return True


    def createScarV2(self, mesh, path, numGenScar=10):
        """
            createScar
        """

        if (augment.scarCreatingV2(
            mesh=mesh,
            path=path,
            numGenScar=numGenScar
        )) == True:
            return True
    

        