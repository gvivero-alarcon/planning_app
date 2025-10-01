from model.footprint import FootprintModel
from view.footprint import FootprintView


class FootprintController:
    '''
    Controlador del menú de cota óptima de extracción

    Atributos:
        model (HeightModel): modelo del menú de cota óptima
        view (HeightView): vista del menú de cota óptima
    '''

    def __init__(self, model: FootprintModel, view: FootprintView):
        self.model = model
        self.view = view

        # Enlazar eventos de la vista:
        self.bind()


    def bind(self):
        '''Enlaza los eventos de la vista con las funciones del controlador'''
        # El botón button_create se maneja desde el controlador principal (MainController)
        # porque necesita valores de la vista height
        pass


    def calculate_footprint(self, dp_area, dp_cost, discount, velocity):
        '''Calcula la cota óptima de extracción'''

        # Calcular costo de inversión del PE:
        inv_cost = dp_area * dp_cost
        
        # Calcular valores económicos para cada cota:
        zname = self.model.names['z']
        height = self.view.text_height.value
        x, y, v = self.model.get_footprint(
            height=height,
            discount=discount,
            rate=velocity,
            inv_cost=inv_cost
        )

        # Graficar valores por cota:
        self.view.plot_footprint(x, y, v, height)