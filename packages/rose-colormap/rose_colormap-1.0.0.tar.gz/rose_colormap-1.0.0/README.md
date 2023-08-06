<p align="center"><img src="https://raw.githubusercontent.com/Rose-STL-Lab/rose_colormap/main/test/figs/RoseMosaic.jpg" width="600"></p>
<h2 align="center">The Rose Colormap - Rose-inspired Python Colormaps</h2>
<p align="center">For Spatiotemporal Visualization</p>

<p align="center">
    <a href="https://zzhou.info/LICENSE"><img src="https://camo.githubusercontent.com/87d0b0ec1c0a97dbf68ce4d3098de6912bca75aa006304dd0a55976e6673cbe1/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f64656c67616e2f6c6f677572752e737667" alt="license"></a>
    <img src="https://img.shields.io/badge/Python-3.8+-yellow" alt="python">
    <img src="https://img.shields.io/badge/Version-1.0.0-green" alt="version">
</p>



## What is the Rose Colormap?

The Rose Colormap is a series of Python colormaps / colorscales including *Rose*, *Rose Muted* and *Rose Vivid*. The pink tops and the green basis constitute a sharp contrast such that it is perfect for visualizing peaks in spatiotemporal dynamics.

<p align="center">
    <img src="https://raw.githubusercontent.com/ZihaoZhou/DeepSTPP/master/example.gif" width="400" alt="intensity">
</p>
<p align="center">
    Visualizing spatiotemporal event arrival rate using <i>Rose Vivid</i>
</p>

## How do I install the Rose Colormap?

The Rose Colormap can be installed via pip from [PyPI](https://pypi.org/).

```
pip install rose_colormap
```

## How do I use the Rose Colormap?

The Rose colormap can be used with either **Matplotlib** or **Plotly.py**.

**(1) Matplotlib example usage**

```python
import matplotlib.pyplot as plt
import numpy as np
from rose_colormap import rose, rose_muted, rose_vivid

x = np.random.rand(100)
y = np.random.rand(100)
t = np.arange(100)
plt.scatter(x, y, c=t, cmap=rose_vivid)
plt.colorbar()
plt.show()
```

**(2) Plotly Express example usage**

```python
import plotly.express as px
import numpy as np
from rose_colormap import rose, rose_muted, rose_vivid

x = np.random.rand(100)
y = np.random.rand(100)
t = np.arange(100)
fig = px.scatter(x=x, y=y, color=t, color_continuous_scale=rose_vivid)
fig.show()
```

**(3) Plotly Graph Object example usage**

```python
import plotly.graph_objects as go
import numpy as np
from rose_colormap import rose, rose_muted, rose_vivid

x = np.outer(np.linspace(-3, 3, 32), np.ones(32))
y = x.copy().T
z = (np.sin(x ** 2) + np.cos(y ** 2))
fig = go.Figure(go.Surface(x=x, y=y, z=z, colorscale=rose_vivid))
fig.show()
```

## Uninstall

```
pip uninstall rose_colormap
```


### Thanks To:

Members of the Rose lab for supporting this work.
