#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#
import numpy as np
from django import forms
from django.core import exceptions
import json


class NDArrayFormField(forms.CharField):
    def prepare_value(self, value):
        if isinstance(value, np.ndarray):
            return json.dumps(value.tolist(), indent=2)
        return value

    def to_python(self, value):
        value = super().to_python(value)
        try:
            value = json.loads(value)
        except json.decoder.JSONDecodeError:
            raise exceptions.ValidationError(
                "Can not decode json string", code="badjson"
            )

        return value

    def has_changed(self, initial_value, data_value):
        return True
