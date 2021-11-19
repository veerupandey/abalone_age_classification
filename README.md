---
editor_options: 
  markdown: 
    wrap: 72
---

[**Milestone \# 1: Part 3. Project Proposal**]{.ul}

-   **About the Data set**

    -   Data set name: Abalone -- predict the age of abalone from
        physical measurements

    -   Link: <https://archive-beta.ics.uci.edu/ml/datasets/abalone>

-   **Description:**

    The data set that was used in this project was sourced from the UC
    Irvine Machine Learning Repository published in 1995. It can be
    found here. The age of an abalone is represented by its number of
    rings plus 1.5 as number of years lived. The number of rings were
    counted manually using a microscope by the researchers. Each row in
    the data set represents the attributes and physical measurements of
    the abalone including its sex, length, diameter, height, weight,
    etc. and its number of rings. **In this project we will focus on
    classifying whether an abalone is young, i.e. number of rings
    smaller than or equal to 11, or old, i.e. number of rings is larger
    than 11, based on the input features.** The data set has already
    removed its missing values and the range of the continuous values
    have been scaled by dividing by 200 for use.

    -   Data set license:

        This dataset is licensed under a Creative Commons Attribution
        4.0 International (CC BY 4.0) license. This allows for the
        sharing and adaptation of the datasets for any purpose, provided
        that the appropriate credit is given.

-   **Predictive research question:**

    Predict whether an abalone is young, i.e. number of rings smaller
    than or equal to 11, or old, i.e. number of rings is larger than 11,
    based on the input features (sex, longest shell measurement,
    diameter perpendicular to length, height with meat in shell, whole
    weight, weight of meat, gut weight after bleeding, shell weight
    after being dried).

    -   Sub questions:

        Which features are more important/significant in predicting
        whether an abalone is old or young?

-   **Plan of how we will analyze the data:**

    -   Data download

    -   EDA on the features (Note: do not analyze test data in EDA)

    -   Data preprocessing

    -   Classification with a decision tree (random forest)

    -   Final report on the results

-   **Discussion of at least one EDA table and one exploratory data
    analysis figure we will create that makes sense for the research
    question, the data we have and the analysis we plan to do:**

    -    ![](https://github.com/nickmao1994/abalone_age_classification/blob/main/src/eda/target_viz.png)

-   **How to share the analysis results:**

    -   Generate a full report that consists of

        -   Summary

        -   Introduction

        -   Methods (data, analysis)

        -   Results/discussion (include figures and tables here)

        -   Future analysis directions/takeaway

        -   References
