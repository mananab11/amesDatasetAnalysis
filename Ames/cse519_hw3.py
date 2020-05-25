# -*- coding: utf-8 -*-
"""CSE519_HW3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ElerGk-2ICtq85xuxv0qGqmXUwUsiF-H

# Homework 3 - Ames Housing Dataset
"""

from google.colab import drive
drive.mount('/content/drives')

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import seaborn as sns 
from sklearn.linear_model import LogisticRegression 
from sklearn import metrics 
from sklearn.metrics import accuracy_score 
from IPython.display import Image
import statsmodels.api as sm
from sklearn import ensemble
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import permutation_test_score
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
# %matplotlib inline
encoder=LabelEncoder()

pd.set_option('display.max_rows',None)

'''Importing Data files'''
full_df=pd.read_csv('/content/drives/My Drive/DataScience/HomeWork3/Data/train.csv')
original_df=full_df.copy()
fullTestData_df=pd.read_csv('/content/drives/My Drive/DataScience/HomeWork3/Data/test.csv')

"""For all parts below, answer all parts as shown in the Google document for Homework 3. Be sure to include both code that justifies your answer as well as text to answer the questions. We also ask that code be commented to make it easier to follow."""

'''PreProcessing'''
#Columns with nan values
columnswithNAN=full_df.columns[full_df.isna().any()].tolist()
##testfile##
columnswithNAN_test=fullTestData_df.columns[fullTestData_df.isna().any()].tolist()
#columns where nan values not to be replaced with generic 'not present' 
nan_notTobeReplaced=['LotFrontage','GarageYrBlt','MasVnrArea']
nan_notTobeReplacedInTestFile=['LotFrontage','GarageYrBlt','MasVnrArea','BsmtFinSF1','BsmtUnfSF','BsmtFinSF2','TotalBsmtSF','BsmtFullBath','BsmtHalfBath','GarageCars']
#############################columns where nan to be replaced by generic 'not present'#################################
columns_replacedNAN=[item for item in columnswithNAN if item not in nan_notTobeReplaced]
full_df[columns_replacedNAN]=full_df[columns_replacedNAN].replace(np.nan, 'not present', regex=True)
##test file ##
fullTestData_df[columnswithNAN_test]=fullTestData_df[columnswithNAN_test].replace(np.nan, 'not present', regex=True)
lst=['MasVnrArea','GarageYrBlt','LotFrontage']
full_df[lst]=full_df[lst].replace(np.nan,-999,regex=True)
##Test file##
fullTestData_df[nan_notTobeReplacedInTestFile]=fullTestData_df[nan_notTobeReplacedInTestFile].replace(np.nan,-999,regex=True)
dataFrame_forPlots=full_df.copy()

#Label Encoding
#getting non numeric columns
columns_nonNumeric=full_df.select_dtypes(exclude=[np.number]).columns.tolist()
#encoding each column
for col in columns_nonNumeric:
  full_df[col]=encoder.fit_transform(full_df[col].astype('str'))  
columns_nonNumeric_test=fullTestData_df.select_dtypes(exclude=[np.number]).columns.tolist()
#######test file##########
for col in columns_nonNumeric_test:
  fullTestData_df[col]=encoder.fit_transform(fullTestData_df[col].astype('str'))

full_df.LotFrontage = full_df.groupby('Neighborhood')['LotFrontage'].transform(lambda x: x.fillna(x.median()))
full_df.GarageYrBlt = full_df.groupby('Neighborhood')['GarageYrBlt'].transform(lambda x: x.fillna(x.median()))
full_df.MasVnrArea = full_df.groupby('Neighborhood')['MasVnrArea'].transform(lambda x: x.fillna(x.median()))

"""## Part 1 - Pairwise Correlations"""

#Features to be extracted from original data frame for correlation analysis
interesting_features=['TotRmsAbvGrd','TotalBsmtSF','GarageArea','1stFlrSF','2ndFlrSF','BedroomAbvGr','SalePrice','LotFrontage','MSSubClass',
                      'YearBuilt','OverallQual','MSZoning','GarageYrBlt','BldgType','Neighborhood','OverallCond']
