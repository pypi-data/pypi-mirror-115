#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import seaborn as sns
import time
from ParticleSwarmOptimization import Particle

class Swarm:
    def __init__(self):
        pass
    
    def search(self, Particles, max_epochs, estimator, X, y, cv, scoring, search_space, acceleration=1, acceleration_rate=0, verbose=1):
        start = time.time()
        if verbose >= 1:
            print(f'Swarm search started:')
        
        ps = []
        if type(Particles) == int:
            for p in range(Particles):
                ps.append(Particle.Particle(estimator, X, y, cv, scoring, search_space))
            print(f'Number of Particles: {Particles} | Maximum of Epochs: {max_epochs}')
                
        if type(Particles) == list:
            ps = Particles

        swarm_best = {}
        swarm_log = []
        for p in ps:
            p.evaluate()
            swarm_best[p.score] = p.position

        swarm_best_score = max(list(swarm_best.keys()))
        
        metric_str = ' '.join(scoring.split('_')).title().replace('Neg', 'Negative')
        print(f'Initial {metric_str} = {swarm_best_score}')
        swarm_log.append(swarm_best_score)

        epochs = 1
        while True:
            for p in ps:
                swarm_best_score = max(list(swarm_best.keys()))
                p.update_global_best(swarm_best[swarm_best_score])

            for p in ps:
                p.update_velocity(max_epochs)
            
            for p in ps:
                p.move(epochs + 1, acceleration)

            for p in ps:
                p.evaluate()
                swarm_best[p.score] = p.position

            swarm_best_score = max(list(swarm_best.keys()))
            print(f'Epoch {epochs}: {metric_str} = {swarm_best_score}')
            swarm_log.append(swarm_best_score)

            if epochs == max_epochs:
                break
            
            if len(swarm_best.keys()) >= 2:
                if list(swarm_best.keys())[-2] > list(swarm_best.keys())[-1]:
                    acceleration += acceleration_rate
                    if verbose > 1:
                        print(f'Particle Decelerated | Acceleration: {acceleration}')
                    if acceleration <= 0:
                        acceleration = 1
                        if verbose > 1:
                            print('Acceleration set to 1')

                if list(swarm_best.keys())[-2] < list(swarm_best.keys())[-1]:
                    acceleration -= acceleration_rate
                    if verbose > 1:
                        print(f'Particle Decelerated | Acceleration: {acceleration}')
                    if acceleration <= 0:
                        acceleration = 1
                        if verbose > 1:
                            print('Acceleration set to 1')
            
            epochs += 1
        
        self.swarm_best = swarm_best
        self.swarm_log = swarm_log
        self.best_params_ = self.swarm_best[max(list(self.swarm_best.keys()))]
        
        end = time.time()
        duration = end - start
        print(f'Time Spent: {duration}')
        
    def MultiSwarmSearch(self, n_swarms, n_Particles, max_epochs, estimator, X, y, cv, scoring, search_space, acceleration=1, acceleration_rate=0):
        start = time.time()
        print(f'Multiple Swarms Search Started:\n')
            
        ps = [Particle(estimator, X, y, cv, scoring, search_space) for i in range(n_Particles)]
        swarm_params = []
        swarm_score = []
        swarms = {}
        
        slicing = int(n_Particles/n_swarms)
        grps = [ps[i * slicing:(i + 1) * slicing] for i in range(int(n_swarms))]

        for count, g in enumerate(grps):
            groups = [p for p in ps if p in g]
            print(f'Swarms: {count + 1} | Number of Particles: {len(groups)} | Max Epochs: {max_epochs} | Acceleration: {acceleration}')
            self.search(groups, max_epochs, estimator, X, y, cv, scoring, search_space, acceleration, acceleration_rate, verbose=0)
            swarm_score.append(self.swarm_best)
            print('')

        d = {}
        for i in range(len(swarm_score)):
            d[max(list(swarm_score[i].keys()))] = swarm_score[i][max(list(swarm_score[i].keys()))]

        best_param_ = d[max(list(d.keys()))]
        best_score_ = max(list(d.keys()))
        
        self.swarm_params = swarm_params
        self.swarm_score = swarm_score
        self.swarms = swarms
        self.best_param_ = best_param_
        self.best_score_ = best_score_
        
        end = time.time()
        duration = end - start
        print(f'Time Spent: {duration}')
        
    def GroupParticles(self, group_size, Particles):
        similarities = pd.DataFrame()
        for idx1, p1 in enumerate(Particles):
            for idx2, p2 in enumerate(Particles):
                similarity = 1 - distance.cosine(p1.position_vector, p2.position_vector)
                similarities.loc[idx1, idx2] = similarity
                if idx1 == idx2:
                    similarities.loc[idx1, idx2] = np.nan

        flat_list = []
        grouped = []
        while True:
            clusters = [sorted([col] + list(similarities[col].sort_values(ascending=False)[:group_size - 1].index)) for col in similarities.columns]

            clusters_count = {}
            for c1 in clusters:
                clusters_count[str(c1)] = 0
                for c2 in clusters:
                    if c1 == c2:
                        clusters_count[str(c1)] += 1

            clusters_count = pd.DataFrame(clusters_count, index=['Counts']).T
            clusters_count.sort_values('Counts', ascending=False, inplace=True)

            grouped.append(eval(list(clusters_count.index)[0]))
            clusters_count.drop(list(clusters_count.index)[0], inplace=True)

            for sublist in grouped:
                for item in sublist:
                    flat_list.append(item)

            for i in flat_list:
                if i in similarities.columns:
                    similarities.drop(i, inplace=True)
                    similarities.drop(i, axis=1, inplace=True)

            if len(similarities.columns) == 0:
                break
        
        return grouped
    
    def ClusterSwarmSearch(self, n_clusters, Particles, max_epochs, estimator, X, y, cv, scoring, search_space, acceleration=1, acceleration_rate=0):
        start = time.time()
        print(f'Cluster Swarm Search Started:\n')
        ps = []
        for i in range(Particles):
            ps.append(Particle(estimator, X, y, cv, scoring, search_space))

        swarm = Swarm()
        grps = swarm.GroupParticles(int(Particles/n_clusters), ps)

        swarm_params = []
        swarm_score = []
        swarms = {}

        for count, g in enumerate(grps):
            groups = [p for idx, p in enumerate(ps) if idx in g]
            print(f'Cluster: {count + 1} | Number of Particles: {len(groups)} | Max Epochs: {max_epochs} | Acceleration: {acceleration}')
            swarm.search(groups, max_epochs, estimator, X, y, cv, scoring, search_space, acceleration, acceleration_rate, verbose=0)
            swarm_score.append(swarm.swarm_best)
            print('')

        d = {}
        for i in range(len(swarm_score)):
            d[max(list(swarm_score[i].keys()))] = swarm_score[i][max(list(swarm_score[i].keys()))]

        best_param_ = d[max(list(d.keys()))]
        best_score_ = max(list(d.keys()))
        
        self.swarm_params = swarm_params
        self.swarm_score = swarm_score
        self.swarms = swarms
        self.best_param_ = best_param_
        self.best_score_ = best_score_
        
        end = time.time()
        duration = end - start
        print(f'Time Spent: {duration}')
