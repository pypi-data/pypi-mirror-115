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
import io
from django.db import models
from django import forms
import json
from django.core import exceptions
from .forms import NDArrayFormField


def parse_numpy_array(value):
    memfile = io.BytesIO()
    memfile.write(value)
    memfile.seek(0)
    data = np.load(memfile)
    return data


def serialize_numpy_array(value, dtype):
    value = value.astype(dtype)
    memfile = io.BytesIO()
    # after many tests savez_compressed is not a game changer for size
    np.save(memfile, value, allow_pickle=False)
    memfile.seek(0)
    return memfile.getvalue()


class NDArrayField(models.BinaryField):

    description = "Field to store numpy array"

    def __init__(self, *args, **kwargs):
        self.empty_values = []
        kwargs.setdefault("editable", True)
        self.shape = kwargs.pop("shape", None)
        self.dtype = kwargs.pop("dtype", np.float32)
        self.binary_serialize = kwargs.pop("binary_serialize", False)

        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        if self.shape is not None:
            kwargs["shape"] = self.shape

        if self.dtype != np.float32:
            kwargs["dtype"] = self.dtype

        if self.binary_serialize:
            kwargs["binary_serialize"] = self.binary_serialize

        return name, path, args, kwargs

    def get_prep_value(self, value, *args, **kwargs):

        if value is not None:
            value = self.to_python(value)
            value = serialize_numpy_array(value, self.dtype)
            return super().get_prep_value(value, *args, **kwargs)

        return value

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return parse_numpy_array(value)

    def validate(self, value, model_instance):
        try:
            value.reshape(self.shape)
        except ValueError:
            raise exceptions.ValidationError("Bad shape", code="shape")

        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages["null"], code="null")

        if not self.blank and value is None or value.size == 0:
            raise exceptions.ValidationError(self.error_messages["blank"], code="blank")

    def value_to_string(self, obj):
        if self.binary_serialize:
            return super().value_to_string(obj)
        else:
            value = self.value_from_object(obj)
            return value.tolist()

    def to_python(self, value):
        if isinstance(value, list):
            try:
                return np.array(value, dtype=self.dtype).reshape(self.shape)
            except ValueError:
                raise exceptions.ValidationError(
                    "Can not convert list to numpy array", "badlist"
                )

        if isinstance(value, np.ndarray):
            self.validate(value, None)
            return value

        if isinstance(value, str):
            try:
                value = np.array(json.loads(value), dtype=self.dtype)
            except json.decoder.JSONDecodeError:
                try:
                    value = super().to_python(value)
                    b = value.tobytes()
                    value = np.frombuffer(b, self.dtype)
                    value = value.reshape(self.shape)
                except:
                    raise exceptions.ValidationError(
                        "Can not decode json string", code="badjson"
                    )
            self.validate(value, None)
            return value

        if value is None:
            return value

        if isinstance(value, bytes):
            value = parse_numpy_array(value)
            self.validate(value, None)
            return value

        raise exceptions.ValidationError(
            "Can not convert to numpy array", code="unknwon"
        )

    def formfield(self, **kwargs):
        defaults = {"form_class": NDArrayFormField, "widget": forms.Textarea}
        defaults.update(kwargs)
        return super().formfield(**defaults)
