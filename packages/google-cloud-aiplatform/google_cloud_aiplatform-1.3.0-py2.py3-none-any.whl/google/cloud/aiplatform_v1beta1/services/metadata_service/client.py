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
from collections import OrderedDict
from distutils import util
import os
import re
from typing import Callable, Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation as gac_operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.aiplatform_v1beta1.services.metadata_service import pagers
from google.cloud.aiplatform_v1beta1.types import artifact
from google.cloud.aiplatform_v1beta1.types import artifact as gca_artifact
from google.cloud.aiplatform_v1beta1.types import context
from google.cloud.aiplatform_v1beta1.types import context as gca_context
from google.cloud.aiplatform_v1beta1.types import encryption_spec
from google.cloud.aiplatform_v1beta1.types import event
from google.cloud.aiplatform_v1beta1.types import execution
from google.cloud.aiplatform_v1beta1.types import execution as gca_execution
from google.cloud.aiplatform_v1beta1.types import lineage_subgraph
from google.cloud.aiplatform_v1beta1.types import metadata_schema
from google.cloud.aiplatform_v1beta1.types import metadata_schema as gca_metadata_schema
from google.cloud.aiplatform_v1beta1.types import metadata_service
from google.cloud.aiplatform_v1beta1.types import metadata_store
from google.cloud.aiplatform_v1beta1.types import metadata_store as gca_metadata_store
from google.cloud.aiplatform_v1beta1.types import operation as gca_operation
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import MetadataServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import MetadataServiceGrpcTransport
from .transports.grpc_asyncio import MetadataServiceGrpcAsyncIOTransport