#extracting the above features from original data frame
interesting_df=full_df.filter(interesting_features)
#correlation matrix
interesting_df.corr(method='pearson')

#HeatMap Plot
plt.figure(figsize=(14,7))
heatmap=sns.heatmap(interesting_df.corr(),annot=True,cmap=plt.cm.Reds)
plt.show()

"""Most Positive Correlation is between the following pairs:

*   TotalBsmtSF vs 1stFlrSF  : r=0.82
*   OverallQual vs SalePrice : r=0.79
*   BldgType vs MSSubClass   : r=0.75
Most negative Correlation is between the following pairs:
*   Loft Frontage vs BldgType:  r=-0.45
*   LoftFrontage vs MsSubClass: r=-0.39
*   MSZoning vs YearBuilt  : r=-0.31
*   MSZoning vs Neighborhood : r=-0.25

> Seeing the correaltion coefficients, it is natural to see higher coefficient value between overall quality and the selling price
"""

# TODO: show visualization
matplotlib.rcParams['figure.figsize'] = (14.0, 4.0)
plt.hist(full_df.MSSubClass, density=True, bins=100)
plt.ylabel('Frequency');
plt.xlabel('MSSubclass');

"""## Part 2 - Informative Plots"""

# TODO: code to generate Plot 1
#yearbuilt and saleprice
plt.figure(figsize=(17,7))
plt.subplot(2, 1, 1) 
#Count of sales in each neighborhood
frame=dataFrame_forPlots.groupby('Neighborhood').count().reset_index()
plt.plot(frame['Neighborhood'],frame['SalePrice'])
plt.xlabel("Neighborhood")
plt.ylabel("Count Sold")
plt.tight_layout()
#Mean price vs Neighborhood 
plt.subplot(2, 1, 2) 
frame=dataFrame_forPlots.groupby('Neighborhood').mean().reset_index()
plt.plot(frame['Neighborhood'],frame['SalePrice'])
plt.xlabel("Neighborhood")
plt.ylabel("Mean Sale Price")
plt.tight_layout()

"""What interesting properties does Plot 1 reveal?


*   Mean Sale Price is the highest in the neighborhood NoRidge followed by NridgHt
*   With the lowest mean price in neighborhoods of IDOTRR and MeadowV
*   However,seeing the first graph(Count sold vs Neighborhood),we can see that neighborhood with highest mean sale price doesn't necessarily correlate with more number of houses sold.
*   It is the NAmes neighborhood with highest number of sales and Blueste with least count of sales.
"""

# TODO: code to generate Plot 2
dataFrame_forPlots.plot(kind='scatter',x='YearBuilt',y='BsmtFinSF1',color='green',figsize=(10,5))

"""What interesting properties does Plot 2 reveal?


> This plot is between Basement area measured in square feet and Year built.It is interesting to see a gradual increase in the area of houses from mid 1950's.But still most of the houses over this period were scattered in areas under 1000 sqfeet  with some between 1000 and 2000 sqFeet.There was one outlier with over 5000sqFeet of basement area.
"""

# TODO: code to generate Plot 3
dataFrame_forPlots.plot(kind='scatter',x='YearBuilt',y='1stFlrSF',color='blue',figsize=(10,5))
#year sold  as bar graph

"""What interesting properties does Plot 3 reveal?


> The trend for 1st floor area over the period from 1880's to 2000 doesn't follow the expected pattern of basement area.The area if much more sparse and can be seen to have an widening open channel pattern with some periods where more houses have lesser area on 1st floor as compared to previous years.There are some periods where either data is missing or no houses had first floor,and the former conclusion seems likely.
"""

# TODO: code to generate Plot 4
ax=dataFrame_forPlots.plot(kind='scatter',x='BsmtFinSF1',y='SalePrice',color='red',figsize=(10,5),label='basement area')
dataFrame_forPlots.reset_index().plot(kind='scatter',x='1stFlrSF',y='SalePrice',color='green',label='First Floor area',figsize=(10,5),ax=ax)

