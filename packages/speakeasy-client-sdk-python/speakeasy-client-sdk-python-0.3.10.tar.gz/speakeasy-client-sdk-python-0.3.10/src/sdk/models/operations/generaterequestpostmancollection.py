from dataclasses import dataclass, field
from typing import Optional
from sdk.models import shared


@dataclass
class GenerateRequestPostmanCollectionPathParams:request_id: str = field(default=None, metadata={'path_param': { 'field_name': 'requestID', 'style': 'simple', 'explode': False }})
    

@dataclass
class GenerateRequestPostmanCollectionRequest:path_params: GenerateRequestPostmanCollectionPathParams = field(default=None)
    

@dataclass
class GenerateRequestPostmanCollectionResponse:content_type: str = field(default=None)
    error: Optional[shared.Error] = field(default=None)
    postman_collection: Optional[bytes] = field(default=None)
    status_code: int = field(default=None)
    
