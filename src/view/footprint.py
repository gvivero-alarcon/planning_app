# Construcción de la interfaz gráfica:
import ipywidgets as widgets
from IPython.display import display

# Elementos gráficos personalizados:
from view import custom

# Generación de gráficos interactivos:
import plotly.graph_objects as go


class FootprintView(widgets.VBox):
    '''Vista del menú de cálculo y suavizamiento del footprint'''

    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.widgets_layout()
        

    def create_widgets(self):
        '''Crea los elementos gráficos del menú'''

        # 1. Generación y visualización del footprint:
        self.title_footprint = custom.Title(
            value='Generación del footprint'
        )

        self.text_height = custom.LabelText(
            description='Cota del footprint'
        )
        self.button_create = widgets.Button(
            description='Graficar footprint'
        )
        self.output_footprint = widgets.Output()
        
        
        # 2. Suavizamiento del footprint:
        self.title_plot = custom.Title(
            value='Suavizamiento del footprint'
        )
        
        self.text_max_voids = custom.LabelText(
            description='Máx. número de vacíos'
        )
        self.text_min_cols = custom.LabelText(
            description='Añadir cols. adyacentes'
        )
        self.button_smooth = widgets.Button(
            description='Suavizar footprint'
        )
        self.output_smoothing = widgets.Output()


    def widgets_layout(self):
        '''Organiza los elementos gráficos del menú'''

        # 1. Generación y visualización del footprint:
        menu_footprint = widgets.VBox([
            self.title_footprint,
            self.text_height,
            self.button_create,
            self.output_footprint
        ])
        
        # 2. Suavizamiento del footprint:
        menu_smoothing = widgets.VBox([
            self.title_plot,
            self.text_max_voids,
            self.text_min_cols,
            self.button_smooth,
            self.output_smoothing
        ])

        # Organizar los elementos en la vista:
        self.children = [menu_footprint]#, menu_smoothing]


    def plot_footprint(self, x, y, v, level):
        '''Grafica el footprint en la salida correspondiente'''

        # Inicializar figura:
        fig = go.Figure()

        # Barra de color para el beneficio:
        colorbar = dict(
            title='Beneficio [mill $]',
            orientation='v',
            title_side='top'
        )

        # Configuración de los marcadores:
        marker = dict(
            symbol='square',
            size=6,
            line_width=1,
            line_color='gray',
            color=v,
            colorscale='jet',
            showscale=True,
            colorbar=colorbar
        )

        # Graficar el footprint como scatter:
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=marker))

        # Igualar la escala del eje Y con el eje X:
        fig.update_yaxes(scaleanchor="x", scaleratio=1,)

        # Configurar el título de los ejes y razón de aspecto:
        scene = dict(
            xaxis_title='Este [m]',
            yaxis_title='Norte [m]',
            aspectmode='data'
        )

        # Añadir una anotación que funciona como subtítulo:
        fig.update_layout(
            annotations=[dict(
                text='Nivel = {}m'.format(level),
                showarrow=False,
                x=0.5,
                y=1.1,
                xref='paper',
                yref='paper'
            )]
        )

        # Añadir títulos de gráfico y de eje:
        fig.update_layout(
            autosize=True,
            # width=600,
            # height=600,
            title='<b>Gráfico del Footprint</b>',
            title_x=0.5,
            scene=scene
        )

        # Añadir un deslizador para el tamaño de marcador:
        steps = []
        for i in range(12):
            steps.append({
                'args': [{'marker.size': i+1}],
                'method': 'restyle',
                'label': '{}'.format(i+1)
            })

        sliders = [dict(
            active=6,
            steps=steps,
            currentvalue={'prefix': 'Tamaño del marcador: '},
            pad={"t": 50},
            lenmode='fraction',
            len=0.7
        )]

        fig.update_layout(sliders=sliders)

        # Mostrar figura:
        with self.output_footprint:
            self.output_footprint.clear_output()
            display(fig)