"""What interesting properties does Plot 4 reveal?


> The plot between the sale price and 1st floor area seems to folow a linear line with most of the sales under 3000000.The price of houses increases much more steeply as area of the first floor goes above 1800 sqFeet.It also reveals people  houses under 2000 sqFeet first floor areaa and price under 2500000 are more popular amongst the populace.There are some outliers with high area but still low price which seems unlikely seeing just these two features but could be justified if for example,overall condition of house isn't good.
"""

# TODO: code to generate Plot 5
plt.figure(figsize=(14,7))
a=plt.hist(dataFrame_forPlots['MSSubClass'],bins=100)
plt.xlabel('MSubclass- type of dwelling involved in the sale')
plt.figure(figsize=(14,7))
b=plt.hist(dataFrame_forPlots['YearBuilt'],bins=100)
plt.xlabel('Construction Frequency over the Years')
plt.figure(figsize=(14,7))
neigborhood_unique=dataFrame_forPlots.Condition1.unique()
for neighbor in neigborhood_unique:
  a=dataFrame_forPlots[dataFrame_forPlots['Condition1']==neighbor]
  (a.YearBuilt).hist(alpha=0.7,label=neighbor)
plt.legend()
plt.xlabel('Proximity to various conditions')
plt.tight_layout

"""What interesting properties does Plot 5 reveal?

> MSSubClass identifies the type of dwelling involved in the sale.
From graph it can be seen that 1-STORY 1946 & NEWER ALL STYLES has the maximum frequency.Also overall it can be seen that 2000 era has been where most houses have been built.
Seeing the plot of Condition(Proximity to various conditions) over the years ,it is seent that Normal condition has always been the most common amongst the houses built with it peaking in 2000's.There was period in 1960's where Feedr(Adjacent to feeder street) were the second most frequently built with a wide margin between it nand the third and it being overtaken by Artery type in 2000's for the second position.

## Part 3 - Handcrafted Scoring Function
"""

#features selected for calculating final score
list_ofFeatures_forScoring=['LotFrontage','LotArea','OverallQual','YearBuilt','YearRemodAdd','BsmtFinSF1','1stFlrSF','GrLivArea','BsmtFullBath','FullBath','HalfBath'
                           'BedroomAbvGr','KitchenAbvGr','TotRmsAbvGrd','GarageCars','SalePrice','OverallCond']                           
forScoring_df=dataFrame_forPlots.filter(list_ofFeatures_forScoring)
##Assign weight to features##
col_weight_dict={'OverallQual':0.3,'OverallCond':0.05,'YearRemodAdd':0.06,'BsmtFinSF1':0.06,'GrLivArea':0.066,'1stFlrSF':0.067}
#YearBuilt weight based on age ,improve weight if ancient; else reduce
forScoring_df['YearBuilt']=forScoring_df.YearBuilt.apply(lambda x: x*0.1 if (x<1920)  else x*0.066 )
#Apply weights
for col in forScoring_df.columns:
  if col=='YearBuilt':
    continue
  elif col in col_weight_dict:
    w=col_weight_dict.get(col)
    forScoring_df[col]=forScoring_df[col].apply(lambda x:x*w)
  else:
    forScoring_df[col]=forScoring_df[col].apply(lambda x:x*0.045)

#Compute ZScore for all columns 
for col in forScoring_df.columns:
  forScoring_df[col]=(forScoring_df[col] - forScoring_df[col].mean())/forScoring_df[col].std(ddof=0)

#Create column with final scores for each house
forScoring_df['Final_Score']=forScoring_df.sum(axis=1)

#combining Id of houses with scored data frame
forScoring_df.insert(0, 'Id', full_df.Id)

#Presenting Scores vs ID
id_score_df=pd.DataFrame(forScoring_df.Final_Score.sort_values(ascending=False))
id_score_df.head(7)

