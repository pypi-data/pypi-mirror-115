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

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.orchestration.airflow.service_v1beta1.services.environments import (
    pagers,
)
from google.cloud.orchestration.airflow.service_v1beta1.types import environments
from google.cloud.orchestration.airflow.service_v1beta1.types import operations
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import EnvironmentsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import EnvironmentsGrpcTransport
from .transports.grpc_asyncio import EnvironmentsGrpcAsyncIOTransport


class EnvironmentsClientMeta(type):
    """Metaclass for the Environments client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[EnvironmentsTransport]]
    _transport_registry["grpc"] = EnvironmentsGrpcTransport
    _transport_registry["grpc_asyncio"] = EnvironmentsGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[EnvironmentsTransport]:
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


class EnvironmentsClient(metaclass=EnvironmentsClientMeta):
    """Managed Apache Airflow Environments."""

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

    DEFAULT_ENDPOINT = "composer.googleapis.com"
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
            EnvironmentsClient: The constructed client.
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
            EnvironmentsClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> EnvironmentsTransport:
        """Returns the transport used by the client instance.

        Returns:
            EnvironmentsTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def environment_path(project: str, location: str, environment: str,) -> str:
        """Returns a fully-qualified environment string."""
        return "projects/{project}/locations/{location}/environments/{environment}".format(
            project=project, location=location, environment=environment,
        )

    @staticmethod
    def parse_environment_path(path: str) -> Dict[str, str]:
        """Parses a environment path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/environments/(?P<environment>.+?)$",
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
        transport: Union[str, EnvironmentsTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the environments client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, EnvironmentsTransport]): The
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
        if isinstance(transport, EnvironmentsTransport):
            # transport is a EnvironmentsTransport instance.
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

    def create_environment(
        self,
        request: environments.CreateEnvironmentRequest = None,
        *,
        parent: str = None,
        environment: environments.Environment = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Create a new environment.

        Args:
            request (google.cloud.orchestration.airflow.service_v1beta1.types.CreateEnvironmentRequest):
                The request object. Create a new environment.
            parent (str):
                The parent must be of the form
                "projects/{projectId}/locations/{locationId}".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            environment (google.cloud.orchestration.airflow.service_v1beta1.types.Environment):
                The environment to create.
                This corresponds to the ``environment`` field
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
                :class:`google.cloud.orchestration.airflow.service_v1beta1.types.Environment`
                An environment for running orchestration tasks.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, environment])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a environments.CreateEnvironmentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, environments.CreateEnvironmentRequest):
            request = environments.CreateEnvironmentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if environment is not None:
                request.environment = environment

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_environment]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            environments.Environment,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    def get_environment(
        self,
        request: environments.GetEnvironmentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> environments.Environment:
        r"""Get an existing environment.

        Args:
            request (google.cloud.orchestration.airflow.service_v1beta1.types.GetEnvironmentRequest):
                The request object. Get an environment.
            name (str):
                The resource name of the environment
                to get, in the form:
                "projects/{projectId}/locations/{locationId}/environments/{environmentId}"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.orchestration.airflow.service_v1beta1.types.Environment:
                An environment for running
                orchestration tasks.

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
        # in a environments.GetEnvironmentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, environments.GetEnvironmentRequest):
            request = environments.GetEnvironmentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_environment]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_environments(
        self,
        request: environments.ListEnvironmentsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEnvironmentsPager:
        r"""List environments.

        Args:
            request (google.cloud.orchestration.airflow.service_v1beta1.types.ListEnvironmentsRequest):
                The request object. List environments in a project and
                location.
            parent (str):
                List environments in the given
                project and location, in the form:
                "projects/{projectId}/locations/{locationId}"

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.orchestration.airflow.service_v1beta1.services.environments.pagers.ListEnvironmentsPager:
                The environments in a project and
                location.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a environments.ListEnvironmentsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, environments.ListEnvironmentsRequest):
            request = environments.ListEnvironmentsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_environments]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListEnvironmentsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_environment(
        self,
        request: environments.UpdateEnvironmentRequest = None,
        *,
        name: str = None,
        environment: environments.Environment = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Update an environment.

        Args:
            request (google.cloud.orchestration.airflow.service_v1beta1.types.UpdateEnvironmentRequest):
                The request object. Update an environment.
            name (str):
                The relative resource name of the
                environment to update, in the form:
                "projects/{projectId}/locations/{locationId}/environments/{environmentId}"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            environment (google.cloud.orchestration.airflow.service_v1beta1.types.Environment):
                A patch environment. Fields specified by the
                ``updateMask`` will be copied from the patch environment
                into the environment under update.

                This corresponds to the ``environment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. A comma-separated list of paths, relative to
                ``Environment``, of fields to update. For example, to
                set the version of scikit-learn to install in the
                environment to 0.19.0 and to remove an existing
                installation of argparse, the ``updateMask`` parameter
                would include the following two ``paths`` values:
                "config.softwareConfig.pypiPackages.scikit-learn" and
                "config.softwareConfig.pypiPackages.argparse". The
                included patch environment would specify the
                scikit-learn version as follows:

                ::

                    {
                      "config":{
                        "softwareConfig":{
                          "pypiPackages":{
                            "scikit-learn":"==0.19.0"
                          }
                        }
                      }
                    }

                Note that in the above example, any existing PyPI
                packages other than scikit-learn and argparse will be
                unaffected.

                Only one update type may be included in a single
                request's ``updateMask``. For example, one cannot update
                both the PyPI packages and labels in the same request.
                However, it is possible to update multiple members of a
                map field simultaneously in the same request. For
                example, to set the labels "label1" and "label2" while
                clearing "label3" (assuming it already exists), one can
                provide the paths "labels.label1", "labels.label2", and
                "labels.label3" and populate the patch environment as
                follows:

                ::

                    {
                      "labels":{
                        "label1":"new-label1-value"
                        "label2":"new-label2-value"
                      }
                    }

                Note that in the above example, any existing labels that
                are not included in the ``updateMask`` will be
                unaffected.

                It is also possible to replace an entire map field by
                providing the map field's path in the ``updateMask``.
                The new value of the field will be that which is
                provided in the patch environment. For example, to
                delete all pre-existing user-specified PyPI packages and
                install botocore at version 1.7.14, the ``updateMask``
                would contain the path
                "config.softwareConfig.pypiPackages", and the patch
                environment would be the following:

                ::

                    {
                      "config":{
                        "softwareConfig":{
                          "pypiPackages":{
                            "botocore":"==1.7.14"
                          }
                        }
                      }
                    }

                **Note:** Only the following fields can be updated:

                -  ``config.softwareConfig.pypiPackages``

                   -  Replace all custom custom PyPI packages. If a
                      replacement package map is not included in
                      ``environment``, all custom PyPI packages are
                      cleared. It is an error to provide both this mask
                      and a mask specifying an individual package.

                -  ``config.softwareConfig.pypiPackages.``\ packagename

                   -  Update the custom PyPI package *packagename*,
                      preserving other packages. To delete the package,
                      include it in ``updateMask``, and omit the mapping
                      for it in
                      ``environment.config.softwareConfig.pypiPackages``.
                      It is an error to provide both a mask of this form
                      and the ``config.softwareConfig.pypiPackages``
                      mask.

                -  ``labels``

                   -  Replace all environment labels. If a replacement
                      labels map is not included in ``environment``, all
                      labels are cleared. It is an error to provide both
                      this mask and a mask specifying one or more
                      individual labels.

                -  ``labels.``\ labelName

                   -  Set the label named *labelName*, while preserving
                      other labels. To delete the label, include it in
                      ``updateMask`` and omit its mapping in
                      ``environment.labels``. It is an error to provide
                      both a mask of this form and the ``labels`` mask.

                -  ``config.nodeCount``

                   -  Horizontally scale the number of nodes in the
                      environment. An integer greater than or equal to 3
                      must be provided in the ``config.nodeCount``
                      field. \* ``config.webServerNetworkAccessControl``
                   -  Replace the environment's current
                      WebServerNetworkAccessControl.

                -  ``config.softwareConfig.airflowConfigOverrides``

                   -  Replace all Apache Airflow config overrides. If a
                      replacement config overrides map is not included
                      in ``environment``, all config overrides are
                      cleared. It is an error to provide both this mask
                      and a mask specifying one or more individual
                      config overrides.

                -  ``config.softwareConfig.airflowConfigOverrides.``\ section-name

                   -  Override the Apache Airflow config property *name*
                      in the section named *section*, preserving other
                      properties. To delete the property override,
                      include it in ``updateMask`` and omit its mapping
                      in
                      ``environment.config.softwareConfig.airflowConfigOverrides``.
                      It is an error to provide both a mask of this form
                      and the
                      ``config.softwareConfig.airflowConfigOverrides``
                      mask.

                -  ``config.softwareConfig.envVariables``

                   -  Replace all environment variables. If a
                      replacement environment variable map is not
                      included in ``environment``, all custom
                      environment variables are cleared. It is an error
                      to provide both this mask and a mask specifying
                      one or more individual environment variables.

                -  ``config.softwareConfig.imageVersion``

                   -  Upgrade the version of the environment in-place.
                      Refer to ``SoftwareConfig.image_version`` for
                      information on how to format the new image
                      version. Additionally, the new image version
                      cannot effect a version downgrade and must match
                      the current image version's Composer major version
                      and Airflow major and minor versions. Consult the
                      `Cloud Composer Version
                      List <https://cloud.google.com/composer/docs/concepts/versioning/composer-versions>`__
                      for valid values.

                -  ``config.softwareConfig.schedulerCount``

                   -  Horizontally scale the number of schedulers in
                      Airflow. A positive integer not greater than the
                      number of nodes must be provided in the
                      ``config.softwareConfig.schedulerCount`` field. \*
                      ``config.databaseConfig.machineType``
                   -  Cloud SQL machine type used by Airflow database.
                      It has to be one of: db-n1-standard-2,
                      db-n1-standard-4, db-n1-standard-8 or
                      db-n1-standard-16. \*
                      ``config.webServerConfig.machineType``
                   -  Machine type on which Airflow web server is
                      running. It has to be one of:
                      composer-n1-webserver-2, composer-n1-webserver-4
                      or composer-n1-webserver-8. \*
                      ``config.maintenanceWindow``
                   -  Maintenance window during which Cloud Composer
                      components may be under maintenance.

                This corresponds to the ``update_mask`` field
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
                :class:`google.cloud.orchestration.airflow.service_v1beta1.types.Environment`
                An environment for running orchestration tasks.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, environment, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a environments.UpdateEnvironmentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, environments.UpdateEnvironmentRequest):
            request = environments.UpdateEnvironmentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if environment is not None:
                request.environment = environment
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_environment]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            environments.Environment,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_environment(
        self,
        request: environments.DeleteEnvironmentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Delete an environment.

        Args:
            request (google.cloud.orchestration.airflow.service_v1beta1.types.DeleteEnvironmentRequest):
                The request object. Delete an environment.
            name (str):
                The environment to delete, in the
                form:
                "projects/{projectId}/locations/{locationId}/environments/{environmentId}"

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
        # in a environments.DeleteEnvironmentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, environments.DeleteEnvironmentRequest):
            request = environments.DeleteEnvironmentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_environment]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    def restart_web_server(
        self,
        request: environments.RestartWebServerRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Restart Airflow web server.

        Args:
            request (google.cloud.orchestration.airflow.service_v1beta1.types.RestartWebServerRequest):
                The request object. Restart Airflow web server.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.orchestration.airflow.service_v1beta1.types.Environment`
                An environment for running orchestration tasks.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a environments.RestartWebServerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, environments.RestartWebServerRequest):
            request = environments.RestartWebServerRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.restart_web_server]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            environments.Environment,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    def check_upgrade(
        self,
        request: environments.CheckUpgradeRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Check if an upgrade operation on the environment will
        succeed.
        In case of problems detailed info can be found in the
        returned Operation.

        Args:
            request (google.cloud.orchestration.airflow.service_v1beta1.types.CheckUpgradeRequest):
                The request object. Request to check whether image
                upgrade will succeed.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.orchestration.airflow.service_v1beta1.types.CheckUpgradeResponse` Message containing information about the result of an upgrade check
                   operation.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a environments.CheckUpgradeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, environments.CheckUpgradeRequest):
            request = environments.CheckUpgradeRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.check_upgrade]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("environment", request.environment),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            environments.CheckUpgradeResponse,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-orchestration-airflow-service",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("EnvironmentsClient",)
