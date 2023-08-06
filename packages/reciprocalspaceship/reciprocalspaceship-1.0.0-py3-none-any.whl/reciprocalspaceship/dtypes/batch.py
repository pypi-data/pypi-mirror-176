from pandas.core.dtypes.dtypes import register_extension_dtype

from reciprocalspaceship.dtypes.base import MTZInt32Dtype, MTZIntegerArray


@register_extension_dtype
class BatchDtype(MTZInt32Dtype):
    """Dtype for representing batch numbers"""

    name = "Batch"
    mtztype = "B"

    def is_friedel_dtype(self):
        return False

    @classmethod
    def construct_array_type(cls):
        return BatchArray


class BatchArray(MTZIntegerArray):
    """ExtensionArray for supporting BatchDtype"""

    _dtype = BatchDtype()
    pass
