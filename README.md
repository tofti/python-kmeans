# python-kmeans
python implementation of [k-means clustering](https://en.wikipedia.org/wiki/K-means_clustering).

![results](https://github.com/tofti/python-kmeans/blob/master/examples/crime.gif "Crime Example")


# Description

# Resources
+ [edureka example using crime data](https://www.edureka.co/blog/implementing-kmeans-clustering-on-the-crime-dataset/)

+ K-Means is described in [Top 10 Algorithms for Data Mining](https://atasehir.bel.tr/Content/Yuklemeler/Dokuman/Dokuman3_4.pdf);

+ K-Means is outlined [here](http://www.inference.org.uk/mackay/itprnn/ps/284.292.pdf);

+ Professor Andrew Moore of CMU has some good notes [here](https://www.autonlab.org/_media/tutorials/kmeans11.pdf).

## Why not use SciPy?
[SciPy](https://scipy.org/) has a k-means [implementation](https://matplotlib.org/users/installing.html), the objective of this work is to build a bottom up pure python implementation for the purposes of learning the k-means algoritm. 

My hope is others will find this implementation helpful for understanding k-means, also. It is not by any means intended for production use :)

## Running the code

### Prerequisites
This code depends on matplotlib. See [here](https://matplotlib.org/users/installing.html) for installation instructions.

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
    + prefix for png files created during the process, if this isn't specified, images will not be produced in the working directory;
    + the individual plot configurations, limited to 2 dimensions per plot.

 
### Examples
1. crime.sample.config uses the crime data [here](https://www.edureka.co/blog/implementing-kmeans-clustering-on-the-crime-dataset/).

### Results

