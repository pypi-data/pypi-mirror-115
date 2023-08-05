from remote_config.base import RemoteConfig

from jsonschema.exceptions import ValidationError
import mock_data as mock
import pytest


def test_feature_disable():
    RemoteConfig().features = {
        u'google-merchant': {
            u'default': False,
            u'enable': False,
            'stores': set()
        }
    }
    assert RemoteConfig().get_feature('google-merchant', 0) == False

def test_feature_in_cluster():
    RemoteConfig().features = {
        u'google-merchant': {
            u'default': False,
            u'enable': True,
            'stores': set([456, 123])
        }
    }
    assert RemoteConfig().get_feature('google-merchant', 123) == True

def test_feature_default_false():
    RemoteConfig().features = {
        u'google-merchant': {
            u'default': False,
            u'enable': True,
            'stores': set([456])
        }
    }
    assert RemoteConfig().get_feature('google-merchant', 123) == False

def test_feature_default_true():
    RemoteConfig().features = {
        u'google-merchant': {
            u'default': True,
            u'enable': True,
            u'clusters': [u'general/clusters/cluster-google-merchant'],
            'stores': set([456])
        }
    }
    assert RemoteConfig().get_feature('google-merchant', 123) == True

def test_feature_not_exist():
    assert RemoteConfig().get_feature('feature-not-exist', 123) == False

def test_invalid_cluster_consumer():
    RemoteConfig().clusters = None
    RemoteConfig._list_folders = mock.cluster_list
    RemoteConfig._get_value = mock.invalid_cluster_data
    with pytest.raises(ValidationError):
        RemoteConfig()._load_clusters()

def test_invalid_feature_consumer():
    RemoteConfig().clusters = None
    RemoteConfig._list_folders = mock.cluster_list
    RemoteConfig._get_value = mock.cluster_data
    RemoteConfig()._load_clusters()
    RemoteConfig._list_folders = mock.feature_list
    RemoteConfig._get_value = mock.invalid_feature_data
    with pytest.raises(ValidationError):
        RemoteConfig()._load_features()

def test_cluster_feature_consumer():
    rc = RemoteConfig()
    rc.clusters = None
    RemoteConfig._list_folders = mock.cluster_list
    RemoteConfig._get_value = mock.cluster_data
    rc._load_clusters()
    RemoteConfig._list_folders = mock.feature_list
    RemoteConfig._get_value = mock.feature_data
    rc._load_features()
    assert rc.get_feature('google-merchant', 123) == True

def test_cluster_feature_update_cache():
    rc = RemoteConfig()
    RemoteConfig._list_folders = mock.cache_init_list
    RemoteConfig._get_value = mock.cache_init_data
    rc._load_clusters()
    assert rc.get_feature('google-merchant', 124) == False
    RemoteConfig._list_folders = mock.cache_init_list
    RemoteConfig._get_value = mock.cache_update_cluster_data
    rc._load_clusters()
    assert rc.get_feature('google-merchant', 124) == True

def test_cluster_feature_cluster_update_cache():
    rc = RemoteConfig()
    RemoteConfig._list_folders = mock.cache_init_list
    RemoteConfig._get_value = mock.cache_init_data
    rc._load_clusters()
    rc._load_features()
    assert rc.get_feature('google-merchant', 123) == True
    RemoteConfig._list_folders = mock.cache_init_list
    RemoteConfig._get_value = mock.cache_update_cluster_data
    rc._load_clusters()
    rc._load_features()
    assert rc.get_feature('google-merchant', 123) == False

def test_missing_global():
    RemoteConfig().globals = {}
    assert RemoteConfig().get_global('test-global') is None

def test_valid_global():
    RemoteConfig().globals = {}
    RemoteConfig._list_folders = mock.global_list
    RemoteConfig._get_value = mock.global_data

    RemoteConfig()._load_globals()
    assert RemoteConfig().get_global('test-global') == {'some': 'random', 'test': 'values'}

def test_invalid_global():
    RemoteConfig().globals = {}
    RemoteConfig._list_folders = mock.global_list
    RemoteConfig._get_value = mock.invalid_global_data
    with pytest.raises(ValidationError):
        RemoteConfig()._load_globals()