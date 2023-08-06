from typing import TypeAlias

from .vertexai import VertexAIEndpoint

Endpoint: TypeAlias = VertexAIEndpoint  # For future: VertexAIEndpoint | ...

__all__ = ["Endpoint", "VertexAIEndpoint"]
