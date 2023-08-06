
 # Dash Spinner

![PyPI](https://img.shields.io/pypi/v/dash-spinner)
![PyPI - License](https://img.shields.io/pypi/l/dash-spinner)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dash-spinner)
[![Downloads](https://static.pepy.tech/personalized-badge/dash-spinner?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)](https://pepy.tech/project/dash-spinner)

This library is designed for use with [Plotly Dash](https://plotly.com). The components have all been
designed to provide functionality similar to Dash's core 
[`Loading` component](https://dash.plotly.com/dash-core-components/loading),
and will display a loading spinner whilst the underlying children are re-rendering.

The spinners in it have been adapted for use from a number of other existing
libraries:

- [react-spinners-kit](https://github.com/dmitrymorozoff/react-spinners-kit)

The majority of spinner names have been retained from the originals, but some have 
been amended where there were name clashes.

---
## Installation

Dash Spinners is available through 
[PyPI](https://pypi.org/project/dash-spinner), and can be installed with pip:

```bash
pip install dash-spinner
```

---
## Basic Usage

Once installed, you can make use of the components as follows:

```python
import dash_spinner
from dash import Dash
app = Dash(__name__)

app.layout = dash_spinner.DashSpinner(
                                    Size=30,
                                    Color='#00ff89',
                                    spinner_type="PushSpinner",
                                    loading=True
                                    )
if __name__ == '__main__':
    app.run_server(debug=True)
```
- Using `@callbacks`
```python
import dash_spinner
from dash import Dash,html,callback,Input, Output
import time

app = Dash(__name__)
app.layout = html.Div(children=[dash_spinner.DashSpinner(
                                    id = 'dash-spinner',
                                    Size=30,
                                    Color='#00ff89',
                                    spinner_type="PushSpinner",
                                    loading=True
                                    ),
                html.Div(id="input")])
@callback(Output('dash-spinner', 'loading'), Input('input', 'children'))
def display_output(value):
    time.sleep(10)
    return False
if __name__ == '__main__':
    app.run_server(debug=True)
```
## All Dash Spinner

![Dash Spinner](https://raw.githubusercontent.com/Chiranjeevit9/Chiranjeevit9/67127437dfe24fb204f4d8619c707d5154ff888b/ezgif.com-gif-maker%20(2).gif)

## Dash Spinner Attributes

There are a number of attributes which are common across all spinners. These are:

- **`id`** (*string*; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app. 
- **`Size`** (*number*; required): Number Required
- **`Color`** (*string*; required): CSS RGB and Hex Color codes
- **`spinner_type`** (*string*; required):Property that determines which spinner to show one of
`BallSpinner` `ClapSpinner` `BarsSpinner` `CircleSpinner` `ClassicSpinner` `CombSpinner`   `CubeSpinner` `DominoSpinner` `FillSpinner` `FireworkSpinner` `FlagSpinner` `FlapperSpinner` `GooSpinner` `GridSpinner` `GuardSpinner` `HeartSpinner` `HoopSpinner` `ImpulseSpinner` `JellyfishSpinner` `MagicSpinner` `MetroSpinner` `PongSpinner` `PulseSpinner` `PushSpinner` `RainbowSpinner` `RingSpinner` `RotateSpinner` `SequenceSpinner` `SphereSpinner` `SpiralSpinner` `SwapSpinner` `SwishSpinner` `TraceSpinner` `WaveSpinner` `WhisperSpinner` 
- **`loading`** (*boolean*; required `True` or `False`):
    Whether the Spinner should show on app start-up before the loading
    state has been determined.