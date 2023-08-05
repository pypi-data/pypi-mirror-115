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

from google.cloud.retail_v2.services.catalog_service import pagers
from google.cloud.retail_v2.types import catalog
from google.cloud.retail_v2.types import catalog as gcr_catalog
from google.cloud.retail_v2.types import catalog_service
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import CatalogServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import CatalogServiceGrpcAsyncIOTransport
from .client import CatalogServiceClient


class CatalogServiceAsyncClient:
    """Service for managing catalog configuration."""

    _client: CatalogServiceClient

    DEFAULT_ENDPOINT = CatalogServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = CatalogServiceClient.DEFAULT_MTLS_ENDPOINT

    branch_path = staticmethod(CatalogServiceClient.branch_path)
    parse_branch_path = staticmethod(CatalogServiceClient.parse_branch_path)
    catalog_path = staticmethod(CatalogServiceClient.catalog_path)
    parse_catalog_path = staticmethod(CatalogServiceClient.parse_catalog_path)
    common_billing_account_path = staticmethod(
        CatalogServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        CatalogServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(CatalogServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        CatalogServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        CatalogServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        CatalogServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(CatalogServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        CatalogServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(CatalogServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        CatalogServiceClient.parse_common_location_path
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
            CatalogServiceAsyncClient: The constructed client.
        """
        return CatalogServiceClient.from_service_account_info.__func__(CatalogServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            CatalogServiceAsyncClient: The constructed client.
        """
        return CatalogServiceClient.from_service_account_file.__func__(CatalogServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> CatalogServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            CatalogServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(CatalogServiceClient).get_transport_class, type(CatalogServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, CatalogServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the catalog service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.CatalogServiceTransport]): The
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
        self._client = CatalogServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_catalogs(
        self,
        request: catalog_service.ListCatalogsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCatalogsAsyncPager:
        r"""Lists all the [Catalog][google.cloud.retail.v2.Catalog]s
        associated with the project.

        Args:
            request (:class:`google.cloud.retail_v2.types.ListCatalogsRequest`):
                The request object. Request for
                [CatalogService.ListCatalogs][google.cloud.retail.v2.CatalogService.ListCatalogs]
                method.
            parent (:class:`str`):
                Required. The account resource name with an associated
                location.

                If the caller does not have permission to list
                [Catalog][google.cloud.retail.v2.Catalog]s under this
                location, regardless of whether or not this location
                exists, a PERMISSION_DENIED error is returned.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2.services.catalog_service.pagers.ListCatalogsAsyncPager:
                Response for
                   [CatalogService.ListCatalogs][google.cloud.retail.v2.CatalogService.ListCatalogs]
                   method.

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

        request = catalog_service.ListCatalogsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_catalogs,
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
        response = pagers.ListCatalogsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_catalog(
        self,
        request: catalog_service.UpdateCatalogRequest = None,
        *,
        catalog: gcr_catalog.Catalog = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcr_catalog.Catalog:
        r"""Updates the [Catalog][google.cloud.retail.v2.Catalog]s.

        Args:
            request (:class:`google.cloud.retail_v2.types.UpdateCatalogRequest`):
                The request object. Request for
                [CatalogService.UpdateCatalog][google.cloud.retail.v2.CatalogService.UpdateCatalog]
                method.
            catalog (:class:`google.cloud.retail_v2.types.Catalog`):
                Required. The [Catalog][google.cloud.retail.v2.Catalog]
                to update.

                If the caller does not have permission to update the
                [Catalog][google.cloud.retail.v2.Catalog], regardless of
                whether or not it exists, a PERMISSION_DENIED error is
                returned.

                If the [Catalog][google.cloud.retail.v2.Catalog] to
                update does not exist, a NOT_FOUND error is returned.

                This corresponds to the ``catalog`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Indicates which fields in the provided
                [Catalog][google.cloud.retail.v2.Catalog] to update.

                If an unsupported or unknown field is provided, an
                INVALID_ARGUMENT error is returned.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2.types.Catalog:
                The catalog configuration.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([catalog, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = catalog_service.UpdateCatalogRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if catalog is not None:
            request.catalog = catalog
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_catalog,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("catalog.name", request.catalog.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def set_default_branch(
        self,
        request: catalog_service.SetDefaultBranchRequest = None,
        *,
        catalog: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Set a specified branch id as default branch. API methods such as
        [SearchService.Search][google.cloud.retail.v2.SearchService.Search],
        [ProductService.GetProduct][google.cloud.retail.v2.ProductService.GetProduct],
        [ProductService.ListProducts][google.cloud.retail.v2.ProductService.ListProducts]
        will treat requests using "default_branch" to the actual branch
        id set as default.

        For example, if ``projects/*/locations/*/catalogs/*/branches/1``
        is set as default, setting
        [SearchRequest.branch][google.cloud.retail.v2.SearchRequest.branch]
        to ``projects/*/locations/*/catalogs/*/branches/default_branch``
        is equivalent to setting
        [SearchRequest.branch][google.cloud.retail.v2.SearchRequest.branch]
        to ``projects/*/locations/*/catalogs/*/branches/1``.

        Using multiple branches can be useful when developers would like
        to have a staging branch to test and verify for future usage.
        When it becomes ready, developers switch on the staging branch
        using this API while keeping using
        ``projects/*/locations/*/catalogs/*/branches/default_branch`` as
        [SearchRequest.branch][google.cloud.retail.v2.SearchRequest.branch]
        to route the traffic to this staging branch.

        CAUTION: If you have live predict/search traffic, switching the
        default branch could potentially cause outages if the ID space
        of the new branch is very different from the old one.

        More specifically:

        -  PredictionService will only return product IDs from branch
           {newBranch}.
        -  SearchService will only return product IDs from branch
           {newBranch} (if branch is not explicitly set).
        -  UserEventService will only join events with products from
           branch {newBranch}.

        This feature is only available for users who have Retail Search
        enabled. Contact Retail Support
        (retail-search-support@google.com) if you are interested in
        using Retail Search.

        Args:
            request (:class:`google.cloud.retail_v2.types.SetDefaultBranchRequest`):
                The request object. Request message to set a specified
                branch as new default_branch.
            catalog (:class:`str`):
                Full resource name of the catalog, such as
                ``projects/*/locations/global/catalogs/default_catalog``.

                This corresponds to the ``catalog`` field
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
        has_flattened_params = any([catalog])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = catalog_service.SetDefaultBranchRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if catalog is not None:
            request.catalog = catalog

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.set_default_branch,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("catalog", request.catalog),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def get_default_branch(
        self,
        request: catalog_service.GetDefaultBranchRequest = None,
        *,
        catalog: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> catalog_service.GetDefaultBranchResponse:
        r"""Get which branch is currently default branch set by
        [CatalogService.SetDefaultBranch][google.cloud.retail.v2.CatalogService.SetDefaultBranch]
        method under a specified parent catalog.

        This feature is only available for users who have Retail Search
        enabled. Contact Retail Support
        (retail-search-support@google.com) if you are interested in
        using Retail Search.

        Args:
            request (:class:`google.cloud.retail_v2.types.GetDefaultBranchRequest`):
                The request object. Request message to show which branch
                is currently the default branch.
            catalog (:class:`str`):
                The parent catalog resource name, such as
                ``projects/*/locations/global/catalogs/default_catalog``.

                This corresponds to the ``catalog`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2.types.GetDefaultBranchResponse:
                Response message of
                   [CatalogService.GetDefaultBranch][google.cloud.retail.v2.CatalogService.GetDefaultBranch].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([catalog])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = catalog_service.GetDefaultBranchRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if catalog is not None:
            request.catalog = catalog

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_default_branch,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("catalog", request.catalog),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-retail",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("CatalogServiceAsyncClient",)
