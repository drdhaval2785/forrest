# Dependencies
python2.7 (https://www.python.org/downloads/)
numpy (http://www.numpy.org/)

# Instructions
1. copy the content of this folder in a directory.

2. Open Command prompt / terminal and reach the folder e.g. C:/forrest

3. Copy paste the following commands in the command prompt
```
import readcsv as p
training_data, test_data = p.load_data_wrapper(p.datatuple)
import network2
net = network2.Network([p.input_neuron, p.intermediate_neuron, p.output_neuron])
net.SGD(training_data, p.epochs, p.mini_batch_size, p.eta, p.lmbda, evaluation_data=test_data, monitor_evaluation_cost=True, monitor_evaluation_accuracy=True, monitor_training_cost=True, monitor_training_accuracy=True)
```

4. This will read from data1.csv and give the accuracies for each epoch of training.

5. data1.csv has three parameters in each line `runs,average,strikerate,winstatus`. 

runs are runs scored by a team.

average is runs per wicket.

striekrate is runs per balls faced.

winstatus is 0 for loss and 1 for win.

Note - You can add some other data in the same format here to manipulate.

