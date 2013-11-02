import time
import os
import copy
import logging
from functools import *

log = logging.getLogger(__name__)


def timeMe(fun):
  def timed(*args, **kwargs):
    start = time.time()    
    spill = fun(*args, **kwargs)
    log.info("%s() took %f seconds to execute"%(fun.__name__, time.time()-start))
    return spill
  return timed

def showMe(fun):
  def showed(*args, **kwargs):
    spill = fun(*args, **kwargs)
    log.info("%s() returned %s"%(fun.__name__, str(spill)))
    return spill
  return showed

def cacheMemo(interval):
  """Decorator which caches the result of its function for a given interval
     memoized class taken from http://wiki.python.org/moin/PythonDecoratorLibrary
     The intervals are accounted for individually for each arg set.

     For example, if the decorated function is called as fun("abc",123) and then 
     called before the expiry as fun(123,"abc"), two results will be cached, both with
     their own expiry time.

     The value returned are actually deep copies, rather than the original return...

     The interval is in seconds.

     (Hairy - you've been warned)
  """
  import time
  import functools

  class ExpireMemoized(object):
    def __init__(self, func):
      time.time()
      self.func = func
      self.cache = {}
    def __call__(self, *args):
      if CACHE:
        try:
          hit = self.cache[args]
          if hit["expiry"] < time.time():
            return self.__renew(*args)
          else:
            return copy.deepcopy(hit["value"])
        except KeyError:
          return self.__renew(*args)
        except TypeError:
          return self.__renew()
      else:
        return self.func(*args)
    def __renew(self, *args):
      try:
        value = self.func(*args)
        self.cache[args] = {"value" : value, "expiry": time.time() + interval }
        return copy.deepcopy(value)
      except TypeError:
        return self.func(*args)
    @property
    def __name__(self):
      return "ExpireMemoized(%s)"%self.func.__name__
    def __get__(self, obj, objtype):
      return functools.partial(self.__call__, obj)

  return ExpireMemoized
