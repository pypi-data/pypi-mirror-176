from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.create_entity_request import CreateEntityRequest
from ...models.entity import Entity
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    client: Client,
    json_body: CreateEntityRequest,
) -> Dict[str, Any]:
    url = "{}/workspaces/{workspace}/entities".format(
        client.base_url, workspace=workspace
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Entity]:
    if response.status_code == 200:
        response_200 = Entity.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Entity]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Client,
    json_body: CreateEntityRequest,
) -> Response[Entity]:
    """Create an entity

    Args:
        workspace (str):
        json_body (CreateEntityRequest):

    Returns:
        Response[Entity]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
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
    *,
    client: Client,
    json_body: CreateEntityRequest,
) -> Optional[Entity]:
    """Create an entity

    Args:
        workspace (str):
        json_body (CreateEntityRequest):

    Returns:
        Response[Entity]
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Client,
    json_body: CreateEntityRequest,
) -> Response[Entity]:
    """Create an entity

    Args:
        workspace (str):
        json_body (CreateEntityRequest):

    Returns:
        Response[Entity]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    workspace: str,
    *,
    client: Client,
    json_body: CreateEntityRequest,
) -> Optional[Entity]:
    """Create an entity

    Args:
        workspace (str):
        json_body (CreateEntityRequest):

    Returns:
        Response[Entity]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            json_body=json_body,
        )
    ).parsed
