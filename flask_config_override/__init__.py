import yaml
import logging

from collections import defaultdict, MutableMapping


logger = logging.getLogger(__name__)


class _Subtree(object):
    def __init__(self):
        self._config_tree = defaultdict(_Subtree)

    def __getitem__(self, key_path):
        first_slash = key_path.find('/')
        if first_slash >= 0:
            our_key = key_path[:first_slash]
            try:
                return self._config_tree[our_key][key_path[first_slash+1:]]
            except KeyError:
                raise KeyError(key_path)
        else:
            if key_path in self._config_tree:
                return self._config_tree[key_path]
            raise KeyError(key_path)

    def __setitem__(self, key_path, value):
        first_slash = key_path.find('/')
        if first_slash >= 0:
            our_key = key_path[:first_slash]
            self._config_tree[our_key][key_path[first_slash+1:]] = value
        else:
            self._config_tree[key_path] = value

    def __delitem__(self, key_path):
        first_slash = key_path.find('/')
        if first_slash >= 0:
            our_key = key_path[:first_slash]
            del self._config_tree[our_key][key_path[first_slash+1:]]
        else:
            del self._config_tree[key_path]

    def __iter__(self):
        def item_gen():
            for key, value in self._config_tree.items():
                if isinstance(value, _Subtree):
                    for subkey_path in value:
                        yield "/".join([key, subkey_path])
                else:
                    yield key
        return iter(item_gen())

    def setdefault(self, key_path, value):
        if key_path not in self.keys():
            self[key_path] = value

    def get(self, key_path, default_value=None):
        if key_path in self:
            return self[key_path]
        return default_value

    def keys(self):
        return self._config_tree.keys()

    def items(self):
        return self._config_tree.items()

    def iteritems(self):
        for key, value in self._config_tree.iteritems():
            yield key, value



class Config(_Subtree):
    def __init__(self, default_config=None):
        super(Config, self).__init__()
        if default_config is not None:
            self._apply(self._config_tree, default_config)

    def override(self, config_filename):
        logger.debug('Applying config: %s', config_filename)
        with open(config_filename, 'r') as stream:
            loaded = yaml.load(stream)
            self._apply(self._config_tree, loaded)

    @staticmethod
    def _apply(config_obj, new_config):
        for key, value in new_config.items():
            if isinstance(value, MutableMapping):
                Config._apply(config_obj[key], value)
            else:
                config_obj[key] = value
