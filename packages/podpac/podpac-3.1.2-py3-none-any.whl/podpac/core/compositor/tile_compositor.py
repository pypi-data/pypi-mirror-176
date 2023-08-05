from __future__ import division, unicode_literals, print_function, absolute_import

import numpy as np
import xarray as xr
import pandas as pd
import traitlets as tl

from podpac.core.utils import common_doc
from podpac.core.compositor.compositor import COMMON_COMPOSITOR_DOC, BaseCompositor
from podpac.core.units import UnitsDataArray
from podpac.core.interpolation.interpolation import InterpolationMixin
from podpac.core.coordinates import Coordinates


@common_doc(COMMON_COMPOSITOR_DOC)
class TileCompositorRaw(BaseCompositor):
    """Compositor that combines tiled sources.

    The requested data does not need to be interpolated by the sources before being composited

    Attributes
    ----------
    sources : list
        Source nodes (tiles). The sources should not be overlapping.
    source_coordinates : :class:`podpac.Coordinates`
        Coordinates that make each source unique. Must the same size as ``sources`` and single-dimensional. Optional.
    """

    @common_doc(COMMON_COMPOSITOR_DOC)
    def composite(self, coordinates, data_arrays, result=None):
        """Composites data_arrays (tiles) into a single result.

        Parameters
        ----------
        coordinates : :class:`podpac.Coordinates`
            {requested_coordinates}
        data_arrays : generator
            Evaluated source data.
        result : podpac.UnitsDataArray, optional
            {eval_output}

        Returns
        -------
        {eval_return} This composites tiled sources into a single result.
        """

        # TODO: Fix boundary information on the combined data arrays
        res = next(data_arrays)
        bounds = res.attrs.get("bounds", {})
        for arr in data_arrays:
            res = res.combine_first(arr)

            # combine_first overrides MultiIndex names, even if they match. Reset them here:
            for dim, index in res.indexes.items():
                if isinstance(index, pd.MultiIndex):
                    res = res.reindex({dim: pd.MultiIndex.from_tuples(index.values, names=arr.indexes[dim].names)})

            obounds = arr.attrs.get("bounds", {})
            bounds = {
                k: (min(bounds[k][0], obounds[k][0]), max(bounds[k][1], obounds[k][1])) for k in bounds if k in obounds
            }
        res = UnitsDataArray(res)
        if bounds:
            res.attrs["bounds"] = bounds
        if result is not None:
            result.data[:] = res.transpose(*result.dims).data
            return result
        return res


class TileCompositor(InterpolationMixin, TileCompositorRaw):
    pass
