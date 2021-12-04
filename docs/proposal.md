## Project Proposal

Last updated: Nov 21st, 2021

-   **About the Data Set and Analysis**

    The Abalone data set that was used in this project was sourced from the UC Irvine Machine Learning Repository published in 1995. It can be found [here](https://archive-beta.ics.uci.edu/ml/datasets/abalone). Each row in the data set represents the attributes and physical measurements of abalones including number of rings, sex, length, diameter, height, weight, etc. The number of rings were counted manually using a microscope by the researchers. The age of an abalone is represented by its number of rings plus 1.5 as number of years lived. **In this project we will focus on classifying whether an abalone is young, i.e. number of rings smaller than or equal to 11, or old, i.e. number of rings is larger than 11, based on the input features.**

    The data set has already removed its missing values and the range of the continuous values have been scaled by dividing by 200 for use.

-   **Predictive Research Question**

    Given the physical measurements of an abalone, is an abalone young (i.e. number of rings smaller than or equal to 11), or old (i.e. number of rings is larger than 11)?

    -   Some related sub questions includes:

        -   Which features are more important/significant in predicting whether an abalone is old or young?

        -   Are there relationships between these features?

-   **Preliminary Analysis Plan**

    Here is our prelimary analysis plan. Firstly, after the data download, we split the data into train set and test set and perform data wrangling that includes creating the "Is Old" target variable that identifies an abalone's age. We then perform EDA on the training data to investigate the relationships across the independent variables, as well as differences between young and old abalones. Next, since we are dealing with a binary classification problem, we decide to fit a Logistic Regression model on the data set. In this project, we choose Logistic Regression model since it is easier to implement, interpret, and very efficient to train when compared to other models. Due to limited time span of this project, we will not be testing the data with other models. Before we fit the model, we preprocess the data including scaling the numerical features and one-hot-encoding the categorical feature. When fitting a Logistic Regression model to classify the abalone ages, we use random search cross validation to find the best performing hyperparameter and evaluate the best performing model on the test set on various scores. We also examine the feature importance by looking at their coefficients in the logistic model. The final step of this project is creating a Jupyter Book report that shares the analysis results.

-   **Report**

    The final report can be found [here](https://UBC-MDS.github.io/abalone_age_classification/README.html).
