# Abalone Age Classifier

Data analysis project for DSCI 522 (Data Science workflows); a course in the Master of Data Science program at the University of British Columbia.

## Authors
- Nick Lisheng Mao
- Beilin Wu (Lynn)
- Kiran Phaterpekar
- Rakesh Pandey


## Introduction
Abalones are endangered marine snails that are found in the cold coastal water around the world. The price of an abalone is positively associated with its age. However, determining how old an abalone is a very complex process. 

In this project we are classifying abalone snails into "young" and "old" according to their number of rings based on input features such as abalone's gender, height with meat in shell, weight of the shell etc.


## Project Proposal

Last updated: Nov 19th, 2021

-   **About the Data Set and Analysis**

    The Abalone data set that was used in this project was sourced from the UC
    Irvine Machine Learning Repository published in 1995. It can be
    found <a href="https://archive-beta.ics.uci.edu/ml/datasets/abalone" >here</a>. Each row in
    the data set represents the attributes and physical measurements of
    abalones including number of rings, sex, length, diameter, height, weight,
    etc. The number of rings were
    counted manually using a microscope by the researchers. The age of an abalone is represented by its number of
    rings plus 1.5 as number of years lived. **In this project we will focus on
    classifying whether an abalone is young, i.e. number of rings
    smaller than or equal to 11, or old, i.e. number of rings is larger
    than 11, based on the input features.** 
    
    The data set has already
    removed its missing values and the range of the continuous values
    have been scaled by dividing by 200 for use.
      

-   **Predictive Research Question**

    Given the input features (sex, longest shell measurement,
    diameter perpendicular to length, height with meat in shell, whole
    weight, weight of meat, gut weight after bleeding, shell weight
    after being dried), is an abalone young (i.e. number of rings smaller
    than or equal to 11), or old (i.e. number of rings is larger than 11)?

    -   Some related sub questions includes:

        - Which features are more important/significant in predicting whether an abalone is old or young?
        
        - Are there relationships between these features?

-   **Preliminary Analysis Plan**

    Here is our prelimary analysis plan. Firstly, after the data download, we perform EDA on the features and investigate the relationships between the independent variables used in the prediction model. We then preprocess the data including scaling the numerical features and one-hot-encoding the categorical feature. Next, after examining the statistical assumptions, we fit a random forest classification model on the data set. The final step is creating a full report that shares the analysis results, as structured below.


-   **Report**

    The final report can be found here. *(Link will be added when a report is finalized.)* The final analysis report consists of the following components: summary, introduction, methods including data and analysis, results/discussion, future analysis directions/takeaway and references.

## Usage
To download the data, run the script below.

```bash
python src/data/data_download.py --url="https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data" --outputfile="data/raw/abalone.data"
```
In case script is called without arguments, arguments will be fetched from config file.

```bash
python src/data/data_download.py
```

## Discussion of EDA Table and Figure
A detailed EDA report can be found here. (**TODO**: Add link to the EDA notebook)

Here are some preliminary EDA table and figures that we found interesting during our data exploration:
- The table below displays the descriptive data analysis to our training data. There is no missing value in our training data.
         ![](https://github.com/nickmao1994/abalone_age_classification/blob/main/src/eda/summary_table.png)
         
- The first EDA is on target distribution in train set. We can observe an unblanced data in target variable.
         ![](https://github.com/nickmao1994/abalone_age_classification/blob/main/src/eda/target_viz.png)
         
- The second EDA is on corrleation heat map. We can observe that most feature variables are highly correlated.
         ![](https://github.com/nickmao1994/abalone_age_classification/blob/main/src/eda/corr_viz.png)
         
- The third EDA is a trend line of length and rings. We can observe that length of young abalones is positively correlated with the rings. But such correlation is barely found in old abalones.
         ![](https://github.com/nickmao1994/abalone_age_classification/blob/main/src/eda/length_reg_viz.png)


## License

This dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license. This allows for the sharing and adaptation of the datasets for any purpose, provided that the appropriate credit is given.


## References

Dua, D. and Graff, C. (2019). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.
