from model.envelope import EnvelopeModel
from view.envelope import EnvelopeView

import numpy as np

class EnvelopeController:
    '''
    Controlador del menú de definición de envolvente económica

    Atributos:
        model (EnvelopeModel): modelo del menú de envolvente económica
        view (EnvelopeView): vista del menú de envolvente económica
    '''

    def __init__(self, model: EnvelopeModel, view: EnvelopeView):
        self.model = model
        self.view = view


    def calculate_envelope(self, level, profit_name):
        '''Genera la envolvente económica'''

        # Recuperar parámetros geométricos:
        min_height = self.view.text_min_height.value
        max_height = self.view.text_max_height.value
        slope = self.view.text_slope.value

        # Filtrar los datos entre la cota óptima y la altura:
        data = self.model.data[
            (self.model.data[self.model.names['z']] >= level) &
            (self.model.data[self.model.names['z']] <= level + max_height)
        ]
        data = data.sort_values('z', ascending = True)

        # Inicializar vectores de coordenadas:
        xcoord = np.array(data[self.model.names['x']])
        ycoord = np.array(data[self.model.names['y']])
        zcoord = np.array(data[self.model.names['z']])
        profit = np.array(data[profit_name])

        # Vectores que almacenan la envolvente:
        x_cave = np.array([])
        y_cave = np.array([])
        z_cave = np.array([])
        v_cave = np.array([])

        # Recorrer cada cota del modelo de bloques:
        for z in np.unique(zcoord):

            # Recorrer cada punto del plano Z = Z0:
            cond1 = (zcoord == z) & (profit > 0)

            for x, y in zip(xcoord[cond1], ycoord[cond1]):

                # Comprobar que el punto sea parte del footprint:
                cond = (self.model.fp_x == x) & (self.model.fp_y == y)
                if not any(cond):
                    continue

                # Calcular el ángulo de los bloques:
                dx2 = np.power(xcoord - x, 2)
                dy2 = np.power(ycoord - y, 2)
                ang = np.arctan2(np.abs(zcoord - z), np.sqrt(dx2 + dy2))
                ang = np.degrees(ang)

                # Definir el cono con aquellos bloques que cumplan con la condición de ángulo:
                cond2 = np.logical_and(ang >= slope, zcoord <= z)

                # Calcular el valor del cono:
                cone_value = np.sum(profit[cond2])

                # Continuar la próxima iteración del algoritmo si el valor es negativo:
                if cone_value <= 0:
                    continue

                # Guardar las bloques del pit:
                x_cave = np.append(x_cave, xcoord[cond2])
                y_cave = np.append(y_cave, ycoord[cond2])
                z_cave = np.append(z_cave, zcoord[cond2])
                v_cave = np.append(v_cave, profit[cond2])

                # Quitar los bloques del modelo:
                xcoord = np.delete(xcoord, cond2)
                ycoord = np.delete(ycoord, cond2)
                zcoord = np.delete(zcoord, cond2)
                profit = np.delete(profit, cond2)

        # Eliminar las columnas por debajo del mínimo:
        for x, y in zip(x_cave, y_cave):

            # Condición:
            cond3 = (x_cave == x) & (y_cave == y)

            # Filtrar vector Z:
            z = z_cave[cond3]
            try:
                zmax = z.max()
            except:
                continue

            # Calcular altura de columna:
            height = zmax - level

            if height < min_height:
                x_cave = np.delete(x_cave, cond3)
                y_cave = np.delete(y_cave, cond3)
                z_cave = np.delete(z_cave, cond3)
                v_cave = np.delete(v_cave, cond3)

        self.view.show_info(v_cave.sum())
        self.view.plot_envelope(x_cave, y_cave, z_cave, v_cave, data)