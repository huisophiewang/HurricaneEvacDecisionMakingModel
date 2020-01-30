import pandas as pd

# fp = 'data/Ivan_common_only_subjective.csv'
# df = pd.read_csv(fp)
# total = len(df)
# print total
# print sum(df['evac'])
# evac_cat2 = total - sum(df['sf_cat2_wind_water'])
# evac_cat3 = total - sum(df['sf_cat3_wind_water'])
# evac_cat4 = total - sum(df['sf_cat4_wind_water'])
# print evac_cat2
# print evac_cat3
# print evac_cat4
# 
# print total - sum(df['sf_cat2_water'])
# print total - sum(df['sf_cat3_water'])
# print total - sum(df['sf_cat4_water'])


from sklearn.datasets import load_iris
from sklearn.decomposition import FactorAnalysis
iris = load_iris()
X, y = iris.data, iris.target
res = FactorAnalysis(n_components=3, random_state=0).fit(X)
print res.components_