# Auto annotation using DL models in OpenVINO toolkit format

## Requirements:
Docker, docker_compose, tensorflow >=1.12, python 3.6, the object detection api .

Intel Core with 6th generation and higher or Intel Xeon CPUs. Verify with this command
```
cat /proc/cpuinfo | grep "model name"
```

## InstallationS:
- Install object detection api
 
Clone [this github repository](https://github.com/tensorflow/models) and follow installation instruction [here](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md)

- Install CVAT.

Clone CVAT source code from the GitHub repository.
git clone https://github.com/opencv/cvat
Follow the Quick installation guide for Ubuntu [here](https://github.com/opencv/cvat/blob/develop/cvat/apps/documentation/installation.md#additional-components)

- Install Intel Open Vino toolkits 

Download the latest Intel Open Vino toolkits package from  [ Intel® Distribution of OpenVINO™ toolkit for Linux*](https://software.intel.com/en-us/openvino-toolkit/choose-download?elq_cid=5898142).
Choose Linux* and Get the software by clicking _Register & Download_ .
Follow instruction in the Install the Intel® Distribution of OpenVINO™ Toolkit Core Components part [here](https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_linux.html#install-openvino)
	
## STEP:
1. Freeze the tf_model obtain after trainning.

From models/research/object_detection directory (in the object detection api)
```
python export_inference_graph.py \
    --input_type image_tensor \
    --pipeline_config_path path/to/faster_rcnn_inception_v2.config \
    --trained_checkpoint_prefix path/to/model.ckpt \
    --output_directory path/to/exported_model_directory
```

2. Convert the tf_model to IR representation via the model optimizer tool

The Intermediate Representation is a pair of files that describe the whole model:

.xml: Describes the network topology

.bin: Contains the weights and biases binary data

To convert a TensorFlow* Object Detection API model, go to the 

opt/intel/openvino_version/deployment_tools/model_optimizer directory and run
```
sudo python3 mo_tf.py --input_model <path_to_frozen.pb> \
	--tensorflow_use_custom_operations_config <path_to_subgraph_replacement_configuration_file.json> \
	--tensorflow_object_detection_api_pipeline_config <path_to_pipeline.config> \
	--output_dir <path_to_save_the_IR_representation>
```

where:	
	<path_to_frozen.pb> : File with a pre-trained model (binary or text .pb file after freezing)

	<path_to_subgraph_replacement_configuration_file.json> : A subgraph replacement configuration file that describes rules to convert specific TensorFlow* topologies.

You can find the configuration files in the <INSTALL_DIR>/deployment_tools/model_optimizer/extensions/front/tf directory.

For Faster R-CNN topologies trained manually using the TensorFlow* Object Detection API version 1.12.0 or higher use faster_rcnn_support_api_v1.14.json

	<path_to_pipeline.config> : samme as the pipeline_config_path in the freezins step

After this step you obtain the  .xml and the .bin files.

3. Add the open vino toolkits installer to cvat to make auto annotation

* Put the latest OpenVINO toolkit .tgz installer (offline or online) for Ubuntu platforms downloaded file into
 
cvat/components/openvino. 

Note that OpenVINO does not maintain forward compatability between Intermediate Representations (IRs), so the version of OpenVINO in CVAT and the version used to translate the models needs to be the same.

* Accept EULA in the cvat/components/eula.cfg file.

* Build docker image
```
	# From project root directory
docker-compose -f docker-compose.yml -f components/openvino/docker-compose.openvino.yml build
```
* Run docker container
```
	# From project root directory
docker-compose -f docker-compose.yml -f components/openvino/docker-compose.openvino.yml up -d
```

You should be able to login and see the web interface for CVAT now, complete with the new "Model Manager" button.

4. Make auto annotation in CVAT.

Open the installed Google Chrome browser and go to localhost:8080. Type your login/password for the superuser on the login page and press the Login button.


	- Upload deep learning (DL) models using model manager:
 
* Enter model name
* select Source local

* select model file using "Select files" button and select the 4 files you need:

Model config (*.xml) - a text file with network configuration.

Model weights (*.bin) - a binary file with trained weights.

Label map (*.json) - a simple json file with label_map dictionary like an object with string values for label numbers.

Interpretation script (*.py) - a file used to convert net output layer to a predefined structure which can be processed by CVAT. 

More information [here](https://github.com/opencv/cvat/blob/develop/cvat/apps/auto_annotation/README.md)

You can find a sample of this 4 files in  the Sicara_container_IR folder.

	- After downloading a model you have to create a task:


press _Create New Task_ button on the main page.


Specify mandatory parameters of the task. You have to fill in __Name__, __Labels__ and press the _Select Files_ button. After that you have to choose data you want to annotate.

For __Labels__ Use the following layout to create labels:
 
```
label_name <prefix>input_type=attribute_name:attribute_value1,attribute_value2.
```

You can specify multiple labels and attributes and divide them pressing the space button.

Example: car person bike - three labels without attributes

	- click _Run Auto Annotation_ button to generate annotaion for the task.

Select a model you need.If it's necessary select the Delete current annotation checkbox. Adjust the labels so that the task labels will correspond to the labels of the DL model. Click Start to begin the auto annotatiton process.

	- click the _Jobs links_ to views the results

Now you can edit the bounding boxes by removing false positives, adding unlabeled objects.













