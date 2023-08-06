
## Description

Secure settings in json file

# install
```
  pip install secure-json
```

#### import

```python
from secure_json import Settings
```

#### Description
```text
The library allows you to encrypt your settings stored in json format.
It is possible to convert from a simple storage option to an encrypted one. 
To work with the encrypted version of the settings, you need to pass the startup parameter - the password with which the encryption took place.
Try it, the library is very simple.
```


#### Usage
# Import lib
```python
  settings = Settings('Settings.json').data

  path_to_repo = settings.repo.path
  user = settings.repo.user
  pass = settings.repo.password
  base_name = settings.base_name
```

#### Encoding\Decoding

```http
encoding settings:
    python main.py <password> encode
	
decoding settings:
	python main.py <password> decode

help:
	python main.py help
```
