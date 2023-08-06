# django-ndarrayfield
New Django field to store numpy ndarray.

## Description
Store a numpy n-dimensional array in database (compatible with all database backend).
Use numpy save/load, you can define a shape (not required), and a dtype (default float32).

## Usage

```python
import numpy as np
from django.db import models
from ndarraydjango.fields import NDArrayField


class MyModel(models.Model):
    vec1 = NDArrayField(shape=(32, 4), dtype=np.float64)
    date = models.DateTimeField(auto_now_add=True)
```

## Parameters

* **dtype**: the ndarray dtype (default np.float32)
* **shape**: the ndarray shape (default None)
* **binary_serialize**: when dump data, serialize to binary (base64) or json lists (default False)



## Warning
This field type does not replace a static file storage.
The main goal is to store parameter data, results of algorithms and
small and medium machine learning models.
A good indication is the shape of the nd-array. It would be static,
and with a reasonable size. The overrall data size should not exceed 1mb.
For example a field of 300x400 of 2 float32 value ( (300, 400, 2) dtype=float32)
should be a maximum.
