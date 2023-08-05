# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.aiplatform.v1beta1.schema.predict.prediction",
    manifest={"ClassificationPredictionResult",},
)


class ClassificationPredictionResult(proto.Message):
    r"""Prediction output format for Image and Text Classification.
    Attributes:
        ids (Sequence[int]):
            The resource IDs of the AnnotationSpecs that
            had been identified.
        display_names (Sequence[str]):
            The display names of the AnnotationSpecs that
            had been identified, order matches the IDs.
        confidences (Sequence[float]):
            The Model's confidences in correctness of the
            predicted IDs, higher value means higher
            confidence. Order matches the Ids.
    """

    ids = proto.RepeatedField(proto.INT64, number=1,)
    display_names = proto.RepeatedField(proto.STRING, number=2,)
    confidences = proto.RepeatedField(proto.FLOAT, number=3,)


__all__ = tuple(sorted(__protobuf__.manifest))
