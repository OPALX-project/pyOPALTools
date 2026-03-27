"""Compatibility helpers for older pyOPALTools plotting styles."""

_PATCHED = False


def install_rcparams_compat():
    """Ignore rcParams removed by newer Matplotlib releases.

    The original style files predate current Matplotlib and still assign a few
    obsolete keys or old values. Those settings should not prevent example
    notebooks from running.
    """

    global _PATCHED
    if _PATCHED:
        return

    import matplotlib as mpl

    rcparams_cls = type(mpl.rcParams)
    original_setitem = rcparams_cls.__setitem__

    def safe_setitem(self, key, value):
        if key == 'lines.marker' and value is None:
            value = 'None'
        elif key == 'grid.color' and value == 'b0b0b0':
            value = '#b0b0b0'

        try:
            original_setitem(self, key, value)
        except (KeyError, ValueError):
            return

    rcparams_cls.__setitem__ = safe_setitem
    _PATCHED = True
