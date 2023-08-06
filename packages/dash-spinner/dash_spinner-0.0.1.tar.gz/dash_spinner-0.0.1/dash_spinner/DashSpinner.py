# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashSpinner(Component):
    """A DashSpinner component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- Color (string; required):
    The Color used to specified color of spinner.

- Size (number; required):
    A Size used to size of spinner.

- loading (boolean; required):
    The loading used to enable and disable the spinner.

- spinner_type (string; required):
    The spinner_type used to specified type of spinner."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_spinner'
    _type = 'DashSpinner'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, spinner_type=Component.REQUIRED, Size=Component.REQUIRED, Color=Component.REQUIRED, loading=Component.REQUIRED, **kwargs):
        self._prop_names = ['id', 'Color', 'Size', 'loading', 'spinner_type']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'Color', 'Size', 'loading', 'spinner_type']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['Color', 'Size', 'loading', 'spinner_type']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(DashSpinner, self).__init__(**args)
