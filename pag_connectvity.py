from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache
from allensdk.api.queries.ontologies_api import OntologiesApi
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# The manifest file is a simple JSON file that keeps track of all of
# the data that has already been downloaded onto the hard drives.
# If you supply a relative path, it is assumed to be relative to your
# current working directory.

mcc = MouseConnectivityCache()
# open up a list of all of the experiments
all_experiments = mcc.get_experiments(dataframe=True)
print("%d total experiments" % len(all_experiments))
all_experiments.loc[122642490]

# grab the StructureTree instance
structure_tree = mcc.get_structure_tree()
# get info on some structures
structures = structure_tree.get_structures_by_acronym(['PAG']) #Periaqueductal gray
df = pd.DataFrame(structures)
print(df['structure_set_ids'][0])


oapi = OntologiesApi()
# get the ids of all the structure sets in the tree
structure_set_ids = structure_tree.get_structure_sets()
# query the API for information on those structure sets
pd.DataFrame(oapi.get_structure_sets(structure_set_ids))
pd.DataFrame(oapi.get_structure_sets(df['structure_set_ids'][0]))
# From the above table, "Mouse Connectivity - Summary" has id 167587189
summary_structures = structure_tree.get_structures_by_set_id([167587189])
summary_structures_df = pd.DataFrame(summary_structures)

# "Summary structures of the midbrain" has id 688152365
summary_structures_midbrain = structure_tree.get_structures_by_set_id([688152365]) # Summary structures of the midbrain
summary_structures_midbrain_df = pd.DataFrame(summary_structures_midbrain)

# fetch the experiments that have injections in the isocortex of cre-positive mice
isocortex = structure_tree.get_structures_by_name(['Isocortex'])[0]

pag = structure_tree.get_structures_by_name(['Periaqueductal gray'])[0]
cre_pag_experiments = mcc.get_experiments(cre=True, injection_structure_ids=[pag['id']])
cre_pag_df = pd.DataFrame(cre_pag_experiments)
print("%d cre PAG experiments" % len(cre_pag_experiments))

wt_pag_experiments = mcc.get_experiments(cre=False, injection_structure_ids=[pag['id']])
wt_pag_df = pd.DataFrame(wt_pag_experiments)
print("%d WT PAG experiments" % len(wt_pag_experiments))

# same as before, but restrict the cre line
gad2_pag_experiments = mcc.get_experiments(cre=['Gad2-IRES-Cre'], injection_structure_ids=[pag['id']])
gad2_pag_df = pd.DataFrame(gad2_pag_experiments)
print("%d GAD2 PAG experiments" % len(gad2_pag_experiments))

# find the experiments with the primary injection is PAG
tmp = pd.DataFrame()
#tmp = pd.DataFrame(cre_pag_df.shape[1])
count = 0
for i in cre_pag_df['primary_injection_structure']:
    count += 1
    tmp[count] = summary_structures_df[summary_structures_df['id'] == i]['name'].to_numpy()
tmp = tmp.transpose()
cre_pag_df['primary_injection_name'] = tmp.to_numpy()
pag_prime_inj_cre = cre_pag_df[cre_pag_df['primary_injection_structure'] == pag['id']]# no experiment

# wild type experiments primary injection at PAG
tmp = pd.DataFrame()
count = 0
for i in wt_pag_df['primary_injection_structure']:
    count += 1
    tmp[count] = summary_structures_df[summary_structures_df['id'] == i]['name'].to_numpy()
tmp = tmp.transpose()
wt_pag_df['primary_injection_name'] = tmp.to_numpy()
pag_prime_inj_wt = wt_pag_df[wt_pag_df['primary_injection_structure'] == pag['id']]

# print(summary_structures_df['id']==pag['id'])
structure_unionizes_prime_pag = mcc.get_structure_unionizes([e for e in pag_prime_inj_cre['id']], is_injection=False, include_descendants=True)
print("%d PAG non-injection, cortical structure unionizes" % len(structure_unionizes_prime_pag))

dense_unionizes_prime_pag = structure_unionizes_prime_pag[structure_unionizes_prime_pag.projection_density > .13]
large_unionizes_prime_pag = dense_unionizes_prime_pag[dense_unionizes_prime_pag.volume > .5]
large_structures_prime_pag = pd.DataFrame(structure_tree.nodes(large_unionizes_prime_pag.structure_id))

print("%d large, dense, cortical, non-injection unionizes, %d structures" % (len(large_unionizes_prime_pag), len(large_structures_prime_pag)))
print(large_structures_prime_pag.name)

