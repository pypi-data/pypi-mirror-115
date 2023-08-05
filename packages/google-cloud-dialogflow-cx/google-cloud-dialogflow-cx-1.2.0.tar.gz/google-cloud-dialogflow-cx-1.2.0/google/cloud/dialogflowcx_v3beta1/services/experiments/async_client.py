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

from google.cloud.dialogflowcx_v3beta1.services.experiments import pagers
from google.cloud.dialogflowcx_v3beta1.types import experiment
from google.cloud.dialogflowcx_v3beta1.types import experiment as gcdc_experiment
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import ExperimentsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import ExperimentsGrpcAsyncIOTransport
from .client import ExperimentsClient


class ExperimentsAsyncClient:
    """Service for managing
    [Experiments][google.cloud.dialogflow.cx.v3beta1.Experiment].
    """

    _client: ExperimentsClient

    DEFAULT_ENDPOINT = ExperimentsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ExperimentsClient.DEFAULT_MTLS_ENDPOINT

    experiment_path = staticmethod(ExperimentsClient.experiment_path)
    parse_experiment_path = staticmethod(ExperimentsClient.parse_experiment_path)
    version_path = staticmethod(ExperimentsClient.version_path)
    parse_version_path = staticmethod(ExperimentsClient.parse_version_path)
    common_billing_account_path = staticmethod(
        ExperimentsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ExperimentsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ExperimentsClient.common_folder_path)
    parse_common_folder_path = staticmethod(ExperimentsClient.parse_common_folder_path)
    common_organization_path = staticmethod(ExperimentsClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        ExperimentsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ExperimentsClient.common_project_path)
    parse_common_project_path = staticmethod(
        ExperimentsClient.parse_common_project_path
    )
    common_location_path = staticmethod(ExperimentsClient.common_location_path)
    parse_common_location_path = staticmethod(
        ExperimentsClient.parse_common_location_path
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
            ExperimentsAsyncClient: The constructed client.
        """
        return ExperimentsClient.from_service_account_info.__func__(ExperimentsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ExperimentsAsyncClient: The constructed client.
        """
        return ExperimentsClient.from_service_account_file.__func__(ExperimentsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ExperimentsTransport:
        """Returns the transport used by the client instance.

        Returns:
            ExperimentsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ExperimentsClient).get_transport_class, type(ExperimentsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, ExperimentsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the experiments client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ExperimentsTransport]): The
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
        self._client = ExperimentsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_experiments(
        self,
        request: experiment.ListExperimentsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListExperimentsAsyncPager:
        r"""Returns the list of all experiments in the specified
        [Environment][google.cloud.dialogflow.cx.v3beta1.Environment].

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.ListExperimentsRequest`):
                The request object. The request message for
                [Experiments.ListExperiments][google.cloud.dialogflow.cx.v3beta1.Experiments.ListExperiments].
            parent (:class:`str`):
                Required. The
                [Environment][google.cloud.dialogflow.cx.v3beta1.Environment]
                to list all environments for. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.services.experiments.pagers.ListExperimentsAsyncPager:
                The response message for
                [Experiments.ListExperiments][google.cloud.dialogflow.cx.v3beta1.Experiments.ListExperiments].

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

        request = experiment.ListExperimentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_experiments,
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
        response = pagers.ListExperimentsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_experiment(
        self,
        request: experiment.GetExperimentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> experiment.Experiment:
        r"""Retrieves the specified
        [Experiment][google.cloud.dialogflow.cx.v3beta1.Experiment].

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.GetExperimentRequest`):
                The request object. The request message for
                [Experiments.GetExperiment][google.cloud.dialogflow.cx.v3beta1.Experiments.GetExperiment].
            name (:class:`str`):
                Required. The name of the
                [Environment][google.cloud.dialogflow.cx.v3beta1.Environment].
                Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/experiments/<Experiment ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.types.Experiment:
                Represents an experiment in an
                environment.

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

        request = experiment.GetExperimentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_experiment,
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

    async def create_experiment(
        self,
        request: gcdc_experiment.CreateExperimentRequest = None,
        *,
        parent: str = None,
        experiment: gcdc_experiment.Experiment = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_experiment.Experiment:
        r"""Creates an
        [Experiment][google.cloud.dialogflow.cx.v3beta1.Experiment] in
        the specified
        [Environment][google.cloud.dialogflow.cx.v3beta1.Environment].

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.CreateExperimentRequest`):
                The request object. The request message for
                [Experiments.CreateExperiment][google.cloud.dialogflow.cx.v3beta1.Experiments.CreateExperiment].
            parent (:class:`str`):
                Required. The
                [Agent][google.cloud.dialogflow.cx.v3beta1.Agent] to
                create an
                [Environment][google.cloud.dialogflow.cx.v3beta1.Environment]
                for. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            experiment (:class:`google.cloud.dialogflowcx_v3beta1.types.Experiment`):
                Required. The experiment to create.
                This corresponds to the ``experiment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.types.Experiment:
                Represents an experiment in an
                environment.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, experiment])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_experiment.CreateExperimentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if experiment is not None:
            request.experiment = experiment

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_experiment,
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

        # Done; return the response.
        return response

    async def update_experiment(
        self,
        request: gcdc_experiment.UpdateExperimentRequest = None,
        *,
        experiment: gcdc_experiment.Experiment = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_experiment.Experiment:
        r"""Updates the specified
        [Experiment][google.cloud.dialogflow.cx.v3beta1.Experiment].

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.UpdateExperimentRequest`):
                The request object. The request message for
                [Experiments.UpdateExperiment][google.cloud.dialogflow.cx.v3beta1.Experiments.UpdateExperiment].
            experiment (:class:`google.cloud.dialogflowcx_v3beta1.types.Experiment`):
                Required. The experiment to update.
                This corresponds to the ``experiment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The mask to control which
                fields get updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.types.Experiment:
                Represents an experiment in an
                environment.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([experiment, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_experiment.UpdateExperimentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if experiment is not None:
            request.experiment = experiment
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_experiment,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("experiment.name", request.experiment.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_experiment(
        self,
        request: experiment.DeleteExperimentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified
        [Experiment][google.cloud.dialogflow.cx.v3beta1.Experiment].

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.DeleteExperimentRequest`):
                The request object. The request message for
                [Experiments.DeleteExperiment][google.cloud.dialogflow.cx.v3beta1.Experiments.DeleteExperiment].
            name (:class:`str`):
                Required. The name of the
                [Environment][google.cloud.dialogflow.cx.v3beta1.Environment]
                to delete. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/experiments/<Experiment ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
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

        request = experiment.DeleteExperimentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_experiment,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def start_experiment(
        self,
        request: experiment.StartExperimentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> experiment.Experiment:
        r"""Starts the specified
        [Experiment][google.cloud.dialogflow.cx.v3beta1.Experiment].
        This rpc only changes the state of experiment from PENDING to
        RUNNING.

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.StartExperimentRequest`):
                The request object. The request message for
                [Experiments.StartExperiment][google.cloud.dialogflow.cx.v3beta1.Experiments.StartExperiment].
            name (:class:`str`):
                Required. Resource name of the experiment to start.
                Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/experiments/<Experiment ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.types.Experiment:
                Represents an experiment in an
                environment.

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

        request = experiment.StartExperimentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.start_experiment,
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

    async def stop_experiment(
        self,
        request: experiment.StopExperimentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> experiment.Experiment:
        r"""Stops the specified
        [Experiment][google.cloud.dialogflow.cx.v3beta1.Experiment].
        This rpc only changes the state of experiment from RUNNING to
        DONE.

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.StopExperimentRequest`):
                The request object. The request message for
                [Experiments.StopExperiment][google.cloud.dialogflow.cx.v3beta1.Experiments.StopExperiment].
            name (:class:`str`):
                Required. Resource name of the experiment to stop.
                Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/experiments/<Experiment ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.types.Experiment:
                Represents an experiment in an
                environment.

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

        request = experiment.StopExperimentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.stop_experiment,
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


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflowcx",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ExperimentsAsyncClient",)
