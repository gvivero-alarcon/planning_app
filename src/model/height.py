import numpy as np


class HeightModel:
    '''
    Modelo para el cálculo de la cota óptima de extracción

    Atributos:
        data (pd.DataFrame): datos del modelo de bloques
        names (dict): nombres de las variables espaciales
    '''

    def __init__(self, data, names):
        self.data = data
        self.names = names


    def economic_value(self):
        '''Calcula el valor económico de cada bloque'''


    def floor_value(self, height, discount, rate, inv_cost) -> float:
        '''
        Calcula el valor de económico del piso dado. El modelo de bloques debe
        contener una columna para el beneficio de cada bloque llamda "profit"

        Argumentos:
            height (float): cota de extracción
            discount (float): tasa de descuento
            rate (float): tasa de extracción anual en m/año
            inv_cost (float): costo de inversión del PE

        Retorna:
            float: valor económico del piso
        '''

        # Nombre de las variables espaciales:
        xname = self.names['x']
        yname = self.names['y']
        zname = self.names['z']

        # filtrar modelo de bloques y ordenar valor Z:
        model = self.data[self.data[zname] >= height].copy()
        model = model.sort_values(by=zname, ascending=True)

        # Calcular la altura del bloque:
        dz = model[zname] - height

        # Actualizar el valor de cada bloque:
        model['discounted'] = model['profit'] / (1 + discount) ** (dz / rate)

        # Calcular el valor acumulado en cada columna:
        model['cumulative'] = model.groupby([xname, yname])['discounted'].cumsum()

        # Obtener el máximo de cada columna:
        max_values = model.groupby([xname, yname])['cumulative'].max()

        # Sumar aquellos bloques que pagan la inversión del PE:
        return max_values[max_values > inv_cost].sum()
    

    def value_by_height(self, heights, discount, rate, inv_cost):
        '''
        Calcula el valor económico del piso para una serie de cotas

        Argumentos:
            heights (list): lista de cotas de extracción
            discount (float): tasa de descuento
            rate (float): tasa de extracción anual en m/año
            inv_cost (float): costo de inversión del PE

        Retorna:
            list: lista con el valor económico del piso para cada cota
        '''

        values = []
        for z in heights:
            values.append(self.floor_value(z, discount, rate, inv_cost))
        
        return values
            

    def find_optimum(self, heights, values):
        '''
        Encuentra la cota óptima de extracción y su valor económico

        Argumentos:
            heights (list): lista de cotas de extracción
            values (list): lista con el valor económico del piso para cada cota

        Retorna:
            tuple: cota óptima y su valor económico
        '''

        max_index = np.argmax(values)
        return heights[max_index], values[max_index]

