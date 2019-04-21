from . import dataCal2, manifold
import numpy as np
from . import MCFS, PCA
from . import construct_W, unsupervised_evaluation
def fs(X, num_fea, num_cluster):
    print('PCA:', X.shape);
    ans = {};
    kwargs = {"metric": "euclidean", "neighborMode": "knn", "weightMode": "heatKernel", "k": 2, 't': 1}
    W = construct_W.construct_W(X, **kwargs)
    # num_fea = 5    # specify the number of selected features
    # num_cluster = 3    # specify the number of clusters, it is usually set as the number of classes in the ground truth
    Weight = MCFS.mcfs(X, n_selected_features=num_fea, W=W, n_clusters=num_cluster)
    idx = MCFS.feature_ranking(Weight)
    selected_features = X[:, idx[0:num_fea]]
    
    ans = {
            'idx': idx.tolist(),
            'selected_features': selected_features.tolist()
            }
    return ans;

def dimReduction(X, opt):
    np.seterr(divide= 'ignore', invalid='ignore')
    np.nan_to_num(X)
    tsne = manifold.TSNE(n_components=opt['n_components'], init='pca', random_state=opt['randomState'], perplexity=opt['perplexity'], early_exaggeration=opt['early_exaggeration'])
    X_tsne = tsne.fit_transform(X)
    print("Org data dimension is {}. Embedded data dimension is {}".format(X.shape[-1], X_tsne.shape[-1]))
    x_min, x_max = X_tsne.min(0), X_tsne.max(0)
    X_norm = (X_tsne - x_min) / ((x_max - x_min) + 1e-40)
    X_norm = X_norm.tolist()
    return X_norm

def getResult(indexes, dimensions, isDataProjection=1 ,randomState=50, perplexity=30, early_exaggeration=12.0):
    #carsData = carsData.split(',')
    #carsData = np.array(carsData, dtype='float')
    #X = np.reshape(carsData, (392, 10))
    np.seterr(divide= 'ignore', invalid='ignore')
    X = dataCal2()
    X = X['data_norm']
    np.nan_to_num(X)
    if dimensions != []:
        X = X[:, dimensions]
    if indexes != []:
        X = X[indexes]
    if isDataProjection == 0:
        X = X.T

    tsne = manifold.TSNE(n_components=2, init='pca', random_state=randomState, perplexity=perplexity, early_exaggeration=early_exaggeration)
    X_tsne = tsne.fit_transform(X)

    print("Org data dimension is {}. Embedded data dimension is {}".format(X.shape[-1], X_tsne.shape[-1]))

    x_min, x_max = X_tsne.min(0), X_tsne.max(0)
    #x_min = x_min    + sys.float_info.min
    #print(X_tsne)
    #print(x_min)
    #print(x_max)
    #print(x_max == x_min)
    #if x_max != x_min:
    X_norm = (X_tsne - x_min) / ((x_max - x_min) + 1e-40)
    X_norm = X_norm.tolist()
    return X_norm

def getPCA(indexes, dimensions, num=5):
   X=dataCal2()
   X = X['data_norm']
   np.nan_to_num(X)
   if dimensions != []:
       X = X[:, dimensions]
   if indexes != []:
       X = X[indexes]
   pca = PCA()
   pca.fit(X)
   X_new = pca.transform(X)
   print(type(X_new.tolist()))
   print(type(X.tolist())) 
   ans = {
#           'new': X_new.tolist(),
           'orgin': X.tolist(),
#           'n_components': pca.components_.tolist(),
#           'ratio': pca.explained_variance_ratio_.tolist(),
#           'var': pca.explained_variance_.tolist(),
#           'score':pca.score(X, y=None),
           'correla':pca.get_covariance().tolist(),
           'fs': fs(X)
           }
   return ans