from model.block import BlockModel
from view.block import BlockView


class BlockController:
    '''
    Controlador del menú de modelos de bloques
    
    Atributos:
        model (BlockModel): modelo de gestión de modelos de bloques
        view (BlockView): vista del menú de bloques
    '''

    def __init__(self, model: BlockModel, view: BlockView):
        
        # Inicializar modelo y vista:
        self.model = model
        self.view = view

        # Enlazar eventos a los elementos de la vista:
        self.bind()

        # Actualizar lista de archivos en directorio:
        self.set_names()


    def bind(self):
        '''Enlaza los eventos de la vista con las funciones del controlador'''

        # Enlazar funciones a los botones:
        self.view.button_update.on_click(self.set_names)
        self.view.button_save.on_click(self.save_name)
        self.view.button_plot.on_click(self.plot_model)

        # Enlazar funciones a los menús desplegables:
        self.view.drop_variable.observe_(self.set_vrange, names='value')
        self.view.drop_xcoord.observe_(self.set_xrange, names='value')
        self.view.drop_ycoord.observe_(self.set_yrange, names='value')
        self.view.drop_zcoord.observe_(self.set_zrange, names='value')


    def set_names(self, *event):
        '''Actualiza la lista de archivos en el menú desplegable'''
        list_files = self.model.list_files()
        self.view.update_names(list_files)


    def load_file(self):
        '''Carga un archivo seleccionado como modelo de bloques. Este método
        se llama desde el controlador principal de la aplicación para conectar
        con el menú de footprint'''
        
        # Reestablecer etiqueta de estado y estadísticas:
        self.view.clear_outputs()
        self.model.names.clear()

        # Leer el archivo de modelo de bloques:        
        try:
            self.model.read_file(
                name=self.view.drop_name.value,
                sep=self.view.drop_sep.value,
                header=self.view.radio_header.value
            )
            self.view.show_import_info()
        except:
            self.view.update_variables([])
            self.view.show_import_error()
            return
        
        # Realizar resumen estadístico del modelo de bloques:
        stats = self.model.describe()
        self.view.show_stats(stats)

        # Actualizar las opciones de los menús desplegables:
        cols = self.model.columns()
        self.view.update_variables(cols)
        
        return cols
        

    def set_slider_range(self, slider, variable):
        '''
        Establece el rango del deslizador según la variable seleccionada
        
        Argumentos:
            slider (widgets.FloatRangeSlider): deslizador a actualizar
            variable (str): nombre de la variable seleccionada
        '''

        # Ignorar si la variable no es válida:
        if not variable:
            return

        # Recuperar mínimo y máximo de la variable:
        min_value = self.model.data[variable].min()
        max_value = self.model.data[variable].max()

        # Establecer el rango del deslizador:
        try:
            slider.min, slider.max = min_value, max_value
        except:
            slider.max, slider.min = max_value, min_value
            
        slider.value = (min_value, max_value)


    def set_vrange(self, change):
        '''Establece el rango para la variable'''
        self.set_slider_range(self.view.slider_variable, change['new'])


    def set_xrange(self, change):
        '''Establece el rango para la coordenada X'''
        self.set_slider_range(self.view.slider_xcoord, change['new'])

    
    def set_yrange(self, change):
        '''Establece el rango para la coordenada Y'''
        self.set_slider_range(self.view.slider_ycoord, change['new'])


    def set_zrange(self, change):
        '''Establece el rango para la coordenada Z'''
        self.set_slider_range(self.view.slider_zcoord, change['new'])
        

    def save_name(self, event):
        '''Guarda los nombres de las variables espaciales seleccionadas'''

        # Recuperar nombres seleccionados:
        xname = self.view.drop_xcoord.value
        yname = self.view.drop_ycoord.value
        zname = self.view.drop_zcoord.value

        # Comprobar que se hayan seleccionado todas las variables:
        if any(name is None for name in [xname, yname, zname]):
            self.view.show_save_error()
            return

        # Guardar nombre de las variables espaciales:
        self.model.names.update({
            'x': self.view.drop_xcoord.value,
            'y': self.view.drop_ycoord.value,
            'z': self.view.drop_zcoord.value
        })

        self.view.show_save_info()


    def plot_model(self, event):
        '''Genera una visualización del modelo de bloques'''

        # Comprobar que se han definido las variables:
        if not self.model.names:
            self.view.show_save_error()
            return
        
        vname = self.view.drop_variable.value
        if not vname:
            return
        
        # Recuperar datos a graficar:
        plot_data = self.model.get_plot_data(
            vname=vname,
            vrange=self.view.slider_variable.value,
            xrange=self.view.slider_xcoord.value,
            yrange=self.view.slider_ycoord.value,
            zrange=self.view.slider_zcoord.value
        )

        # Generar la visualización:
        self.view.plot_blocks(vname, plot_data, None)
        