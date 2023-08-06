from .rose import rose as rose_, rose_muted as rose_muted_, rose_vivid as rose_vivid_
import numpy as np

__all__ = ['rose', 'rose_muted', 'rose_vivid']


def mpl_to_plotly(cmap, pl_entries: int = 255, r_digits: int = 2):
    """
    Convert matplotlib cmap to plotly colorscale
    :param cmap: colormap
    :param pl_entries: number of Plotly colorscale entries
    :param r_digits: number of digits for rounding scale values
    :return: plotly colorscale
    """
    scale = np.linspace(0, 1, pl_entries)
    colors = (cmap(scale)[:, :3]*255).astype(np.uint8)
    pl_colorscale = [[round(s, r_digits), f'rgb{tuple(color)}'] for s, color in zip(scale, colors)]
    return pl_colorscale


rose = mpl_to_plotly(rose_)
rose_muted = mpl_to_plotly(rose_muted_)
rose_vivid = mpl_to_plotly(rose_vivid_)

