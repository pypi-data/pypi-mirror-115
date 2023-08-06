from sklearn.manifold import TSNE
from .scp_core import ScatterPlot


from .scp_themes import get_marker


"""
========================
Method Name: ComputeTSNE
========================

Computes the first two reduced dimension of the data using t-SNE and saves it in the celldata assay 
of the single cell object. 


Parameters
========== 

sc                  -   A single cell object which contains the data and metadata of genes and cells.

tsne_dist_metric    -   The metric to use when calculating distance between instances in a feature array.

tsne_init           -   Initialization of the t-SNE embedding. 

tsne_perplexity     -   The perplexity is related to the number of nearest neighbors that is used in other manifold learning algorithms.

tsne_iterations     -   Maximum number of iterations for the optimization.

tsne_learning_rate  -   The learning rate for t-SNE.

tsne_early_exaggeration -   Controls how tight natural clusters in the original space are in the embedded space and how much space will be between them.

tsne_random_state   -   Determines the random number generator.


Returns
=======

sc                  -   The single cell object.

"""

def ComputeTSNE(    sc, 
                    tsne_dist_metric,
                    tsne_init,
                    tsne_perplexity,
                    tsne_iterations,
                    tsne_learning_rate,
                    tsne_early_exaggeration,
                    tsne_random_state):

    tsne = TSNE(    n_components = 2, 
                    metric=tsne_dist_metric,
                    init= tsne_init,
                    perplexity=tsne_perplexity,
                    n_iter=tsne_iterations,
                    learning_rate=tsne_learning_rate,
                    early_exaggeration=tsne_early_exaggeration,
                    random_state=tsne_random_state
                    )

    X = sc.getCounts() # X is (features, samples)

    X_red = tsne.fit_transform(X.T)
    x = X_red[:, 0]
    y = X_red[:, 1]

    sc.addCellData(col_data = x, col_name = 't-SNE 1')
    sc.addCellData(col_data = y, col_name = 't-SNE 2')

    return sc



# Produces a t-SNE scatter plot

"""
=====================
Method Name: tSNEPlot
=====================

Computes the first two reduced dimension of the data using t-SNE and saves it in the celldata assay 
of the single cell object. 


Parameters
========== 

axis                -   A matplotlib axis handle.

sc                  -   A single cell object which contains the data and metadata of genes and cells.

color_by            -   A string for the column name in celldata assay of single cell (sc) object that 
                        contains the cell clusters. A different color will be applied for each cluster. 
                        Clusters can be represented by string or numeric value. Default None.

marker_by           -   A string for the column name in celldata assay of single cell (sc) object that 
                        contains the cell clusters. A different marker style will be applied for each 
                        cluster. Clusters can be represented by string or numeric value. Default None.

marker_style        -   A string representing matplotlib markers. Refer to matplotlib documentation for
                        marker options. Default '.'.

marker_size         -   Integer representing matplotlib marker size. Refer to the matplotlib documentation 
                        for marker sizes. Default 50.

tsne_dist_metric    -   The metric to use when calculating distance between instances in a feature array.

tsne_init           -   Initialization of the t-SNE embedding. 

tsne_perplexity     -   The perplexity is related to the number of nearest neighbors that is used in other manifold learning algorithms.

tsne_iterations     -   Maximum number of iterations for the optimization.

tsne_learning_rate  -   The learning rate for t-SNE.

tsne_early_exaggeration -   Controls how tight natural clusters in the original space are in the embedded space and how much space will be between them.

tsne_random_state   -   Determines the random number generator.


Returns
=======

axis                -   A matplotlib axis handle.

"""

def tSNEPlot(   axis,
                sc, 
                color_by = None, 
                marker_by = None, 
                marker_style = '.',
                marker_size = 50,
                tsne_dist_metric = 'euclidean',
                tsne_init = 'random',
                tsne_perplexity = 30,
                tsne_iterations = 1000,
                tsne_learning_rate = 200,
                tsne_early_exaggeration = 12,
                tsne_random_state = None
                ):


    sc = ComputeTSNE(   sc, 
                        tsne_dist_metric,
                        tsne_init,
                        tsne_perplexity,
                        tsne_iterations,
                        tsne_learning_rate,
                        tsne_early_exaggeration,
                        tsne_random_state)

    if (type(marker_by) == str):
        cell_labels = sc.getNumericCellLabels(marker_by)
        cell_types = sc.getDistinctCellTypes(marker_by)

        
        if (type(cell_types[0]) != str):
            for i in range(len(cell_types)):
                cell_types[i] = str(cell_types[i])

        for i in range(1, len(cell_types) + 1):
            mask = (cell_labels == i)
            axis = ScatterPlot( axis,
                                sc[mask.tolist()],
                                x = 't-SNE 1',
                                y = 't-SNE 2',
                                color_by = color_by,
                                marker_style = get_marker(i-1),
                                marker_size = marker_size,
                                legend_title = cell_types[i-1] + '-'
                                )

        axis.legend(title = 'batch-cell type')

    else:
        axis = ScatterPlot(     axis,
                                sc,
                                x = 't-SNE 1',
                                y = 't-SNE 2',
                                color_by = color_by,
                                marker_style = marker_style,
                                marker_size = marker_size,
                                legend_title = ""
                                )

        axis.legend(title = 'cell type')

    axis.set_ylabel('t-SNE 2')
    axis.set_xlabel('t-SNE 1')

    return axis