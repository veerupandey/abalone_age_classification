**Milestone \# 1: Part 3. Project Proposal**

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

    -   Data set license:

        This dataset is licensed under a Creative Commons Attribution
        4.0 International (CC BY 4.0) license. This allows for the
        sharing and adaptation of the datasets for any purpose, provided
        that the appropriate credit is given.

-   **Predictive Research Question**

    Given the input features (sex, longest shell measurement,
    diameter perpendicular to length, height with meat in shell, whole
    weight, weight of meat, gut weight after bleeding, shell weight
    after being dried), is an abalone young (i.e. number of rings smaller
    than or equal to 11), or old (i.e. number of rings is larger than 11)?

    -   Sub questions:

        - Which features are more important/significant in predicting
        whether an abalone is old or young?
        - Are there relationships between these features?

-   **Preliminary Analysis Plan**

    -   Data download

    -   EDA on the features (Note: do not analyze test data in EDA)

    -   Data preprocessing

    -   Classification with a decision tree (random forest)

    -   Final report on the results

-   **Discussion of EDA Table and Exploratory Data Analysis Figure 
    for the Research Question, the Data and the Analysis**
    -    Here are some preliminary EDA figures that we found interesting during our data exploration:
    -    The first EDA is on target distribution in train set. We can observe an unblanced data in target variable.
         ![](https://github.com/nickmao1994/abalone_age_classification/blob/main/src/eda/target_viz.png)
    -    The second EDA is on corrleation heat map. We can observe that most feature variables are highly correlated.
         ![](https://github.com/nickmao1994/abalone_age_classification/blob/main/src/eda/corr_viz.png)
    -    The third EDA is a trend line of length and rings. We can observe that length of young abalones is positively correlated with the rings. But such correlation is barely found in old abalones.
         ![](https://github.com/nickmao1994/abalone_age_classification/blob/main/src/eda/length_reg_viz.png)

-   **How to Share the Analysis Results**

    -   Generate a full report that consists of

        -   Summary

        -   Introduction

        -   Methods
            - Data
            - Analysis

        -   Results/discussion

        -   Future analysis directions/takeaway

        -   References
