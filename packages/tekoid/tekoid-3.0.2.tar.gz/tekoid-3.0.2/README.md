# Identity Client Library Python

## How to install

- use pip:
  ```py
  pip install tekoid
  ```

## How to use

- First, import `ClientSDK` into your sourcecode. I.E:

```py
from tekoid import ClientSDK
```

- Second, you need to instantiate ClientSDK. See example:

```py
clientSDK = ClientSDK(client_id=os.getenv("CLIENT_ID"),
                      client_secret=os.getenv("CLIENT_SECRET"),
                      redirect_uri="http://localhost:5000/callback")
```

Note: `redirect_uri` must be declare in iam admin system

| addition field     | type    | default                    |
| ------------------ | ------- | -------------------------- |
| scope              | array   | [openid,profile]           |
| base_uri           | string  | https://oauth.tekoapis.com |
| authorize_path     | string  | /oauth/authorize           |
| token_path         | string  | /oauth/token               |
| refresh_token_path | string  | /oauth/token               |
| revoke_token_path  | string  | /oauth/revoke              |
| jwks_path          | string  | /.well-known/jwks.json     |
| userinfo_path      | string  | /userinfo                  |
| verify_ssl         | boolean | True                       |

- Support function:

  - get_authorization_url():

    - return url, state, nonce, code_verifier

  - get_token(self, url, state, nonce=None, code_verifier=None):

    - use for authorization code flow, pass url get from authorization server and state get above
    - code_verifier is not require, use only for public client
    - nonce is not require, use only when client require openid scope
    - return token data

  - get_token():

    - use for client credentials flow
    - return token data

  - get_user_info(token):

    - pass id_token get from get_token()
    - return user data through decode id_token

  - refresh_token(refresh_token):

    - pass refresh token get from get_token()
    - return new token data

  - get_full_user_info(access_token):

    - pass access token get from get_token()
    - return user data through call api

- you can see the sample code at
  https://git.teko.vn/user-profile/iam/tekoid-py/-/blob/master/example/app.py

## Support

- vietnk: viet.nk@teko.vn
