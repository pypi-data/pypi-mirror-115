from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET

from typing import Dict
from ...models.record_read import RecordRead
from typing import cast
from ...models.error import Error



def _get_kwargs(
    *,
    client: Client,
    id: str,

) -> Dict[str, Any]:
    url = "{}/records/{id}/draft/actions/publish".format(
        client.base_url,id=id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Error, RecordRead]]:
    if response.status_code == 202:
        response_202 = RecordRead.from_dict(response.json())



        return response_202
    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Error, RecordRead]]:
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

) -> Response[Union[Error, RecordRead]]:
    kwargs = _get_kwargs(
        client=client,
id=id,

    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    id: str,

) -> Optional[Union[Error, RecordRead]]:
    """  """

    return sync_detailed(
        client=client,
id=id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    id: str,

) -> Response[Union[Error, RecordRead]]:
    kwargs = _get_kwargs(
        client=client,
id=id,

    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,
    id: str,

) -> Optional[Union[Error, RecordRead]]:
    """  """

    return (await asyncio_detailed(
        client=client,
id=id,

    )).parsed
