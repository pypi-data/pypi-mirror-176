import pytest
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os
dirname = os.path.dirname(__file__)


def colorize(fig, cm):
    """
    Add random color and remove ticks for appearance
    """
    def tint(rgb, tint_factor):
        """
        Tint a color by tint_factor
        :param rgb: scalar r or g or b value, between 0.0 ~ 1.0
        :param tint_factor: degree of tint, between 0.0 ~ 1.0. <br>
                            0 will be no tint, 1 will be white.
        """
        return rgb + (255 - rgb) * tint_factor

    # Add colored foreground and background with randomly sampled colors
    front_color = [int(i) for i in cm[np.random.randint(255)][1][4:-1].split(',')]
    front_color = [int(tint(c, 0.8)) for c in front_color]
    back_color = [int(i) for i in cm[np.random.randint(255)][1][4:-1].split(',')]
    back_color = [int(tint(c, 0.5)) for c in back_color]

    fig.update_layout({
        'plot_bgcolor': f"rgb{tuple(front_color)}",
        'paper_bgcolor': f"rgb{tuple(back_color)}",
    })

    # hide subplot y-axis titles and x-axis titles
    for axis in fig.layout:
        if len(axis) == 5 and axis.endswith('axis'):
            fig.layout[axis].title.text = ''
            fig.layout[axis].tickfont = dict(color='rgba(0,0,0,0)')

    fig.layout['margin'] = dict(l=0, r=0, t=60, b=0)

    return front_color, back_color


def scatter_plot(cm, cm_name):
    """
    Draw a random points scatter plot
    """
    x = np.random.rand(100)
    y = np.random.rand(100)
    t = np.arange(100)
    fig = px.scatter(x=x, y=y, color=t, color_continuous_scale=cm, width=614, height=463,
                     title=f'scatter plot, {cm_name}')
    colorize(fig, cm)
    fig.write_image(os.path.join(dirname, f"figs/plotly/scatter_{cm_name}.png"), scale=1.5)


def wave_plot(cm, cm_name):
    """
    Draw a wave-like array plot
    """
    x, y = np.mgrid[-5:5:0.05, -5:5:0.05]
    z = (np.sqrt(x ** 2 + y ** 2) + np.sin(x ** 2 + y ** 2))

    fig = px.imshow(z, color_continuous_scale=cm, width=614, height=463,
                    title=f'wave plot, {cm_name}')
    colorize(fig, cm)
    fig.write_image(os.path.join(dirname, f"figs/plotly/wave_{cm_name}.png"), scale=1.5)


def surface_plot(cm, cm_name):
    """
    Draw a 3D surface plot
    """
    x = np.outer(np.linspace(-3, 3, 32), np.ones(32))
    y = x.copy().T
    z = (np.sin(x ** 2) + np.cos(y ** 2))

    # Creating figure
    fig = go.Figure(go.Surface(x=x, y=y, z=z, colorscale=cm))
    fig.update_layout(title=f'surface plot, {cm_name}', autosize=False,
                      width=614, height=463)
    front_color, _ = colorize(fig, cm)
    fig.update_scenes({
            'xaxis': {"backgroundcolor": f"rgb{tuple(front_color)}"},
            'yaxis': {"backgroundcolor": f"rgb{tuple(front_color)}"},
            'zaxis': {"backgroundcolor": f"rgb{tuple(front_color)}"}
    })
    fig.layout['margin'] = dict(l=40, r=40, t=40, b=10)
    fig.write_image(os.path.join(dirname, f"figs/plotly/surface_{cm_name}.png"), scale=1.5)


@pytest.mark.parametrize("cm_name", ["rose", "rose_muted", "rose_vivid"])
def test_colormap_plotly(cm_name):
    # noinspection PyUnresolvedReferences
    from visualization.rose_colormap.plotly import rose, rose_muted, rose_vivid

    cm = locals()[cm_name]
    # scatter_plot(cm, cm_name)
    # wave_plot(cm, cm_name)
    surface_plot(cm, cm_name)
