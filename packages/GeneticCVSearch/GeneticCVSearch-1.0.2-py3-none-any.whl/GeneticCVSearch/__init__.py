#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import seaborn as sns

class GeneticCVSearch:
    def __init__(self):
        pass
    
    def gene(self, pop_size, lower, upper, method):
        allele = np.arange(lower, upper)

        if method == 'random':
            return [np.random.choice(allele) for i in range(pop_size)]

        if method == 'normal':
            mu = allele.mean()
            sigma = allele.std()
            return [abs(round(np.random.normal(loc=mu, scale=sigma))) for i in range(pop_size)]
    
    
    def allele(self, allele_range, pop_size):
        allele_range['size'] = (allele_range['size'], allele_range['size'])

        chromosome = []
        for k in list(allele_range.keys())[1:]:
            lower = allele_range[k][0]
            upper = allele_range[k][-1]
            allele_size = allele_range['size'][0]
            chromosome.append(pd.DataFrame(self.gene(pop_size, lower, upper, 'normal'), dtype='O'))

        population = pd.concat(chromosome, axis=1)
        population.columns=list(allele_range.keys())[1:]

        for col in population.columns:
            if sum(population[col]) == 0:
                population[col] = abs(np.random.normal(population['learning_rate']))
                def limit(row):
                    return 1 if row > 1 else row
                population[col] = population[col].apply(limit)

        return population
    
    def chromosome(self, population):
        population = population.copy()
        return [{k:[v] for (k, v) in zip(population.columns, population.iloc[i])} for i in range(len(population))]

    
    def trial(self, chromosomes, estimator, cv, scoring, X, y, verbose=0):
        individuals = []
        for c in chromosomes:
            gs = GridSearchCV(estimator, c, cv=cv, scoring='neg_mean_absolute_error')
            gs.fit(X, y)
            fitness = gs.best_score_
            c['fitness'] = fitness
            individuals.append(pd.DataFrame(c, dtype='O'))

        individuals = pd.concat(individuals)
        individuals.sort_values('fitness', ascending=False, inplace=True)
        individuals.index = range(len(individuals))
        if verbose > 1:
            print(individuals)
        print('')

        return individuals
    
    def selection(self, individuals, method, offspring_size, Tournament_size=2):
        if method == 'R' or method == 'RW':
            if offspring_size == None:
                raise TypeError("'offspring_size' cannot be None if using Rank Selection or Roulette Wheel Selection.")

        # Roulette Wheel
        if method == 'RW':
            individuals['prob'] = individuals['fitness']/sum(individuals['fitness'])
            selected_idx = np.random.choice(individuals.index, offspring_size, p=individuals['prob'])
            individuals = individuals.iloc[selected_idx, :-1]
            return individuals

        # Steady State/Stratify
        if method == 'SS':
            individuals.drop_duplicates(inplace=True)
            individuals['bin'] = pd.qcut(individuals['fitness'], 3)
            individuals = individuals.groupby('bin').apply(lambda grp: grp[:2]).reset_index(drop=True)[individuals.columns[:-1]]
            return individuals

        # Tournament    
        if method == 'T':    
            individuals = individuals.sample(frac=1)
            individuals.index = range(len(individuals))
            odd = [i for i in range(len(individuals)) if i % Tournament_size == 1]
            even = [i for i in range(len(individuals)) if i % Tournament_size == 0]

            winners = []
            for o, e in zip(odd, even):
                if individuals.iloc[o, -1] >= individuals.iloc[e, -1]:
                     winners.append(individuals.iloc[o])

                if individuals.iloc[o, -1] < individuals.iloc[e, -1]:
                     winners.append(individuals.iloc[e])

            winners = pd.concat(winners, axis=1).T

            return winners

        # Stochastic Universal Sampling
        if method == 'SUS':
            sus_index = [np.random.choice(individuals.index) for i in range(offspring_size)]
            individuals = individuals.iloc[sus_index, :]
            return individuals

        # Rank  
        if method == 'R':    
            individuals = individuals.sort_values('fitness', ascending=False).head(offspring_size)
            return individuals
        
    def crossover(self, pairs, pt):
        pairs = pairs.copy()
        pt = int(len(pairs.columns)/pt)

        for i in range(len(pairs.columns)):
            if (i + 1) * pt % 2 != 1 and i < pt - 1:
                pairs[:2].iloc[0, i*pt:(i+1)*pt], pairs[:2].iloc[1, i*pt:(i+1)*pt] = pairs[:2].iloc[1, i*pt:(i+1)*pt], pairs[:2].iloc[0, i*pt:(i+1)*pt]

        return pairs

    def reproduction(self, parents, c_pt, dominance=True, weighted=True, verbose=0):
        parents = parents.copy()
        children = []
        if dominance == False:
            for i in range(len(parents)):
                if i != len(parents) - 1:
                    children.append(self.crossover(parents[i:i+2], c_pt))

                if i == len(parents) - 1:
                    children.append(self.crossover(parents.iloc[[0, -1], :], c_pt))

            children = pd.concat(children)
            children.index = range(len(children))
        
        if dominance == True:
            parents.sort_values('fitness', ascending=False, inplace=True)
            parents.index = range(len(parents))
            dtypes = [type(i) for i in parents.iloc[0].values]

            parents['prob'] = (parents['fitness']/parents['fitness'].sum())
            parents['prob'] = np.array(parents['prob'].iloc[::-1])

            children = pd.DataFrame(columns=parents.columns)
            for f, t in zip(parents.columns, dtypes):
                for row in range(len(parents[1:])):
                    if weighted == False:
                        if t == int:
                            children.loc[row, f] = int((parents.loc[0, f] + parents.loc[row, f])/2)
                        else:
                            children.loc[row, f] = float((parents.loc[0, f] + parents.loc[row, f])/2)

                    if weighted == True:
                        if t == int:
                            children.loc[row, f] = int((parents.loc[0, f] * parents.loc[0, 'prob'] + parents.loc[row, f] * parents.loc[row, 'prob'])/(parents.loc[0, 'prob'] + parents.loc[row, 'prob']))
                        else:
                            children.loc[row, f] = float((parents.loc[0, f] * parents.loc[0, 'prob'] + parents.loc[row, f] * parents.loc[row, 'prob'])/(parents.loc[0, 'prob'] + parents.loc[row, 'prob']))           
        
        if 'fitness' in children.columns:
                children.drop('fitness', axis=1, inplace=True)

        if 'prob' in children.columns:
                children.drop('prob', axis=1, inplace=True)
        
        return children

    def mutation(self, offspring, method, epsilon=.1, momentum=0.05, verbose=0):
        offspring = offspring.copy()
        idx = [np.random.choice(offspring.index) for i in range(len(offspring)) if epsilon > np.random.random()]

        # Boundary
        if method == 'Boundary':
            for genes in offspring.columns:
                upper = max(offspring[genes])
                lower = min(offspring[genes])
                mutated = [np.random.choice([upper, lower]) for i in range(len(idx))]
                offspring.loc[idx, genes] = mutated
                if verbose > 0:
                    print(f'Mutation occured (Boundary).')

        # Non-Uniform/Uniform
        if method == 'Non-Uniform' or method == 'Uniform':
            for genes in offspring.columns:
                mutated = [np.random.choice(offspring[genes]) for i in range(len(offspring)) if epsilon > np.random.random()]
                idx2 = [np.random.choice(offspring.index) for i in range(len(mutated))]
                offspring.loc[idx2, genes] = mutated

                if method == 'Uniform':
                    epsilon += momentum
            
            if verbose > 0:
                print(f'Mutation occured (Non-Uniform/Uniform).')
            
        # Shrink/Gaussian
        if method == 'Shrink' or method == 'Gaussian':
            for genes in offspring.columns:
                mu = offspring[genes].mean()
                sigma = offspring[genes].std()
                for i in idx:
                    if method == 'Shrink':
                        offspring.loc[idx, genes] = round(np.random.normal(loc=mu, scale=sigma))

                    if method == 'Gaussian':
                        offspring.loc[idx, genes] = round(np.random.normal(loc=0, scale=1))
                        
            if verbose > 0:
                print(f'Mutation occured (Shrink/Gaussian).')
        
        if verbose > 0:
            print(f'Mutation Rate: {epsilon}')
        
        return offspring

    def seq_evo(self, X, y, search_space, pop_size, estimator, cv, scoring, select_fn, Tournament_size, offspring_size, c_pt, dominance, weighted, n_elite, mu_method, epsilon=.1, momentum=0.05, torlerance=3, verbose=0):
        population = self.allele(search_space, pop_size)
        chromosomes = self.chromosome(population)
        n_gen = 1
        track = {}
        mean_fitness = {}
        
        self.fitness_score_track = []
        self.mean_fitness_score_track = []
        
        selection_pressure = 0
        if Tournament_size == 'adaptive':
            Tournament_size = selection_pressure + 1
        while True:
            if len(track.keys()) >= 2:
                if list(track.keys())[-1] <= list(track.keys())[-2]:
                    if verbose > 0:
                        print('No Improvement.')
                    selection_pressure += 1
                else:
                    selection_pressure -= 1
                    
                if selection_pressure >= torlerance:
                    if verbose > 0:
                        print('\nGenetic CV Search ended.')
                    break
                    
                if mean_fitness[list(mean_fitness.keys())[-1]] <= mean_fitness[list(mean_fitness.keys())[-2]]:
                    if verbose > 0:
                        print('No improvement in mean fitness.')
                    break
                    
            if verbose > 0:        
                print(f'----------------------------------------Generation {n_gen}----------------------------------------')
            fitness = self.trial(chromosomes, estimator, cv, scoring, X, y, verbose)

            if n_elite > 0:
                to_keep = int(len(fitness) * n_elite)
                elite = fitness.sort_values('fitness', ascending=False).drop('fitness', axis=1)[:to_keep]
                
            individuals = self.selection(fitness, select_fn, offspring_size)
            
            if select_fn == 'T':
                print(f'Tournament_size: {Tournament_size}')
                
            if n_elite > 0:
                individuals.sort_values('fitness', ascending=False, inplace=True)
                individuals.iloc[to_keep:]
                if verbose > 0:
                    print(f'{to_keep} elite(s) pass througth to the next generation.\n')
            
            offspring = self.reproduction(individuals, c_pt, dominance, weighted, verbose)
            if verbose > 0:
                print(f'Selection Pressure: {selection_pressure}')
            mutated = self.mutation(offspring, mu_method, epsilon, momentum, verbose)
            chromosomes = self.chromosome(mutated)
            
            fitness.sort_values('fitness', ascending=False, inplace=True)
            fitness_score = fitness.astype(object).head(1)['fitness'].iloc[0]
            fitness_param = fitness.astype(object).head(1)[fitness.columns[:-1]].iloc[0].to_dict()
            mean_fitness_score = fitness['fitness'].mean()
            track[fitness_score] = fitness_param
            mean_fitness[f'Gen {n_gen}'] = mean_fitness_score
            
            if verbose > 0:
                print(f'Best Chromosome: {fitness_param}')
                print(f'Best Score: {fitness_score}')
                print(f'Mean Fitness: {mean_fitness_score}')
            
            self.fitness_score_track.append(fitness_score)
            self.mean_fitness_score_track.append(mean_fitness_score)
            
            n_gen += 1
            if momentum != None:
                epsilon += momentum
                
        self.best_param_ = list(track.values())[np.argmax(list(track.keys()))]
                
        sns.set_theme()
        fig, ax = plt.subplots(figsize=(15, 6))  
        plt.plot(self.fitness_score_track, marker='o')
        plt.plot(self.mean_fitness_score_track, marker='o')
        plt.axvline(x = np.argmax(self.fitness_score_track), color='black', linewidth=2, linestyle='--')
        plt.ylabel('Fitness')
        plt.xlabel('Generations')
        plt.legend(['Trial Best', 'Mean Fitness'])
        title_str = 'neg_mean_absolute_error'.replace('_', ' ').title()
        if 'Neg' in title_str:
            title_str = title_str.replace('Neg', 'Negative')
        plt.title(f'{title_str} of Each Generations')
        plt.show()
