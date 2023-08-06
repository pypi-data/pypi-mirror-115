import numpy as np

from sklearn.metrics import silhouette_samples

from .scp_themes import get_color


# Compute Silhouette Score
"""
==============================
Method Name: ComputeSilhouette
==============================

Computes the first silhouette coefficient of each cell in the data and saves it in the 
celldata assay of the single cell object.


Parameters
========== 

sc                  -   A single cell object which contains the data and metadata of genes and cells.

cluster_by          -   A string for the column name in celldata assay of single cell (sc) object that 
                        contains the cell clusters.

Returns
=======

sc                  -   The single cell object with the silhouette coeffiecients stored in the celldata assay.

"""

def ComputeSilhouette(sc, cluster_by):

    cell_labels = sc.getNumericCellLabels(cluster_by)

    X = sc.getCounts() # X is (features, samples)

    sil_scores = silhouette_samples(X.T, cell_labels)

    sc.addCellData(col_data = sil_scores, col_name = 'Silhouette_Scores')

    return sc

    
"""
===========================
Method Name: SilhouettePlot
===========================

Generates a silhouette plot from the cell clusters in data represented by the 'cluster_by' argument.


Parameters
========== 

axis                -   A matplotlib axis handle.

sc                  -   A single cell object which contains the data and metadata of genes and cells.

cluster_by          -   A string for the column name in celldata assay of single cell (sc) object that 
                        contains the cell clusters.

Returns
=======

axis                -   The matplotlib axis handle.

"""

def SilhouettePlot(axis, sc, cluster_by):

    sc = ComputeSilhouette(sc, cluster_by)

    silhouette_scores = sc.getCellData('Silhouette_Scores')

    cell_labels = sc.getNumericCellLabels(cluster_by)

    cell_types = sc.getDistinctCellTypes(cluster_by)


    if (type(cell_types[0]) != str):

        for i in range(len(cell_types)):

            cell_types[i] = str(cell_types[i])


    y_lower = 10

    for i in range(1, len(cell_types) + 1):

        mask = (cell_labels == i)

        cluster_sil_scores = silhouette_scores[mask]

        cluster_sil_scores.sort()

        cluster_n = cluster_sil_scores.shape[0]

        y_upper = y_lower + cluster_n

        axis.fill_betweenx(np.arange(y_lower, y_upper), 0, cluster_sil_scores, facecolor=get_color(i-1), edgecolor=get_color(i-1), label = cell_types[i-1])

        # axis.text(-0.05, y_lower + 0.5 * cluster_n, cell_types[i-1])

        y_lower = y_upper + 10


    axis.set_title("Silhouette Plot")

    axis.set_xlabel("silhouette coefficient")

    axis.set_ylabel("clusters")

    axis.legend(title = 'cell types', bbox_to_anchor=(1.2, 1))

    axis.axvline(x=np.mean(silhouette_scores), color="red", linestyle="--")

    axis.set_yticks([])
    #axis.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])


    return axis