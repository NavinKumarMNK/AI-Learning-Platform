import requests
import numpy as np

EMBEDDING_URL = "http://172.16.0.57:8000/api/v1/embedder/embed"  # Adjust if your deployment is on a different port

# Test data
test_cases = [
    {
        "type": "PASSAGE_EMBED",
        "data": "Sample passage for embedding.",
        "expected_shape": (1024,),  # Hypothetical embedding dimension, adjust as needed
    },
    {
        "type": "QUERY_EMBED",
        "data": "A short query to embed.",
        "expected_shape": (1024,),
    },
    {
        "type": "PLAIN_EMBED",
        "data": "Some text for plain embedding.",
        "expected_shape": (1024,),
    },
]


def test_embedding_endpoint():
    for case in test_cases:
        response = requests.post(EMBEDDING_URL, params=case)

        assert response.status_code == 200

        data = response.json()
        embedding = np.array(data["embedding"])
        assert embedding.shape == case["expected_shape"]


def test_invalid_request_type():
    response = requests.post(
        EMBEDDING_URL, params={"type": "INVALID_TYPE", "data": "Text"}
    )
    assert response.status_code == 400  # Expect some bad request error
