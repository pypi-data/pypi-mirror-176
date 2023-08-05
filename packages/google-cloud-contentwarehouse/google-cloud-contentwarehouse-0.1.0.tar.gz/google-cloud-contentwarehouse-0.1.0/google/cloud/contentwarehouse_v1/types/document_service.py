# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.iam.v1 import policy_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.contentwarehouse_v1.types import common
from google.cloud.contentwarehouse_v1.types import document as gcc_document
from google.cloud.contentwarehouse_v1.types import histogram, rule_engine

__protobuf__ = proto.module(
    package="google.cloud.contentwarehouse.v1",
    manifest={
        "CreateDocumentResponse",
        "UpdateDocumentResponse",
        "QAResult",
        "SearchDocumentsResponse",
        "FetchAclResponse",
        "SetAclResponse",
    },
)


class CreateDocumentResponse(proto.Message):
    r"""Response message for DocumentService.CreateDocument.

    Attributes:
        document (google.cloud.contentwarehouse_v1.types.Document):
            Document created after executing create
            request.
        rule_engine_output (google.cloud.contentwarehouse_v1.types.RuleEngineOutput):
            Output from Rule Engine recording the rule evaluator and
            action executor's output.

            Refer format in:
            google/cloud/contentwarehouse/v1/rule_engine.proto
        metadata (google.cloud.contentwarehouse_v1.types.ResponseMetadata):
            Additional information for the API
            invocation, such as the request tracking id.
    """

    document = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcc_document.Document,
    )
    rule_engine_output = proto.Field(
        proto.MESSAGE,
        number=2,
        message=rule_engine.RuleEngineOutput,
    )
    metadata = proto.Field(
        proto.MESSAGE,
        number=3,
        message=common.ResponseMetadata,
    )


class UpdateDocumentResponse(proto.Message):
    r"""Response message for DocumentService.UpdateDocument.

    Attributes:
        document (google.cloud.contentwarehouse_v1.types.Document):
            Updated document after executing update
            request.
        rule_engine_output (google.cloud.contentwarehouse_v1.types.RuleEngineOutput):
            Output from Rule Engine recording the rule evaluator and
            action executor's output.

            Refer format in:
            google/cloud/contentwarehouse/v1/rule_engine.proto
        metadata (google.cloud.contentwarehouse_v1.types.ResponseMetadata):
            Additional information for the API
            invocation, such as the request tracking id.
    """

    document = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcc_document.Document,
    )
    rule_engine_output = proto.Field(
        proto.MESSAGE,
        number=2,
        message=rule_engine.RuleEngineOutput,
    )
    metadata = proto.Field(
        proto.MESSAGE,
        number=3,
        message=common.ResponseMetadata,
    )


class QAResult(proto.Message):
    r"""Additional result info for the question-answering feature.

    Attributes:
        highlights (Sequence[google.cloud.contentwarehouse_v1.types.QAResult.Highlight]):
            Highlighted sections in the snippet.
        confidence_score (float):
            The calibrated confidence score for this document, in the
            range [0., 1.]. This represents the confidence level for
            whether the returned document and snippet answers the user's
            query.
    """

    class Highlight(proto.Message):
        r"""A text span in the search text snippet that represents a
        highlighted section (answer context, highly relevant sentence,
        etc.).

        Attributes:
            start_index (int):
                Start index of the highlight.
            end_index (int):
                End index of the highlight, exclusive.
        """

        start_index = proto.Field(
            proto.INT32,
            number=1,
        )
        end_index = proto.Field(
            proto.INT32,
            number=2,
        )

    highlights = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=Highlight,
    )
    confidence_score = proto.Field(
        proto.FLOAT,
        number=2,
    )


