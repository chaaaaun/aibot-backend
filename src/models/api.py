from typing import Union, Optional
from pydantic import BaseModel

class LLMParams(BaseModel):
    frequency_penalty: float = 0
    logit_bias: Optional[dict] = None
    logprobs: bool = False
    top_logprobs: Optional[int] = None
    max_completion_tokens: Optional[int] = None
    n: int = 1
    presence_penalty: float = 0
    seed: Optional[int] = None
    stop: Union[str, list, None] = None
    temperature: float = 1
    top_p: float = 1

class CreateConversationRequest(BaseModel):
    name: str
    params: LLMParams

class CreateConversationResponse(BaseModel):
    id: str

class ListConversationsItem(BaseModel):
    id: str
    name: str
    params: LLMParams
    tokens: int

class ListConversationsResponse(BaseModel):
    conversations: list[ListConversationsItem]    

class UpdateConversationRequest(BaseModel):
    name: str
    params: LLMParams

class ReadConversationQueryItem(BaseModel):
    role: str
    content: str

class ReadConversationResponse(BaseModel):
    id: str
    name: str
    params: LLMParams
    tokens: int
    messages: list[ReadConversationQueryItem]

class CreateQueryRequest(BaseModel):
    role: str
    content: str

class CreateQueryResponse(BaseModel):
    id: str

class ApiErrorResponse(BaseModel):
    code: int
    message: str
    request: dict = None
    details: dict = None