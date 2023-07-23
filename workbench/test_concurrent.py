import concurrent.futures as f
import math


def heavy_foo():
  # perform heavy computations
  fact = math.factorial(1000000)
  print("foo done")
  return "foo"


def heavy_bar():
  # perform heavy computations
  fact = math.factorial(1000000)
  print("bar done")
  return "bar"


def heavy_tam():
  # perform heavy computations
  fact = math.factorial(1000000)
  print("tam done")
  return "tam"


with f.ThreadPoolExecutor() as ex:

  futures = {
    ex.submit(heavy_foo),
    ex.submit(heavy_bar),
    ex.submit(heavy_tam)
  }

  for future in f.as_completed(futures):
    result = future.result()
    print("result", result)