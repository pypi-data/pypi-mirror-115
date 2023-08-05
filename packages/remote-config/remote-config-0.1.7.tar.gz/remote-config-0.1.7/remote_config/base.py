import time
import json
from datetime import datetime, timedelta

from remote_config.validator import validate_feature, validate_cluster, validate_global

from consul import Consul
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger


FEATURE_TOGGLE_PATH = 'general/feature-toggle'
CLUSTER_PATH = 'general/clusters'
GLOBAL_PATH = 'general/globals'


class Singleton(type):
    _instances = dict()
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = \
                super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RemoteConfig():
    __metaclass__ = Singleton

    def __init__(self,
                 host='127.0.0.1',
                 port=8500,
                 token=None,
                 toggle_path=FEATURE_TOGGLE_PATH,
                 cluster_path=CLUSTER_PATH,
                 global_path=GLOBAL_PATH,
                 feature_minute=5,
                 cluster_minute=50,
                 global_minute=30):
        self.consul = Consul(host, port, token)
        self.cluster_path = cluster_path
        self.toggle_path = toggle_path
        self.global_path = global_path
        self.features = dict()
        self.clusters = dict()
        self.globals = dict()
        self.feature_minute = feature_minute
        self.cluster_minute = cluster_minute
        self.global_minute = global_minute
        self.sched = None
        self.cluster_job_id = None
        self.feature_job_id = None
        self.global_job_id = None

    def start(self, start_sched=True):
        if self.sched:
            self.stop()
        job_time = str(time.time)
        self.cluster_job_id = 'cluster_{}'.format(job_time)
        self.feature_job_id = 'feature_{}'.format(job_time)
        self.global_job_id = 'global_{}'.format(job_time)
        self.sched = BackgroundScheduler(daemon=True)
        feature_trigger = OrTrigger(
            [DateTrigger(datetime.now() + timedelta(seconds=10)),
             IntervalTrigger(minutes=self.feature_minute)])
        cluster_trigger = OrTrigger(
            [DateTrigger(),
             IntervalTrigger(minutes=self.cluster_minute)])
        global_trigger = OrTrigger(
            [DateTrigger(),
             IntervalTrigger(minutes=self.global_minute)]
        )
        self.sched.add_job(self._load_features, feature_trigger,
                           id=self.feature_job_id)
        self.sched.add_job(self._load_clusters, cluster_trigger,
                           id=self.cluster_job_id)
        self.sched.add_job(self._load_globals, global_trigger,
                           id=self.global_job_id)
        self.sched.start()

    def stop(self):
        self.sched.remove_all_jobs()

    def _get_value(self, key):
        return json.loads(self.consul.kv.get(key)[1]['Value'])

    def _list_folders(self, path):
        return self.consul.kv.get(path, keys=True)[1][1:]

    def _load_features(self):
        list_feature = self._list_folders(self.toggle_path)

        for feature in list_feature:
            feature_name = feature[len(self.toggle_path) + 1:]
            feature_data = self._get_value(feature)
            validate_feature(feature_data)
            stores = set()
            for cluster in feature_data['clusters']:
                cluster_name = cluster[len(self.cluster_path) + 1:]
                stores.update(self.clusters[cluster_name]['ids'])
            self.features[feature_name] = feature_data
            self.features[feature_name]['stores'] = stores

    def _load_clusters(self):
        self.clusters = dict()
        list_cluster = self._list_folders(self.cluster_path)
        for cluster in list_cluster:
            cluster_name = cluster[len(self.cluster_path) + 1:]
            cluster_data = self._get_value(cluster)
            validate_cluster(cluster_data)
            self.clusters[cluster_name] = cluster_data

        for feature_name in self.features:
            stores = set()
            for cluster in self.features[feature_name]['clusters']:
                cluster_name = cluster[len(self.cluster_path) + 1:]
                stores.update(self.clusters[cluster_name]['ids'])
            self.features[feature_name]['stores'] = stores
    
    def _load_globals(self):
        self.globals = dict()
        list_global = self._list_folders(self.global_path)
        
        for global_config in list_global:
            global_name = global_config[len(self.global_path) + 1:]
            global_data = self._get_value(global_config)
            validate_global(global_data)
            self.globals[global_name] = global_data

    
    def get_feature(self, feature_name, store_id):
        try:
            feat = self.features[feature_name]
            if not feat['enable']:
                return False
            enabled = store_id in self.features[feature_name]['stores']
            return enabled or feat['default']
        except KeyError:
            return False
    
    def get_global(self, global_name):
        try:
            return self.globals[global_name]
        except KeyError:
            return None
