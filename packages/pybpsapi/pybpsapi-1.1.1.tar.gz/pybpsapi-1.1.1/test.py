import pybpsapi

ptm = pybpsapi.CircularChecker('ptm')
general = pybpsapi.CircularChecker('general')

group = pybpsapi.CircularCheckerGroup(ptm, general)

e = group.check()
print(e)