# rocket_token

rocket_token is a simple Python package that allows:

1. Encrypting/Decrypt a dictionary.
2. Generating an encrypted token to be sent to the Adzooma API.


# Installing rocket_token And Supported Versions
rocket_token is available on PyPI:
```console
$ pip install rocket_token
```

rocket_token officially supports Python 3.8+.

# Encrypting/Decrypting A Dictionary
Encrypting a dictionary is accomplished using the `encrypt_dictionary` method of RocketToken.
```python
import os

from rocket_token import RocketToken

my_dictionary = {"one": 1, "two": [], "three": {"sub1": 1, "sub2": 2}}

# Generate Private and Public key files in a directory called 'keys'
RocketToken.generate_key_pair(path="keys")

# Instantiate RocketToken object with private and public keys loaded
rocket = RocketToken.rocket_token_from_path(private_path=os.path.join("keys", "id_rsa"),
                                    public_path=os.path.join("keys", "id_rsa.pub"))

# Generate an encrypted token
token = rocket.generate_web_token(my_dictionary)

# Decode token
token_dict = rocket.decode_token(token)

print(token)
"Bearer kgYEkR9t57Jx/xcWwkTP03Y...7Wy3jzkdmVUea7dVO/fC5="
print(token_dict)
{'one': 1, 'two': [], 'three': {'sub1': 1, 'sub2': 2}}
```

# Generating An API Token
Encrypting a dictionary is accomplished using the `generate_web_token` method of RocketToken.

Required keyword arguments are:

    1. path: (str) Path to the requested resource.
    2. exp: (int) Expiry time of request in minutes.
    3. method: (str) A valid HTTP request method.

Followed by an arbitrary number of keyword arguments.

```python
import os

from rocket_token import RocketToken

# Generate Private and Public key files in a directory called 'keys'
RocketToken.generate_key_pair(path="keys")

# Instantiate RocketToken object with private and public keys loaded
rocket = RocketToken.rocket_token_from_path(private_path=os.path.join("keys", "id_rsa"),
                                    public_path=os.path.join("keys", "id_rsa.pub"))

# Generate an encrypted token
token = rocket.generate_web_token(path="/reports/campaign",
                         exp=10, 
                         method="GET", 
                         customer_id=3)

# Decode token
token_dict = rocket.decode_token(token)

print(token)
"Bearer kgYEkR9t57Jx/xcWwkTP03Y...7Wy3jzkdmVUea7dVO/fC5="
print(token_dict)
{'path': '/reports/campaign', 'expiry': 10, 'expiry_date': '2021-06-25T10:02:36.556318', 'method': 'GET', 'customer_id': 3}
```

# Command Line Interface
The above functionality can also be accessed through a command line interface.

## CLI: Generate Public And Private Key Files
```console
>>> rt_new_keys keys
Key-pair saved to `keys`
```

## CLI: Generate A Token
```
>>> rt_web_token C:\Users\kmpla\Documents\dev\adzooma\rocket_token\keys\id_rsa.pub /campaign post 15
Token: Bearer Eb1L8xc5cUMXV52PCXX7woFRtSZXORHSp2ncd1M...7Usx0Q1m3RijNa7k=
```

## Developer Mode
Users can put the rocket token library into developer mode by setting the environment variable `ROCKET_DEVELOPER_MODE` equal to `true`. In developer mode the RocketTokens library uses hard-coded public and private key's to remove the need to store key files locally or modify the environment during development. THIS VAR SHOULD NEVER BE SET IN PRODUCTION.

### Developer Mode - CLI
The CLI also comes with a command to support developer mode so no keyfile has to be specified to generate a web token.
```
rt_dev_web_token /campaign POST 15 -p customer_id=5
```

## Unit testing and coverage
To run unit tests users must have pytest installled and have cloned the repository from the repo. Once installed the command `pytest` can be ran from the root directory of the project to run all unit tests.

### Checking Coverage
To check the unit test coverage users must have pytest and coverage installed and have cloned the repository from the repo. Once they're installed you can check the coverage by running `coverage run --source=./src -m pytest`. The results can then be seen by running `coverage report`

### Using cover-gutters
Cover-gutters is a vs-code extension that allows you to see your line level coverage for your code. In order to use this you need `pytest` and `pytest-cov` installed. You can then generate the coverage file required for it to work by running `pytest ./tests --cov-report xml:cov.xml --cov ./src/rocket_token` from the root of the project. To view the coverage in your source code you can then press `Ctrl + Shift + 7`.

### Uploading the package
1. python -m pip install --upgrade twine
2. python -m pip install --upgrade build
3. python -m build
4. Check your package contains the expected files: tar tzf dist/rocket_token-2.0.0.tar.gz
Use twine to check package description will render correctly on PyPI: twine check dist/*
5. twine upload dist/*

### Converting a key into a string
`base64.b64encode(key_string.encode('utf-8')).decode("utf-8")`