from pandas.core.dtypes.dtypes import register_extension_dtype

from reciprocalspaceship.dtypes.base import MTZInt32Dtype, MTZIntegerArray


@register_extension_dtype
class M_IsymDtype(MTZInt32Dtype):
    """Dtype for representing M/ISYM values"""

    name = "M/ISYM"
    mtztype = "Y"

    def is_friedel_dtype(self):
        return False

    @classmethod
    def construct_array_type(cls):
        return M_IsymArray


class M_IsymArray(MTZIntegerArray):
    """ExtensionArray for supporting M_IsymDtype"""

    _dtype = M_IsymDtype()
    pass
