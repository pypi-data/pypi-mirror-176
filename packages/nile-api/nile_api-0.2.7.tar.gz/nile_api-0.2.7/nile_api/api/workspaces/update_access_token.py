from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.access_token_info import AccessTokenInfo
from ...models.create_access_token_request import CreateAccessTokenRequest
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    workspace: str,
    id: str,
    *,
    client: Client,
    json_body: CreateAccessTokenRequest,
) -> Dict[str, Any]:
    url = "{}/workspaces/{workspace}/access_tokens/{id}".format(
        client.base_url, workspace=workspace, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[AccessTokenInfo, Error]]:
    if response.status_code == 200:
        response_200 = AccessTokenInfo.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401
    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[AccessTokenInfo, Error]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    workspace: str,
    id: str,
    *,
    client: Client,
    json_body: CreateAccessTokenRequest,
) -> Response[Union[AccessTokenInfo, Error]]:
    """Update an access token

     Update a workspace access token.

    Args:
        workspace (str):
        id (str):
        json_body (CreateAccessTokenRequest):

    Returns:
        Response[Union[AccessTokenInfo, Error]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    workspace: str,
    id: str,
    *,
    client: Client,
    json_body: CreateAccessTokenRequest,
) -> Optional[Union[AccessTokenInfo, Error]]:
    """Update an access token

     Update a workspace access token.

    Args:
        workspace (str):
        id (str):
        json_body (CreateAccessTokenRequest):

    Returns:
        Response[Union[AccessTokenInfo, Error]]
    """

    return sync_detailed(
        workspace=workspace,
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    id: str,
    *,
    client: Client,
    json_body: CreateAccessTokenRequest,
) -> Response[Union[AccessTokenInfo, Error]]:
    """Update an access token

     Update a workspace access token.

    Args:
        workspace (str):
        id (str):
        json_body (CreateAccessTokenRequest):

    Returns:
        Response[Union[AccessTokenInfo, Error]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    workspace: str,
    id: str,
    *,
    client: Client,
    json_body: CreateAccessTokenRequest,
) -> Optional[Union[AccessTokenInfo, Error]]:
    """Update an access token

     Update a workspace access token.

    Args:
        workspace (str):
        id (str):
        json_body (CreateAccessTokenRequest):

    Returns:
        Response[Union[AccessTokenInfo, Error]]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
