#%%
from . import anomaly_detection as ad
from . import anomaly_libs as al
from . import anomaly_data_preprocessing as adp

#%%
original_data = "syntethic_original.csv"
original_DF = al.pd.read_csv(original_data, sep=";")

data_file = "synthetic_input_data.csv"
data_set = al.pd.read_csv(data_file, sep=";")

input_DF = data_set.copy()

features = "demand_quantity"

available_models = ['DBSCAN', 'IsolationForest', 'ThymeBoost', 'TADGAN', 'LOF', 'OCSVM']

# %%
# If labels are provided - we can compute the performance metrics, otherwise return only labels
class AnomalyDetection():
    # must have: data_set, id_column, time_column, time_format, labels - if any

    
    def __init__(self, data_set, id_column, time_column, time_format, models=['full'], labels=False):
        self.data_set = data_set
        self.labels = labels
        self.id_column = id_column
        self.time_column = time_column
        self.time_format = time_format
        self.models = models
        self.dbscan_eps = 0.2 
        self.dbscan_n_samples = 5
        self.iforest_contamination = 0.07
        self.ocsvm_kernel = 'linear'
        self.ocsvm_nu = 0.6 
        self.lof_alg = 'auto'
        self.threshold = 0.7
        self.tadgan_epochs = 4
        self.tadgan_limit = 3
        self.thyme_boost_p = 12
        self.final_df = 0
        self.full_df = 0
        self.performance_df = 0
            
    
        #python_version = al.platform.python_version()
        #splitted_version = python_version.split('.')
        #joined_version = float('.'.join(splitted_version[0:2]))
        #if self.models == ['full'] or 'TADGAN' in models:
        #    if joined_version > 3.7:
        #        print(f"Using Python's current version {python_version} it won't be possible to fit TADGAN, for that you need Python 3.7 \n Skipping TADGAN")
        #        self.models = self.models.remove('TADGAN')
        #    else:
        #        print("All good we can run on a full speed!")
        #        self.models = ['dbscan', 'iforest', 'ThymeBoost', 'ocsvm', 'lof']#, 'tadgan']

        if self.models == ['full']:
             self.models = ['dbscan', 'iforest', 'ThymeBoost', 'ocsvm', 'lof']


    # This function will find the best parameters for the given data so that the user can get the best results
    def find_parameters(self):

        print("--------------------------\n\t\t Here will be a progress bar\n--------------------------")
        #def find_parameters(input_DF, time_column, time_format, features, labels, id_column, models=['full']):
        """
        input_DF - the DF with true labels
        true_outlier - the column with true labels
        """
        data_set = input_DF[[self.time_column, self.id_column, features]]
        # Detrending and deseasoning the data
        #detrended_df = adp.detrend(data_set, self.id_column, self.time_column, self.time_format)
        #deseasonalized_df = adp.deseasone(detrended_df, self.id_column, self.time_column, self.time_format)

        self.data_set = data_set#deseasonalized_df
        self.dbscan_eps = adp.find_eps(self.data_set[[features]])
        self.dbscan_n_samples = adp.find_min_samples(self.data_set)
        self.thyme_boost_p = adp.find_seasonal_period(self.data_set[[self.time_column]])

        if self.labels!=False:
            self.ocsvm_kernel, self.ocsvm_nu = adp.parameters_oc_svm(self.data_set[[features]], self.data_set[self.labels]) 
            self.lof_alg = adp.parameters_lof(self.data_set[[features]], self.data_set[self.labels])
        else:
            print("Sorry can't find best parameters for OCSVM and LOF. But you can provide your inputs")
        
        print(f"Suggested parameters are:\nDBSCAN_epsilon={self.dbscan_eps}\nDBSCAN_n_samples={self.dbscan_n_samples}\nOCSVM kernel={self.ocsvm_kernel}\nOCSVM nu={self.ocsvm_nu}\nLOF algorithm={self.lof_alg}\nThymeBoost p={self.thyme_boost_p}")


    # This function will detect anomalies within the given data. It will return a table with each model's performance as well as final labels of the app. 
    def find_anomalies(self):
        """
        data_set - the input data (data in which anomalies should be detected) [params: NxM dataset]
        id_column - index column or the column with distinct names
        time_column - the base data column. The most important date column [series/feature]
        time_format - needed to check the seasonality and trend [params ex: YYYY-MM-DD]
        """
        print("--------------------------\n\t\t Here will be a progress bar\n--------------------------")
        full_df = self.data_set.copy()
        work_data_set = self.data_set[['yyyymm', "spare_part_id", "demand_quantity"]]

        models = full_df.columns.values.tolist()
        #print(work_data_set)
        #spare_parts = work_data_set[self.id_column].drop_duplicates()
        print(self.models)

        parameters = {
            "id":self.id_column, 
            "time_column":self.time_column, 
            "models":self.models, 
            "threshold":self.threshold, 
            "eps":self.dbscan_eps, 
            "min_samples":self.dbscan_n_samples, 
            "contamination":self.iforest_contamination, 
            "p":self.thyme_boost_p, 
            "k":self.ocsvm_kernel, 
            "nu":self.ocsvm_nu, 
            "alg":self.lof_alg, 
            "e":self.tadgan_epochs, 
            "l":self.tadgan_limit}

        results_df, results_dict = ad.get_labels(work_data_set, **parameters) 
        self.full_df = self.data_set.join(results_df)
        self.final_df = self.full_df.copy()
        self.final_df.drop(self.models, axis=1, inplace=True)

        if self.labels!=False:
            print("Computing performance metrics")
            accuracy = []
            exec_time = []
            precision = []
            recall = []
            f1_score = []
            ### COMPUTING performance metrics  (test_phase)
            for m in self.models:
                print(m)
                e_time = results_dict[m]['exec_time']
                acc = al.metrics.accuracy_score(self.full_df.true_outlier, self.full_df[m])
                pre = al.metrics.precision_score(self.full_df.true_outlier, self.full_df[m])
                rec = al.metrics.recall_score(self.full_df.true_outlier, self.full_df[m])
                f1 = al.metrics.f1_score(self.full_df.true_outlier, self.full_df[m])
                accuracy.append(acc)
                precision.append(pre)
                recall.append(rec)
                f1_score.append(f1)
                exec_time.append(e_time)


            performance = al.np.array([self.models, accuracy, precision, recall, f1_score, exec_time]).T.tolist()
            for e in performance:
                print(e)
            self.performance_DF = al.pd.DataFrame(performance, columns=['Model', 'Accuracy', 'Precision', 'Recall', 'F1 score', 'Time'])#, 'Time'])
            print("Got performance metrics")


#%%
anomaly_detection_obj = AnomalyDetection(input_DF, 'spare_part_id', 'yyyymm', '%Y%m', models=["full"])#, labels='true_outlier')
#%%
anomaly_detection_labels = AnomalyDetection(original_DF, 'spare_part_id', 'yyyymm', '%Y%m', models=["full"], labels='true_outlier')
#best_parameters = anomaly_detection_obj.find_parameters(models=[]) # the user should decide which models are to be fit so that we know which parameters we try to find
# Change suggested/default parameters
#anomalies = anomaly_detection_obj.find_anomalies(models=[]) # get params directly. Define with default 

# %%