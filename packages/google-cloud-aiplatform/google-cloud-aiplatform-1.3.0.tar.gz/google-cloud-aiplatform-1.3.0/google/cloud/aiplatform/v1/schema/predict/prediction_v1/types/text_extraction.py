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
    package="google.cloud.aiplatform.v1.schema.predict.prediction",
    manifest={"TextExtractionPredictionResult",},
)


class TextExtractionPredictionResult(proto.Message):
    r"""Prediction output format for Text Extraction.
    Attributes:
        ids (Sequence[int]):
            The resource IDs of the AnnotationSpecs that
            had been identified, ordered by the confidence
            score descendingly.
        display_names (Sequence[str]):
            The display names of the AnnotationSpecs that
            had been identified, order matches the IDs.
        text_segment_start_offsets (Sequence[int]):
            The start offsets, inclusive, of the text
            segment in which the AnnotationSpec has been
            identified. Expressed as a zero-based number of
            characters as measured from the start of the
            text snippet.
        text_segment_end_offsets (Sequence[int]):
            The end offsets, inclusive, of the text
            segment in which the AnnotationSpec has been
            identified. Expressed as a zero-based number of
            characters as measured from the start of the
            text snippet.
        confidences (Sequence[float]):
            The Model's confidences in correctness of the
            predicted IDs, higher value means higher
            confidence. Order matches the Ids.
    """

    ids = proto.RepeatedField(proto.INT64, number=1,)
    display_names = proto.RepeatedField(proto.STRING, number=2,)
    text_segment_start_offsets = proto.RepeatedField(proto.INT64, number=3,)
    text_segment_end_offsets = proto.RepeatedField(proto.INT64, number=4,)
    confidences = proto.RepeatedField(proto.FLOAT, number=5,)


__all__ = tuple(sorted(__protobuf__.manifest))