"""What is the ten most desirable houses?


> Based on the built scoring function the following houses are most desirable in terms of value:




1.   ID number 1298
2.   ID number 313
1.   ID number 1182
1.   ID number 523
2.   ID number 691
6.   ID number 1169
1.   ID number 769
1.   ID number 185
2.   ID number 898
10.  ID number 440

What is the ten least desirable houses?


> Based on the built scoring function the following houses are least desirable in terms of value:




1.   ID number 533
2.   ID number 375
1.   ID number 636
1.   ID number 916
2.   ID number 1100
6.   ID number 393
1.   ID number 1321
1.   ID number 1035
2.   ID number 1325
10.  ID number 1218

Describe your scoring function and how well you think it worked.


> The scoring function did a decent job taking into account the value of a property.It combined multiple features and weighed them with certain values ,positive( if feature added to the value of property) and negative (if feature brought down the value of the property).This value is used as the measure for desirability.The value was  majorly regulated by the "Overall Quality"(positive) and "SalePrice"(negative) features.Increasing salePrice reduced the value of the score.
Data preprocessing is done before calculating the final score.Z-score is calculated for individual columns and then weights are applied to each  of them.Finally score is calculated by linear sum of all the column values in each row.

> All the  features used  by this function are :'LotFrontage','LotArea','OverallQual','YearBuilt','YearRemodAdd','BsmtFinSF1','1stFlrSF','GrLivArea','BsmtFullBath','FullBath','HalfBath'                  'BedroomAbvGr','KitchenAbvGr','TotRmsAbvGrd','GarageCars','SalePrice','OverallCond'

> This scoring function is limited :it uses only numerical value and encoded features.
The weights applied to features are not optimal and can be further optimized based on reinforcement learning or in some other way.

## Part 4 - Pairwise Distance Function
"""

#distance function using Euclidean distance
data_euclidean =full_df.copy()
newdf_euc=pd.DataFrame(squareform(pdist(data_euclidean)))
newdf_euc.head(3)

#distance function using cosine similarity
data=full_df.copy()
data.drop(['Neighborhood'],axis=1,inplace=True)
for col in data.columns:
  data[col]=(data[col] - data[col].mean())/data[col].std(ddof=0)
newdf_cos=pd.DataFrame(squareform(pdist(data, metric='cosine')))
newdf_cos.head(3)

#Normalizing and further dropping some features seems to improve the function
data1=full_df.copy()
furtherlstToDrop=['Neighborhood','LotConfig','SalePrice','YearBuilt','YearRemodAdd','MasVnrArea']
for col in furtherlstToDrop:
    data1.drop([col],axis=1,inplace=True)
for col in data1.columns:
  data1[col]=(data1[col] - data1[col].mean())/data1[col].std(ddof=0)
newdf_norm=pd.DataFrame(squareform(pdist(data1, metric='cosine')))
newdf_norm.head(3)

"""How well does the distance function work? When does it do well/badly?


> 
For House with ID 4 should be closer to ID 1 as compared to ID 5.This is also confirmed by seeing that 4 and 1 belong to the adjacent neighborhoods while ID 4 is farther away.However, our distance function shows the reverse,that is 5 being closer to 1 instead of 4.Possible reason could be the data difference in YearBuilt and YearRemod features.Also some features which shouldn't weigh more on the distance function should be removed as is done above in the code.These features negatively affect the similarity computation. Removing these features improves the distance score as can be seen in comparing the ID 4 ,5 and 1 again after removing these features.We can't generalize this conclusion for whole data set but it gives a decent improvement over the calculating similarity based on all the features.
Cosine  produced better results rather than mere euclidean distance computation.

## Part 5 - Clustering
"""

clustering = AgglomerativeClustering(affinity='precomputed',                         
                        linkage='complete', n_clusters=24)
clustering.fit(newdf_euc.values)
Cluster=clustering.labels_
print(type(clustering.labels_))
df = pd.DataFrame(clustering.labels_,columns=['ClusterLabel'])
plt.scatter(newdf_euc.values[:,0],newdf_euc.values[:,1],c=Cluster,cmap='rainbow')
plt.legend()
df.insert(0,'Id',full_df.Id)
##########Cluster based on  normalized data#################
fig = plt.figure(figsize=(15,10))
ax = fig.add_subplot(111)
scatter = ax.scatter(newdf_norm.values[:,0],newdf_norm.values[:,1],
                     c=Cluster,s=50)
ax.set_title('Clustering')
ax.set_xlabel('Cluster')
ax.set_ylabel('SalePrice')
plt.colorbar(scatter)

cluster_df=full_df.copy()
cluster_df.insert(0,'cluster',Cluster)
cluster_df.groupby('Neighborhood')['cluster'].unique()

