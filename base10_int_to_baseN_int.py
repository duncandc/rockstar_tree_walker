""" Function calculates the base-n representation of a base-10 integer.
"""
import string
digs = string.digits + string.letters

__all__ = ('base_10_signed_int_to_base_n_signed_int', )


def base_10_signed_int_to_base_n_signed_int(i, n):
  if i < 0: sign = -1
  elif i == 0: return digs[0]
  else: sign = 1
  i *= sign
  digits = []
  while i:
    digits.append(digs[i % n])
    i /= n
  if sign < 0:
    digits.append('-')
  digits.reverse()
  return int(''.join(digits))
