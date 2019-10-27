import json
import numpy as np
import os
import sys


def merge_all_files(pathToFiles):
	data = {
		'target_regression_energyconsumption': [],
		'target_regression_latency': [],
		'target_regression_packetloss': [],
		'target_classification_packetloss': [],
		'target_classification_latency': [],
		'features': [],
		'verification_times': []
	}
	i = 1
	while True:
		path = os.path.join(pathToFiles, "dataset_with_all_features%d.json"%i)

		if not os.path.isfile(path):
			break

		print("Collecting data from cycle %d"%i)

		with open(os.path.join(pathToFiles, 'dataset_with_all_features%d.json'%i), 'r') as f:
			currentData = json.load(f)

		data['target_regression_energyconsumption'] += currentData['target_regression_energyconsumption']
		data['target_regression_latency'] += currentData['target_regression_latency']
		data['target_regression_packetloss'] += currentData['target_regression_packetloss']
		data['target_classification_packetloss'] += currentData['target_classification_packetloss']
		data['target_classification_latency'] += currentData['target_classification_latency']
		data['features'] += currentData['features']
		data['verification_times'] += currentData['verification_times']
	
		i += 1

	outputFile = os.path.join(pathToFiles, 'dataset_with_all_features.json')
	with open(outputFile, 'w') as f:
		json.dump(data, f)


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Make sure to provide the directory as an argument to this program.')

	else:
		merge_all_files(sys.argv[1])