cluster_df.head(10)
plt.scatter(cluster_df.Neighborhood,cluster_df.cluster,c=Cluster,cmap='rainbow')

'''
sample_df=full_df.copy()
def doAgglomerative(X, nclust=2):
    model = AgglomerativeClustering(n_clusters=nclust, affinity = 'cosine', linkage = 'complete')
    clust_labels = model.fit_predict(X)
    return (clust_labels)

clust_labels = doAgglomerative(sample_df.values, 20)
agglomerative = pd.DataFrame(clust_labels)
#sample_df.insert((sample_df.shape[1]),'agglomerative',agglomerative)
'''

'''
fig = plt.figure()
ax = fig.add_subplot(111)
scatter = ax.scatter(sample_df.values[:,0],sample_df.values[:,1],
                     c=clust_labels,s=50)
ax.set_title('Agglomerative Clustering')
ax.set_xlabel('Cluster')
ax.set_ylabel('SalePrice')
plt.colorbar(scatter)
'''

"""How well do the clusters reflect neighborhood boundaries? Write a discussion on what your clusters capture and how well they work.


>It is verified by seeing that the ID's of houses in the same cluster are present in the same Neighborhood,although there are many cases where clustering label is different than the actual Neighborhood.
Also majority of label are clustered in Neighborhood of 4,7,16 and 23 which are the label encoded vaues of Neighborhoods. 
Created 15 clusters for the properties.The properties have been segregated into the clusters as desired.The clusters have been formed through agglomerative algorithm.All the features were normalized and a distance matrix was calculated.It was a pairwise distance between individual housing ID's.The matrix being multidimensional couldn't be fed to the more general algorithms.So ,the agglomerative was used with input as the precomputed distance matrix. It took in all the features of the properties and based on the distance matrix it clustered the properties into same clusters.


> The clustering didn't work as expectd for the normalized data however ,it showed certain distinct clusters when seen in the graph plotted immediately after clustering algorithm.

## Part 6 - Linear Regression
"""

# TODO: code for linear regression

regressor = LinearRegression()
linear_dfFrame=full_df.corr()
cor_target = linear_dfFrame["SalePrice"]
#Selecting highly correlated features
features_upperbound = cor_target[cor_target>0.22]
features_lowerbound = cor_target[cor_target<-0.56]
#Features filtered based on correlation
featuresTobeFiltered=features_upperbound.index.tolist()+features_lowerbound.index.tolist()
newFrameForRegression=full_df.filter(featuresTobeFiltered)
fullTestData_df_filtered=fullTestData_df.filter(featuresTobeFiltered)

y=newFrameForRegression.SalePrice.copy() 
X=newFrameForRegression.drop('SalePrice', axis=1) 
#splitting training data in 70% 30% ratio
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=1) 
#Training the model 
model=regressor.fit(X_train, y_train) 

#prediction the algorithm
y_pred=regressor.predict(X_test)

print('Variance score: %.2f' % regressor.score(X_test, y_test)) 
accuracy = regressor.score(X_test,y_test)
print(accuracy*100,'%')
df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print("Most Important features:",featuresTobeFiltered)
df.head(15)

"""How well/badly does it work? Which are the most important variables?


> With linear regression model , taking in the most significant features,the variance score is around 85%.Comparing the actual and predicted SalePrice,it is evident that the model has worked done a decent job at estimating the price.
The most important variables have been filtered based on their correlation values with SalePrice ,above 0.25 and below -0.5.

> The variables used here are:
'LotArea', 'OverallQual', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea', 'Foundation', 'BsmtFinSF1', 'TotalBsmtSF', 'CentralAir', '1stFlrSF', '2ndFlrSF', 'GrLivArea', 'FullBath', 'HalfBath', 'TotRmsAbvGrd', 'Fireplaces', 'GarageYrBlt', 'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF', 'SalePrice', 'ExterQual', 'BsmtQual', 'KitchenQual', 'GarageFinish'



> OverallQual is a significant feature in predicting the SalePrice and the variance score is 0.85

## Part 7 - External Dataset
"""

