# Construcción de la interfaz gráfica:
import ipywidgets as widgets
from IPython.display import display

# Elementos gráficos personalizados:
from view import custom

# Generación de gráficos interactivos:
import plotly.graph_objects as go


class HeightView(widgets.VBox):
    '''Vista del menú de cálculo de altura óptima del UCL'''
    
    def __init__(self, ):
        super().__init__()
        self.create_widgets()
        self.widgets_layout()


    def create_widgets(self):
        '''Crear los elementos gráficos del menú'''

        # 1. Parámetros económicos:
        self.title_economics = custom.Title(
            value='Parámetros económicos'
        )

        self.drop_profit = custom.LabelDrop(
            description='Valor del bloque'
        )
        
        self.text_discount = custom.LabelText(
            description='Tasa de descuento',
            units='%'
        )

        self.text_dp_cost = custom.LabelText(
            description='Costo de apertura DP',
            units='$/m²'
        )

        # 2. Parámetros operacionales:
        self.title_operational = custom.Title(
            value='Parámetros operacionales'
        )

        self.text_velocity = custom.LabelText(
            description='Tasa extracción vertical',
            units='m/año'
        )

        self.text_dp_area = custom.LabelText(
            description='Área punto de extracción',
            units='m²'
        )
        
        # 3. Botón de cálculo y visualización de resultados:
        self.button_calculate = widgets.Button(
            description='Calcular cota'
        )
        
        self.output_results = widgets.HTML()
        self.output_plot = widgets.Output()
        
        
    def widgets_layout(self):
        '''Colocar los elementos gráficos del menú en el layout'''

        # 1. Parámetros económicos:
        menu_economics = widgets.VBox([
            self.title_economics,
            self.drop_profit,
            self.text_discount,
            self.text_dp_cost
        ])

        # 2. Parámetros operacionales:
        menu_operational = widgets.VBox([
            self.title_operational,
            self.text_velocity,
            self.text_dp_area
        ])

        # 3. Botón de cálculo y visualización de resultados:
        menu_calculation = widgets.VBox([
            self.button_calculate,
            self.output_results,
            self.output_plot
        ])

        # 4. Colocar en el layout principal:
        self.children = [menu_economics, menu_operational, menu_calculation]


    def update_profit(self, cols):
        '''
        Actualizar la lista de archivos en el menú desplegable
        
        Argumentos:
            cols (list): lista de columnas del modelo de bloques
        '''
        self.drop_profit.options = cols
        self.drop_profit.value = None


    def show_info(self, height, value):
        '''
        Muestra un mensaje de información en la salida de resultados
        
        Argumentos:
            height (float): cota óptima de extracción
            value (float): valor económico del piso
        '''
        self.output_results.value = f'''
            <span "font-weight: bold;">
                Nivel que maximiza el valor económico = {height:.2f} m <br>
                Máximo valor económico = ${round(value, 2):,}
            </span>
        '''

    
    def show_get_error(self):
        '''Muestra un mensaje de error de carga'''
        self.output_results.value = '''
            <span style="color:red; font-weight: bold;">
                Complete todos los campos con valores numéricos válidos
            </span>
        '''
            
    
    def plot_height_vs_value(self, heights, values, opt_height, opt_value):
        '''
        Genera un gráfico del valor económico del piso vs cota de extracción
        
        Argumentos:
            heights (list): lista de cotas de extracción
            values (list): lista de valores económicos del piso
        '''
        
        # Limpiar la salida del gráfico:
        self.output_plot.clear_output()

        # Crear el gráfico:
        fig = go.Figure(data=[
            go.Scatter(
                x=heights,
                y=values,
                mode='lines',
                name='Valor'
            ),
            go.Scatter(
                x=[opt_height, opt_height, min(heights)],
                y=[0, opt_value, opt_value],
                mode='lines',
                name='Óptimo',
                line=dict(dash='dash', color='green')
            )
        ])

        fig.update_layout(
            title='Valor económico del piso vs cota de extracción',
            xaxis_title='Elevación (m)',
            yaxis_title='Valor económico del piso ($)',
            title_x=0.5,
            showlegend=False,
            autosize=True
        )

        # Mostrar el gráfico en la salida correspondiente:
        with self.output_plot:
            display(fig)

