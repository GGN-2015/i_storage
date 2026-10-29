def W_ErrorDefault(defaultValue):
    def _wrapper(func):
        def _f(*arg, **karg):
            try:
                ans = func(*arg, **karg)
            except Exception:
                ans = defaultValue
            return ans
        return _f
    return _wrapper
