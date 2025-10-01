class FootprintModel:
    '''
    Modelo para la definición de la geometría de la cota óptima

    Atributos:
        data (pd.DataFrame): datos del modelo de bloques
        names (dict): nombres de las variables espaciales
    '''

    def __init__(self, data, names, fp_x, fp_y):
        self.data = data
        self.names = names
        self.fp_x = fp_x
        self.fp_y = fp_y


    def get_footprint(self, height, discount, rate, inv_cost):
        '''
        Calcula el valor de económico del piso dado. El modelo de bloques debe
        contener una columna para el beneficio de cada bloque llamda "profit".
        
        Argumentos:
            height (float): cota de extracción
            discount (float): tasa de descuento
            rate (float): tasa de extracción anual en m/año
            inv_cost (float): costo de inversión del PE

        Retorna:
            pd.DataFrame: modelo de bloques con valor económico acumulado
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
        max_values = max_values[max_values > inv_cost]

        # Obtener los datos para graficar:
        x = [point[0] for point in max_values.index.values]
        y = [point[1] for point in max_values.index.values]
        v = max_values.values

        # Guardar geometría del footprint:
        self.fp_x.resize(len(x), refcheck=False)
        self.fp_x[:] = x

        self.fp_y.resize(len(y), refcheck=False)
        self.fp_y[:] = y

        return x, y, v


    