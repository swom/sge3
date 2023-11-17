import random
import copy


def tournament(population, tsize=3):
    pool = random.sample(population, tsize)
    pool.sort(key=lambda i: i['fitness'])
    n_indiv = copy.deepcopy(pool[0])
    n_indiv['lineage'] = [pool[0]['id'] for _ in pool[0]['genotype']]
    return n_indiv
