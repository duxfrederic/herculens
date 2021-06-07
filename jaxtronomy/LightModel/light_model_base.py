import jax.numpy as np
from jaxtronomy.LightModel.Profiles import sersic, pixelated
from jaxtronomy.Util.util import convert_bool_list

__all__ = ['LightModelBase']


_SUPPORTED_MODELS = ['SERSIC', 'SERSIC_ELLIPSE', 'CORE_SERSIC', 'PIXELATED']


class LightModelBase(object):
    """Base class for source and lens light models."""
    def __init__(self, light_model_list, smoothing=0.001):
        """Create a LightModelBase object.

        Parameters
        ----------
        light_model_list : list of str
            Light model types.
        smoothing : float
            Smoothing factor for some models (deprecated).

        """
        self.profile_type_list = light_model_list
        func_list = []
        for profile_type in light_model_list:
            if profile_type == 'SERSIC':
                func_list.append(sersic.Sersic(smoothing))
            elif profile_type == 'SERSIC_ELLIPSE':
                func_list.append(sersic.SersicElliptic(smoothing))
            elif profile_type == 'CORE_SERSIC':
                func_list.append(sersic.CoreSersic(smoothing))
            elif profile_type == 'PIXELATED':
                func_list.append(pixelated.PixelatedSource())
            else:
                err_msg = (f"No light model of type {profile_type} found. " +
                           f"Supported types are: {_SUPPORTED_MODELS}")
                raise ValueError(err_msg)
        self.func_list = func_list
        self._num_func = len(self.func_list)

    def surface_brightness(self, x, y, kwargs_list, k=None):
        """Total source flux at a given position.

        Parameters
        ----------
        x, y : float or array_like
            Position coordinate(s) in arcsec relative to the image center.
        kwargs_list : list
            List of parameter dictionaries corresponding to each source model.
        k : int, optional
            Position index of a single source model component.

        """
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        flux = np.zeros_like(x)
        bool_list = convert_bool_list(self._num_func, k=k)
        for i, func in enumerate(self.func_list):
            if bool_list[i]:
                out = np.array(func.function(x, y, **kwargs_list[i]), dtype=float)
                flux += out
        return flux
