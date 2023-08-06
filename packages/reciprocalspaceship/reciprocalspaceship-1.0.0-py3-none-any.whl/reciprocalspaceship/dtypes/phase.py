from pandas.core.dtypes.dtypes import register_extension_dtype

from reciprocalspaceship.dtypes.base import MTZFloat32Dtype, MTZFloatArray


@register_extension_dtype
class PhaseDtype(MTZFloat32Dtype):
    """Dtype for representing phase data in reflection tables"""

    name = "Phase"
    mtztype = "P"

    def is_friedel_dtype(self):
        return False

    @classmethod
    def construct_array_type(cls):
        return PhaseArray


class PhaseArray(MTZFloatArray):
    """ExtensionArray for supporting PhaseDtype"""

    _dtype = PhaseDtype()
    pass


@register_extension_dtype
class HendricksonLattmanDtype(MTZFloat32Dtype):
    """
    Dtype for representing phase probability coefficients
    (Hendrickson-Lattman) in reflection tables
    """

    name = "HendricksonLattman"
    mtztype = "A"

    def is_friedel_dtype(self):
        return False

    @classmethod
    def construct_array_type(cls):
        return HendricksonLattmanArray


class HendricksonLattmanArray(MTZFloatArray):
    """ExtensionArray for supporting HendricksonLattmanDtype"""

    _dtype = HendricksonLattmanDtype()
    pass
