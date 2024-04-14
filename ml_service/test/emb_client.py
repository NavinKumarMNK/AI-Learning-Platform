import requests
import numpy as np

EMBEDDING_URL = "http://172.16.0.57:9999/api/v1/embedder/embed"  # Adjust if your deployment is on a different port

# Test data
test_cases = [
    {
        "type": "PASSAGE_EMBED",
        "data": [
            "Sample passage for embedding.",
            "Sample passage for embedding.",
        ],
    },
    {
        "type": "QUERY_EMBED",
        "data": [
            "A short query to embed.",
            "A short query to embed.",
        ],
    },
    {
        "type": "PLAIN_EMBED",
        "data": [
            "Some text for plain embedding.",
            "Some text for plain embedding.",
        ],
    },
]


def test_embedding_endpoint():
    import time

    for case in test_cases:
        start = time.time()
        print(case)
        response = requests.post(EMBEDDING_URL, json=case)

        assert response.status_code == 200

        data = response.json()
        embedding = np.array(data["embedding"])
        print(embedding.shape)
        print(time.time() - start)


def test_invalid_request_type():
    response = requests.post(
        EMBEDDING_URL, json={"type": "INVALID_TYPE", "data": "Text"}
    )
    assert response.status_code == 400  # Expect some bad request error


if __name__ == "__main__":
    test_embedding_endpoint()
    test_invalid_request_type()