# TODO: code to import external dataset and test
'''extern_df=pd.read_csv('/content/drives/My Drive/DataScience/HomeWork3/Data/housing.csv')

matplotlib.rcParams['figure.figsize'] = (14.0, 4.0)

#extern_df.hist()
extern_df['total_bedrooms']=extern_df['total_bedrooms'].replace(np.nan,-999,regex=True)
plt.hist(extern_df.median_income, density=True, bins=100)
plt.ylabel('Frequency')
plt.xlabel('MSSubclass')
#extern_df.head(10)

original_df.Neighborhood.unique()
'''
#Reading in external data set
extern_df=pd.read_csv('/content/drives/My Drive/DataScience/HomeWork3/Data/cpi_index.csv')
extern_df['Inflation']=extern_df['Inflation'].replace(np.nan,0,regex=True)#replacing nan values
extern_df.head(15)

#Changing object type to DateTime
extern_df['Date'] = pd.to_datetime(extern_df['Date'])
extern_df['YrSold']= extern_df['Date'].dt.year
#caluclating mean cpi for each year
cpi_df=pd.DataFrame(extern_df.groupby(['YrSold'])['Inflation'].mean().reset_index()) 
cpi_df.head()

test_df=full_df.copy()
#joining the two data frames
test_df1=test_df.merge(cpi_df, on="YrSold",how='left')
#mutiplying the Inflation Adjustment Factor to the sale price
test_df1['newSalePrice'] = test_df1['SalePrice']*(1+((test_df1['Inflation'])/100)) 
df = pd.DataFrame({'Actual salePrice': test_df1.SalePrice, 'New Estimate': test_df1.newSalePrice})
df.head()

"""Describe the dataset and whether this data helps with prediction.


> The data set is taken from the CPI which takes into acount the month wise inflation over period of years.Tha dataset has Date as object type ,Index  and Inflation over the date period.The inflation values can be used to estimate the inflation adjusted salePrice of each property using the inflation value provided over the period of it being sold.The inflation is used to calculate Inflation Adjustment Factor and is multiplied to get the new estimated salePrice.This additional feature is gonna improve the predictions as we get much more realistic,uniform (inflation adjusted) and upto date salePrice for the properties.

## Part 8 - Permutation Test
"""

# TODO: code for all permutation tests
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error

svr= SVR(kernel='linear')
originaldf_copy=full_df.copy()
y_trgfeature = np.log(originaldf_copy["SalePrice"])
tendifferent_variables=['MiscVal','Condition2','Utilities','PoolArea','LotShape','Foundation','BsmtFinSF1','TotalBsmtSF','GarageFinish','OverallQual','CentralAir','TotRmsAbvGrd','ExterQual','SaleCondition','LotArea']
for eachFeature in tendifferent_variables:
  X_indfeature=originaldf_copy.filter([eachFeature])
  #splitting training data in 70% 30% ratio
  X_train, X_test, y_train, y_test = train_test_split(X_indfeature, y_trgfeature, test_size=0.3,random_state=1) 
  model = sm.OLS(y_train, X_train).fit()
  predictions = model.predict(X_test) # make the predictions by the model

  #  permutation  tests 
  print("Pvalue of ",eachFeature,model.pvalues[0])

  #permutation score 
  target=originaldf_copy["SalePrice"]
  xx=X_indfeature
  xx.to_numpy()
  target.to_numpy()
  score, permutation_scores, pvalue = permutation_test_score(
        regressor, xx, target,cv=3,n_permutations=100, n_jobs=-1)
  print("score",score)
  print("pval with  permutations ",eachFeature,pvalue)
  #print("permutation",permutation_scores)
  ############Plots########################
  plt.hist(permutation_scores, 30, label='Permutation scores')
  ylim = plt.ylim()
  plt.plot(2 * [score], ylim, '--g', linewidth=3,
         label='Classification Score'
         ' (pvalue %s)' % pvalue)
  classes_n = np.unique(target).size
  plt.plot(2 * [1. / classes_n], ylim, '--k', linewidth=3, label='Luck')
  #plt.ylim(ylim)
  plt.legend()
  plt.xlabel('Score')
  plt.show()

