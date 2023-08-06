import numpy as np



from .scp_themes import get_color

"""
===========================
Method Name: GeneExpHeatmap
===========================

Plots a heatmap to show the expression of the top genes in the data acorss all the cells. The gene 
expression will be sorted by the feature importance values stored in the genedata assay referred to 
by the sort_by argument.


Parameters
========== 

axis                -   A matplotlib axis handle.

sc                  -   A single cell object which contains the data and metadata of genes and cells.

color_by            -   A string for the column name in celldata assay of single cell (sc) object that 
                        contains the cell clusters. A different color will be applied for each cluster. 
                        Clusters can be represented by string or numeric value. 

sort_by             -   A string for the column name in genedata assay of single cell (sc) object that 
                        contains the values to sort the genes by.

name_by             -   A string for the column name in genedata assay of single cell (sc) object that 
                        contains the names of the genes in the data.

top_num_genes       -   The number of top genes to shown in the heatmap plot. Default 10.

sort                -   String representing whether to sort in ascending or descending order. Default 'descending'.


Returns
=======

axis                -   The matplotlib axis handle.

"""

def GeneExpHeatmap(axis, sc, color_by, sort_by, name_by, top_num_genes = 10, sort = 'descending'):
    
    cell_idx = np.arange(sc.dim[1])  # Cell indexes, first cell index is 1. 

    X = sc.getCounts() # X is (features, samples)

    cell_labels = sc.getNumericCellLabels(color_by) # Cell labels of the cells, can be numeric array or string array
    gene_names = sc.getGeneData(name_by)

    idx = np.argsort(cell_labels)
    cell_labels = cell_labels[idx]
    X = X[:, idx]

    # Get the different cell types 
    cell_types = sc.getDistinctCellTypes(color_by)

    if (type(cell_types[0]) != str):
            for i in range(len(cell_types)):
                cell_types[i] = str(cell_types[i])


    # Sort according to the gene score
    if (type(sort_by) != type(None)):
        sort_values = sc.getGeneData(sort_by)
        idx = np.argsort(sort_values)
        if (sort == 'descending'):
            idx = np.flip(idx)

        X = X[idx, :]
        gene_names = gene_names[idx]

    gene_names = gene_names[0:top_num_genes]
    X = X[0:top_num_genes, :]




    # Draw the heatmap
    im = axis.imshow(X, aspect = 'auto', cmap = 'inferno', interpolation = 'none')

    cbar = axis.figure.colorbar(im, ax=axis)
    cbar.ax.set_ylabel('expression value', rotation=-90, va="bottom")

    axis.set_yticks(np.arange(len(gene_names)))
    axis.set_yticklabels(gene_names)

    axis.set_ylabel('genes')
    axis.set_xlabel('cells')

    # Do what?
    axis.spines['right'].set_visible(False)
    axis.spines['top'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['left'].set_visible(False)
    
    
    # Draw the line (later)

    y = -1*np.ones(cell_idx.shape[0])

    for i in range(1, len(cell_types) + 1):
        mask = (cell_labels == i)
        axis.plot(cell_idx[mask], y[mask], color = get_color(i-1), linewidth = 7, label = cell_types[i-1])

    axis.legend(title = 'cell type', bbox_to_anchor=(1.5, 1))

    return axis