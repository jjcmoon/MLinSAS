# Machine Learning in Self Adaptive Systems
This repository contains the code of the approach that we mentioned in the thesis called: *Applying Machine Learning to Reduce the Adaptation Space in Self-Adaptive Systems: an exploratory work* (http://lnu.diva-portal.org/smash/record.jsf?pid=diva2%3A1240014&dswid=-7780)

This repository contains two main modules:

1. **machine_learner**: This contains all the code related to machine learning

2. **simulation**: This module contains two sub-modules:
        
    - **activforms**: This contains all the code related to ActivFORMS approach. In addition, it also has some code that connects this module to **machine_learner** module through HTTP.
    
    - **simulator**: This contains all the code related to DeltaIOT simulator.

    Other than above two sub-modules, **simulation** module also contains some some folders/files (SMCConfig.properties, models, uppaal-verifyta). These folder/files are used by **activform** module during runtime.


## How to run:
-------------------------------
1. Download this repository (master branch)

2. Install Docker (https://www.docker.com/) and start it on your machine

3. Open a terminal window in the `machine_learner` directory

4. Now, we are in **machine_learner** module. Run this module by executing following commands in terminal:
    
    1. `docker-compose build`
    
    2. `docker-compose up`

    **NOTE**: You can verify this by going to http://localhost:8000 on browser. It will say *{'mesage': 'only POST requests are allowed'}*. `ctr + c` can be used to stop this module. If you want to run again, only use `docker-compose up` command.

    Any change in code will be executed directly due to hot-reloading (no need to re-run every time)

5. Open a new terminal window in the `simulation` directory

6. Now, we are in **simulation** module. Run this module (sub-modules will be automatically executed) by executing following commands in terminal:
    
    1. `docker-compose build`
    
    2. `docker-compose up`

    - This will start the feeback loop that will print out some data in each run. Below is the print format of this data:
        
        - When **Mode = Testing, TaskType = Classification or Regrssion**:
            
            - While *# of adaptation cycles <=  \# of training cycles*:
                
                - adaptation cycle ; start time ; training time ; end time
            
            - While *# of adaptation cycles > \# of training cycles*:  
                
                - adaptation cycle ; start time ; testing time ; adaptation space ; training time ; end time
        
        - When **Mode = Comparsion, TaskType does not matter**:
            
            - While *# of adaptation cycles <=  \# of training cycles*:
                
                - adaptation cycle ; start time ; classification prediction time ; regression prediction time ; adaptation space ; activform adaptation space ; classification training time ; regression training time ; classification prediction time ; regression prediction time ; saving data time ; end time
            
            - While *# of adaptation cycles > \# of training cycles*:  
                - adaptation cycle ; start time ; classification prediction time ; regression prediction time ; classification adaptation space ; regression adaptation space ; activform adaptation space ; 
                classificaton training time ; regression training time ; classification prediction time ; regression prediction time ; saving data time ; end time
        
        - When **TaskType = ActivFORMS, Mode does not matter**:
            
            - adaptation cycle ; start time ; adaptation space ; end time

        - When all the adaptation cycles are executed:
            
            - packet loss ; energy consumption ; latency
        
        
## How to change settings:
----------------------------

The settings of this project can be changed in the properties file `simulation/SMCConfig.properties`.
The following settings can be changed:

| Property                        | Explanation                                                                                    |
|---------------------------------|------------------------------------------------------------------------------------------------|
| simulationNetwork               | The network which should be used for the simulation.                                           |
| requirements                    | The quality requirements used in the simulation.                                               |
| amountOfLearningCycles          | The amount of cycles spent learning the classifier/regressor.                                  |
| amountOfCycles                  | The total amount of cycles the simulation should run.                                          |
| distributionGap                 | Step size of the distribution settings over multiple links.                                    |
| explorationPercentage           | The percentage of options which should be explored for learning.                               |
| cappedVerificationTime          | The amount of time that can be used for verification.                                          |
| runMode                         | The run mode (machinelearning/activforms/comparison).                                          |
| taskType                        | The task type (classification/regression/pllaclassification/pllaregression).                   |
| targets, operators, thressholds | The goals in the simulator.                                                                    |
| readableTimeFormat              | The way time is printed in the console (HH-MM-SS if true, #milliseconds otherwise).            |
| deletePreviousModels            | Boolean which indicates if the previously learned models should be deleted in the first cycle. |


## Recommended software when developing
---------------------------------------
We recommend using VSCode (https://code.visualstudio.com/). We do not recommend any IDE (eclipse, intellij, etc.). VSCode has some plugins that we use in the development. They are not required to run the project. However, they can help you in the development.
    
    - For docker: https://marketplace.visualstudio.com/items?itemName=PeterJausovec.vscode-docker
    
    - For java: https://marketplace.visualstudio.com/items?itemName=redhat.java
    
    - For python: https://marketplace.visualstudio.com/items?itemName=ms-python.python

    **Note**: The above plugins might ask you to download some more plugins. These are not necessary.


## Offline steps
-----------------

To obtain the data needed for the offline steps in the machine learning process, run the simulator in `activforms` mode and any task type. Every cycle, data about the features and verified qualities of the different adaptation options is collected in `simulation/activforms/log/`. These data files can be merged into a single file using the python script `simulation/activforms/log/mergeFiles.py` after the simulation has ended.

After merging all the different data files, we can perform feature selection.
Put the merged file in `machine_learner/machine_learner/collected_data` and open a terminal in `machine_learner/`. Execute the following command:

`python3 machine_learner/preprocessing/feature_selection_multigoal.py`

This will results in the file `machine_learner/machine_learner/collected_data/dataset_selected_features.json`.

The next step is using this data file (with only the relevant features) for model simulation. Execute the following command:

`python3 machine_learner/preprocessing/model_simulations_multigoal.py`

This will simulate different versions of classifiers/regressors, and produce the output for all these version. The output files are stored in `machine_learner/machine_learner/collected_data/target/`. These resulting files are used to compare the different classifiers/regressors. Run the following command:

`python3 machine_learner/util/classificationComparison_multigoal.py machine_learner/collected_data/target/ outputDir/`
with 
    - `outputDir` a self made directory where the results of the evaluation can be stored.

At the end of the analysis, a web page will pop up containing all the metrics for the different versions of classifiers/regressors.



## Generating graphs
--------------------

### Graphs per configuration

Graphs which track a single adaptation options can be generated with the following file:

`machine_learner/machine_learner/util/uncertaintyInspection_multigoal.py`

In the respective file, functions are provided to draw a few different graphs (e.g. tracking a single configuration over multiple cycles). The file can be run as follows:

`python3 machine_learner/util/uncertaintyInspection_multigoal.py outputDir/ dataFile.json`
with 
    - `outputDir` a self made directory where the resulting graphs will be stored.
    - `dataFile.json` the actual data of the different configurations over multiple cycles.


### Graphs per cycle

To generate graphs per cycle, run the `selected_adaptation_options_multigoal` function in the the file `machine_learner/machine_learner/util/graph.py`. The file with this function is run as follows:

`python3 machine_learner/util/graph.py dataFile.json outputDir/`
with 
    - `outputDir` a self made directory where the resulting graphs will be stored.
    - `dataFile.json` the actual data of the different configurations over multiple cycles.


### Boxplots comparison with/without learning

Lastly, the `boxplotResults` function in the file `machine_learner/machine_learner/util/graph.py` can be used to to produce boxplots and a .csv file which compare no learning techniques with classification and regression. The file is run as follows:

`python3 machine_learner/util/graph.py dataFileClassification.json dataFileRegression.json outputDir/`
with 
    - `outputDir` a self made directory where the resulting graph and .csv file will be stored.
    - `dataFileClassification.json`/`dataFileRegression.json` the data files for classification and regression respectively.


## API of online supervised learning
-------------------
**Training a model**
----
* **URL** `http://localhost:8000?task-type=classification&mode=training&cycle=10`
* **Method:** `POST`
* **Headers:** `Content-Type: application/json`
* **Body:**
        
        {
            "features": [
                -2, 5, 2, ...
            ],
            "target": {
                0, 0, 1, ...
            }
        }

* **Success Response:**
    * **Content:**  <br />
                
            { 
                "message": "training successful"
            }

* **Error Responses:**
   * **Content:**  <br />
                
            { 
                "message": "training failed"
            }
        OR

            { 
                "message": "invalid request"
            }

The task type, as well as the cycle number, can be adjusted to another task type or cycle respectively.
---

**Testing a model**
----
* **URL** `http://localhost:8000?task-type=classification&mode=testing&cycle=10`
* **Method:** `POST`
* **Headers:** `Content-Type: application/json`
* **Body:**
        
        {
            "features": [
                -2, 5, 2, ...
            ]
        }

* **Success Response:**
    * **Content:**  <br />
                
            { 
                "predictions": [
                    1, 1, 0, ....
                ],
                "adaptation_space": 100
            }

* **Error Responses:**
   * **Content:**  <br />
                
            { 
                "message": "testing failed"
            }
        OR

            { 
                "message": "invalid request"
            }

Similar to training, the task type and cycle are adjustable.
---

