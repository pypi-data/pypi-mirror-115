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
from google.cloud.retail_v2.services.product_service import pagers
from google.cloud.retail_v2.types import common
from google.cloud.retail_v2.types import import_config
from google.cloud.retail_v2.types import product
from google.cloud.retail_v2.types import product as gcr_product
from google.cloud.retail_v2.types import product_service
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from .transports.base import ProductServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import ProductServiceGrpcTransport
from .transports.grpc_asyncio import ProductServiceGrpcAsyncIOTransport


class ProductServiceClientMeta(type):
    """Metaclass for the ProductService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[ProductServiceTransport]]
    _transport_registry["grpc"] = ProductServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = ProductServiceGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[ProductServiceTransport]:
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


class ProductServiceClient(metaclass=ProductServiceClientMeta):
    """Service for ingesting [Product][google.cloud.retail.v2.Product]
    information of the customer's website.
    """

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

    DEFAULT_ENDPOINT = "retail.googleapis.com"
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
            ProductServiceClient: The constructed client.
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
            ProductServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ProductServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ProductServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def branch_path(project: str, location: str, catalog: str, branch: str,) -> str:
        """Returns a fully-qualified branch string."""
        return "projects/{project}/locations/{location}/catalogs/{catalog}/branches/{branch}".format(
            project=project, location=location, catalog=catalog, branch=branch,
        )

    @staticmethod
    def parse_branch_path(path: str) -> Dict[str, str]:
        """Parses a branch path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/catalogs/(?P<catalog>.+?)/branches/(?P<branch>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def product_path(
        project: str, location: str, catalog: str, branch: str, product: str,
    ) -> str:
        """Returns a fully-qualified product string."""
        return "projects/{project}/locations/{location}/catalogs/{catalog}/branches/{branch}/products/{product}".format(
            project=project,
            location=location,
            catalog=catalog,
            branch=branch,
            product=product,
        )

    @staticmethod
    def parse_product_path(path: str) -> Dict[str, str]:
        """Parses a product path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/catalogs/(?P<catalog>.+?)/branches/(?P<branch>.+?)/products/(?P<product>.+?)$",
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
        transport: Union[str, ProductServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the product service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ProductServiceTransport]): The
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
        if isinstance(transport, ProductServiceTransport):
            # transport is a ProductServiceTransport instance.
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

    def create_product(
        self,
        request: product_service.CreateProductRequest = None,
        *,
        parent: str = None,
        product: gcr_product.Product = None,
        product_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcr_product.Product:
        r"""Creates a [Product][google.cloud.retail.v2.Product].

        Args:
            request (google.cloud.retail_v2.types.CreateProductRequest):
                The request object. Request message for
                [CreateProduct][] method.
            parent (str):
                Required. The parent catalog resource name, such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            product (google.cloud.retail_v2.types.Product):
                Required. The [Product][google.cloud.retail.v2.Product]
                to create.

                This corresponds to the ``product`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            product_id (str):
                Required. The ID to use for the
                [Product][google.cloud.retail.v2.Product], which will
                become the final component of the
                [Product.name][google.cloud.retail.v2.Product.name].

                If the caller does not have permission to create the
                [Product][google.cloud.retail.v2.Product], regardless of
                whether or not it exists, a PERMISSION_DENIED error is
                returned.

                This field must be unique among all
                [Product][google.cloud.retail.v2.Product]s with the same
                [parent][google.cloud.retail.v2.CreateProductRequest.parent].
                Otherwise, an ALREADY_EXISTS error is returned.

                This field must be a UTF-8 encoded string with a length
                limit of 128 characters. Otherwise, an INVALID_ARGUMENT
                error is returned.

                This corresponds to the ``product_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2.types.Product:
                Product captures all metadata
                information of items to be recommended
                or searched.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, product, product_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a product_service.CreateProductRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, product_service.CreateProductRequest):
            request = product_service.CreateProductRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if product is not None:
                request.product = product
            if product_id is not None:
                request.product_id = product_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_product]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_product(
        self,
        request: product_service.GetProductRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> product.Product:
        r"""Gets a [Product][google.cloud.retail.v2.Product].

        Args:
            request (google.cloud.retail_v2.types.GetProductRequest):
                The request object. Request message for [GetProduct][]
                method.
            name (str):
                Required. Full resource name of
                [Product][google.cloud.retail.v2.Product], such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/some_product_id``.

                If the caller does not have permission to access the
                [Product][google.cloud.retail.v2.Product], regardless of
                whether or not it exists, a PERMISSION_DENIED error is
                returned.

                If the requested
                [Product][google.cloud.retail.v2.Product] does not
                exist, a NOT_FOUND error is returned.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2.types.Product:
                Product captures all metadata
                information of items to be recommended
                or searched.

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
        # in a product_service.GetProductRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, product_service.GetProductRequest):
            request = product_service.GetProductRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_product]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_products(
        self,
        request: product_service.ListProductsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListProductsPager:
        r"""Gets a list of [Product][google.cloud.retail.v2.Product]s.

        Args:
            request (google.cloud.retail_v2.types.ListProductsRequest):
                The request object. Request message for
                [ProductService.ListProducts][google.cloud.retail.v2.ProductService.ListProducts]
                method.
            parent (str):
                Required. The parent branch resource name, such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/0``.
                Use ``default_branch`` as the branch ID, to list
                products under the default branch.

                If the caller does not have permission to list
                [Product][google.cloud.retail.v2.Product]s under this
                branch, regardless of whether or not this branch exists,
                a PERMISSION_DENIED error is returned.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2.services.product_service.pagers.ListProductsPager:
                Response message for
                   [ProductService.ListProducts][google.cloud.retail.v2.ProductService.ListProducts]
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

        # Minor optimization to avoid making a copy if the user passes
        # in a product_service.ListProductsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, product_service.ListProductsRequest):
            request = product_service.ListProductsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_products]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListProductsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_product(
        self,
        request: product_service.UpdateProductRequest = None,
        *,
        product: gcr_product.Product = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcr_product.Product:
        r"""Updates a [Product][google.cloud.retail.v2.Product].

        Args:
            request (google.cloud.retail_v2.types.UpdateProductRequest):
                The request object. Request message for
                [UpdateProduct][] method.
            product (google.cloud.retail_v2.types.Product):
                Required. The product to update/create.

                If the caller does not have permission to update the
                [Product][google.cloud.retail.v2.Product], regardless of
                whether or not it exists, a PERMISSION_DENIED error is
                returned.

                If the [Product][google.cloud.retail.v2.Product] to
                update does not exist and
                [allow_missing][google.cloud.retail.v2.UpdateProductRequest.allow_missing]
                is not set, a NOT_FOUND error is returned.

                This corresponds to the ``product`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Indicates which fields in the provided
                [Product][google.cloud.retail.v2.Product] to update. The
                immutable and output only fields are NOT supported. If
                not set, all supported fields (the fields that are
                neither immutable nor output only) are updated.

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
            google.cloud.retail_v2.types.Product:
                Product captures all metadata
                information of items to be recommended
                or searched.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([product, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a product_service.UpdateProductRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, product_service.UpdateProductRequest):
            request = product_service.UpdateProductRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if product is not None:
                request.product = product
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_product]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("product.name", request.product.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_product(
        self,
        request: product_service.DeleteProductRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a [Product][google.cloud.retail.v2.Product].

        Args:
            request (google.cloud.retail_v2.types.DeleteProductRequest):
                The request object. Request message for
                [DeleteProduct][] method.
            name (str):
                Required. Full resource name of
                [Product][google.cloud.retail.v2.Product], such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/some_product_id``.

                If the caller does not have permission to delete the
                [Product][google.cloud.retail.v2.Product], regardless of
                whether or not it exists, a PERMISSION_DENIED error is
                returned.

                If the [Product][google.cloud.retail.v2.Product] to
                delete does not exist, a NOT_FOUND error is returned.

                The [Product][google.cloud.retail.v2.Product] to delete
                can neither be a
                [Product.Type.COLLECTION][google.cloud.retail.v2.Product.Type.COLLECTION]
                [Product][google.cloud.retail.v2.Product] member nor a
                [Product.Type.PRIMARY][google.cloud.retail.v2.Product.Type.PRIMARY]
                [Product][google.cloud.retail.v2.Product] with more than
                one
                [variants][google.cloud.retail.v2.Product.Type.VARIANT].
                Otherwise, an INVALID_ARGUMENT error is returned.

                All inventory information for the named
                [Product][google.cloud.retail.v2.Product] will be
                deleted.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a product_service.DeleteProductRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, product_service.DeleteProductRequest):
            request = product_service.DeleteProductRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_product]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def import_products(
        self,
        request: import_config.ImportProductsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Bulk import of multiple
        [Product][google.cloud.retail.v2.Product]s.

        Request processing may be synchronous. No partial updating is
        supported. Non-existing items are created.

        Note that it is possible for a subset of the
        [Product][google.cloud.retail.v2.Product]s to be successfully
        updated.

        Args:
            request (google.cloud.retail_v2.types.ImportProductsRequest):
                The request object. Request message for Import methods.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.retail_v2.types.ImportProductsResponse` Response of the
                   [ImportProductsRequest][google.cloud.retail.v2.ImportProductsRequest].
                   If the long running operation is done, then this
                   message is returned by the
                   google.longrunning.Operations.response field if the
                   operation was successful.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a import_config.ImportProductsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, import_config.ImportProductsRequest):
            request = import_config.ImportProductsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.import_products]

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
            import_config.ImportProductsResponse,
            metadata_type=import_config.ImportMetadata,
        )

        # Done; return the response.
        return response

    def set_inventory(
        self,
        request: product_service.SetInventoryRequest = None,
        *,
        inventory: product.Product = None,
        set_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates inventory information for a
        [Product][google.cloud.retail.v2.Product] while respecting the
        last update timestamps of each inventory field.

        This process is asynchronous and does not require the
        [Product][google.cloud.retail.v2.Product] to exist before
        updating fulfillment information. If the request is valid, the
        update will be enqueued and processed downstream. As a
        consequence, when a response is returned, updates are not
        immediately manifested in the
        [Product][google.cloud.retail.v2.Product] queried by
        [GetProduct][google.cloud.retail.v2.ProductService.GetProduct]
        or
        [ListProducts][google.cloud.retail.v2.ProductService.ListProducts].

        When inventory is updated with
        [CreateProduct][google.cloud.retail.v2.ProductService.CreateProduct]
        and
        [UpdateProduct][google.cloud.retail.v2.ProductService.UpdateProduct],
        the specified inventory field value(s) will overwrite any
        existing value(s) while ignoring the last update time for this
        field. Furthermore, the last update time for the specified
        inventory fields will be overwritten to the time of the
        [CreateProduct][google.cloud.retail.v2.ProductService.CreateProduct]
        or
        [UpdateProduct][google.cloud.retail.v2.ProductService.UpdateProduct]
        request.

        If no inventory fields are set in
        [CreateProductRequest.product][google.cloud.retail.v2.CreateProductRequest.product],
        then any pre-existing inventory information for this product
        will be used.

        If no inventory fields are set in
        [UpdateProductRequest.set_mask][], then any existing inventory
        information will be preserved.

        Pre-existing inventory information can only be updated with
        [SetInventory][google.cloud.retail.v2.ProductService.SetInventory],
        [AddFulfillmentPlaces][google.cloud.retail.v2.ProductService.AddFulfillmentPlaces],
        and
        [RemoveFulfillmentPlaces][google.cloud.retail.v2.ProductService.RemoveFulfillmentPlaces].

        This feature is only available for users who have Retail Search
        enabled. Contact Retail Support
        (retail-search-support@google.com) if you are interested in
        using Retail Search.

        Args:
            request (google.cloud.retail_v2.types.SetInventoryRequest):
                The request object. Request message for [SetInventory][]
                method.
            inventory (google.cloud.retail_v2.types.Product):
                Required. The inventory information to update. The
                allowable fields to update are:

                -  [Product.price_info][google.cloud.retail.v2.Product.price_info]
                -  [Product.availability][google.cloud.retail.v2.Product.availability]
                -  [Product.available_quantity][google.cloud.retail.v2.Product.available_quantity]
                -  [Product.fulfillment_info][google.cloud.retail.v2.Product.fulfillment_info]
                   The updated inventory fields must be specified in
                   [SetInventoryRequest.set_mask][google.cloud.retail.v2.SetInventoryRequest.set_mask].

                If [SetInventoryRequest.inventory.name][] is empty or
                invalid, an INVALID_ARGUMENT error is returned.

                If the caller does not have permission to update the
                [Product][google.cloud.retail.v2.Product] named in
                [Product.name][google.cloud.retail.v2.Product.name],
                regardless of whether or not it exists, a
                PERMISSION_DENIED error is returned.

                If the [Product][google.cloud.retail.v2.Product] to
                update does not have existing inventory information, the
                provided inventory information will be inserted.

                If the [Product][google.cloud.retail.v2.Product] to
                update has existing inventory information, the provided
                inventory information will be merged while respecting
                the last update time for each inventory field, using the
                provided or default value for
                [SetInventoryRequest.set_time][google.cloud.retail.v2.SetInventoryRequest.set_time].

                The last update time is recorded for the following
                inventory fields:

                -  [Product.price_info][google.cloud.retail.v2.Product.price_info]
                -  [Product.availability][google.cloud.retail.v2.Product.availability]
                -  [Product.available_quantity][google.cloud.retail.v2.Product.available_quantity]
                -  [Product.fulfillment_info][google.cloud.retail.v2.Product.fulfillment_info]

                If a full overwrite of inventory information while
                ignoring timestamps is needed, [UpdateProduct][] should
                be invoked instead.

                This corresponds to the ``inventory`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            set_mask (google.protobuf.field_mask_pb2.FieldMask):
                Indicates which inventory fields in the provided
                [Product][google.cloud.retail.v2.Product] to update. If
                not set or set with empty paths, all inventory fields
                will be updated.

                If an unsupported or unknown field is provided, an
                INVALID_ARGUMENT error is returned and the entire update
                will be ignored.

                This corresponds to the ``set_mask`` field
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

                The result type for the operation will be :class:`google.cloud.retail_v2.types.SetInventoryResponse` Response of the SetInventoryRequest. Currently empty because
                   there is no meaningful response populated from the
                   [SetInventory][] method.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([inventory, set_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a product_service.SetInventoryRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, product_service.SetInventoryRequest):
            request = product_service.SetInventoryRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if inventory is not None:
                request.inventory = inventory
            if set_mask is not None:
                request.set_mask = set_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_inventory]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("inventory.name", request.inventory.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            product_service.SetInventoryResponse,
            metadata_type=product_service.SetInventoryMetadata,
        )

        # Done; return the response.
        return response

    def add_fulfillment_places(
        self,
        request: product_service.AddFulfillmentPlacesRequest = None,
        *,
        product: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Incrementally adds place IDs to
        [Product.fulfillment_info.place_ids][google.cloud.retail.v2.FulfillmentInfo.place_ids].

        This process is asynchronous and does not require the
        [Product][google.cloud.retail.v2.Product] to exist before
        updating fulfillment information. If the request is valid, the
        update will be enqueued and processed downstream. As a
        consequence, when a response is returned, the added place IDs
        are not immediately manifested in the
        [Product][google.cloud.retail.v2.Product] queried by
        [GetProduct][google.cloud.retail.v2.ProductService.GetProduct]
        or
        [ListProducts][google.cloud.retail.v2.ProductService.ListProducts].

        This feature is only available for users who have Retail Search
        enabled. Contact Retail Support
        (retail-search-support@google.com) if you are interested in
        using Retail Search.

        Args:
            request (google.cloud.retail_v2.types.AddFulfillmentPlacesRequest):
                The request object. Request message for
                [AddFulfillmentPlaces][] method.
            product (str):
                Required. Full resource name of
                [Product][google.cloud.retail.v2.Product], such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/some_product_id``.

                If the caller does not have permission to access the
                [Product][google.cloud.retail.v2.Product], regardless of
                whether or not it exists, a PERMISSION_DENIED error is
                returned.

                This corresponds to the ``product`` field
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

                The result type for the operation will be :class:`google.cloud.retail_v2.types.AddFulfillmentPlacesResponse` Response of the RemoveFulfillmentPlacesRequest. Currently empty because
                   there is no meaningful response populated from the
                   [AddFulfillmentPlaces][] method.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([product])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a product_service.AddFulfillmentPlacesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, product_service.AddFulfillmentPlacesRequest):
            request = product_service.AddFulfillmentPlacesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if product is not None:
                request.product = product

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_fulfillment_places]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("product", request.product),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            product_service.AddFulfillmentPlacesResponse,
            metadata_type=product_service.AddFulfillmentPlacesMetadata,
        )

        # Done; return the response.
        return response

    def remove_fulfillment_places(
        self,
        request: product_service.RemoveFulfillmentPlacesRequest = None,
        *,
        product: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Incrementally removes place IDs from a
        [Product.fulfillment_info.place_ids][google.cloud.retail.v2.FulfillmentInfo.place_ids].

        This process is asynchronous and does not require the
        [Product][google.cloud.retail.v2.Product] to exist before
        updating fulfillment information. If the request is valid, the
        update will be enqueued and processed downstream. As a
        consequence, when a response is returned, the removed place IDs
        are not immediately manifested in the
        [Product][google.cloud.retail.v2.Product] queried by
        [GetProduct][google.cloud.retail.v2.ProductService.GetProduct]
        or
        [ListProducts][google.cloud.retail.v2.ProductService.ListProducts].

        This feature is only available for users who have Retail Search
        enabled. Contact Retail Support
        (retail-search-support@google.com) if you are interested in
        using Retail Search.

        Args:
            request (google.cloud.retail_v2.types.RemoveFulfillmentPlacesRequest):
                The request object. Request message for
                [RemoveFulfillmentPlaces][] method.
            product (str):
                Required. Full resource name of
                [Product][google.cloud.retail.v2.Product], such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/some_product_id``.

                If the caller does not have permission to access the
                [Product][google.cloud.retail.v2.Product], regardless of
                whether or not it exists, a PERMISSION_DENIED error is
                returned.

                This corresponds to the ``product`` field
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

                The result type for the operation will be :class:`google.cloud.retail_v2.types.RemoveFulfillmentPlacesResponse` Response of the RemoveFulfillmentPlacesRequest. Currently empty because there
                   is no meaningful response populated from the
                   [RemoveFulfillmentPlaces][] method.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([product])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a product_service.RemoveFulfillmentPlacesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, product_service.RemoveFulfillmentPlacesRequest):
            request = product_service.RemoveFulfillmentPlacesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if product is not None:
                request.product = product

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.remove_fulfillment_places
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("product", request.product),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            product_service.RemoveFulfillmentPlacesResponse,
            metadata_type=product_service.RemoveFulfillmentPlacesMetadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-retail",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ProductServiceClient",)
