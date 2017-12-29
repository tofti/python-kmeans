# python-kmeans
python implementation of [k-means clustering](https://en.wikipedia.org/wiki/K-means_clustering).

![results](https://github.com/tofti/python-kmeans/blob/master/examples/crime.gif "Crime Example")

# Description
k-means attempts to identify a user specified k(<N) number of clusters from a set of N d-dimensional real valued vectors. In lay terms, it attempts to group together similar data points in to a specified number of groups. More specifically the algorithm attempts to minimize the sum of squared distances from a cluster center, to the cluster members. The sum of squares distances is referred to as the "distortion" due to the methods origins in signal processing. The output of the algorithm is a cluster assignment for each data point, and a final level of "distortion". 

The algorithm does not produce a provably optimal solution, and initial cluster centers may cause the algorithm to get stuck in a locally optimum solution that is clearly sub-optimal ([see the basic 2d example](#basic-synthetic-2d-data) in the [Results](#results) section). Much research has focused on selecting initial cluster centers, see K-Means++ and the comparative review of initialization methods in the Resources section.
 
# Resources

## Basic Algorithm 
+ K-Means is described in [Top 10 Algorithms for Data Mining](https://atasehir.bel.tr/Content/Yuklemeler/Dokuman/Dokuman3_4.pdf);

+ K-Means is outlined in [Information Theory, Inference, and Learning Algorithms](http://www.inference.org.uk/mackay/itila/book.html), excerpt [here](http://www.inference.org.uk/mackay/itprnn/ps/284.292.pdf);

+ Professor Andrew Moore of CMU has some good notes [here](https://www.autonlab.org/_media/tutorials/kmeans11.pdf);

+ [Edureka example](https://www.edureka.co/blog/implementing-kmeans-clustering-on-the-crime-dataset/), using crime data

## Initialization of Clusters
+ [K-Means++](https://en.wikipedia.org/wiki/K-means%2B%2B), and full paper [here](http://ilpubs.stanford.edu:8090/778/1/2006-13.pdf)

+ [A Comparative Study of Efficient Initialization Methods for the K-Means
Clustering Algorithm](https://arxiv.org/pdf/1209.1960.pdf)

## Why not use SciPy?
[SciPy](https://scipy.org/) has a k-means [implementation](https://docs.scipy.org/doc/scipy/reference/cluster.vq.html). The objective of this work is to build a pure python implementation for the purposes of learning, and helping others learn the k-means algorithm. Interested readers with only minimal python experience will be able to read, and step over this code without the added complexity of a library such as SciPy. It is not by any means intended for production use :)

# Running the code

## Dependencies
+ python 3.6.3
+ matplotlib 2.1.1 - see [here](https://matplotlib.org/users/installing.html) for installation instructions.

## Execution
Run the code with the python interpreter: 

```python kmeans.py ./resources/<config.cfg>```

Where config.cfg is a plain text configuration file. The format of the config file is a python abstract syntax tree representing a dict with the following fields:

``
{
   'data_file' : '\\resources\\crime.sample.data.csv',
   'data_project_columns' : ['City','Murder','Assault','UrbanPop','Rape'],
   'k' : 4,
   'cluster_atts' : ['Murder','Assault','UrbanPop','Rape'],
   'plot_config' :
    {'output_file_prefix' : 'crime_clustering',
     'plots_configs': [
        {'plot_atts' : ['Murder', 'Assault']},
        {'plot_atts' : ['Murder', 'UrbanPop']},
        {'plot_atts' : ['Murder', 'Rape']},
        {'plot_atts' : ['Assault', 'UrbanPop']}
     ]
   },
}
``

You have to specify:
 + a csv data file;
 + a subset of fields to project from the file;
 + the number of clusters to form, k;
 + the subset of attributes used in the clustering process;
 + a plot config that includes
    + prefix for png files created during the process in the working directory, if this isn't specified, images will not be produced;
    + the individual plot configurations, limited to 2 dimensions per plot.

 
# Results

## Iris Data Set
The Iris data set ([iris.config](./blob/master/resources/iris.config)), [Lichman, M. (2013). UCI Machine Learning Repository . Irvine, CA: University of California, School of Information and Computer Science.](http://archive.ics.uci.edu/ml), is a very well known data set in the machine learning community. Here are the results of my random initial clusters:

![iris_init_results](https://github.com/tofti/python-kmeans/blob/master/results/iris0.png "Iris Initial")
![iris_final_results](https://github.com/tofti/python-kmeans/blob/master/results/iris11.png "Iris Final")

## Basic Synthetic 2D data
This data was generated for debugging purposes (see ([basic2d.config](./blob/master/resources/basic2d.config))), and illustrates the effect of having a poor choice of initial random clusters. The below results show one such case, where the initial centroid configuration prevents the algorithm from reaching the obvious cluster assignment:

![basic_init](https://github.com/tofti/python-kmeans/blob/master/results/basic_clustering0.png "Basic Initial")
![basic_interim](https://github.com/tofti/python-kmeans/blob/master/results/basic_clustering1.png "Basic Interim")
![basic_final](https://github.com/tofti/python-kmeans/blob/master/results/basic_clustering2.png "Basic Interim")

## Crime
The crime data set (([crime.config](./blob/master/resources/crime.config))) is from [Edureka, here](https://www.edureka.co/blog/implementing-kmeans-clustering-on-the-crime-dataset/).
    


