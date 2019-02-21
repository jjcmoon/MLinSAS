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
		path = os.path.join(pathToFiles, f'dataset_with_all_features{i}.json')

		if os.path.isfile(path):
			print(f'Collecting data from cycle {i}')

			with open(os.path.join(pathToFiles, f'dataset_with_all_features{i}.json'), 'r') as f:
				currentData = json.load(f)

			data['target_regression_energyconsumption'] += currentData['target_regression_energyconsumption']
			data['target_regression_latency'] += currentData['target_regression_latency']
			data['target_regression_packetloss'] += currentData['target_regression_packetloss']
			data['target_classification_packetloss'] += currentData['target_classification_packetloss']
			data['target_classification_latency'] += currentData['target_classification_latency']
			data['features'] += currentData['features']
			data['verification_times'] += currentData['verification_times']
		
			i += 1
		else:
			break


	with open(os.path.join(pathToFiles, 'dataset_with_all_features.json'), 'w') as f:
		json.dump(data, f)


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Make sure to provide the directory as an argument to this program.')

	else:
		merge_all_files(sys.argv[1])


