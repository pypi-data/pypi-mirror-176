from dataclasses import dataclass, field
from typing import Optional
from sdk.models import shared


@dataclass
class GenerateOpenAPISpecForAPIEndpointPathParams:api_endpoint_id: str = field(default=None, metadata={'path_param': { 'field_name': 'apiEndpointID', 'style': 'simple', 'explode': False }})
    api_id: str = field(default=None, metadata={'path_param': { 'field_name': 'apiID', 'style': 'simple', 'explode': False }})
    version_id: str = field(default=None, metadata={'path_param': { 'field_name': 'versionID', 'style': 'simple', 'explode': False }})
    

@dataclass
class GenerateOpenAPISpecForAPIEndpointRequest:path_params: GenerateOpenAPISpecForAPIEndpointPathParams = field(default=None)
    

@dataclass
class GenerateOpenAPISpecForAPIEndpointResponse:content_type: str = field(default=None)
    error: Optional[shared.Error] = field(default=None)
    generate_open_api_spec_diff: Optional[shared.GenerateOpenAPISpecDiff] = field(default=None)
    status_code: int = field(default=None)
    
