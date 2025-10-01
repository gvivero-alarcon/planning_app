from controller.block import BlockController
from controller.height import HeightController
from controller.footprint import FootprintController
from controller.envelope import EnvelopeController

class MainController:
    def __init__(self, model, view):
        
        # Inicializar modelo y vista principales:
        self.model = model
        self.view = view

        # Inicializar controladores específicos:
        self.block = BlockController(
            model=self.model.block,
            view=self.view.block
        )

        self.height = HeightController(
            model=self.model.height,
            view=self.view.height
        )

        self.footprint = FootprintController(
            model=self.model.footprint,
            view=self.view.footprint
        )

        self.envelope = EnvelopeController(
            model=self.model.envelope,
            view=self.view.envelope
        )


        # Enlazar eventos de la vista principal:
        self.bind()


    def bind(self):
        '''Enlaza los eventos de la vista con las funciones del controlador'''
        
        # Enlazar función al botón de cargar archivo:
        self.view.block.button_import.on_click(self.load_file)
        self.view.footprint.button_create.on_click(self.generate_footprint)
        self.view.envelope.button_calculate.on_click(self.generate_envelope)


    def load_file(self, event):
        '''Carga un archivo seleccionado como modelo de bloques'''
        cols = self.block.load_file()
        self.view.height.update_profit(cols)


    def generate_footprint(self, event):
        '''Calcula la cota óptima de extracción'''

        # Recuperar parámetros de cálculo:
        try:
            discount = self.view.height.text_discount.value / 100
            velocity = self.view.height.text_velocity.value
            dp_area = self.view.height.text_dp_area.value
            dp_cost = self.view.height.text_dp_cost.value
        except:
            self.view.height.show_error()
            return
        
        # Calcular cota óptima de extracción:
        self.footprint.calculate_footprint(
            dp_area=dp_area,
            dp_cost=dp_cost,
            discount=discount,
            velocity=velocity
        )


    def generate_envelope(self, event):
        level = self.view.footprint.text_height.value
        profit_name = self.view.height.drop_profit.value

        self.envelope.calculate_envelope(level, profit_name)
