"""
the function of W_ErrorWrap is to wrap a function whoes return
value is always `C_Sucess()`
here is an example:

```py
@W_ErrorWrap
def readfile(filepath) -> I_Status:
    ...
    return C_Success()
```

When code ... throw an exception, W_ErrorWrap will catch it and
turn it into a `C_Failure(repr(err))`.
"""

from ...Abstract.Common.I_Status import I_Status
from .C_Failure import C_Failure

def W_ErrorWrap(func):
    def wrapFunc(*arg, **karg) -> I_Status:
        try:
            status = func(*arg, **karg)
        except Exception as err:
            status = C_Failure(repr(err))
        return status
    return wrapFunc
