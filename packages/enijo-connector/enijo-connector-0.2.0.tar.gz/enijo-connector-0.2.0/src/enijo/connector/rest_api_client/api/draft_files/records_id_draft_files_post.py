from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET

from typing import cast
from typing import cast, List
from ...models.draft_files_read import DraftFilesRead
from ...models.draft_files_create_item import DraftFilesCreateItem
from typing import Dict



def _get_kwargs(
    *,
    client: Client,
    id: str,
    json_body: List[DraftFilesCreateItem],

) -> Dict[str, Any]:
    url = "{}/records/{id}/draft/files".format(
        client.base_url,id=id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    json_json_body = []
    for componentsschemas_draft_files_create_item_data in json_body:
        componentsschemas_draft_files_create_item = componentsschemas_draft_files_create_item_data.to_dict()

        json_json_body.append(componentsschemas_draft_files_create_item)






    

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[DraftFilesRead]:
    if response.status_code == 201:
        response_201 = DraftFilesRead.from_dict(response.json())



        return response_201
    return None


def _build_response(*, response: httpx.Response) -> Response[DraftFilesRead]:
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
    json_body: List[DraftFilesCreateItem],

) -> Response[DraftFilesRead]:
    kwargs = _get_kwargs(
        client=client,
id=id,
json_body=json_body,

    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    id: str,
    json_body: List[DraftFilesCreateItem],

) -> Optional[DraftFilesRead]:
    """  """

    return sync_detailed(
        client=client,
id=id,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    id: str,
    json_body: List[DraftFilesCreateItem],

) -> Response[DraftFilesRead]:
    kwargs = _get_kwargs(
        client=client,
id=id,
json_body=json_body,

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
    json_body: List[DraftFilesCreateItem],

) -> Optional[DraftFilesRead]:
    """  """

    return (await asyncio_detailed(
        client=client,
id=id,
json_body=json_body,

    )).parsed
