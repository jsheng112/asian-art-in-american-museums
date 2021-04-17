import numpy as np
from sklearn.cluster import KMeans
import os
import joblib
from sklearn.neighbors import KNeighborsClassifier
import pickle
import gzip
from boto.s3.connection import S3Connection
import pandas as pd


class model_pred():
    
    def __init__(self):
        self.files = np.load('cluster_data_small.npy')
        
        s3_connection = S3Connection(ACCESS_KEY, SECRET_KEY)
        s3_bucket = s3_connection.get_bucket('museum-image')
        local_file = 'vgg_feature_vectors_small.pkl'
        s3_bucket.get_key('vgg_feature_vectors_small.pkl').get_contents_to_filename(local_file)
        
        self.feature_vectors = joblib.load(open("vgg_feature_vectors_small.pkl", 'rb'))
        os.remove(local_file)

        local_file = 'knn_model_clusters_small_neighbors_12.pkl'
        s3_bucket.get_key('knn_model_clusters_small_neighbors_12.pkl').get_contents_to_filename(local_file)
        
        self.knn_model = joblib.load(open("knn_model_clusters_small_neighbors_12.pkl", 'rb'))
        os.remove(local_file)
        
        self.kmeans_model = joblib.load(open("kmeans_model_cluster_small.pkl", 'rb'))

                                        


def predictions(query, N, size, models):
    feature = models.feature_vectors[query]
    res = models.knn_model.kneighbors(feature.reshape(1,-1),return_distance=True,n_neighbors=N)
    return ["all_image_data/" + file for file in models.files[list(res[1][0])[1:][:N+1]]]


def main():
    files = list(pd.read_csv("test_images.csv")['filepath'])

    models = model_pred()
    for f in files:
        images = predictions(f, 11, (224, 224), models)
        if not len(images) == 10:
            print(f)

if __name__ == '__main__':
    main()