class SearchDocumentsResponse(proto.Message):
    r"""Response message for DocumentService.SearchDocuments.

    Attributes:
        matching_documents (Sequence[google.cloud.contentwarehouse_v1.types.SearchDocumentsResponse.MatchingDocument]):
            The document entities that match the specified
            [SearchDocumentsRequest][google.cloud.contentwarehouse.v1.SearchDocumentsRequest].
        next_page_token (str):
            The token that specifies the starting
            position of the next page of results. This field
            is empty if there are no more results.
        total_size (int):
            The total number of matched documents which is available
            only if the client set
            [SearchDocumentsRequest.require_total_size][google.cloud.contentwarehouse.v1.SearchDocumentsRequest.require_total_size]
            to ``true``. Otherwise, the value will be ``-1``.
            ``total_size`` will max at "100,000". If this is returned,
            then it can be assumed that the count is equal to or greater
            than 100,000. Typically a UI would handle this condition by
            displaying "of many", for example: "Displaying 10 of many".
        metadata (google.cloud.contentwarehouse_v1.types.ResponseMetadata):
            Additional information for the API
            invocation, such as the request tracking id.
        histogram_query_results (Sequence[google.cloud.contentwarehouse_v1.types.HistogramQueryResult]):
            The histogram results that match with the specified
            [SearchDocumentsRequest.histogram_queries][google.cloud.contentwarehouse.v1.SearchDocumentsRequest.histogram_queries].
    """

    class MatchingDocument(proto.Message):
        r"""Document entry with metadata inside
        [SearchDocumentsResponse][google.cloud.contentwarehouse.v1.SearchDocumentsResponse]

        Attributes:
            document (google.cloud.contentwarehouse_v1.types.Document):
                Document that matches the specified
                [SearchDocumentsRequest][google.cloud.contentwarehouse.v1.SearchDocumentsRequest].
                This document only contains indexed metadata information.
            search_text_snippet (str):
                Contains snippets of text from the document full raw text
                that most closely match a search query's keywords, if
                available. All HTML tags in the original fields are stripped
                when returned in this field, and matching query keywords are
                enclosed in HTML bold tags.

                If the question-answering feature is enabled, this field
                will instead contain a snippet that answers the user's
                natural-language query. No HTML bold tags will be present,
                and highlights in the answer snippet can be found in
                [QAResult.highlights][google.cloud.contentwarehouse.v1.QAResult.highlights].
            qa_result (google.cloud.contentwarehouse_v1.types.QAResult):
                Experimental.
                Additional result info if the question-answering
                feature is enabled.
        """

        document = proto.Field(
            proto.MESSAGE,
            number=1,
            message=gcc_document.Document,
        )
        search_text_snippet = proto.Field(
            proto.STRING,
            number=2,
        )
        qa_result = proto.Field(
            proto.MESSAGE,
            number=3,
            message="QAResult",
        )

    @property
    def raw_page(self):
        return self

    matching_documents = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=MatchingDocument,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    total_size = proto.Field(
        proto.INT32,
        number=3,
    )
    metadata = proto.Field(
        proto.MESSAGE,
        number=4,
        message=common.ResponseMetadata,
    )
    histogram_query_results = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message=histogram.HistogramQueryResult,
    )


class FetchAclResponse(proto.Message):
    r"""Response message for DocumentService.FetchAcl.

    Attributes:
        policy (google.iam.v1.policy_pb2.Policy):
            The IAM policy.
        metadata (google.cloud.contentwarehouse_v1.types.ResponseMetadata):
            Additional information for the API
            invocation, such as the request tracking id.
    """

    policy = proto.Field(
        proto.MESSAGE,
        number=1,
        message=policy_pb2.Policy,
    )
    metadata = proto.Field(
        proto.MESSAGE,
        number=2,
        message=common.ResponseMetadata,
    )


class SetAclResponse(proto.Message):
    r"""Response message for DocumentService.SetAcl.

    Attributes:
        policy (google.iam.v1.policy_pb2.Policy):
            The policy will be attached to a resource
            (e.g. projecct, document).
        metadata (google.cloud.contentwarehouse_v1.types.ResponseMetadata):
            Additional information for the API
            invocation, such as the request tracking id.
    """

    policy = proto.Field(
        proto.MESSAGE,
        number=1,
        message=policy_pb2.Policy,
    )
    metadata = proto.Field(
        proto.MESSAGE,
        number=2,
        message=common.ResponseMetadata,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
