import numpy as np
from sge.parameters import params
import json
import os



def evolution_progress(generation, pop, archive):
    best=pop[0]
    fitness_samples = [i['fitness'] for i in pop]
    if params['META_MUTATION']:
        data = f"{generation};{best['fitness']};{best['genotype']};{best['phenotype']};{best['mutation_probs']};{np.mean(fitness_samples)};{np.std(fitness_samples)};{best['other_info']['test_error']}"
    else:
        data = f"{generation};{best['fitness']};{best['genotype']};{best['phenotype']};{np.mean(fitness_samples)};{np.std(fitness_samples)};{best['other_info']['test_error']}"

    if params['VERBOSE']:
        print(data)
    save_progress_to_file(data)
    
    if generation % params['SAVE_STEP'] == 0:
        save_step(generation, pop, num_inds=5)
        save_lineage(archive, pop, 5, generation)


def save_progress_to_file(data):
    with open('%s/run_%d/progress_report.csv' % (params['EXPERIMENT_NAME'], params['RUN']), 'a') as f:
        f.write(data + '\n')


def save_step(generation, population, num_inds):
    to_save = []
    evenly_spaced_indexes = np.round(np.linspace(0, len(population) - 1, num_inds + 1)).astype(int)[-num_inds:]#first index is best ind which is always recorded so we can exclude it
    for i in np.array(population)[evenly_spaced_indexes]:
        if params['META_MUTATION']:
            to_save.append({"fitness": i['fitness'], "phenotype": i['phenotype'], "mutation_probs": i["mutation_probs"]})
        else:
            to_save.append({"fitness": i['fitness'], "phenotype": i['phenotype']})
    open('%s/run_%d/iteration_%d.json' % (params['EXPERIMENT_NAME'], params['RUN'], generation), 'a').write(json.dumps(to_save))

def save_parameters():
    params_lower = dict((k.lower(), v) for k, v in params.items())
    c = json.dumps(params_lower)
    open('%s/run_%d/parameters.json' % (params['EXPERIMENT_NAME'], params['RUN']), 'a').write(c)


def prepare_dumps():
    try:
        os.makedirs('%s/run_%d' % (params['EXPERIMENT_NAME'], params['RUN']))
    except FileExistsError as e:
        pass
    save_parameters()

def save_lineage(archive, population, num_inds, gen):
    to_save = []
    evenly_spaced_indexes = np.round(np.linspace(0, len(population) - 1, num_inds + 1)).astype(int)[-num_inds:]#first index is best ind which is always recorded so we can exclude it
    lineages = []
    #print(archive)
    for i in np.array(population)[evenly_spaced_indexes]:
        if params['META_MUTATION']:
            lineages.append([])
            for ix in range(len(i['mutation_probs'])):
                #print(i)
                lineage = reconstruct_lineage_mut_and_fit(archive, i, ix)
                lineages[-1].append(lineage)
        else:
            lineages.append(reconstruct_lineage_fit(archive, i))
    open('%s/run_%d/lineage_report_%d.json' % (params['EXPERIMENT_NAME'], params['RUN'], gen),  'w').write(json.dumps(lineages))

def reconstruct_lineage_mut_and_fit(archive, indiv, ix):
    
    to_add = {'mut_rate': indiv['mutation_probs'][ix], 'fit':indiv['fitness']}
    if 'lineage' in indiv:
        parent = archive[indiv['lineage'][ix]]
        lineage = reconstruct_lineage_mut_and_fit(archive, parent, ix)
        lineage.extend(to_add)
        #print(indiv)
        #print(f"Archive:, Lineage:{lineage}, Indiv:{indiv['id']}, Ix:{ix}")
        return lineage
    else:
        return to_add

def reconstruct_lineage_fit(archive, indiv):
    
    to_add = [indiv['fitness']]
    if 'lineage' in indiv:
        parent = archive[indiv['lineage'][0]]
        lineage = reconstruct_lineage_fit(archive, parent)
        lineage.extend(to_add)
        #print(indiv)
        #print(f"Archive:, Lineage:{lineage}, Indiv:{indiv['id']}, Ix:{ix}")
        return lineage
    else:
        return to_add
