import numpy as np

A=np.array([[2,4],[1,3]])

u,s,v=np.linalg.svd(A)

print(np.linalg.svd(A))

print('u:',u)
print('s:',s)
print('v:',v)
