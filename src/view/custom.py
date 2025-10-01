import ipywidgets as widgets

LABEL_WIDTH = '180px'
MARGIN = '10px 0px 0px 0px'


class LabelDrop(widgets.HBox):
    '''
    Layout horizontal que contiene una etiqueta y un menú desplegable

    Argumentos:
        description (str): texto de la etiqueta
        options (list): opciones del menú desplegable

    Atributos:
        _label (widgets.Label): etiqueta
        _drop (widgets.Dropdown): menú desplegable
    '''

    def __init__(self, description, options=[]):
        super().__init__()

        # Crear los elementos gráficos:
        self._label = widgets.Label(description, layout={'width': LABEL_WIDTH})
        self._drop = widgets.Dropdown(options=options)

        # Colocar los elementos gráficos:
        self.children = [self._label, self._drop]

    
    def observe_(self, handler, names=..., type="change"):
        '''Enlaza una función a los cambios en el menú desplegable'''
        return self._drop.observe(handler, names, type)
    
    
    @property
    def value(self):
        '''Devuelve el valor seleccionado en el menú desplegable'''
        return self._drop.value
    

    @value.setter
    def value(self, value):
        '''Establece el valor seleccionado en el menú desplegable'''
        self._drop.value = value
        

    @property
    def options(self):
        '''Devuelve las opciones del menú desplegable'''
        return self._drop.options
    
    @options.setter
    def options(self, options):
        '''Establece las opciones del menú desplegable'''
        self._drop.options = options


class LabelRadio(widgets.HBox):
    '''
    Layout horizontal que contiene una etiqueta y un botón de radio

    Argumentos:
        description (str): texto de la etiqueta
        options (list): opciones del botón de radio

    Atributos:
        _label (widgets.Label): etiqueta
        _radio (widgets.RadioButtons): botón de radio
    '''

    def __init__(self, description, options=[]):
        super().__init__()

        # Crear los elementos gráficos:
        self._label = widgets.Label(description, layout={'width': LABEL_WIDTH})
        self._radio = widgets.RadioButtons(options=options)

        # Colocar los elementos gráficos:
        self.children = [self._label, self._radio]
        

    @property
    def value(self):
        '''Devuelve el valor seleccionado en el botón de radio'''
        return self._radio.value
    

    @value.setter
    def value(self, value):
        '''Establece el valor seleccionado en el botón de radio'''
        self._radio.value = value


class LabelSlider(widgets.HBox):
    '''
    Layout horizontal que contiene una etiqueta y un deslizador de rango

    Argumentos:
        description (str): texto de la etiqueta

    Atributos:
        _label (widgets.Label): etiqueta
        _slider (widgets.FloatRangeSlider): deslizador de rango
    '''

    def __init__(self, description):
        super().__init__()

        # Crear los elementos gráficos:
        self._label = widgets.Label(description, layout={'width': LABEL_WIDTH})
        self._slider = widgets.FloatRangeSlider()

        # Colocar los elementos gráficos:
        self.children = [self._label, self._slider]
        

    @property
    def value(self):
        '''Devuelve el valor seleccionado en el deslizador de rango'''
        return self._slider.value
    

    @value.setter
    def value(self, value):
        '''Establece el valor seleccionado en el deslizador de rango'''
        self._slider.value = value


    @property
    def min(self):
        '''Devuelve el valor mínimo del deslizador de rango'''
        return self._slider.min
    
    @min.setter
    def min(self, min):
        '''Establece el valor mínimo del deslizador de rango'''
        self._slider.min = min

    @property
    def max(self):
        '''Devuelve el valor máximo del deslizador de rango'''
        return self._slider.max
    
    @max.setter
    def max(self, max):
        '''Establece el valor máximo del deslizador de rango'''
        self._slider.max = max


class LabelText(widgets.HBox):
    '''
    Layout horizontal que contiene una etiqueta y un campo de texto

    Argumentos:
        description (str): texto de la etiqueta

    Atributos:
        _label (widgets.Label): etiqueta
        _text (widgets.Text): campo de texto
    '''

    def __init__(self, description, units=''):
        super().__init__()

        # Crear los elementos gráficos:
        self._label = widgets.Label(description, layout={'width': LABEL_WIDTH})
        self._text = widgets.Text()
        self._units = widgets.Label(value=units)

        # Colocar los elementos gráficos:
        self.children = [self._label, self._text, self._units]
        

    @property
    def value(self):
        '''Devuelve el valor seleccionado en el campo de texto'''
        return float(self._text.value)
    

    @value.setter
    def value(self, value):
        '''Establece el valor seleccionado en el campo de texto'''
        self._text.value = value
        

class Title(widgets.Label):
    '''Etiqueta personalizada para títulos'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Establecer texto en mayúsculas:
        self.value = self.value.upper()

        # Configurar layout de la etiqueta:
        self.layout = widgets.Layout(margin=MARGIN)
        

class ToolButton(widgets.Button):
    '''
    Layout horizontal que contiene una etiqueta y un botón

    Argumentos:
        tool (str): tipo de símbolo del botón
        **kwargs: argumentos adicionales para el botón
    '''

    def __init__(self, tool='update', **kwargs):
        super().__init__(**kwargs)

        # Configurar el estilo del botón:
        self.layout.width = '35px'
        
        # Cambiar el símbolo del botón:
        if tool == 'update':
            symbol = '\u21ba'
        else:
            symbol = '...'
        
        self.description = symbol
        

class CheckDropdown(widgets.HBox):
    '''
    Layout horizontal que contiene una casilla de verificación y un menú
    desplegable

    Argumentos:
        description (str): texto de la etiqueta
        options (list): opciones del menú desplegable

    Atributos:
        _check (widgets.Checkbox): casilla de verificación
        _drop (widgets.Dropdown): menú desplegable
    '''

    def __init__(self, description, options=[]):
        super().__init__()

        # Crear los elementos gráficos:
        self._check = widgets.Checkbox(
            description=description,
            indent=False,
            layout={'width': LABEL_WIDTH}
        )
        self._drop = widgets.Dropdown(options=options)

        # Colocar los elementos gráficos:
        self.children = [self._check, self._drop]
        

    @property
    def checked(self):
        '''Devuelve el estado de la casilla de verificación'''
        return self._check.value
    

    @checked.setter
    def checked(self, value):
        '''Establece el estado de la casilla de verificación'''
        self._check.value = value
        

    @property
    def value(self):
        '''Devuelve el valor seleccionado en el menú desplegable'''
        return self._drop.value
    

    @value.setter
    def value(self, value):
        '''Establece el valor seleccionado en el menú desplegable'''
        self._drop.value = value
        

    @property
    def options(self):
        '''Devuelve las opciones del menú desplegable'''
        return self._drop.options
    
    @options.setter
    def options(self, options):
        '''Establece las opciones del menú desplegable'''
        self._drop.options = options