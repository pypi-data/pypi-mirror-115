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
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
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
from .transports.grpc_asyncio import EnvironmentsGrpcAsyncIOTransport
from .client import EnvironmentsClient


class EnvironmentsAsyncClient:
    """Managed Apache Airflow Environments."""

    _client: EnvironmentsClient

    DEFAULT_ENDPOINT = EnvironmentsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = EnvironmentsClient.DEFAULT_MTLS_ENDPOINT

    environment_path = staticmethod(EnvironmentsClient.environment_path)
    parse_environment_path = staticmethod(EnvironmentsClient.parse_environment_path)
    common_billing_account_path = staticmethod(
        EnvironmentsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        EnvironmentsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(EnvironmentsClient.common_folder_path)
    parse_common_folder_path = staticmethod(EnvironmentsClient.parse_common_folder_path)
    common_organization_path = staticmethod(EnvironmentsClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        EnvironmentsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(EnvironmentsClient.common_project_path)
    parse_common_project_path = staticmethod(
        EnvironmentsClient.parse_common_project_path
    )
    common_location_path = staticmethod(EnvironmentsClient.common_location_path)
    parse_common_location_path = staticmethod(
        EnvironmentsClient.parse_common_location_path
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
            EnvironmentsAsyncClient: The constructed client.
        """
        return EnvironmentsClient.from_service_account_info.__func__(EnvironmentsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            EnvironmentsAsyncClient: The constructed client.
        """
        return EnvironmentsClient.from_service_account_file.__func__(EnvironmentsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> EnvironmentsTransport:
        """Returns the transport used by the client instance.

        Returns:
            EnvironmentsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(EnvironmentsClient).get_transport_class, type(EnvironmentsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, EnvironmentsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the environments client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.EnvironmentsTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
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

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = EnvironmentsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_environment(
        self,
        request: environments.CreateEnvironmentRequest = None,
        *,
        parent: str = None,
        environment: environments.Environment = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Create a new environment.

        Args:
            request (:class:`google.cloud.orchestration.airflow.service_v1beta1.types.CreateEnvironmentRequest`):
                The request object. Create a new environment.
            parent (:class:`str`):
                The parent must be of the form
                "projects/{projectId}/locations/{locationId}".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            environment (:class:`google.cloud.orchestration.airflow.service_v1beta1.types.Environment`):
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
            google.api_core.operation_async.AsyncOperation:
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

        request = environments.CreateEnvironmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if environment is not None:
            request.environment = environment

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_environment,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            environments.Environment,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_environment(
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
            request (:class:`google.cloud.orchestration.airflow.service_v1beta1.types.GetEnvironmentRequest`):
                The request object. Get an environment.
            name (:class:`str`):
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

        request = environments.GetEnvironmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_environment,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_environments(
        self,
        request: environments.ListEnvironmentsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEnvironmentsAsyncPager:
        r"""List environments.

        Args:
            request (:class:`google.cloud.orchestration.airflow.service_v1beta1.types.ListEnvironmentsRequest`):
                The request object. List environments in a project and
                location.
            parent (:class:`str`):
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
            google.cloud.orchestration.airflow.service_v1beta1.services.environments.pagers.ListEnvironmentsAsyncPager:
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

        request = environments.ListEnvironmentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_environments,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListEnvironmentsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_environment(
        self,
        request: environments.UpdateEnvironmentRequest = None,
        *,
        name: str = None,
        environment: environments.Environment = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Update an environment.

        Args:
            request (:class:`google.cloud.orchestration.airflow.service_v1beta1.types.UpdateEnvironmentRequest`):
                The request object. Update an environment.
            name (:class:`str`):
                The relative resource name of the
                environment to update, in the form:
                "projects/{projectId}/locations/{locationId}/environments/{environmentId}"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            environment (:class:`google.cloud.orchestration.airflow.service_v1beta1.types.Environment`):
                A patch environment. Fields specified by the
                ``updateMask`` will be copied from the patch environment
                into the environment under update.

                This corresponds to the ``environment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
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
            google.api_core.operation_async.AsyncOperation:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_environment,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            environments.Environment,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_environment(
        self,
        request: environments.DeleteEnvironmentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Delete an environment.

        Args:
            request (:class:`google.cloud.orchestration.airflow.service_v1beta1.types.DeleteEnvironmentRequest`):
                The request object. Delete an environment.
            name (:class:`str`):
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
            google.api_core.operation_async.AsyncOperation:
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

        request = environments.DeleteEnvironmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_environment,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def restart_web_server(
        self,
        request: environments.RestartWebServerRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Restart Airflow web server.

        Args:
            request (:class:`google.cloud.orchestration.airflow.service_v1beta1.types.RestartWebServerRequest`):
                The request object. Restart Airflow web server.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.orchestration.airflow.service_v1beta1.types.Environment`
                An environment for running orchestration tasks.

        """
        # Create or coerce a protobuf request object.
        request = environments.RestartWebServerRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.restart_web_server,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            environments.Environment,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def check_upgrade(
        self,
        request: environments.CheckUpgradeRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Check if an upgrade operation on the environment will
        succeed.
        In case of problems detailed info can be found in the
        returned Operation.

        Args:
            request (:class:`google.cloud.orchestration.airflow.service_v1beta1.types.CheckUpgradeRequest`):
                The request object. Request to check whether image
                upgrade will succeed.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.orchestration.airflow.service_v1beta1.types.CheckUpgradeResponse` Message containing information about the result of an upgrade check
                   operation.

        """
        # Create or coerce a protobuf request object.
        request = environments.CheckUpgradeRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.check_upgrade,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("environment", request.environment),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
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


__all__ = ("EnvironmentsAsyncClient",)
