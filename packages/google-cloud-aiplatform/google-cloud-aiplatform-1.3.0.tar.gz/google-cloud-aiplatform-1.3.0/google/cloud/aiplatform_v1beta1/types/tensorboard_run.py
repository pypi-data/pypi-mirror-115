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

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.aiplatform.v1beta1", manifest={"TensorboardRun",},
)


class TensorboardRun(proto.Message):
    r"""TensorboardRun maps to a specific execution of a training job
    with a given set of hyperparameter values, model definition,
    dataset, etc

    Attributes:
        name (str):
            Output only. Name of the TensorboardRun. Format:
            ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}``
        display_name (str):
            Required. User provided name of this
            TensorboardRun. This value must be unique among
            all TensorboardRuns belonging to the same parent
            TensorboardExperiment.
        description (str):
            Description of this TensorboardRun.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when this
            TensorboardRun was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when this
            TensorboardRun was last updated.
        labels (Sequence[google.cloud.aiplatform_v1beta1.types.TensorboardRun.LabelsEntry]):

        etag (str):
            Used to perform a consistent read-modify-
            rite updates. If not set, a blind "overwrite"
            update happens.
    """

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    create_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=8,)
    etag = proto.Field(proto.STRING, number=9,)


__all__ = tuple(sorted(__protobuf__.manifest))
