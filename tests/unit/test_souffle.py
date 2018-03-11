"""Test module for souffle package."""

import pytest
from souffle.util import (
    extract_bearer_token,
    extract_bearer_token_from_api_event,
    generate_api_gateway_response
)

class TestExtractBearerToken(object):
    """Tests for souffle.util.extract_bearer_token"""

    def test_valid_bearer_token(self):
        """A valid bearer token"""

        # Given
        auth_header = 'Bearer MY_TOKEN'

        # When
        bearer_token = extract_bearer_token(auth_header)

        # Then
        assert bearer_token == "MY_TOKEN"

    def test_empty_bearer_token(self):
        """An empty bearer token. Should return None"""

        # Given
        auth_header = 'Bearer '

        # When
        bearer_token = extract_bearer_token(auth_header)

        # Then
        assert bearer_token is None

    def test_empty_string(self):
        """An emtpy string. Should return None"""

        # Given
        auth_header = ''

        # When
        bearer_token = extract_bearer_token(auth_header)

        # Then
        assert bearer_token is None

    def test_missing_bearer_prefix(self):
        """A token with no 'Bearer ' prefix. Should return None"""

        # Given
        auth_header = 'MY_TOKEN'

        # When
        bearer_token = extract_bearer_token(auth_header)

        # Then
        assert bearer_token is None

    def test_two_tokens(self):
        """A Bearer token with two tokens. Should return None"""

        # Given
        auth_header = 'Bearer MY_TOKEN MY_OTHER_TOKEN'

        # When
        bearer_token = extract_bearer_token(auth_header)

        # Then
        assert bearer_token is None


class TestExtractBearerTokenFromApiEvent(object):
    """Tests for souffle.util.extract_bearer_token_from_api_event"""

    def test_valid_event(self):
        """Valid event with valid ['headers']['Authorization']"""

        # Given
        event = {
            'headers': {
                'Authorization': 'Bearer MY_TOKEN'
            }
        }

        # When
        bearer_token = extract_bearer_token_from_api_event(event)

        # Then
        assert bearer_token == 'MY_TOKEN'


    def test_missing_headers(self):
        """Event has no 'headers' key. Should raise LookupError"""

        # Given
        event = {
            'resource': '/'
        }

        # When / Then
        with pytest.raises(LookupError):
            extract_bearer_token_from_api_event(event)


    def test_headers_is_none(self):
        """Event has headers key but it is None. Should raise LookupError.
        (Not sure if this could happen but I've seen it with other event fields.)
        """

        # Given
        event = {
            'resource': '/',
            'headers': None
        }

        # When / Then
        with pytest.raises(LookupError):
            extract_bearer_token_from_api_event(event)


    def test_missing_authorization(self):
        """Event has headers but does not have 'Authorization' header. Should raise LookupError"""

        # Given
        event = {
            'resource': '/',
            'headers': {
                'Accept': 'text/html'
            }
        }

        # When / Then
        with pytest.raises(LookupError):
            extract_bearer_token_from_api_event(event)

    def test_invalid_bearer_token(self):
        """Event has headers but does not have 'Authorization' header. Should raise LookupError"""

        # Given
        event = {
            'resource': '/',
            'headers': {
                'Authorization': 'MY_TOKEN'
            }
        }

        # When / Then
        with pytest.raises(LookupError):
            extract_bearer_token_from_api_event(event)


class TestGenerateApiGatewayResponse(object):
    """Tests for souffle.util.generate_api_gateway_response"""

    def test_no_kwargs(self):
        """No kwargs. Should just return statuscode."""

        # Given / When
        response = generate_api_gateway_response(401)

        # Then
        expected_response = {'statusCode': 401}
        assert response == expected_response


    def test_scalar_body_kwargs(self):
        """Body fields are all scalar fields. Should return valid gateway response."""

        # Given / When
        response = generate_api_gateway_response(
            200,
            foo='foo_value',
            bar='bar_value',
            number=1337,
            flag=True,
            empty=None
        )

        # Then
        expected_response = {
            'statusCode': 200,
            'body': '{"foo": "foo_value", "bar": "bar_value", "number": 1337, "flag": true, "empty": null}'
        }
        assert response == expected_response


    def test_complex_body_kwargs(self):
        """Body fields are all scalar fields. Should return valid gateway response."""

        # Given / When
        response = generate_api_gateway_response(
            200,
            foo=['f', 'o', 'o'],
            bar={'type': 'law exam'}
        )

        # Then
        expected_response = {
            'statusCode': 200,
            'body': '{"foo": ["f", "o", "o"], "bar": {"type": "law exam"}}'
        }
        assert response == expected_response
