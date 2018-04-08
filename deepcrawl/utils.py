
def atoi(s):
  if isinstance(s, str):
    last = s[-1]
    if last == 'w':
      return int(float(s[:-1]) * 10000)
  return s