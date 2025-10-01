# Construcción de la interfaz gráfica:
import ipywidgets as widgets
from IPython.display import display

# Elementos gráficos personalizados:
from view import custom

# Generación de gráficos interactivos:
import plotly.graph_objects as go


class BlockView(widgets.VBox):
    '''Vista del menú de importación y visualización de modelos de bloques'''

    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.widgets_layout()
        

    def create_widgets(self):
        '''Crea los elementos gráficos del menú'''

        # Opciones predeterminadas:
        seps = [('Coma', ','), ('Punto y coma', ';'), 
                ('Espacio', ' '), ('Tabulación', '\t')]

        header = [('Sí', 0), ('No', None)]

        # 1. Importación del modelo de bloques:
        self.title_import = custom.Title(
            value='Importar modelo de bloques'
        )

        self.drop_name = custom.LabelDrop(
            description='Modelo de bloques'
        )
        self.drop_sep = custom.LabelDrop(
            description='Tipo de separador',
            options=seps
        )
        self.radio_header = custom.LabelRadio(
            description='Encabezado',
            options=header
        )
        self.button_update = custom.ToolButton(
            tool='update'
        )
        self.button_import = widgets.Button(
            description='Cargar archivo'
        )
        self.import_status = widgets.HTML()

        
        # 2. Resumen estadístico del modelo de bloques:
        self.title_stats = custom.Title(
            value='Resumen descriptivo del modelo'
        )
        self.output_stats = widgets.Output()


        # 3. Variables espaciales del modelo de bloques:
        self.title_spatial = custom.Title(
            value='Variables espaciales del modelo'
        )

        self.drop_xcoord = custom.LabelDrop(
            description='Coordenada X'
        )
        
        self.drop_ycoord = custom.LabelDrop(
            description='Coordenada Y'
        )

        self.drop_zcoord = custom.LabelDrop(
            description='Coordenada Z'
        )

        self.button_save = widgets.Button(
            description='Guardar nombres'
        )

        self.save_status = widgets.HTML()


        # 4. Visualización del modelo de bloques:
        self.title_view = custom.Title(
            value='Visualización del modelo de bloques'
        )

        self.drop_variable = custom.LabelDrop(
            description='Variable de interés'
        )
        self.slider_variable = custom.LabelSlider(
            description='Valor de corte'
        )
        self.slider_xcoord = custom.LabelSlider(
            description='Coordenada X'
        )
        self.slider_ycoord = custom.LabelSlider(
            description='Coordenada Y'
        )
        self.slider_zcoord = custom.LabelSlider(
            description='Coordenada Z'
        )
        self.button_plot = widgets.Button(
            description='Graficar'
        )
        self.output_plot = widgets.Output()


    def widgets_layout(self):
        '''Configura la disposición de los elementos gráficos'''

        # 1. Importación del modelo de bloques:
        menu_import = widgets.VBox([
            self.title_import,
            widgets.HBox([
                self.drop_name, self.button_update
            ]),
            self.drop_sep,
            self.radio_header,
            self.button_import,
            self.import_status
        ])

        # 2. Resumen estadístico del modelo de bloques:
        menu_stats = widgets.VBox([
            self.title_stats,
            self.output_stats
        ])

        # 3. Variables espaciales del modelo de bloques:
        menu_spatial = widgets.VBox([
            self.title_spatial,
            self.drop_xcoord,
            self.drop_ycoord,
            self.drop_zcoord,
            self.button_save,
            self.save_status
        ])

        # 4. Visualización del modelo de bloques:
        menu_view = widgets.VBox([
            self.title_view,
            self.drop_variable,
            self.slider_variable,
            self.slider_xcoord,
            self.slider_ycoord,
            self.slider_zcoord,
            self.button_plot,
            self.output_plot
        ])

        # 5. Colocar en el layout principal:
        self.children = [menu_import, menu_stats, menu_spatial, menu_view]


    def update_names(self, names):
        '''
        Actualizar la lista de archivos en el menú desplegable
        
        Argumentos:
            names (list): lista de nombres de archivos
        '''
        self.drop_name.options = names
        self.drop_name.value = names[0]


    def update_variables(self, cols):
        '''
        Actualizar las opciones del menú desplegable de variables
        
        Argumentos:
            cols (list): lista de nombres de columnas
        '''
        for drop_name in ['xcoord', 'ycoord', 'zcoord', 'variable']:
            
            # Recuperar el menú desplegable correspondiente:
            drop = getattr(self, f'drop_{drop_name}')
            
            # Actualizar las opciones y vaciar la selección:
            drop.options = cols
            drop.value = None


    def show_import_info(self):
        '''Muestra un mensaje de información de carga'''
        self.import_status.value = '''
            <span style="color:green; font-weight: bold;">
                ¡El modelo de bloques se cargó correctamente!
            </span>
        '''


    def show_import_error(self):
        '''Muestra un mensaje de error de carga'''
        self.import_status.value = '''
            <span style="color:red; font-weight: bold;">
                No es posible cargar el modelo de bloques
            </span>
        '''


    def show_save_info(self):
        '''Muestra un mensaje de información sobre guardado'''
        self.save_status.value = '''
            <span style="color:green; font-weight: bold;">
                La definición de variables espaciales se guardó correctamente.
            </span>
        '''


    def show_save_error(self):
        '''Muestra un mensaje de error de carga'''
        self.save_status.value = '''
            <span style="color:red; font-weight: bold;">
                No se ha guardado la definición de variables espaciales. 
                Compruebe que todas las variables hayan sido asignadas.
            </span>
        '''


    def clear_outputs(self):
        '''Limpia el mensaje de información sobre importación'''
        self.import_status.value = ''
        self.save_status.value = ''
        self.output_stats.clear_output()


    def show_stats(self, stats):
        '''
        Muestra el resumen estadístico del modelo de bloques

        Argumentos:
            stats (pd.DataFrame): resumen estadístico del modelo de bloques
        '''
        with self.output_stats:
            self.output_stats.clear_output()
            display(stats)


    def plot_blocks(self, name, data, box):
        '''
        Crea una visualización 3D de los bloques

        Argumentos:
            name (str): nombre de la variable a graficar
            data (pd.DataFrame): datos del modelo de bloques
            box (pd.DataFrame): caja delimitadora del modelo de bloques
        '''

        # Inicializar la figura:
        fig = go.Figure()

        # Configuración de la barra de colores:
        colorbar = dict(
            title=name,
            orientation='v',
            title_side='top'
        )

        # Configuración de los marcadores:
        marker = dict(
            size=3,
            color=data[name],
            colorscale='jet',
            opacity=1.0,
            showscale=True,
            colorbar=colorbar
        )

        # Graficar los bloques como puntos:
        fig.add_trace(
            go.Scatter3d(
                name='Modelo',
                x=data['x'],
                y=data['y'],
                z=data['z'],
                mode='markers',
                marker=marker
            )
        )

        # Configuración de los ejes del gráfico:
        scene = dict(
            xaxis_title='Coordenada X',
            yaxis_title='Coordenada Y',
            zaxis_title='Coordenada Z',
            aspectmode='data'
        )

        # Configuración del título del gráfico:
        title = dict(
            text='<b>Visualización del Modelo de Bloques</b>',
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top'
        )

        # Configuración de los márgenes de la figura:
        margin = dict(l=20, r=20, b=10, t=20)

        # Agregar configuración del gráfico:
        fig.update_layout(
            scene=scene,
            title=title,
            margin=margin,
            showlegend=False
        )

        # Mostrar el gráfico en el output:
        with self.output_plot:
            self.output_plot.clear_output()
            display(fig)
