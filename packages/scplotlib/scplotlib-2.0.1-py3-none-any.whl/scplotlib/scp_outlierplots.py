import numpy as np

from .scp_themes import get_color

"""
==============================
Method Name: PlotOutlierScores
==============================

Creates a bar chart showing the outlier score for each cell. The outlier scores are represented by the values 
in the celldata column of the sc object pointed to by the outlier_score argument. Bars representing the cells 
are colored according to its clusters pointed to by the color_by argument. A threshold line is also plotted.


Parameters
========== 

axis                -   A matplotlib axis handle.

sc                  -   A single cell object which contains the data and metadata of genes and cells.

outlier_score       -   A string for the column name in celldata assay of single cell (sc) object that 
                        contains the cell outlier scores.

color_by            -   A string for the column name in celldata assay of single cell (sc) object that 
                        contains the cell clusters. A different color will be applied for each cluster. 
                        Clusters can be represented by string or numeric value.

threshold           -   A string for the column name in celldata assay of single cell (sc) object that 
                        contains the threshold for classifying a cell as an outlier.


Returns
=======

axis                -   The matplotlib axis handle

"""

def PlotOutlierScores(
    axis,
    sc,
    outlier_score,
    color_by,
    threshold
):

    out_score = sc.getCellData(outlier_score)

    thres = sc.getCellData(threshold)


    cell_labels = sc.getNumericCellLabels(color_by)

    cell_types = sc.getDistinctCellTypes(color_by)


    idx = np.argsort(cell_labels)
    
    cell_labels = cell_labels[idx]

    out_score = out_score[idx]


    if (type(cell_types[0]) != str):

        for i in range(len(cell_types)):

            cell_types[i] = str(cell_types[i])


    x = np.arange(1, out_score.shape[0] + 1)


    for i in range(1, len(cell_types) + 1):

        mask = (cell_labels == i)

        axis.bar(x[mask], out_score[mask], color = get_color(i-1), label = cell_types[i-1])

    
    axis.legend(title = 'cell types', bbox_to_anchor=(1.2, 1))


    axis.plot(x, thres, color = 'black', linestyle = 'dashed')
    

    axis.set_ylabel(outlier_score)

    axis.set_xlabel('cells')

    
    return axis



