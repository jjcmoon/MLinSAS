import matplotlib.pyplot as plt
import json
import sys
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier, ExtraTreesRegressor
import os

def doFeatureSelection(network = 'DeltaIoTv1'):
    path = os.path.join('machine_learner', 'collected_data', 'dataset_with_all_features.json')

    data = json.load(open(path))

    plt_index = 1

    classif = ('Classification', [data['target_classification_packetloss'], data['target_classification_latency']], ExtraTreesClassifier)
    # NOTE: add regression later
    # regres = ('Regression', [data['target_regression_packetloss'], data['target_regression_latency']], ExtraTreesRegressor)

    for target_type, targets, model in [classif]:
        target_packetloss, target_latency = targets

        totalTargets = []
        # TODO adjust this later on for regression
        for target_pl, target_l in zip(target_packetloss, target_latency):
            totalTargets.append(target_pl + (target_l << 1))

        # for i in range(4):
        #     print(f'Options in class {i}: {totalTargets.count(i)}')

        model = model(random_state=10)
        model.fit(data['features'], totalTargets)

        importances = model.feature_importances_

        plt.subplot(1, 1, plt_index)

        if network == 'DeltaIoTv1':
            plt.bar(range(1, 18), importances[:17], color='r', label='1-17 SNR')
            plt.bar(range(18, 35), importances[17:34], color='b', label='18-34 Power Settings')
            plt.bar(range(35, 52), importances[34:51], color='orange', label='35-51 Packets Distribution')
            plt.bar(range(52, 66), importances[51:65], color='green', label='52-65 Traffic Load')

            print("SNR:   " + str([f'{i:.4f}' for i in importances[:17]]))
            print("Power: " + str([f'{i:.4f}' for i in importances[17:34]]))
            print("Distr: " + str([f'{i:.4f}' for i in importances[34:51]]))
            print("Load:  " + str([f'{i:.4f}' for i in importances[51:65]]))
            # print("Overall importances: " + str([f'{i:.4f}' for i in importances]))

            plt.xticks([1, 17, 34, 51, 65])
        elif network == 'DeltaIoTv2':
            plt.bar(range(1, 43), importances[:42], color='r', label='1-42 SNR')
            plt.bar(range(43, 85), importances[42:84], color='b', label='43-84 Power Settings')
            plt.bar(range(85, 127), importances[84:126], color='orange', label='85-126 Packets Distribution')
            plt.bar(range(127, 163), importances[126:162], color='green', label='127-162 Traffic Load')

            print("SNR:   " + str([f'{i:.4f}' for i in importances[:42]]))
            print("Power: " + str([f'{i:.4f}' for i in importances[42:84]]))
            print("Distr: " + str([f'{i:.4f}' for i in importances[84:126]]))
            print("Load:  " + str([f'{i:.4f}' for i in importances[126:162]]))
            # print("Overall importances: " + str([f'{i:.4f}' for i in importances]))

            plt.xticks([1, 42, 84, 126, 162])
        else:
            print(f'Network \'{network}\' is currently not supported.')
            sys.exit(1)

                
        plt.xlabel('Features')
        plt.ylabel('Importance Score')
        plt.title(target_type)

        plt_index += 1

        if plt_index == 2:
            plt.legend()
            
        indices = np.array([i for i in range(len(importances)) if importances[i] != 0])

        # save the selected features in a separate file
        newFileData = json.load(open(path))

        newFeatures = []
        for feature_vec in newFileData['features']:
            newFeatures.append(np.array(feature_vec)[indices].tolist())

        newFileData['features'] = newFeatures

        outputPath = os.path.join('machine_learner','collected_data',f'dataset_selected_features_{target_type}.json')
        with open(outputPath, 'w') as f:
            json.dump(newFileData, f, indent=1)
        

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    doFeatureSelection('DeltaIoTv2')

