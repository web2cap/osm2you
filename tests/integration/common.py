def check_response(response, expected_code, required_fields):
    """Check that response hasn't 404 code, that response has expected code.
    Check that response data have required fields."""

    assert hasattr(response, "request") and response.request.get(
        "PATH_INFO"
    ), "Response has wrong format"
    url = response.request["PATH_INFO"]

    assert (
        response.status_code != 404 or expected_code == 404
    ), f"Page `{url}` not found, check this address in *urls.py*"

    assert response.status_code == expected_code, (
        f"Check that request `{url}` with valid data "
        f"has status code {expected_code} in response. "
        f"Now code is {response.status_code}. Response data: {response.data}"
    )

    response_json = response.json()
    for field in required_fields:
        assert field in response_json.keys() and len(response_json[field]), (
            f"Check that request `{url}` with valid data"
            f" in the response there is a filled {field}."
        )
