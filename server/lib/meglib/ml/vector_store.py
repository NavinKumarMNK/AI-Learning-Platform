import qdrant_client
from typing import Dict


class QdrantDB:
    def __init__(self, config: Dict):
        self.client = qdrant_client()
