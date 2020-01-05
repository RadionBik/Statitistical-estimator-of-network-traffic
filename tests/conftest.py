import pytest
import stat_estimator as estimator
import settings
from collections import defaultdict
import numpy as np

import traffic_helpers


@pytest.fixture
def traffic_dict():
    pcapfile = f'{settings.BASE_DIR}/traffic_dumps/skypeLANhome.pcap'
    return estimator.getTrafficFeatures(pcapfile,
                                        type_of_identifier=traffic_helpers.TrafficObjects.FLOW,
                                        percentiles=(1, 99),
                                        min_samples_to_estimate=100)[0]


@pytest.fixture
def gmm_states():
    states = defaultdict(dict)
    states['UDP 192.168.0.102:18826 192.168.0.105:26454'] = {'from': np.random.randint(0, 16, 3547),
                                                             'to': np.random.randint(0, 16, 3625)}
    return states
