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
    package="google.cloud.aiplatform.v1", manifest={"MigratableResource",},
)


class MigratableResource(proto.Message):
    r"""Represents one resource that exists in automl.googleapis.com,
    datalabeling.googleapis.com or ml.googleapis.com.

    Attributes:
        ml_engine_model_version (google.cloud.aiplatform_v1.types.MigratableResource.MlEngineModelVersion):
            Output only. Represents one Version in
            ml.googleapis.com.
        automl_model (google.cloud.aiplatform_v1.types.MigratableResource.AutomlModel):
            Output only. Represents one Model in
            automl.googleapis.com.
        automl_dataset (google.cloud.aiplatform_v1.types.MigratableResource.AutomlDataset):
            Output only. Represents one Dataset in
            automl.googleapis.com.
        data_labeling_dataset (google.cloud.aiplatform_v1.types.MigratableResource.DataLabelingDataset):
            Output only. Represents one Dataset in
            datalabeling.googleapis.com.
        last_migrate_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when the last
            migration attempt on this MigratableResource
            started. Will not be set if there's no migration
            attempt on this MigratableResource.
        last_update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when this
            MigratableResource was last updated.
    """

    class MlEngineModelVersion(proto.Message):
        r"""Represents one model Version in ml.googleapis.com.
        Attributes:
            endpoint (str):
                The ml.googleapis.com endpoint that this model Version
                currently lives in. Example values:

                -  ml.googleapis.com
                -  us-centrall-ml.googleapis.com
                -  europe-west4-ml.googleapis.com
                -  asia-east1-ml.googleapis.com
            version (str):
                Full resource name of ml engine model Version. Format:
                ``projects/{project}/models/{model}/versions/{version}``.
        """

        endpoint = proto.Field(proto.STRING, number=1,)
        version = proto.Field(proto.STRING, number=2,)

    class AutomlModel(proto.Message):
        r"""Represents one Model in automl.googleapis.com.
        Attributes:
            model (str):
                Full resource name of automl Model. Format:
                ``projects/{project}/locations/{location}/models/{model}``.
            model_display_name (str):
                The Model's display name in
                automl.googleapis.com.
        """

        model = proto.Field(proto.STRING, number=1,)
        model_display_name = proto.Field(proto.STRING, number=3,)

    class AutomlDataset(proto.Message):
        r"""Represents one Dataset in automl.googleapis.com.
        Attributes:
            dataset (str):
                Full resource name of automl Dataset. Format:
                ``projects/{project}/locations/{location}/datasets/{dataset}``.
            dataset_display_name (str):
                The Dataset's display name in
                automl.googleapis.com.
        """

        dataset = proto.Field(proto.STRING, number=1,)
        dataset_display_name = proto.Field(proto.STRING, number=4,)

    class DataLabelingDataset(proto.Message):
        r"""Represents one Dataset in datalabeling.googleapis.com.
        Attributes:
            dataset (str):
                Full resource name of data labeling Dataset. Format:
                ``projects/{project}/datasets/{dataset}``.
            dataset_display_name (str):
                The Dataset's display name in
                datalabeling.googleapis.com.
            data_labeling_annotated_datasets (Sequence[google.cloud.aiplatform_v1.types.MigratableResource.DataLabelingDataset.DataLabelingAnnotatedDataset]):
                The migratable AnnotatedDataset in
                datalabeling.googleapis.com belongs to the data
                labeling Dataset.
        """

        class DataLabelingAnnotatedDataset(proto.Message):
            r"""Represents one AnnotatedDataset in
            datalabeling.googleapis.com.

            Attributes:
                annotated_dataset (str):
                    Full resource name of data labeling AnnotatedDataset.
                    Format:
                    ``projects/{project}/datasets/{dataset}/annotatedDatasets/{annotated_dataset}``.
                annotated_dataset_display_name (str):
                    The AnnotatedDataset's display name in
                    datalabeling.googleapis.com.
            """

            annotated_dataset = proto.Field(proto.STRING, number=1,)
            annotated_dataset_display_name = proto.Field(proto.STRING, number=3,)

        dataset = proto.Field(proto.STRING, number=1,)
        dataset_display_name = proto.Field(proto.STRING, number=4,)
        data_labeling_annotated_datasets = proto.RepeatedField(
            proto.MESSAGE,
            number=3,
            message="MigratableResource.DataLabelingDataset.DataLabelingAnnotatedDataset",
        )

    ml_engine_model_version = proto.Field(
        proto.MESSAGE, number=1, oneof="resource", message=MlEngineModelVersion,
    )
    automl_model = proto.Field(
        proto.MESSAGE, number=2, oneof="resource", message=AutomlModel,
    )
    automl_dataset = proto.Field(
        proto.MESSAGE, number=3, oneof="resource", message=AutomlDataset,
    )
    data_labeling_dataset = proto.Field(
        proto.MESSAGE, number=4, oneof="resource", message=DataLabelingDataset,
    )
    last_migrate_time = proto.Field(
        proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,
    )
    last_update_time = proto.Field(
        proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
