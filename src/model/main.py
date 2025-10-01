# Trabajo con arreglos de datos:
import pandas as pd

# Trabajo con arreglos numéricos:
import numpy as np

# Modelos de cada menú de la aplicación:
from model.block import BlockModel
from model.height import HeightModel
from model.footprint import FootprintModel
from model.envelope import EnvelopeModel


class MainModel:

    def __init__(self):
        
        # Inicializar variables de la aplicación:
        self.data = pd.DataFrame()
        self.names = {}
        self.fp_x = np.array([])
        self.fp_y = np.array([])

        # Inicializar modelos de cada menú:
        self.block = BlockModel(self.data, self.names)
        self.height = HeightModel(self.data, self.names)
        self.footprint = FootprintModel(
            self.data, self.names, self.fp_x, self.fp_y
        )
        self.envelope = EnvelopeModel(
            self.data, self.names, self.fp_x, self.fp_y
        )
