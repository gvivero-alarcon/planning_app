# Construcción de la intefaz gráfica:
import ipywidgets as widgets
from IPython.display import display

# Menús principales de la aplicación:
from view.block import BlockView
from view.height import HeightView
from view.footprint import FootprintView
from view.envelope import EnvelopeView


class MainView:
    '''Vista principal de la aplicación'''

    def __init__(self):
        
        # Crear y mostrar los menús principales:
        self.create_menus()
        self.show()

    
    def create_menus(self):
        '''Crea la vista de los menús principales'''

        # Inicializar los menús de la aplicación:
        self.block = BlockView()
        self.height = HeightView()
        self.footprint = FootprintView()
        self.envelope = EnvelopeView()
        
        # Añadir pestañas para cada menú:
        self.tabs = widgets.Tab([
            self.block,
            widgets.VBox([
                self.height, self.footprint]),
            self.envelope
        ])
        
        self.tabs.set_title(0, 'Modelo de bloques')
        # self.tabs.set_title(1, 'Altura óptima')
        self.tabs.set_title(1, 'Footprint')
        self.tabs.set_title(2, 'Envolvente')


    def show(self):
        '''Mostrar la vista principal'''
        display(self.tabs)
