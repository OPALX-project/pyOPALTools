import matplotlib.ticker

# 12. March 2019
# https://stackoverflow.com/questions/45815396/how-to-change-the-the-number-of-digits-of-the-mantissa-using-offset-notation-in
class FormatScalarFormatter(matplotlib.ticker.ScalarFormatter):
    def __init__(self, fformat="%1.1f", offset=True, mathText=True):
        self.fformat = fformat
        matplotlib.ticker.ScalarFormatter.__init__(self,
                                                   useOffset=offset,
                                                   useMathText=mathText)
    def _set_format(self, vmin, vmax):
        self.format = self.fformat
        if self._useMathText:
            self.format = '$%s$' % matplotlib.ticker._mathdefault(self.format)