class MetadataServiceClientMeta(type):
    """Metaclass for the MetadataService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[MetadataServiceTransport]]
    _transport_registry["grpc"] = MetadataServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = MetadataServiceGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[MetadataServiceTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class MetadataServiceClient(metaclass=MetadataServiceClientMeta):
    """Service for reading and writing metadata entries."""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "aiplatform.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            MetadataServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            MetadataServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> MetadataServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            MetadataServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def artifact_path(
        project: str, location: str, metadata_store: str, artifact: str,
    ) -> str:
        """Returns a fully-qualified artifact string."""
        return "projects/{project}/locations/{location}/metadataStores/{metadata_store}/artifacts/{artifact}".format(
            project=project,
            location=location,
            metadata_store=metadata_store,
            artifact=artifact,
        )

    @staticmethod
    def parse_artifact_path(path: str) -> Dict[str, str]:
        """Parses a artifact path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/metadataStores/(?P<metadata_store>.+?)/artifacts/(?P<artifact>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def context_path(
        project: str, location: str, metadata_store: str, context: str,
    ) -> str:
        """Returns a fully-qualified context string."""
        return "projects/{project}/locations/{location}/metadataStores/{metadata_store}/contexts/{context}".format(
            project=project,
            location=location,
            metadata_store=metadata_store,
            context=context,
        )

    @staticmethod
    def parse_context_path(path: str) -> Dict[str, str]:
        """Parses a context path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/metadataStores/(?P<metadata_store>.+?)/contexts/(?P<context>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def execution_path(
        project: str, location: str, metadata_store: str, execution: str,
    ) -> str:
        """Returns a fully-qualified execution string."""
        return "projects/{project}/locations/{location}/metadataStores/{metadata_store}/executions/{execution}".format(
            project=project,
            location=location,
            metadata_store=metadata_store,
            execution=execution,
        )

    @staticmethod
    def parse_execution_path(path: str) -> Dict[str, str]:
        """Parses a execution path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/metadataStores/(?P<metadata_store>.+?)/executions/(?P<execution>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def metadata_schema_path(
        project: str, location: str, metadata_store: str, metadata_schema: str,
    ) -> str:
        """Returns a fully-qualified metadata_schema string."""
        return "projects/{project}/locations/{location}/metadataStores/{metadata_store}/metadataSchemas/{metadata_schema}".format(
            project=project,
            location=location,
            metadata_store=metadata_store,
            metadata_schema=metadata_schema,
        )

    @staticmethod
    def parse_metadata_schema_path(path: str) -> Dict[str, str]:
        """Parses a metadata_schema path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/metadataStores/(?P<metadata_store>.+?)/metadataSchemas/(?P<metadata_schema>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def metadata_store_path(project: str, location: str, metadata_store: str,) -> str:
        """Returns a fully-qualified metadata_store string."""
        return "projects/{project}/locations/{location}/metadataStores/{metadata_store}".format(
            project=project, location=location, metadata_store=metadata_store,
        )

    @staticmethod
    def parse_metadata_store_path(path: str) -> Dict[str, str]:
        """Parses a metadata_store path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/metadataStores/(?P<metadata_store>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str,) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project, location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, MetadataServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the metadata service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, MetadataServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        # Create SSL credentials for mutual TLS if needed.
        use_client_cert = bool(
            util.strtobool(os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"))
        )

        client_cert_source_func = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                is_mtls = True
                client_cert_source_func = client_options.client_cert_source
            else:
                is_mtls = mtls.has_default_client_cert_source()
                if is_mtls:
                    client_cert_source_func = mtls.default_client_cert_source()
                else:
                    client_cert_source_func = None

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        else:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
            if use_mtls_env == "never":
                api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                if is_mtls:
                    api_endpoint = self.DEFAULT_MTLS_ENDPOINT
                else:
                    api_endpoint = self.DEFAULT_ENDPOINT
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted "
                    "values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, MetadataServiceTransport):
            # transport is a MetadataServiceTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=(
                    Transport == type(self).get_transport_class("grpc")
                    or Transport == type(self).get_transport_class("grpc_asyncio")
                ),
            )

    def create_metadata_store(
        self,
        request: metadata_service.CreateMetadataStoreRequest = None,
        *,
        parent: str = None,
        metadata_store: gca_metadata_store.MetadataStore = None,
        metadata_store_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gac_operation.Operation:
        r"""Initializes a MetadataStore, including allocation of
        resources.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.CreateMetadataStoreRequest):
                The request object. Request message for
                [MetadataService.CreateMetadataStore][google.cloud.aiplatform.v1beta1.MetadataService.CreateMetadataStore].
            parent (str):
                Required. The resource name of the
                Location where the MetadataStore should
                be created. Format:
                projects/{project}/locations/{location}/

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            metadata_store (google.cloud.aiplatform_v1beta1.types.MetadataStore):
                Required. The MetadataStore to
                create.

                This corresponds to the ``metadata_store`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            metadata_store_id (str):
                The {metadatastore} portion of the resource name with
                the format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}
                If not provided, the MetadataStore's ID will be a UUID
                generated by the service. Must be 4-128 characters in
                length. Valid characters are /[a-z][0-9]-/. Must be
                unique across all MetadataStores in the parent Location.
                (Otherwise the request will fail with ALREADY_EXISTS, or
                PERMISSION_DENIED if the caller can't view the
                preexisting MetadataStore.)

                This corresponds to the ``metadata_store_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.aiplatform_v1beta1.types.MetadataStore` Instance of a metadata store. Contains a set of metadata that can be
                   queried.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, metadata_store, metadata_store_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.CreateMetadataStoreRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.CreateMetadataStoreRequest):
            request = metadata_service.CreateMetadataStoreRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if metadata_store is not None:
                request.metadata_store = metadata_store
            if metadata_store_id is not None:
                request.metadata_store_id = metadata_store_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_metadata_store]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = gac_operation.from_gapic(
            response,
            self._transport.operations_client,
            gca_metadata_store.MetadataStore,
            metadata_type=metadata_service.CreateMetadataStoreOperationMetadata,
        )

        # Done; return the response.
        return response

    def get_metadata_store(
        self,
        request: metadata_service.GetMetadataStoreRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metadata_store.MetadataStore:
        r"""Retrieves a specific MetadataStore.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.GetMetadataStoreRequest):
                The request object. Request message for
                [MetadataService.GetMetadataStore][google.cloud.aiplatform.v1beta1.MetadataService.GetMetadataStore].
            name (str):
                Required. The resource name of the
                MetadataStore to retrieve. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.MetadataStore:
                Instance of a metadata store.
                Contains a set of metadata that can be
                queried.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.GetMetadataStoreRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.GetMetadataStoreRequest):
            request = metadata_service.GetMetadataStoreRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_metadata_store]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_metadata_stores(
        self,
        request: metadata_service.ListMetadataStoresRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMetadataStoresPager:
        r"""Lists MetadataStores for a Location.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.ListMetadataStoresRequest):
                The request object. Request message for
                [MetadataService.ListMetadataStores][google.cloud.aiplatform.v1beta1.MetadataService.ListMetadataStores].
            parent (str):
                Required. The Location whose
                MetadataStores should be listed. Format:
                projects/{project}/locations/{location}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.services.metadata_service.pagers.ListMetadataStoresPager:
                Response message for
                [MetadataService.ListMetadataStores][google.cloud.aiplatform.v1beta1.MetadataService.ListMetadataStores].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.ListMetadataStoresRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.ListMetadataStoresRequest):
            request = metadata_service.ListMetadataStoresRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_metadata_stores]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListMetadataStoresPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_metadata_store(
        self,
        request: metadata_service.DeleteMetadataStoreRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gac_operation.Operation:
        r"""Deletes a single MetadataStore.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.DeleteMetadataStoreRequest):
                The request object. Request message for
                [MetadataService.DeleteMetadataStore][google.cloud.aiplatform.v1beta1.MetadataService.DeleteMetadataStore].
            name (str):
                Required. The resource name of the
                MetadataStore to delete. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.DeleteMetadataStoreRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.DeleteMetadataStoreRequest):
            request = metadata_service.DeleteMetadataStoreRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_metadata_store]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = gac_operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=metadata_service.DeleteMetadataStoreOperationMetadata,
        )

        # Done; return the response.
        return response

    def create_artifact(
        self,
        request: metadata_service.CreateArtifactRequest = None,
        *,
        parent: str = None,
        artifact: gca_artifact.Artifact = None,
        artifact_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_artifact.Artifact:
        r"""Creates an Artifact associated with a MetadataStore.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.CreateArtifactRequest):
                The request object. Request message for
                [MetadataService.CreateArtifact][google.cloud.aiplatform.v1beta1.MetadataService.CreateArtifact].
            parent (str):
                Required. The resource name of the
                MetadataStore where the Artifact should
                be created. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            artifact (google.cloud.aiplatform_v1beta1.types.Artifact):
                Required. The Artifact to create.
                This corresponds to the ``artifact`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            artifact_id (str):
                The {artifact} portion of the resource name with the
                format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/artifacts/{artifact}
                If not provided, the Artifact's ID will be a UUID
                generated by the service. Must be 4-128 characters in
                length. Valid characters are /[a-z][0-9]-/. Must be
                unique across all Artifacts in the parent MetadataStore.
                (Otherwise the request will fail with ALREADY_EXISTS, or
                PERMISSION_DENIED if the caller can't view the
                preexisting Artifact.)

                This corresponds to the ``artifact_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.Artifact:
                Instance of a general artifact.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, artifact, artifact_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.CreateArtifactRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.CreateArtifactRequest):
            request = metadata_service.CreateArtifactRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if artifact is not None:
                request.artifact = artifact
            if artifact_id is not None:
                request.artifact_id = artifact_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_artifact]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_artifact(
        self,
        request: metadata_service.GetArtifactRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> artifact.Artifact:
        r"""Retrieves a specific Artifact.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.GetArtifactRequest):
                The request object. Request message for
                [MetadataService.GetArtifact][google.cloud.aiplatform.v1beta1.MetadataService.GetArtifact].
            name (str):
                Required. The resource name of the
                Artifact to retrieve. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/artifacts/{artifact}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.Artifact:
                Instance of a general artifact.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.GetArtifactRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.GetArtifactRequest):
            request = metadata_service.GetArtifactRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_artifact]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_artifacts(
        self,
        request: metadata_service.ListArtifactsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListArtifactsPager:
        r"""Lists Artifacts in the MetadataStore.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.ListArtifactsRequest):
                The request object. Request message for
                [MetadataService.ListArtifacts][google.cloud.aiplatform.v1beta1.MetadataService.ListArtifacts].
            parent (str):
                Required. The MetadataStore whose
                Artifacts should be listed. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.services.metadata_service.pagers.ListArtifactsPager:
                Response message for
                [MetadataService.ListArtifacts][google.cloud.aiplatform.v1beta1.MetadataService.ListArtifacts].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.ListArtifactsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.ListArtifactsRequest):
            request = metadata_service.ListArtifactsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_artifacts]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListArtifactsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_artifact(
        self,
        request: metadata_service.UpdateArtifactRequest = None,
        *,
        artifact: gca_artifact.Artifact = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_artifact.Artifact:
        r"""Updates a stored Artifact.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.UpdateArtifactRequest):
                The request object. Request message for
                [MetadataService.UpdateArtifact][google.cloud.aiplatform.v1beta1.MetadataService.UpdateArtifact].
            artifact (google.cloud.aiplatform_v1beta1.types.Artifact):
                Required. The Artifact containing updates. The
                Artifact's
                [Artifact.name][google.cloud.aiplatform.v1beta1.Artifact.name]
                field is used to identify the Artifact to be updated.
                Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/artifacts/{artifact}

                This corresponds to the ``artifact`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. A FieldMask indicating
                which fields should be updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.Artifact:
                Instance of a general artifact.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([artifact, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.UpdateArtifactRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.UpdateArtifactRequest):
            request = metadata_service.UpdateArtifactRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if artifact is not None:
                request.artifact = artifact
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_artifact]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("artifact.name", request.artifact.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_artifact(
        self,
        request: metadata_service.DeleteArtifactRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gac_operation.Operation:
        r"""Deletes an Artifact.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.DeleteArtifactRequest):
                The request object. Request message for
                [MetadataService.DeleteArtifact][google.cloud.aiplatform.v1beta1.MetadataService.DeleteArtifact].
            name (str):
                Required. The resource name of the
                Artifact to delete. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/artifacts/{artifact}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.DeleteArtifactRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.DeleteArtifactRequest):
            request = metadata_service.DeleteArtifactRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_artifact]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = gac_operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=gca_operation.DeleteOperationMetadata,
        )

        # Done; return the response.
        return response

    def purge_artifacts(
        self,
        request: metadata_service.PurgeArtifactsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gac_operation.Operation:
        r"""Purges Artifacts.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.PurgeArtifactsRequest):
                The request object. Request message for
                [MetadataService.PurgeArtifacts][google.cloud.aiplatform.v1beta1.MetadataService.PurgeArtifacts].
            parent (str):
                Required. The metadata store to purge
                Artifacts from. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.aiplatform_v1beta1.types.PurgeArtifactsResponse`
                Response message for
                [MetadataService.PurgeArtifacts][google.cloud.aiplatform.v1beta1.MetadataService.PurgeArtifacts].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.PurgeArtifactsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.PurgeArtifactsRequest):
            request = metadata_service.PurgeArtifactsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.purge_artifacts]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = gac_operation.from_gapic(
            response,
            self._transport.operations_client,
            metadata_service.PurgeArtifactsResponse,
            metadata_type=metadata_service.PurgeArtifactsMetadata,
        )

        # Done; return the response.
        return response

    def create_context(
        self,
        request: metadata_service.CreateContextRequest = None,
        *,
        parent: str = None,
        context: gca_context.Context = None,
        context_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_context.Context:
        r"""Creates a Context associated with a MetadataStore.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.CreateContextRequest):
                The request object. Request message for
                [MetadataService.CreateContext][google.cloud.aiplatform.v1beta1.MetadataService.CreateContext].
            parent (str):
                Required. The resource name of the
                MetadataStore where the Context should
                be created. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            context (google.cloud.aiplatform_v1beta1.types.Context):
                Required. The Context to create.
                This corresponds to the ``context`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            context_id (str):
                The {context} portion of the resource name with the
                format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/contexts/{context}.
                If not provided, the Context's ID will be a UUID
                generated by the service. Must be 4-128 characters in
                length. Valid characters are /[a-z][0-9]-/. Must be
                unique across all Contexts in the parent MetadataStore.
                (Otherwise the request will fail with ALREADY_EXISTS, or
                PERMISSION_DENIED if the caller can't view the
                preexisting Context.)

                This corresponds to the ``context_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.Context:
                Instance of a general context.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, context, context_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.CreateContextRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.CreateContextRequest):
            request = metadata_service.CreateContextRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if context is not None:
                request.context = context
            if context_id is not None:
                request.context_id = context_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_context]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_context(
        self,
        request: metadata_service.GetContextRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> context.Context:
        r"""Retrieves a specific Context.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.GetContextRequest):
                The request object. Request message for
                [MetadataService.GetContext][google.cloud.aiplatform.v1beta1.MetadataService.GetContext].
            name (str):
                Required. The resource name of the
                Context to retrieve. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/contexts/{context}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.Context:
                Instance of a general context.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.GetContextRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.GetContextRequest):
            request = metadata_service.GetContextRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_context]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_contexts(
        self,
        request: metadata_service.ListContextsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListContextsPager:
        r"""Lists Contexts on the MetadataStore.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.ListContextsRequest):
                The request object. Request message for
                [MetadataService.ListContexts][google.cloud.aiplatform.v1beta1.MetadataService.ListContexts]
            parent (str):
                Required. The MetadataStore whose
                Contexts should be listed. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.services.metadata_service.pagers.ListContextsPager:
                Response message for
                [MetadataService.ListContexts][google.cloud.aiplatform.v1beta1.MetadataService.ListContexts].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.ListContextsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.ListContextsRequest):
            request = metadata_service.ListContextsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_contexts]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListContextsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_context(
        self,
        request: metadata_service.UpdateContextRequest = None,
        *,
        context: gca_context.Context = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_context.Context:
        r"""Updates a stored Context.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.UpdateContextRequest):
                The request object. Request message for
                [MetadataService.UpdateContext][google.cloud.aiplatform.v1beta1.MetadataService.UpdateContext].
            context (google.cloud.aiplatform_v1beta1.types.Context):
                Required. The Context containing updates. The Context's
                [Context.name][google.cloud.aiplatform.v1beta1.Context.name]
                field is used to identify the Context to be updated.
                Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/contexts/{context}

                This corresponds to the ``context`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. A FieldMask indicating
                which fields should be updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.Context:
                Instance of a general context.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([context, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.UpdateContextRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.UpdateContextRequest):
            request = metadata_service.UpdateContextRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if context is not None:
                request.context = context
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_context]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("context.name", request.context.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_context(
        self,
        request: metadata_service.DeleteContextRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gac_operation.Operation:
        r"""Deletes a stored Context.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.DeleteContextRequest):
                The request object. Request message for
                [MetadataService.DeleteContext][google.cloud.aiplatform.v1beta1.MetadataService.DeleteContext].
            name (str):
                Required. The resource name of the
                Context to delete. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/contexts/{context}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.DeleteContextRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.DeleteContextRequest):
            request = metadata_service.DeleteContextRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_context]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = gac_operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=gca_operation.DeleteOperationMetadata,
        )

        # Done; return the response.
        return response

    def purge_contexts(
        self,
        request: metadata_service.PurgeContextsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gac_operation.Operation:
        r"""Purges Contexts.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.PurgeContextsRequest):
                The request object. Request message for
                [MetadataService.PurgeContexts][google.cloud.aiplatform.v1beta1.MetadataService.PurgeContexts].
            parent (str):
                Required. The metadata store to purge
                Contexts from. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.aiplatform_v1beta1.types.PurgeContextsResponse`
                Response message for
                [MetadataService.PurgeContexts][google.cloud.aiplatform.v1beta1.MetadataService.PurgeContexts].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.PurgeContextsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.PurgeContextsRequest):
            request = metadata_service.PurgeContextsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.purge_contexts]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = gac_operation.from_gapic(
            response,
            self._transport.operations_client,
            metadata_service.PurgeContextsResponse,
            metadata_type=metadata_service.PurgeContextsMetadata,
        )

        # Done; return the response.
        return response

    def add_context_artifacts_and_executions(
        self,
        request: metadata_service.AddContextArtifactsAndExecutionsRequest = None,
        *,
        context: str = None,
        artifacts: Sequence[str] = None,
        executions: Sequence[str] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metadata_service.AddContextArtifactsAndExecutionsResponse:
        r"""Adds a set of Artifacts and Executions to a Context.
        If any of the Artifacts or Executions have already been
        added to a Context, they are simply skipped.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.AddContextArtifactsAndExecutionsRequest):
                The request object. Request message for
                [MetadataService.AddContextArtifactsAndExecutions][google.cloud.aiplatform.v1beta1.MetadataService.AddContextArtifactsAndExecutions].
            context (str):
                Required. The resource name of the
                Context that the Artifacts and
                Executions belong to. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/contexts/{context}

                This corresponds to the ``context`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            artifacts (Sequence[str]):
                The resource names of the Artifacts
                to attribute to the Context.
                Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/artifacts/{artifact}

                This corresponds to the ``artifacts`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            executions (Sequence[str]):
                The resource names of the Executions
                to associate with the Context.

                Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/executions/{execution}

                This corresponds to the ``executions`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.AddContextArtifactsAndExecutionsResponse:
                Response message for
                [MetadataService.AddContextArtifactsAndExecutions][google.cloud.aiplatform.v1beta1.MetadataService.AddContextArtifactsAndExecutions].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([context, artifacts, executions])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.AddContextArtifactsAndExecutionsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, metadata_service.AddContextArtifactsAndExecutionsRequest
        ):
            request = metadata_service.AddContextArtifactsAndExecutionsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if context is not None:
                request.context = context
            if artifacts is not None:
                request.artifacts = artifacts
            if executions is not None:
                request.executions = executions

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.add_context_artifacts_and_executions
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("context", request.context),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def add_context_children(
        self,
        request: metadata_service.AddContextChildrenRequest = None,
        *,
        context: str = None,
        child_contexts: Sequence[str] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metadata_service.AddContextChildrenResponse:
        r"""Adds a set of Contexts as children to a parent Context. If any
        of the child Contexts have already been added to the parent
        Context, they are simply skipped. If this call would create a
        cycle or cause any Context to have more than 10 parents, the
        request will fail with an INVALID_ARGUMENT error.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.AddContextChildrenRequest):
                The request object. Request message for
                [MetadataService.AddContextChildren][google.cloud.aiplatform.v1beta1.MetadataService.AddContextChildren].
            context (str):
                Required. The resource name of the
                parent Context.
                Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/contexts/{context}

                This corresponds to the ``context`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            child_contexts (Sequence[str]):
                The resource names of the child
                Contexts.

                This corresponds to the ``child_contexts`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.AddContextChildrenResponse:
                Response message for
                [MetadataService.AddContextChildren][google.cloud.aiplatform.v1beta1.MetadataService.AddContextChildren].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([context, child_contexts])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.AddContextChildrenRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.AddContextChildrenRequest):
            request = metadata_service.AddContextChildrenRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if context is not None:
                request.context = context
            if child_contexts is not None:
                request.child_contexts = child_contexts

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_context_children]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("context", request.context),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def query_context_lineage_subgraph(
        self,
        request: metadata_service.QueryContextLineageSubgraphRequest = None,
        *,
        context: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> lineage_subgraph.LineageSubgraph:
        r"""Retrieves Artifacts and Executions within the
        specified Context, connected by Event edges and returned
        as a LineageSubgraph.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.QueryContextLineageSubgraphRequest):
                The request object. Request message for
                [MetadataService.QueryContextLineageSubgraph][google.cloud.aiplatform.v1beta1.MetadataService.QueryContextLineageSubgraph].
            context (str):
                Required. The resource name of the Context whose
                Artifacts and Executions should be retrieved as a
                LineageSubgraph. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/contexts/{context}

                The request may error with FAILED_PRECONDITION if the
                number of Artifacts, the number of Executions, or the
                number of Events that would be returned for the Context
                exceeds 1000.

                This corresponds to the ``context`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.LineageSubgraph:
                A subgraph of the overall lineage
                graph. Event edges connect Artifact and
                Execution nodes.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([context])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.QueryContextLineageSubgraphRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.QueryContextLineageSubgraphRequest):
            request = metadata_service.QueryContextLineageSubgraphRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if context is not None:
                request.context = context

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.query_context_lineage_subgraph
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("context", request.context),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_execution(
        self,
        request: metadata_service.CreateExecutionRequest = None,
        *,
        parent: str = None,
        execution: gca_execution.Execution = None,
        execution_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_execution.Execution:
        r"""Creates an Execution associated with a MetadataStore.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.CreateExecutionRequest):
                The request object. Request message for
                [MetadataService.CreateExecution][google.cloud.aiplatform.v1beta1.MetadataService.CreateExecution].
            parent (str):
                Required. The resource name of the
                MetadataStore where the Execution should
                be created. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            execution (google.cloud.aiplatform_v1beta1.types.Execution):
                Required. The Execution to create.
                This corresponds to the ``execution`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            execution_id (str):
                The {execution} portion of the resource name with the
                format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/executions/{execution}
                If not provided, the Execution's ID will be a UUID
                generated by the service. Must be 4-128 characters in
                length. Valid characters are /[a-z][0-9]-/. Must be
                unique across all Executions in the parent
                MetadataStore. (Otherwise the request will fail with
                ALREADY_EXISTS, or PERMISSION_DENIED if the caller can't
                view the preexisting Execution.)

                This corresponds to the ``execution_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.Execution:
                Instance of a general execution.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, execution, execution_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.CreateExecutionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.CreateExecutionRequest):
            request = metadata_service.CreateExecutionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if execution is not None:
                request.execution = execution
            if execution_id is not None:
                request.execution_id = execution_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_execution]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_execution(
        self,
        request: metadata_service.GetExecutionRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> execution.Execution:
        r"""Retrieves a specific Execution.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.GetExecutionRequest):
                The request object. Request message for
                [MetadataService.GetExecution][google.cloud.aiplatform.v1beta1.MetadataService.GetExecution].
            name (str):
                Required. The resource name of the
                Execution to retrieve. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/executions/{execution}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.Execution:
                Instance of a general execution.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.GetExecutionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.GetExecutionRequest):
            request = metadata_service.GetExecutionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_execution]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_executions(
        self,
        request: metadata_service.ListExecutionsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListExecutionsPager:
        r"""Lists Executions in the MetadataStore.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.ListExecutionsRequest):
                The request object. Request message for
                [MetadataService.ListExecutions][google.cloud.aiplatform.v1beta1.MetadataService.ListExecutions].
            parent (str):
                Required. The MetadataStore whose
                Executions should be listed. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.services.metadata_service.pagers.ListExecutionsPager:
                Response message for
                [MetadataService.ListExecutions][google.cloud.aiplatform.v1beta1.MetadataService.ListExecutions].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.ListExecutionsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.ListExecutionsRequest):
            request = metadata_service.ListExecutionsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_executions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListExecutionsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_execution(
        self,
        request: metadata_service.UpdateExecutionRequest = None,
        *,
        execution: gca_execution.Execution = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_execution.Execution:
        r"""Updates a stored Execution.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.UpdateExecutionRequest):
                The request object. Request message for
                [MetadataService.UpdateExecution][google.cloud.aiplatform.v1beta1.MetadataService.UpdateExecution].
            execution (google.cloud.aiplatform_v1beta1.types.Execution):
                Required. The Execution containing updates. The
                Execution's
                [Execution.name][google.cloud.aiplatform.v1beta1.Execution.name]
                field is used to identify the Execution to be updated.
                Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/executions/{execution}

                This corresponds to the ``execution`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. A FieldMask indicating
                which fields should be updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.Execution:
                Instance of a general execution.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([execution, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.UpdateExecutionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.UpdateExecutionRequest):
            request = metadata_service.UpdateExecutionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if execution is not None:
                request.execution = execution
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_execution]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("execution.name", request.execution.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_execution(
        self,
        request: metadata_service.DeleteExecutionRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gac_operation.Operation:
        r"""Deletes an Execution.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.DeleteExecutionRequest):
                The request object. Request message for
                [MetadataService.DeleteExecution][google.cloud.aiplatform.v1beta1.MetadataService.DeleteExecution].
            name (str):
                Required. The resource name of the
                Execution to delete. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/executions/{execution}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.DeleteExecutionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.DeleteExecutionRequest):
            request = metadata_service.DeleteExecutionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_execution]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = gac_operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=gca_operation.DeleteOperationMetadata,
        )

        # Done; return the response.
        return response

    def purge_executions(
        self,
        request: metadata_service.PurgeExecutionsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gac_operation.Operation:
        r"""Purges Executions.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.PurgeExecutionsRequest):
                The request object. Request message for
                [MetadataService.PurgeExecutions][google.cloud.aiplatform.v1beta1.MetadataService.PurgeExecutions].
            parent (str):
                Required. The metadata store to purge
                Executions from. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.aiplatform_v1beta1.types.PurgeExecutionsResponse`
                Response message for
                [MetadataService.PurgeExecutions][google.cloud.aiplatform.v1beta1.MetadataService.PurgeExecutions].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.PurgeExecutionsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.PurgeExecutionsRequest):
            request = metadata_service.PurgeExecutionsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.purge_executions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = gac_operation.from_gapic(
            response,
            self._transport.operations_client,
            metadata_service.PurgeExecutionsResponse,
            metadata_type=metadata_service.PurgeExecutionsMetadata,
        )

        # Done; return the response.
        return response

    def add_execution_events(
        self,
        request: metadata_service.AddExecutionEventsRequest = None,
        *,
        execution: str = None,
        events: Sequence[event.Event] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metadata_service.AddExecutionEventsResponse:
        r"""Adds Events to the specified Execution. An Event
        indicates whether an Artifact was used as an input or
        output for an Execution. If an Event already exists
        between the Execution and the Artifact, the Event is
        skipped.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.AddExecutionEventsRequest):
                The request object. Request message for
                [MetadataService.AddExecutionEvents][google.cloud.aiplatform.v1beta1.MetadataService.AddExecutionEvents].
            execution (str):
                Required. The resource name of the
                Execution that the Events connect
                Artifacts with. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/executions/{execution}

                This corresponds to the ``execution`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            events (Sequence[google.cloud.aiplatform_v1beta1.types.Event]):
                The Events to create and add.
                This corresponds to the ``events`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.AddExecutionEventsResponse:
                Response message for
                [MetadataService.AddExecutionEvents][google.cloud.aiplatform.v1beta1.MetadataService.AddExecutionEvents].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([execution, events])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.AddExecutionEventsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.AddExecutionEventsRequest):
            request = metadata_service.AddExecutionEventsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if execution is not None:
                request.execution = execution
            if events is not None:
                request.events = events

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_execution_events]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("execution", request.execution),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def query_execution_inputs_and_outputs(
        self,
        request: metadata_service.QueryExecutionInputsAndOutputsRequest = None,
        *,
        execution: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> lineage_subgraph.LineageSubgraph:
        r"""Obtains the set of input and output Artifacts for
        this Execution, in the form of LineageSubgraph that also
        contains the Execution and connecting Events.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.QueryExecutionInputsAndOutputsRequest):
                The request object. Request message for
                [MetadataService.QueryExecutionInputsAndOutputs][google.cloud.aiplatform.v1beta1.MetadataService.QueryExecutionInputsAndOutputs].
            execution (str):
                Required. The resource name of the
                Execution whose input and output
                Artifacts should be retrieved as a
                LineageSubgraph. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/executions/{execution}

                This corresponds to the ``execution`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.LineageSubgraph:
                A subgraph of the overall lineage
                graph. Event edges connect Artifact and
                Execution nodes.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([execution])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.QueryExecutionInputsAndOutputsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, metadata_service.QueryExecutionInputsAndOutputsRequest
        ):
            request = metadata_service.QueryExecutionInputsAndOutputsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if execution is not None:
                request.execution = execution

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.query_execution_inputs_and_outputs
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("execution", request.execution),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_metadata_schema(
        self,
        request: metadata_service.CreateMetadataSchemaRequest = None,
        *,
        parent: str = None,
        metadata_schema: gca_metadata_schema.MetadataSchema = None,
        metadata_schema_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_metadata_schema.MetadataSchema:
        r"""Creates a MetadataSchema.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.CreateMetadataSchemaRequest):
                The request object. Request message for
                [MetadataService.CreateMetadataSchema][google.cloud.aiplatform.v1beta1.MetadataService.CreateMetadataSchema].
            parent (str):
                Required. The resource name of the
                MetadataStore where the MetadataSchema
                should be created. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            metadata_schema (google.cloud.aiplatform_v1beta1.types.MetadataSchema):
                Required. The MetadataSchema to
                create.

                This corresponds to the ``metadata_schema`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            metadata_schema_id (str):
                The {metadata_schema} portion of the resource name with
                the format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/metadataSchemas/{metadataschema}
                If not provided, the MetadataStore's ID will be a UUID
                generated by the service. Must be 4-128 characters in
                length. Valid characters are /[a-z][0-9]-/. Must be
                unique across all MetadataSchemas in the parent
                Location. (Otherwise the request will fail with
                ALREADY_EXISTS, or PERMISSION_DENIED if the caller can't
                view the preexisting MetadataSchema.)

                This corresponds to the ``metadata_schema_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.MetadataSchema:
                Instance of a general MetadataSchema.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, metadata_schema, metadata_schema_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.CreateMetadataSchemaRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.CreateMetadataSchemaRequest):
            request = metadata_service.CreateMetadataSchemaRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if metadata_schema is not None:
                request.metadata_schema = metadata_schema
            if metadata_schema_id is not None:
                request.metadata_schema_id = metadata_schema_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_metadata_schema]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_metadata_schema(
        self,
        request: metadata_service.GetMetadataSchemaRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metadata_schema.MetadataSchema:
        r"""Retrieves a specific MetadataSchema.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.GetMetadataSchemaRequest):
                The request object. Request message for
                [MetadataService.GetMetadataSchema][google.cloud.aiplatform.v1beta1.MetadataService.GetMetadataSchema].
            name (str):
                Required. The resource name of the
                MetadataSchema to retrieve. Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/metadataSchemas/{metadataschema}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.MetadataSchema:
                Instance of a general MetadataSchema.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.GetMetadataSchemaRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.GetMetadataSchemaRequest):
            request = metadata_service.GetMetadataSchemaRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_metadata_schema]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_metadata_schemas(
        self,
        request: metadata_service.ListMetadataSchemasRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMetadataSchemasPager:
        r"""Lists MetadataSchemas.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.ListMetadataSchemasRequest):
                The request object. Request message for
                [MetadataService.ListMetadataSchemas][google.cloud.aiplatform.v1beta1.MetadataService.ListMetadataSchemas].
            parent (str):
                Required. The MetadataStore whose
                MetadataSchemas should be listed.
                Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.services.metadata_service.pagers.ListMetadataSchemasPager:
                Response message for
                [MetadataService.ListMetadataSchemas][google.cloud.aiplatform.v1beta1.MetadataService.ListMetadataSchemas].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.ListMetadataSchemasRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metadata_service.ListMetadataSchemasRequest):
            request = metadata_service.ListMetadataSchemasRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_metadata_schemas]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListMetadataSchemasPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def query_artifact_lineage_subgraph(
        self,
        request: metadata_service.QueryArtifactLineageSubgraphRequest = None,
        *,
        artifact: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> lineage_subgraph.LineageSubgraph:
        r"""Retrieves lineage of an Artifact represented through
        Artifacts and Executions connected by Event edges and
        returned as a LineageSubgraph.

        Args:
            request (google.cloud.aiplatform_v1beta1.types.QueryArtifactLineageSubgraphRequest):
                The request object. Request message for
                [MetadataService.QueryArtifactLineageSubgraph][google.cloud.aiplatform.v1beta1.MetadataService.QueryArtifactLineageSubgraph].
            artifact (str):
                Required. The resource name of the Artifact whose
                Lineage needs to be retrieved as a LineageSubgraph.
                Format:
                projects/{project}/locations/{location}/metadataStores/{metadatastore}/artifacts/{artifact}

                The request may error with FAILED_PRECONDITION if the
                number of Artifacts, the number of Executions, or the
                number of Events that would be returned for the Context
                exceeds 1000.

                This corresponds to the ``artifact`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.LineageSubgraph:
                A subgraph of the overall lineage
                graph. Event edges connect Artifact and
                Execution nodes.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([artifact])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metadata_service.QueryArtifactLineageSubgraphRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, metadata_service.QueryArtifactLineageSubgraphRequest
        ):
            request = metadata_service.QueryArtifactLineageSubgraphRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if artifact is not None:
                request.artifact = artifact

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.query_artifact_lineage_subgraph
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("artifact", request.artifact),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-aiplatform",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("MetadataServiceClient",)
