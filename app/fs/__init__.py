from sklearn import manifold,datasets
from skfeature.function.sparse_learning_based import MCFS
from skfeature.utility import construct_W
from skfeature.utility import unsupervised_evaluation
from sklearn.decomposition import PCA

from ..data.process import dataCal2