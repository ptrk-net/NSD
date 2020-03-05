# Import python libraries
import logging
from datetime import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
# from scipy.stats import gaussian_kde
from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split, GridSearchCV

# Import NSD libraries
from bin.NSD_Database import NSD_Database
from bin.NSD_Monitor_Data import NSD_Monitor_Data
from conf import variables as opts


class NSD_AI:

    def __init__(self, log_level, db_server, db_port, sync_queue):
        self.log_level = log_level
        self.logger = logging.getLogger(__name__)
        self.SQ = sync_queue
        self.db_server = db_server
        self.db_port = db_port

    def NSD_Flow_fork_database(self):
        self.DB = NSD_Database(self.log_level, self.db_server, self.db_port, self.SQ)  # MongoDB


    def NSD_AI_get_flows(self, prot):
        flows_returned = []
        while True:
            for flow in getattr(NSD_Monitor_Data(), 'NSD_Monitor_Data_get_flows_' + prot)():
                if flow not in flows_returned:
                    flows_returned.append(flow)
                    yield flow

    def NSD_AI_training_get_set(self, type_cc, prot, chats, packets, bbdd, intervals):
        data_Not_CC = []
        data_CC = []
        data_chat = []
        flows = self.NSD_AI_get_flows(prot)

        # counter_chats = 0
        # counter_packets = 0
        # counter_diffs_out = 0
        # intervals = [64.0, 67.31333333, 70.62666667, 73.94, 77.25333333, 80.56666667, 83.88, 87.19333333, 90.50666667,
        #             93.82, 97.13333333, 100.44666667, 103.76, 107.07333333,110.38666667, 113.7, 117.01333333,
        #             120.32666667, 123.64, 126.95333333, 130.26666667, 133.58, 136.89333333, 140.20666667, 143.52,
        #             146.83333333, 150.14666667, 153.46, 156.77333333, 160.08666667, 163.4]
        if type_cc == opts.CC_PT1:
            while True:
                flow = next(flows)
                pkts_date = getattr(self.DB, 'NSD_Database_get_' + prot + bbdd + '_date_by_id')(flow[0])
                pkt_date_before = datetime.strptime(pkts_date.pop(0)['Date'], '%d/%m/%Y %H:%M:%S.%f')
                """
                
                for pkt_date in pkts_date:
                    pkt_date_next = datetime.strptime(pkt_date['Date'], '%d/%m/%Y %H:%M:%S.%f')
                    # diff = (pkt_date_next - pkt_date_before).total_seconds()*100000
                    diff = (pkt_date_next - pkt_date_before).total_seconds()
                    if diff < 0.025:
                        data_chat.append(diff)
                        # counter_packets += 1
                        # if counter_packets == packets:
                        if len(data_chat) == packets:
                            (hist, intervals) = np.histogram(data_chat, bins=intervals)
                            data_training_set.append(hist)
                            # counter_packets = 0
                            data_chat.clear()
                            # counter_chats += 1
                            # if counter_chats == chats:
                            if len(data_training_set) == chats:
                                # self.logger.info('packets diff out: ' + str(counter_diffs_out))
                                return data_training_set, intervals
                    # else:
                    # counter_diffs_out += 1
                    pkt_date_before = pkt_date_next
                """
        elif type_cc == opts.CC_PT11:
            intervals = list(range(0, 31))
            while True:
                self.logger.info('PT11 training starting..')
                flow = next(flows)
                self.logger.info('--- flow: ' + str(flow))
                pkts_data = getattr(self.DB, 'NSD_Database_get_' + prot + '_info_PT11_training_by_id')(flow[0])
                counter_zeros = 0
                total_zeros = 0
                total_ones = 0
                for pkt_data in pkts_data:
                    data = list(map(int, pkt_data['Data'].decode('utf-8').split(' ')))
                    #print('-----------------> data: ' + str(data))
                    if data[2] == 1:
                        data_chat.append(counter_zeros)
                        #total_ones += 1
                        if len(data_chat) == packets:
                            #self.logger.info('**** data_chat: ' + str(data_chat))
                            (hist, intervals) = np.histogram(data_chat, bins=intervals)
                            #self.logger.info('**** hist: ' + str(hist))
                            data_chat.clear()
                            if len(data_Not_CC) < chats and pkt_data['cc'] == 0:
                                data_Not_CC.append(hist)
                                self.logger.info('---> len data_Not_CC: ' + str(len(data_Not_CC)))
                            elif len(data_CC) < chats and pkt_data['cc'] == 1:
                                data_CC.append(hist)
                                self.logger.info('---> len data_CC: ' + str(len(data_CC)))
                            if len(data_CC) == chats and len(data_Not_CC) == chats:
                                return data_Not_CC, data_CC, intervals
                        counter_zeros = 0
                    else:
                        counter_zeros += 1
                        #total_zeros += 1
                #self.logger.info('----------> total zeros: ' + str(total_zeros))
                #self.logger.info('----------> total ones: ' + str(total_ones))

    # PT1 training
    def NSD_AI_training_PT1(self, chats, data_ts_Not_CC, data_ts_CC):
        gammas = [10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001]
        # gammas = [ 'scale' ]
        Cs = [1, 10, 100, 1000, 10000, 100000, 1000000]
        # kernels = [ 'rbf', 'sigmoid', 'poly' ]
        kernels = ['rbf']
        # best_score = 0.0
        # best_gamma = ''
        # best_kernel = ''

        X_train, X_test, y_train, y_test = train_test_split(np.concatenate([data_ts_Not_CC, data_ts_CC]),
                                                            np.concatenate([np.zeros(chats), np.ones(chats)]),
                                                            test_size=0.1, shuffle=True)

        # for kernel in kernels:
        #   for gamma in gammas:
        #        self.logger.info('running kernel {} and gamma {}'.format(kernel, gamma))
        parameters = {'kernel': kernels, 'C': Cs, 'gamma': gammas}
        svc = svm.SVC()
        classifier = GridSearchCV(svc, parameters)
        classifier.fit(X_train, y_train)
        predicted = classifier.predict(X_test)
        actual_score = metrics.precision_score(y_test, predicted)
        #        if actual_score > best_score:
        #            best_kernel = kernel
        #            best_gamma = gamma
        #            best_score = actual_score

        self.logger.info('best parameters: {}'.format(classifier.best_params_))
        self.logger.info('best score: {}'.format(classifier.best_score_))
        self.logger.info('actual score: {}'.format(actual_score))

        # print("Best precision score:\n\t - kernel {}\n\t - gamma {}\n\t - precision {}\n".format(best_kernel,
        #                                                                                         best_gamma,
        #                                                                                         best_score))

        # print("Classification report for classifier %s:\n%s\n"
        #      % (classifier, metrics.classification_report(y_test, predicted)))

        self.SQ.put('DATA_PROCESSED')
        self.SQ.put('KILL')
        exit(0)

    # PT1 training
    def NSD_AI_training_PT11(self, chats, data_ts_Not_CC, data_ts_CC):
        gammas = [10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001]
        # gammas = [ 'scale' ]
        Cs = [10, 100, 1000, 10000, 100000, 1000000]
        # kernels = [ 'rbf', 'sigmoid', 'poly' ]
        kernels = ['rbf']
        # best_score = 0.0
        # best_gamma = ''
        # best_kernel = ''

        X_train, X_test, y_train, y_test = train_test_split(np.concatenate([data_ts_Not_CC, data_ts_CC]),
                                                            np.concatenate([np.zeros(chats), np.ones(chats)]),
                                                            test_size=0.1, shuffle=True)

        # for kernel in kernels:
        #   for gamma in gammas:
        #        self.logger.info('running kernel {} and gamma {}'.format(kernel, gamma))
        parameters = {'kernel': kernels, 'C': Cs, 'gamma': gammas}
        svc = svm.SVC()
        classifier = GridSearchCV(svc, parameters)
        classifier.fit(X_train, y_train)
        predicted = classifier.predict(X_test)
        actual_score = metrics.precision_score(y_test, predicted)
        #        if actual_score > best_score:
        #            best_kernel = kernel
        #            best_gamma = gamma
        #            best_score = actual_score

        self.logger.info('best parameters: {}'.format(classifier.best_params_))
        self.logger.info('best score: {}'.format(classifier.best_score_))
        self.logger.info('actual score: {}'.format(actual_score))

        # print("Best precision score:\n\t - kernel {}\n\t - gamma {}\n\t - precision {}\n".format(best_kernel,
        #                                                                                         best_gamma,
        #                                                                                         best_score))

        # print("Classification report for classifier %s:\n%s\n"
        #      % (classifier, metrics.classification_report(y_test, predicted)))

        self.SQ.put('DATA_PROCESSED')
        self.SQ.put('KILL')
        exit(0)

        """
        datediff = []
        pkts_date = self.DB.NSD_Database_get_ICMP_date_by_id(flow)
        pkt_date_before = datetime.strptime(pkts_date[0]['Date'], '%d/%m/%Y %H:%M:%S.%f')
        for pkt_date in pkts_date:
            pkt_date_next = datetime.strptime(pkt_date['Date'], '%d/%m/%Y %H:%M:%S.%f')
            diff = (pkt_date_next - pkt_date_before).total_seconds()*10000
            #self.logger.info(diff)
            if diff < 30:   
                datediff.append(diff)
            pkt_date_before = pkt_date_next
        #self.logger.info(str(datediff))
        date_diff_bef_norm = np.array(datediff)
        mean = np.mean(date_diff_bef_norm)
        std = np.std(date_diff_bef_norm)
        xx = []
        for c in date_diff_bef_norm:
            xx.append((c-mean)/std)
        x = np.array(xx)
        y = [0]*len(x)

        (counts, bins) = np.histogram(date_diff_bef_norm, bins=range(30))

        plt.figure(figsize=[10, 8])

        plt.bar(bins[:-1], counts, width=0.5, color='#0504aa', alpha=0.7)
        plt.xlim(min(bins), max(bins))
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Value', fontsize=15)
        plt.ylabel('Frequency', fontsize=15)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.ylabel('Frequency', fontsize=15)
        plt.title('Normal Distribution Histogram', fontsize=15)
        plt.show()

        #factor = 2
        #plt.hist(bins[:-1], bins, weights=factor * counts)
        #plt.hist2d(x, y, (50, 50), cmap=plt.cm.jet)
        #plt.colorbar()
        # Histogram of example data and normalized data
        #num_bins = 'auto'
        #n, bins, patches = plt.hist(date_diff_norm, num_bins, facecolor='blue', alpha=0.5)
        #n, bins, patches = plt.hist(x)
        #plt.scatter(x, y)
        #plt.show()
        """

    def NSD_AI_training(self, type_cc, prot, chats, packets, intervals):
        self.NSD_Flow_fork_database()

        self.logger.info('AI training starting...')
        data_training_set_Not_CC, data_training_set_CC, intervals = self.NSD_AI_training_get_set(type_cc, prot, chats,
                                                                                                 packets, '_CC',
                                                                                                 intervals)

        plt.hist(data_training_set_CC[10], intervals)
        plt.ylabel('frecuencia')
        plt.xlabel('num paquetes intercalados')
        plt.title('CC')
        plt.show()
        plt.hist(data_training_set_Not_CC[10], intervals)
        plt.ylabel('frecuencia')
        plt.xlabel('num paquetes intercalados')
        plt.title('NOT CC')
        plt.show()

        f = open("training_set_Not_CC_UPD.txt", "a")
        f.write(str(intervals))
        f.write(str(data_training_set_Not_CC))
        f.close()
        f = open("training_set_CC_UDP.txt", "a")
        f.write(str(intervals))
        f.write(str(data_training_set_CC))
        f.close()
        self.NSD_AI_training_PT11(chats, data_training_set_Not_CC, data_training_set_CC)


        """
        ---
        data = []
        time.sleep(5)
        for flow in NSD_Monitor_Data.NSD_Monitor_Data_get_flows_ICMP():
            if NSD_Monitor_Data.NSD_Monitor_Data_get_status_flow_ICMP(flow[0]) != opts.FLOW_AI_TRAINED:
                self.NSD_AI_training_PT1(flow[0], data)
                flow_status = {
                    'Flow': opts.FLOW_FINISHED,
                    'AI': opts.FLOW_AI_FINISHED,
                    'Result': opts.FLOW_AI_TRAINED
                }
                NSD_Monitor_Data.NSD_Monitor_Data_update_status_flow_ICMP(flow[0], flow_status)
        """
