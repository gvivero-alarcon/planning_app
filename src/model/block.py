import pandas as pd
import os


class BlockModel:
    '''
    Modelo de importación y manipulación de modelos de bloques
    
    Atributos:
        data (pd.DataFrame): datos del modelo de bloques
        names (dict): nombres de las variables espaciales
    '''

    def __init__(self, data, names):
        self.data = data
        self.names = names


    def list_files(self):
        '''
        Devuelve una lista con los archivos del directorio actual
        
        Retorna:
            list: lista de nombres de archivos
        '''
        return [_file for _file in os.listdir() if os.path.isfile(_file)]
    
        
    def read_file(self, name, sep, header):
        '''
        Lee un archivo y lo carga en el modelo de bloques
        
        Argumentos:
            name (str): nombre del archivo
            sep (str): separador de columnas
            header (int or None): fila del encabezado
        '''
        
        # Leer los nuevos datos:
        new_data = pd.read_csv(name, sep=sep, header=header)

        # Vaciar el contenido del dataframe actual:
        self.data.drop(self.data.index, inplace=True)
        self.data.drop(self.data.columns, axis=1, inplace=True)

        # Agregar los nuevos datos:
        for col in new_data.columns:
            self.data[col] = new_data[col]
        
    
    def columns(self):
        '''
        Devuelve una lista con los nombres de las columnas del modelo de bloques
        
        Retorna:
            list: lista de nombres de columnas
        '''
        return self.data.columns.tolist()    

    
    def describe(self):
        '''
        Realiza un resumen estadístico del modelo de bloques
        
        Retorna:
            pd.DataFrame: resumen estadístico del modelo de bloques
        '''
        return self.data.describe()


    def get_plot_data(self, vname, vrange, xrange, yrange, zrange):
        '''
        Filtra los datos del modelo de bloques para la visualización 3D

        Argumentos:
            vname (str): nombre de la variable a graficar
            vrange (tuple): rango de valores de la variable a graficar
            xrange (tuple): rango de valores de la coordenada X
            yrange (tuple): rango de valores de la coordenada Y
            zrange (tuple): rango de valores de la coordenada Z

        Retorna:
            pd.DataFrame: datos filtrados para la visualización 3D
        '''

        # Nombre de las variables espaciales:
        xname = self.names['x']
        yname = self.names['y']
        zname = self.names['z']

        # Filtrar los datos según los rangos seleccionados:
        filtered_data = self.data.loc[
            self.data[vname].between(vrange[0], vrange[1]) &
            self.data[xname].between(xrange[0], xrange[1]) &
            self.data[yname].between(yrange[0], yrange[1]) &
            self.data[zname].between(zrange[0], zrange[1])
        ]

        # Devolver los datos filtrados:
        return {
            'x': filtered_data[xname].values,
            'y': filtered_data[yname].values,
            'z': filtered_data[zname].values,
            vname: filtered_data[vname].values
        }
        