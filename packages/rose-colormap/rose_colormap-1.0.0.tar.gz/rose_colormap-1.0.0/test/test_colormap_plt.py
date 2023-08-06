import pytest
import numpy as np
import matplotlib.pyplot as plt
import os
dirname = os.path.dirname(__file__)


def colorize(fig, ax, cm):
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
        return rgb + (1.0 - rgb) * tint_factor

    # Add colored foreground and background with randomly sampled colors
    front_color = cm.__call__(np.random.rand())
    front_color = [tint(c, 0.8) for c in front_color]
    ax.set_facecolor(front_color)
    back_color = cm.__call__(np.random.rand())
    back_color = [tint(c, 0.5) for c in back_color]
    fig.patch.set_facecolor(back_color)

    # Remove ticks
    ax.yaxis.set_major_locator(plt.NullLocator())
    ax.xaxis.set_major_locator(plt.NullLocator())


def scatter_plot(cm, cm_name):
    """
    Draw a random points scatter plot
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, dpi=144)
    x = np.random.rand(100)
    y = np.random.rand(100)
    t = np.arange(100)
    plt.title(f'scatter plot, {cm_name}')
    plt.scatter(x, y, c=t, cmap=cm)
    plt.colorbar()
    colorize(fig, ax, cm)
    fig.tight_layout()
    plt.savefig(os.path.join(dirname, f'figs/scatter_{cm_name}.png'))
    plt.show()


def wave_plot(cm, cm_name):
    """
    Draw a wave-like array plot
    """
    x, y = np.mgrid[-5:5:0.05, -5:5:0.05]
    z = (np.sqrt(x ** 2 + y ** 2) + np.sin(x ** 2 + y ** 2))

    fig, ax = plt.subplots(nrows=1, ncols=1, dpi=144)
    plt.title(f'wave plot, {cm_name}')
    im = ax.imshow(z, cmap=cm)
    fig.colorbar(im)
    colorize(fig, ax, cm)
    fig.tight_layout()
    plt.savefig(os.path.join(dirname, f'figs/wave_{cm_name}.png'))
    plt.show()


def surface_plot(cm, cm_name):
    """
    Draw a 3D surface plot
    """
    x = np.outer(np.linspace(-3, 3, 32), np.ones(32))
    y = x.copy().T
    z = (np.sin(x ** 2) + np.cos(y ** 2))

    # Creating figure
    fig = plt.figure(dpi=144)
    ax = plt.axes(projection ='3d')
    plt.title(f'surface plot, {cm_name}')
    surf = ax.plot_surface(x, y, z, cmap=cm)
    fig.colorbar(surf, ax=ax)
    colorize(fig, ax, cm)

    # Make the panes transparent
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    ax.zaxis.set_major_locator(plt.NullLocator())  # Remove z-axis as well
    fig.tight_layout()
    plt.savefig(os.path.join(dirname, f'figs/surface_{cm_name}.png'))
    plt.show()


@pytest.mark.parametrize("cm_name", ["rose", "rose_muted", "rose_vivid"])
def test_colormap_plt(cm_name):
    # noinspection PyUnresolvedReferences
    from visualization.rose_colormap import rose, rose_muted, rose_vivid

    cm = locals()[cm_name]
    scatter_plot(cm, cm_name)
    wave_plot(cm, cm_name)
    surface_plot(cm, cm_name)
