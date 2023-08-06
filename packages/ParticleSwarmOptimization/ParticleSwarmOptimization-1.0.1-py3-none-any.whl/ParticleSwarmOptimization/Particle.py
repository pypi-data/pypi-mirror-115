#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import seaborn as sns

class Particle:
    def __init__(self, estimator, X, y, cv, scoring, search_space):
        self.estimator = estimator
        self.X = X
        self.y = y
        self.cv = cv
        self.scoring = scoring
        self.search_space = search_space
        
        self.pos_log = []
        self.score_log = []
        self.gbest = None
        self.velo_log = []
        self.stop = None
        
        rand_init = [np.random.choice(self.search_space[k]) for k in self.search_space.keys()]
        self.position = {k:[v] for k, v in zip(self.search_space.keys(), rand_init)}
        self.position_vector = [v[0] for v in self.position.values()]
        
    def update_position(self, position):
        self.position = position
    
    def evaluate(self):
        if self.stop == None or self.stop == False:
            gs = GridSearchCV(self.estimator, self.position, cv=self.cv, scoring=self.scoring)
            gs.fit(self.X, self.y)
            self.score = gs.best_score_
            self.score_log.append(self.score)
            self.pos_log.append(self.position)
        
    def update_global_best(self, gbest):
        if gbest != self.gbest or self.gbest == None:
            self.gbest = gbest
        
    def update_velocity(self, max_step):
        types = [type(i[0]) for i in list(self.gbest.values())]
        velo = [(g[0] - c[0])/max_step for g, c in zip(self.gbest.values(), self.position.values())] 
        self.velo = [t(v) for v, t in zip(velo, types)]
        self.velo_log.append(self.velo)
        self.types = types
        
    def move(self, step, acceleration=1):
        if sum(self.velo) == 0:
            self.stop = True
            
        if sum(self.velo) > 0:
            self.stop = False
            
        if self.stop == False or self.stop == None:    
            self.position = {k:[v] for k, v in zip(self.position, [c[0] + v * step/acceleration for c, v in zip(self.position.values(), self.velo)])}
            self.position = {k:v if v[0] >= 0 else [0] for k, v  in self.position.items()}
            self.position_vals = [t(v) for v, t in zip(self.position.values(), self.types)]
            self.position = {k:v for k, v in zip(self.position.keys(), self.position_vals)}