fig1, (ax1, ax2) = plt.subplots(1, 2)
ax1.hist(structure_unionizes_prime_pag.projection_density, range=[0, 0.3])
ax2.hist(dense_unionizes_prime_pag.volume, range=[0, 20])

pag_prime_inj_cre_experiment_ids = pag_prime_inj_cre['id']
#ctx_children = structure_tree.child_ids( [isocortex['id']] )[0]
print(large_structures_prime_pag.name)
pm = mcc.get_projection_matrix(experiment_ids=pag_prime_inj_cre_experiment_ids,
                               projection_structure_ids=large_structures_prime_pag['id'],
                               parameter='projection_density')

row_labels = pm['rows']# these are just experiment ids
column_labels = [c['label'] for c in pm['columns']]
matrix = pm['matrix']

fig, ax = plt.subplots(figsize=(15, 15))
heatmap = ax.pcolor(matrix, cmap=plt.cm.afmhot)
# put the major ticks at the middle of each cell
ax.set_xticks(np.arange(matrix.shape[1])+0.5, minor=False)
ax.set_yticks(np.arange(matrix.shape[0])+0.5, minor=False)
ax.set_xlim([0, matrix.shape[1]])
ax.set_ylim([0, matrix.shape[0]])
# want a more natural, table-like display
ax.invert_yaxis()
ax.xaxis.tick_top()
ax.set_xticklabels(column_labels, minor=False)
ax.set_yticklabels(row_labels, minor=False)
plt.show()

print(pag_prime_inj_cre_experiment_ids)
experiment_id = pag_prime_inj_cre_experiment_ids[11]
# projection density: number of projecting pixels / voxel volume
pd, pd_info = mcc.get_projection_density(experiment_id)
# injection density: number of projecting pixels in injection site / voxel volume
ind, ind_info = mcc.get_injection_density(experiment_id)
# injection fraction: number of pixels in injection site / voxel volume
inf, inf_info = mcc.get_injection_fraction(experiment_id)
# data mask:
# binary mask indicating which voxels contain valid data
dm, dm_info = mcc.get_data_mask(experiment_id)
template, template_info = mcc.get_template_volume()
annot, annot_info = mcc.get_annotation_volume()
# in addition to the annotation volume, you can get binary masks for individual structures
# in this case, we'll get one for the isocortex
cortex_mask, cm_info = mcc.get_structure_mask(315)
# cortex_mask, cm_info = mcc.get_structure_mask(319)
print(pd_info)
print(pd.shape, template.shape, annot.shape)
# compute the maximum intensity projection (along the anterior-posterior axis) of the projection data
pd_mip = pd.max(axis=0)
ind_mip = ind.max(axis=0)
inf_mip = inf.max(axis=0)

pd_mip_ind = np.argmax(pd.max(axis=1))-np.floor(np.argmax(pd.max(axis=1))/528)*456
print(pd_mip_ind)
# show that slice of all volumes side-by-side
f, pr_axes = plt.subplots(1, 3, figsize=(15, 6))

pr_axes[0].imshow(pd_mip, cmap='hot', aspect='equal')
pr_axes[0].set_title("projection density MaxIP")

pr_axes[1].imshow(ind_mip, cmap='hot', aspect='equal')
pr_axes[1].set_title("injection density MaxIP")

pr_axes[2].imshow(inf_mip, cmap='hot', aspect='equal')
pr_axes[2].set_title("injection fraction MaxIP")

plt.show()
# Look at a slice from the average template and annotation volumes

# pick a slice to show
slice_idx = 228 #260 #319 #435

f, ccf_axes = plt.subplots(1, 3, figsize=(15, 6))

ccf_axes[0].imshow(template[slice_idx,:,:], cmap='gray', aspect='equal', vmin=template.min(), vmax=template.max())
ccf_axes[0].set_title("registration template")

ccf_axes[1].imshow(annot[slice_idx,:,:], cmap='gray', aspect='equal', vmin=0, vmax=2000)
ccf_axes[1].set_title("annotation volume")

ccf_axes[2].imshow(cortex_mask[slice_idx,:,:], cmap='gray', aspect='equal', vmin=0, vmax=1)
ccf_axes[2].set_title("isocortex mask")

plt.show()
f, data_mask_axis = plt.subplots(figsize=(5, 6))

data_mask_axis.imshow(dm[81, :, :], cmap='hot', aspect='equal', vmin=0, vmax=1)
data_mask_axis.set_title('data mask')

plt.show()