"""Describe the results.


> Seeing the permutation results for chosen ten variables ,it can be seen that feature "MiscVal" has p-value above 0.05, 0.0079 to be exact and thus can be considered insignificant for our distribution.A pvalue under 0.05 is considered statically significant,that is there is lesser chance that it happened by chance.Single variable regression is done and pvalues are received after 100 permuations on the outcome.The more the value tends towards zero ,the better the significance is of that particular feature for the regression model.

## Part 9 - Final Result
"""

#finaltraindata_df=full_df.copy()
y=newFrameForRegression.SalePrice.copy() 
X=newFrameForRegression.drop('SalePrice', axis=1) 
#splitting training data in 70% 30% ratio
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=1) 
#Training the model 
model=regressor.fit(X_train, y_train) 
y_pred=regressor.predict(X_test)
print('Variance score: %.2f' % regressor.score(X_test, y_test)) 
accuracy = regressor.score(X_test,y_test)
print(accuracy*100,'%')
#Prdeicting for actual test Data already read in.  
final_prediction=regressor.predict(fullTestData_df_filtered) 

# The mean squared error
print("Mean squared error: %.2f"% mean_squared_error(y_test, y_pred))
# variance score: 1 is perfect prediction
print('Test Variance score: %.2f' % r2_score(y_test, y_pred))

#Output the predicted isFraud values in csv file with TransactionID 
out=pd.DataFrame(final_prediction,fullTestData_df.Id,['SalePrice']) 
out.to_csv('/content/drives/My Drive/DataScience/HomeWork3/Data/out.csv')

"""> Using linear regression we got variance of 0.85 for this data.So i used Gradient boost which does cascading boosting and results in much better variance score of 0.92 as seen from the output below."""

params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2,
          'learning_rate': 0.01, 'loss': 'ls'}

gradient_boosting_regressor = ensemble.GradientBoostingRegressor(**params)

gradient_boosting_regressor.fit(X_train, y_train)
y_pred=gradient_boosting_regressor.predict(X_test)
print('Variance score: %.2f' % gradient_boosting_regressor.score(X_test, y_test)) 
accuracy = gradient_boosting_regressor.score(X_test,y_test)
print(accuracy*100,'%')
final_prediction_withBoost=regressor.predict(fullTestData_df_filtered)

out=pd.DataFrame(final_prediction_withBoost,fullTestData_df.Id,['SalePrice']) 
out.to_csv('/content/drives/My Drive/DataScience/HomeWork3/Data/out_boost.csv')

from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor

y=full_df.SalePrice.copy() 
X=full_df.drop('SalePrice', axis=1) 
#splitting training data in 70% 30% ratio
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=1) 

regressor = RandomForestRegressor(n_estimators=1000, random_state=0)
regressor.fit(X_train, y_train)
y_pred = regressor.predict(fullTestData_df)
print('Variance score: %.2f' % regressor.score(X_test, y_test)) 

out=pd.DataFrame(y_pred,fullTestData_df.Id,['SalePrice']) 
out.to_csv('/content/drives/My Drive/DataScience/HomeWork3/Data/out_random1.csv')

from lightgbm import LGBMRegressor
lightgbm = LGBMRegressor(objective='regression', 
                                       num_leaves=4,
                                       learning_rate=0.01, 
                                       n_estimators=5000,
                                       max_bin=200, 
                                       bagging_fraction=0.75,
                                       bagging_freq=5, 
                                       bagging_seed=7,
                                       feature_fraction=0.2,
                                       feature_fraction_seed=7,
                                       verbose=-1
                                       )
newFrameForRegression=full_df.filter(featuresTobeFiltered)
fullTestData_df_filtered=fullTestData_df.filter(featuresTobeFiltered)
#LGBMRegressor
y=newFrameForRegression.SalePrice.copy() 
X=newFrameForRegression.drop('SalePrice', axis=1) 
lightgbm.fit(X, y)
preds_lightgbm = lightgbm.predict(fullTestData_df_filtered)
out_lightgbm = pd.DataFrame(preds_lightgbm, fullTestData_df.Id,['SalePrice'])
out_lightgbm.to_csv('/content/drives/My Drive/DataScience/HomeWork3/Data/out_lgbm1.csv')