# Construcción de la interfaz gráfica:
import ipywidgets as widgets
from IPython.display import display

# Elementos gráficos personalizados:
from view import custom

# Generación de gráficos interactivos:
import plotly.graph_objects as go


class EnvelopeView(widgets.VBox):
    '''Vista del menú de optimización de envolvente económica'''

    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.widgets_layout()
        

    def create_widgets(self):
        '''Crea los elementos gráficos del menú'''

        # 1. Generación y visualización del footprint:
        self.title_geometry = custom.Title(
            value='Restricciones geométricas'
        )

        self.text_min_height = custom.LabelText(
            description='Altura mínimo de columna',
            units='m'
        )
        self.text_max_height = custom.LabelText(
            description='Altura máxima de columna',
            units='m'
        )
        self.text_slope = custom.LabelText(
            description='Ángulo de socavación',
            units='°'
        )
        self.text_density = custom.LabelText(
            description='Densidad de roca',
            units='t/m3'
        )
        self.button_calculate = widgets.Button(
            description='Generar envolvente'
        )
        self.calculation_status = widgets.HTML()
        self.output_envelope = widgets.Output()
        

    def widgets_layout(self):
        '''Organiza los elementos gráficos del menú'''

        # 1. Generación y visualización del footprint:
        menu_envelope = widgets.VBox([
            self.title_geometry,
            self.text_min_height,
            self.text_max_height,
            self.text_slope,
            self.button_calculate,
            self.output_envelope
        ])

        # Organizar los elementos en la vista:
        self.children = [menu_envelope]


    def show_info(self, value):
        '''
        Muestra un mensaje de información en la salida de resultados
        
        Argumentos:
            height (float): cota óptima de extracción
            value (float): valor económico del piso
        '''
        self.calculation_status.value = f'''
            <span "font-weight: bold;">
                Valor neto de la envolvente = {round(value,2):,} m
            </span>
        '''

    
    def show_error(self):
        '''Muestra un mensaje de error de carga'''
        self.calculation_status.value = '''
            <span style="color:red; font-weight: bold;">
                Complete todos los campos con valores numéricos válidos
            </span>
        '''


    def plot_envelope(self, x_cave, y_cave, z_cave, v_cave, data):

        # Inicializar el gráfico:
        fig = go.Figure()

        # Configurar la barra de color:
        colorbar = dict(
            title       = 'profit' ,   # Título de la barra
            orientation = 'v'      ,   # Posición de la barra
            title_side  = 'right'           # Posición del título de la barra
        )

        # Configuración de los marcadores:
        marker = dict(
            size        = 3         ,   # Tamaño del marcador
            color       = v_cave    ,   # Datos de la escala de color
            colorscale  = 'viridis' ,   # Esquema de color
            opacity     = 0.8       ,   # Opacidad de los marcadores
            showscale   = True      ,   # Mostrar escala de color
            colorbar    = colorbar      # Configuración de la barra de color
        )

        # Generar el grafico inicial para el cobre:
        fig.add_trace(
            go.Scatter3d(
                x       = x_cave    ,
                y       = y_cave    ,
                z       = z_cave    ,
                mode    = 'markers' ,
                marker  = marker
            )
        )

        # fig.add_trace(
        #     go.Scatter3d(
        #         x       = block_model.x[block_model.z == level],
        #         y       = block_model.y[block_model.z == level],
        #         z       = block_model.z[block_model.z == level],
        #         mode    = 'markers' ,
        #         marker_size = 1,
        #         marker_color = 'blue'
        #         # marker  = marker
        #     )
        # )




        dt = data.groupby(['x','y'])['z'].max()
        xx = [point[0] for point in dt.index.values]
        yy = [point[1] for point in dt.index.values]
        zz = dt.values


        lighting_effects = dict(ambient=0.4, diffuse=0.5, roughness = 0.9, specular=0.6, fresnel=0.2)

        fig.add_trace(
            # go.Scatter3d(
            #     x       = np.unique(xx),
            #     y       = np.unique(yy),
            #     z       = zz,
            #     mode    = 'markers' ,
            #     marker_size = 1,
            #     marker_color = 'blue'
            #     # marker  = marker
            # )
            go.Mesh3d(
                x = xx,
                y = yy,
                z = zz,
                opacity = 0.5,
                color = 'turquoise',
                # lighting = {'ambient':0.2}
                lighting = lighting_effects
            )
        )


        # Configuración de los ejes del gráfico:
        scene = dict(
            xaxis_title = 'Coordenada X'        ,
            yaxis_title = 'Coordenada Y'       ,
            zaxis_title = 'Coordenada Z'   ,
            aspectmode  = 'data'
        )

        # Configuración del título del gráfico:
        title = dict(
            text    = '<b>Envolvente económica</b>',
            x       = 0.5       ,
            y       = 0.95      ,
            xanchor = 'center'  ,
            yanchor = 'top'
        )

        # Configuración de los márgenes de la figura:
        margin = dict(
            l = 20  ,
            r = 20  ,
            b = 10  ,
            t = 10
        )

        # Agregar la configuración del gráfico:
        fig.update_layout(
            scene    = scene ,
            margin   = margin,
            title    = title ,
            template = 'plotly_dark',
            height   = 700
        )


        # Generar los gráficos para actualizar la figura (botón):
        list_1 = [v_cave, z_cave]
        list_2 = ['Beneficio', 'Elevación']

        buttons = []
        for varname, var in zip(list_2, list_1):

            args = [{
                'marker.color'          : [var],
                'marker.colorscale'     : 'Viridis',
                'marker.colorbar.title' : varname
            }]

            buttons.append({
                'args'  : args,
                'label' : varname,
                'method': 'restyle'
            })

        # Posición del botón de variables:
        dd_pad = dict(
            r = 10,
            t = 10
        )

        # Configurar el botón de variables:
        dd_set = [dict(
            buttons     = buttons   ,
            direction   = 'down'    ,
            pad         = dd_pad    ,
            showactive  = True      ,
            x           = 0.1       ,
            y           = 1.1       ,
            xanchor     = 'left'    ,
            yanchor     = 'top'
        )]

        # Añadir el botón de variables:
        fig.update_layout(updatemenus = dd_set)

        # Añadir una etiqueta para el botón:
        fig.update_layout(
            annotations = [dict(
                text        = 'Valores: '   ,
                showarrow   = False         ,
                x           = 0.02          ,
                y           = 1.07          ,
                yref        = 'paper'       ,
                align       = 'left'
            )]
        )

        # Añadir un deslizador para el tamaño de marcador:
        steps = []
        for i in range(12):
            steps.append({
                'args'  : [{'marker.size': i+1}],
                'method': 'restyle',
                'label' : '{}'.format(i+1)
            })

        sliders = dict(
            active       = 3,
            steps        = steps,
            currentvalue = {'prefix': 'Tamaño del marcador: '},
            pad          = {"t": 0},
            lenmode      = 'fraction',
            len          = 0.7
        )

        # fig.update_layout(sliders = sliders)

        # Añadir un deslizador para el tamaño de marcador:
        steps = []
        for i in range(10):
            steps.append({
                'args'  : [{'marker.opacity': 10*(i+1)/100}],
                'method': 'restyle',
                'label' : '{}%'.format(10*(i+1))
            })

        sliders2 = dict(
            active       = 8,
            steps        = steps,
            currentvalue = {'prefix': 'Opacidad del marcador: '},
            # tickcolor    = 'black',
            # font         = {'opacity':0},
            pad          = {"t": 80},
            lenmode      = 'fraction',
            len          = 0.7
        )

        fig.update_layout(sliders = [sliders, sliders2])

        with self.output_envelope:
            self.output_envelope.clear_output()
            display(fig)

