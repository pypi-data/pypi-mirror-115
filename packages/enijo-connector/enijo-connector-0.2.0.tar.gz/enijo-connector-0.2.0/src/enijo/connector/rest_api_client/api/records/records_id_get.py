from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET

from typing import Dict
from ...models.record_read import RecordRead
from typing import cast



def _get_kwargs(
    *,
    client: Client,
    id: str,

) -> Dict[str, Any]:
    url = "{}/records/{id}".format(
        client.base_url,id=id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[RecordRead]:
    if response.status_code == 200:
        response_200 = RecordRead.from_dict(response.json())



        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[RecordRead]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    id: str,

) -> Response[RecordRead]:
    kwargs = _get_kwargs(
        client=client,
id=id,

    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    id: str,

) -> Optional[RecordRead]:
    """  """

    return sync_detailed(
        client=client,
id=id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    id: str,

) -> Response[RecordRead]:
    kwargs = _get_kwargs(
        client=client,
id=id,

    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,
    id: str,

) -> Optional[RecordRead]:
    """  """

    return (await asyncio_detailed(
        client=client,
id=id,

    )).parsed
