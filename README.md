# Flask-Config-Override

An alternate implementation of the config object for flask which support overriding subkeys and using yaml.  It is intended to be a drop in replacement.

## Example Usage

`base.yaml`:

```yaml
topkey:
  subkey:
    key: value
tooverride:
  subkey:
    config_value: overrideme
```

`override.yaml`:

```yaml
tooverride:
  subkey:
    config_value: overridden
  newkey: newvalue
```

```python
from flask import Flask
from flask_config_override import Config

new_app = Flask(__name__)

# Optional: intitialize with default settings
cfg = parser.Config(app.config)

# Replace the built in config object
app.config = cfg

# Override the defaults with our first config file
cfg.override('base.yaml')

# Keys accessible by nested path
cfg['topkey/subkey/key']  # value

# Sub objects accessible by path
cfg['topkey/subkey']  # {'key': 'value'}

# Override with additional config files
cfg['tooverride/subkey/config_value']  # overrideme
cfg.override('override.yaml')
cfg['tooverride/subkey/config_value']  # overridden

```