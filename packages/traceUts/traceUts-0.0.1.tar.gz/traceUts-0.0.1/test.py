from TraceUts import traceMap
import TraceUts

TraceUts.CallBack = lambda x:print(x)

@traceMap(main=True)
def soma(a,b):
    return a/b


res = soma(1,0)


a  =1


