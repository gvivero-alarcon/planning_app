import numpy as np

class EnvelopeModel:
    '''
    Modelo para la optimización de la envolvente económica

    Atributos:
        data (pd.DataFrame): datos del modelo de bloques
        names (dict): nombres de las columnas del DataFrame
    '''

    def __init__(self, data, names, fp_x, fp_y):
        self.data = data
        self.names = names
        self.fp_x = fp_x
        self.fp_y = fp_y


    def filter_data(self, level, height):
        '''
        Filtra el modelo de bloques entre el nivel óptimo y la altura máxima
        de extracción

        Argumentos:
            level (float): nivel óptimo de extracción
            height (float): altura máxima de extracción
        '''
        return self.data[
            self.data[self.names['z']] >= level &
            self.data[self.names['z']] <= level + height
        ]
    

    def get_angles(self, x0, y0, z0, x, y, z):
        '''
        Calcula el ángulo de un conjunto de bloques respecto a uno de referencia

        Argumentos:
            x0, y0, z0 (float): coordenadas del bloque de referencia
            x, y, z (pd.Series): coordenadas de los bloques a evaluar
        '''
        dx2 = np.power(x - x0, 2)
        dy2 = np.power(y - y0, 2)
        ang = np.arctan2(np.abs(z - z0), np.sqrt(dx2 + dy2))
        return np.degrees(ang)
    

    def floating_cone(self, xcoord, ycoord, zcoord, profit,
                      min_height, max_height, slope):
        '''
        Operativiza la envolvente de caving usando método del cono flotante
        '''

        # Inicializar vectores de coordenada y beneficio:
        data = self.filter_data()