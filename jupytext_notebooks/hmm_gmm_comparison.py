# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.3.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# https://github.com/RadionBik/Statistical-estimator-of-network-traffic
#
# ## Original traffic characterization

# %%
# %load_ext autoreload
# %autoreload 2
# %matplotlib inline
import sys
sys.path.append("..")
import matplotlib.pyplot as plt

import mixture_models
import markov_models
import pcap_parser as estimator
import utils
from plotting import quantiles_acf_dfs, goodput_dfs, hist_dfs, hist_2d_dfs

# %%
plt.rcParams['figure.figsize'] = [10, 5]

pcapfile = 'traffic_dumps/skypeLANhome.pcap'
traffic_dfs = estimator.get_traffic_features(pcapfile,
                                             type_of_identifier=utils.TrafficObjects.FLOW,
                                             percentiles=(3,97),
                                             min_samples_to_estimate=100)[0]
norm_traffic, scalers = utils.normalize_dfs(traffic_dfs)
hist_dfs(traffic_dfs, log_scale=0)
hist_2d_dfs(traffic_dfs, log_scale=0)
quantiles_acf_dfs(traffic_dfs)
goodput_orig = goodput_dfs(traffic_dfs, '1S')

# %% [markdown]
# ## Train HMM, GMM and GMM-HMM models
#
# 1. Hidden Markov Model, the number of components is adjusted manually. The strategy is to use the highest possible
# number of components, however, in case of issues with training, it must be decreased.
# 2. Gaussian Mixture Model with Dirichlet distributed weights. The principle applies as above. See mixture_models.py
# for example of code adjusting component number by Bayesian Information Criterion.
# 3. GMM-HMM. That is a HMM, where each component is modelled as a GMM. If transitions between components are of
# importance, the general approach is to set more HMM states with fewer GMM components.

# %%
test_cases = ['HMM', 'GMM', 'HMM-GMM']
# test_cases = ['GMM']
comp_numb = 20
models = {}
for test_case in test_cases:
    print(f'-------- Started fitting {test_case} ---------')
    if test_case == 'HMM':
        models.update({test_case: markov_models.get_hmm_gaussian_models(norm_traffic, comp_numb)})
    elif test_case == 'GMM':
        models.update({test_case: mixture_models.get_gmm(norm_traffic, comp_numb)})
    elif test_case == 'HMM-GMM':
        models.update({test_case: markov_models.get_hmm_gmm(norm_traffic, 5, 2)})

# %% [markdown]
# ## Characterize generated traffic

# %%
gener_dfs = {}
for model in models:
    # if model!='HMM':
    #    continue
    gener_df, states = markov_models.gener_samples(models[model], scalers, 3000)
    quantiles_acf_dfs(gener_df)
    hist_2d_dfs(gener_df, states=states)
    hist_dfs(gener_df, log_scale=False)
    goodput_dfs(gener_df)
    gener_dfs.update({model: gener_df})

# %% [markdown]
# ## Compare original and generated traffic statistics

# %%
import stat_metrics as stat

for model in gener_dfs:
    print('Comparison of original distributions with {}:'.format(model))
    kl_divergences = stat.get_KL_divergence(traffic_dfs, gener_dfs[model])
    ks_tests = stat.get_ks_2sample_test(traffic_dfs, gener_dfs[model])
    qq_r = stat.get_qq_r_comparison(traffic_dfs, gener_dfs[model])
    # for device, direction, parameter, ks in iterate_traffic_3_layers(ks_tests):
    #    print(ks)

# %% [markdown]
# ## Conclusions
#
# It appears that all models can model distribution properties well, given sufficient number of components. However,
# HMM and HMM-GMM can reproduce time-series better than GMM due to the ability to handle transitions between components.
# Moreover, HMM imitates original traffic closer than HMM-GMM with the same number of hidden variables.

# %%

# %%