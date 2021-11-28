## Project Proposal

Last updated: Nov 21st, 2021

-   **About the Data Set and Analysis**

    The Abalone data set that was used in this project was sourced from the UC Irvine Machine Learning Repository published in 1995. It can be found [here](https://archive-beta.ics.uci.edu/ml/datasets/abalone). Each row in the data set represents the attributes and physical measurements of abalones including number of rings, sex, length, diameter, height, weight, etc. The number of rings were counted manually using a microscope by the researchers. The age of an abalone is represented by its number of rings plus 1.5 as number of years lived. **In this project we will focus on classifying whether an abalone is young, i.e. number of rings smaller than or equal to 11, or old, i.e. number of rings is larger than 11, based on the input features.**

    The data set has already removed its missing values and the range of the continuous values have been scaled by dividing by 200 for use.

-   **Predictive Research Question**

    Given the input features (sex, longest shell measurement, diameter perpendicular to length, height with meat in shell, whole weight, weight of meat, gut weight after bleeding, shell weight after being dried), is an abalone young (i.e. number of rings smaller than or equal to 11), or old (i.e. number of rings is larger than 11)?

    -   Some related sub questions includes:

        -   Which features are more important/significant in predicting whether an abalone is old or young?

        -   Are there relationships between these features?

-   **Preliminary Analysis Plan**

    Here is our prelimary analysis plan. Firstly, after the data download, we split the data into train set and test set, perform data wrangling, and perform EDA on the train set features to investigate the relationships between the independent variables used in our model. We then preprocess the data including scaling the numerical features and one-hot-encoding the categorical feature. Next, we fit a Logistic Regression classification model on the data set, tune hyperparameters and evaluate the best performing model on the test set. The final step is creating a full report that shares the analysis results, as structured below.

-   **Report**

    The final report can be found [here](https://UBC-MDS.github.io/abalone_age_classification/README.html). The final analysis report consists of the following components: summary, introduction, methods including data and analysis, results/discussion, future analysis directions/takeaway and references.
