T = b'b'
C = "b"

import numpy as np
a = np.zeros(shape=(1, 1), dtype=str)
a[0][0] = "b"
print(a[0][0])

print(str(T), "  ", C)
print(str(T) == C)
print(str(a[0][0]) == C)