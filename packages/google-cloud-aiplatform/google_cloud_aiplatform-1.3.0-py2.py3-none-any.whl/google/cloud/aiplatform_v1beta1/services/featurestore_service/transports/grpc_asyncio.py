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
import warnings
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import gapic_v1  # type: ignore
from google.api_core import grpc_helpers_async  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
import packaging.version

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.aiplatform_v1beta1.types import entity_type
from google.cloud.aiplatform_v1beta1.types import entity_type as gca_entity_type
from google.cloud.aiplatform_v1beta1.types import feature
from google.cloud.aiplatform_v1beta1.types import feature as gca_feature
from google.cloud.aiplatform_v1beta1.types import featurestore
from google.cloud.aiplatform_v1beta1.types import featurestore_service
from google.longrunning import operations_pb2  # type: ignore
from .base import FeaturestoreServiceTransport, DEFAULT_CLIENT_INFO
from .grpc import FeaturestoreServiceGrpcTransport


class FeaturestoreServiceGrpcAsyncIOTransport(FeaturestoreServiceTransport):
    """gRPC AsyncIO backend transport for FeaturestoreService.

    The service that handles CRUD and List for resources for
    Featurestore.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "aiplatform.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "aiplatform.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                credentials=self._credentials,
                credentials_file=credentials_file,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsAsyncClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def create_featurestore(
        self,
    ) -> Callable[
        [featurestore_service.CreateFeaturestoreRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create featurestore method over gRPC.

        Creates a new Featurestore in a given project and
        location.

        Returns:
            Callable[[~.CreateFeaturestoreRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_featurestore" not in self._stubs:
            self._stubs["create_featurestore"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/CreateFeaturestore",
                request_serializer=featurestore_service.CreateFeaturestoreRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_featurestore"]

    @property
    def get_featurestore(
        self,
    ) -> Callable[
        [featurestore_service.GetFeaturestoreRequest],
        Awaitable[featurestore.Featurestore],
    ]:
        r"""Return a callable for the get featurestore method over gRPC.

        Gets details of a single Featurestore.

        Returns:
            Callable[[~.GetFeaturestoreRequest],
                    Awaitable[~.Featurestore]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_featurestore" not in self._stubs:
            self._stubs["get_featurestore"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/GetFeaturestore",
                request_serializer=featurestore_service.GetFeaturestoreRequest.serialize,
                response_deserializer=featurestore.Featurestore.deserialize,
            )
        return self._stubs["get_featurestore"]

    @property
    def list_featurestores(
        self,
    ) -> Callable[
        [featurestore_service.ListFeaturestoresRequest],
        Awaitable[featurestore_service.ListFeaturestoresResponse],
    ]:
        r"""Return a callable for the list featurestores method over gRPC.

        Lists Featurestores in a given project and location.

        Returns:
            Callable[[~.ListFeaturestoresRequest],
                    Awaitable[~.ListFeaturestoresResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_featurestores" not in self._stubs:
            self._stubs["list_featurestores"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/ListFeaturestores",
                request_serializer=featurestore_service.ListFeaturestoresRequest.serialize,
                response_deserializer=featurestore_service.ListFeaturestoresResponse.deserialize,
            )
        return self._stubs["list_featurestores"]

    @property
    def update_featurestore(
        self,
    ) -> Callable[
        [featurestore_service.UpdateFeaturestoreRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update featurestore method over gRPC.

        Updates the parameters of a single Featurestore.

        Returns:
            Callable[[~.UpdateFeaturestoreRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_featurestore" not in self._stubs:
            self._stubs["update_featurestore"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/UpdateFeaturestore",
                request_serializer=featurestore_service.UpdateFeaturestoreRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_featurestore"]

    @property
    def delete_featurestore(
        self,
    ) -> Callable[
        [featurestore_service.DeleteFeaturestoreRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete featurestore method over gRPC.

        Deletes a single Featurestore. The Featurestore must not contain
        any EntityTypes or ``force`` must be set to true for the request
        to succeed.

        Returns:
            Callable[[~.DeleteFeaturestoreRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_featurestore" not in self._stubs:
            self._stubs["delete_featurestore"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/DeleteFeaturestore",
                request_serializer=featurestore_service.DeleteFeaturestoreRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_featurestore"]

    @property
    def create_entity_type(
        self,
    ) -> Callable[
        [featurestore_service.CreateEntityTypeRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create entity type method over gRPC.

        Creates a new EntityType in a given Featurestore.

        Returns:
            Callable[[~.CreateEntityTypeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_entity_type" not in self._stubs:
            self._stubs["create_entity_type"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/CreateEntityType",
                request_serializer=featurestore_service.CreateEntityTypeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_entity_type"]

    @property
    def get_entity_type(
        self,
    ) -> Callable[
        [featurestore_service.GetEntityTypeRequest], Awaitable[entity_type.EntityType]
    ]:
        r"""Return a callable for the get entity type method over gRPC.

        Gets details of a single EntityType.

        Returns:
            Callable[[~.GetEntityTypeRequest],
                    Awaitable[~.EntityType]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_entity_type" not in self._stubs:
            self._stubs["get_entity_type"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/GetEntityType",
                request_serializer=featurestore_service.GetEntityTypeRequest.serialize,
                response_deserializer=entity_type.EntityType.deserialize,
            )
        return self._stubs["get_entity_type"]

    @property
    def list_entity_types(
        self,
    ) -> Callable[
        [featurestore_service.ListEntityTypesRequest],
        Awaitable[featurestore_service.ListEntityTypesResponse],
    ]:
        r"""Return a callable for the list entity types method over gRPC.

        Lists EntityTypes in a given Featurestore.

        Returns:
            Callable[[~.ListEntityTypesRequest],
                    Awaitable[~.ListEntityTypesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_entity_types" not in self._stubs:
            self._stubs["list_entity_types"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/ListEntityTypes",
                request_serializer=featurestore_service.ListEntityTypesRequest.serialize,
                response_deserializer=featurestore_service.ListEntityTypesResponse.deserialize,
            )
        return self._stubs["list_entity_types"]

    @property
    def update_entity_type(
        self,
    ) -> Callable[
        [featurestore_service.UpdateEntityTypeRequest],
        Awaitable[gca_entity_type.EntityType],
    ]:
        r"""Return a callable for the update entity type method over gRPC.

        Updates the parameters of a single EntityType.

        Returns:
            Callable[[~.UpdateEntityTypeRequest],
                    Awaitable[~.EntityType]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_entity_type" not in self._stubs:
            self._stubs["update_entity_type"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/UpdateEntityType",
                request_serializer=featurestore_service.UpdateEntityTypeRequest.serialize,
                response_deserializer=gca_entity_type.EntityType.deserialize,
            )
        return self._stubs["update_entity_type"]

    @property
    def delete_entity_type(
        self,
    ) -> Callable[
        [featurestore_service.DeleteEntityTypeRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete entity type method over gRPC.

        Deletes a single EntityType. The EntityType must not have any
        Features or ``force`` must be set to true for the request to
        succeed.

        Returns:
            Callable[[~.DeleteEntityTypeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_entity_type" not in self._stubs:
            self._stubs["delete_entity_type"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/DeleteEntityType",
                request_serializer=featurestore_service.DeleteEntityTypeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_entity_type"]

    @property
    def create_feature(
        self,
    ) -> Callable[
        [featurestore_service.CreateFeatureRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create feature method over gRPC.

        Creates a new Feature in a given EntityType.

        Returns:
            Callable[[~.CreateFeatureRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_feature" not in self._stubs:
            self._stubs["create_feature"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/CreateFeature",
                request_serializer=featurestore_service.CreateFeatureRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_feature"]

    @property
    def batch_create_features(
        self,
    ) -> Callable[
        [featurestore_service.BatchCreateFeaturesRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the batch create features method over gRPC.

        Creates a batch of Features in a given EntityType.

        Returns:
            Callable[[~.BatchCreateFeaturesRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_create_features" not in self._stubs:
            self._stubs["batch_create_features"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/BatchCreateFeatures",
                request_serializer=featurestore_service.BatchCreateFeaturesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["batch_create_features"]

    @property
    def get_feature(
        self,
    ) -> Callable[[featurestore_service.GetFeatureRequest], Awaitable[feature.Feature]]:
        r"""Return a callable for the get feature method over gRPC.

        Gets details of a single Feature.

        Returns:
            Callable[[~.GetFeatureRequest],
                    Awaitable[~.Feature]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_feature" not in self._stubs:
            self._stubs["get_feature"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/GetFeature",
                request_serializer=featurestore_service.GetFeatureRequest.serialize,
                response_deserializer=feature.Feature.deserialize,
            )
        return self._stubs["get_feature"]

    @property
    def list_features(
        self,
    ) -> Callable[
        [featurestore_service.ListFeaturesRequest],
        Awaitable[featurestore_service.ListFeaturesResponse],
    ]:
        r"""Return a callable for the list features method over gRPC.

        Lists Features in a given EntityType.

        Returns:
            Callable[[~.ListFeaturesRequest],
                    Awaitable[~.ListFeaturesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_features" not in self._stubs:
            self._stubs["list_features"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/ListFeatures",
                request_serializer=featurestore_service.ListFeaturesRequest.serialize,
                response_deserializer=featurestore_service.ListFeaturesResponse.deserialize,
            )
        return self._stubs["list_features"]

    @property
    def update_feature(
        self,
    ) -> Callable[
        [featurestore_service.UpdateFeatureRequest], Awaitable[gca_feature.Feature]
    ]:
        r"""Return a callable for the update feature method over gRPC.

        Updates the parameters of a single Feature.

        Returns:
            Callable[[~.UpdateFeatureRequest],
                    Awaitable[~.Feature]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_feature" not in self._stubs:
            self._stubs["update_feature"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/UpdateFeature",
                request_serializer=featurestore_service.UpdateFeatureRequest.serialize,
                response_deserializer=gca_feature.Feature.deserialize,
            )
        return self._stubs["update_feature"]

    @property
    def delete_feature(
        self,
    ) -> Callable[
        [featurestore_service.DeleteFeatureRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete feature method over gRPC.

        Deletes a single Feature.

        Returns:
            Callable[[~.DeleteFeatureRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_feature" not in self._stubs:
            self._stubs["delete_feature"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/DeleteFeature",
                request_serializer=featurestore_service.DeleteFeatureRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_feature"]

    @property
    def import_feature_values(
        self,
    ) -> Callable[
        [featurestore_service.ImportFeatureValuesRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the import feature values method over gRPC.

        Imports Feature values into the Featurestore from a
        source storage.
        The progress of the import is tracked by the returned
        operation. The imported features are guaranteed to be
        visible to subsequent read operations after the
        operation is marked as successfully done.
        If an import operation fails, the Feature values
        returned from reads and exports may be inconsistent. If
        consistency is required, the caller must retry the same
        import request again and wait till the new operation
        returned is marked as successfully done.
        There are also scenarios where the caller can cause
        inconsistency.
         - Source data for import contains multiple distinct
        Feature values for    the same entity ID and timestamp.
         - Source is modified during an import. This includes
        adding, updating, or  removing source data and/or
        metadata. Examples of updating metadata  include but are
        not limited to changing storage location, storage class,
        or retention policy.
         - Online serving cluster is under-provisioned.

        Returns:
            Callable[[~.ImportFeatureValuesRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_feature_values" not in self._stubs:
            self._stubs["import_feature_values"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/ImportFeatureValues",
                request_serializer=featurestore_service.ImportFeatureValuesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["import_feature_values"]

    @property
    def batch_read_feature_values(
        self,
    ) -> Callable[
        [featurestore_service.BatchReadFeatureValuesRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the batch read feature values method over gRPC.

        Batch reads Feature values from a Featurestore.
        This API enables batch reading Feature values, where
        each read instance in the batch may read Feature values
        of entities from one or more EntityTypes. Point-in-time
        correctness is guaranteed for Feature values of each
        read instance as of each instance's read timestamp.

        Returns:
            Callable[[~.BatchReadFeatureValuesRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_read_feature_values" not in self._stubs:
            self._stubs["batch_read_feature_values"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/BatchReadFeatureValues",
                request_serializer=featurestore_service.BatchReadFeatureValuesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["batch_read_feature_values"]

    @property
    def export_feature_values(
        self,
    ) -> Callable[
        [featurestore_service.ExportFeatureValuesRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the export feature values method over gRPC.

        Exports Feature values from all the entities of a
        target EntityType.

        Returns:
            Callable[[~.ExportFeatureValuesRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_feature_values" not in self._stubs:
            self._stubs["export_feature_values"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/ExportFeatureValues",
                request_serializer=featurestore_service.ExportFeatureValuesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["export_feature_values"]

    @property
    def search_features(
        self,
    ) -> Callable[
        [featurestore_service.SearchFeaturesRequest],
        Awaitable[featurestore_service.SearchFeaturesResponse],
    ]:
        r"""Return a callable for the search features method over gRPC.

        Searches Features matching a query in a given
        project.

        Returns:
            Callable[[~.SearchFeaturesRequest],
                    Awaitable[~.SearchFeaturesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_features" not in self._stubs:
            self._stubs["search_features"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.FeaturestoreService/SearchFeatures",
                request_serializer=featurestore_service.SearchFeaturesRequest.serialize,
                response_deserializer=featurestore_service.SearchFeaturesResponse.deserialize,
            )
        return self._stubs["search_features"]


__all__ = ("FeaturestoreServiceGrpcAsyncIOTransport",)
