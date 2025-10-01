from model.height import HeightModel
from view.height import HeightView


class HeightController:
    '''
    Controlador del menú de cota óptima de extracción

    Atributos:
        model (HeightModel): modelo del menú de cota óptima
        view (HeightView): vista del menú de cota óptima
    '''

    def __init__(self, model: HeightModel, view: HeightView):
        self.model = model
        self.view = view

        # Enlazar eventos de la vista:
        self.bind()


    def bind(self):
        '''Enlaza los eventos de la vista con las funciones del controlador'''
        self.view.button_calculate.on_click(self.calculate_height)


    def calculate_height(self, event):
        '''Calcula la cota óptima de extracción'''
        
        # Recuperar parámetros de cálculo:
        try:
            discount = self.view.text_discount.value / 100
            velocity = self.view.text_velocity.value
            dp_area = self.view.text_dp_area.value
            dp_cost = self.view.text_dp_cost.value
        except:
            self.view.show_get_error()
            return

        # Calcular costo de inversión del PE:
        inv_cost = dp_area * dp_cost
        
        # Calcular valores económicos para cada cota:
        zname = self.model.names['z']
        heights = self.model.data[zname].unique()
        values = self.model.value_by_height(
            heights=heights,
            discount=discount,
            rate=velocity,
            inv_cost=inv_cost
        )

        # Hallar valores óptimos:
        opt_height, opt_value = self.model.find_optimum(heights, values)

        # Entregar resultados óptimos:
        self.view.show_info(opt_height, opt_value)

        # Graficar valores por cota:
        with self.view.output_plot:
            self.view.plot_height_vs_value(
                heights, values, opt_height, opt_value
            )