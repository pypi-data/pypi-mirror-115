import jwt
import json
from .base_client_sdk import BaseClientSDK
from .errors import StateInvalidException, NonceInvalidException
from .utils import create_sha256_code_challenge, get_dict_from_url, get_url_encode_from_dict, get_random_string


class CodeClientSDK(BaseClientSDK):
    def __init__(self, client_id, client_secret, redirect_uri, **kwargs):
        super().__init__(client_id, client_secret, **kwargs)

        self.redirect_uri = redirect_uri

    def __get_public_keys(self):
        jwks = self.client.get(self.jwks_uri).json()
        public_keys = {}
        for jwk in jwks.get('keys'):
            kid = jwk['kid']
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

        self.public_keys = public_keys

    def get_authorization_url(self):
        state = get_random_string()
        nonce = get_random_string()
        code_verifier = get_random_string()

        query_dict = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(self.scope),
            'state': state,
            'nonce': nonce
        }

        if self.is_public_client():
            query_dict['code_challenge'] = create_sha256_code_challenge(code_verifier)
            query_dict['code_challenge_method'] = 'S256'

        query = get_url_encode_from_dict(query_dict)
        authorization_url = f'{self.authorize_uri}?{query}'
        return authorization_url, state, nonce, code_verifier

    def get_token(self, url, state, nonce=None, code_verifier=None):
        params = get_dict_from_url(url)
        req_state = params['state'][0]
        code = params['code'][0]
        if (state != req_state):
            raise StateInvalidException()

        body = {
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code',
            'code': code
        }

        if code_verifier is not None:
            body['code_verifier'] = code_verifier
            body['client_id'] = self.client_id
            res = self.client.post(self.token_uri, data=body)
        else:
            res = self.client.post(self.token_uri, data=body, auth=(self.client_id, self.client_secret))

        data = res.json()

        if 'id_token' in data:
            id_token = data['id_token']
            nonce_token = jwt.decode(id_token, verify=False, algorithms=['RS256']).get('nonce')

            if nonce != nonce_token:
                raise NonceInvalidException(f'invalid nonce = {nonce}')

        return res.json(), res.status_code

    def __decode_token(self, token):
        kid = jwt.get_unverified_header(token).get('kid')
        aud = jwt.decode(token, verify=False, algorithms=['RS256']).get('aud')

        if not hasattr(self, 'public_keys') or kid not in self.public_keys:
            self.__get_public_keys()

        pubkey = self.public_keys.get(kid)
        payload = jwt.decode(token, key=pubkey, algorithms=['RS256'], audience=aud)

        return payload

    def get_user_info(self, token):
        return self.__decode_token(token)

    def refresh_token(self, refresh_token):
        body = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'scope': ' '.join(self.scope),
        }

        if self.is_public_client():
            body['client_id'] = self.client_id
            res = self.client.post(self.refresh_token_uri, data=body)
        else:
            res = self.client.post(self.refresh_token_uri, data=body, auth=(self.client_id, self.client_secret))

        return res.json(), res.status_code
