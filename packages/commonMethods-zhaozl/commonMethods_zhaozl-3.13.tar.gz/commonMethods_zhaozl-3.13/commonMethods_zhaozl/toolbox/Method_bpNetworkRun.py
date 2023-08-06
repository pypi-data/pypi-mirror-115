"""
包括bpNetworkRun一个类

Classes
----------
bpNetworkRun: BP神经网络计算

Example
----------
>>> from commonMethods_zhaozl.toolbox.Method_bpNetworkRun import bpNetworkRun

"""

import os
import sys

import numpy as np  # numpy==1.18.5
import joblib  # joblib==0.16.0
import tensorflow as tf  # tensorflow==2.1.0
import json

from tensorflow_core.python.tools.inspect_checkpoint import print_tensors_in_checkpoint_file  # tensorflow==2.1.0
from tensorflow.python.training import py_checkpoint_reader  # tensorflow==2.1.0

tf.compat.v1.disable_eager_execution()


class bpNetworkRun:
	"""
	BP神经网络计算

	[1] 参数
	----------
	_modelPath:
		str, 网络模型的位置, 形如'E:/99.Python_Develop/rotorVibration/clusterFitting/Cluster_0/netWork/'
	_networkParams:
		dict, 网络参数，形如 {'b': b,'b0': b0, 'b1': b1,'b2': b2, 'iw0': iw0,'iw1': iw1,'iw2':iw2, 'lw': lw}
	_inputSample:
		dataframe, 网络的输入，形如DF([input1, input2], columns=['input1', 'input2'])

	[2] 返回
	-------
	networkOutput:
		ndarray, 网络的输出，形如[[77.2], [77.1], [77.4], ...]

	[3] 网络计算
	--------
	>>> networkParams = {'b': b,'b0': b0, 'b1': b1,'b2': b2, 'iw0': iw0,'iw1': iw1,'iw2':iw2, 'lw': lw}
	>>> res = bpNetworkRun(_networkParams=networkParams, _inputSamples=inputSample).networkOutput

	[4] 网络计算
	--------
	>>> modelPath = 'E:/99.Python_Develop/rotorVibration/clusterFitting/Cluster_0/netWork/'
	>>> res = bpNetworkRun(_modelPath=modelPath, _inputSamples=inputSample).networkOutput

	[5] 备注
	--------
	* 默认的网络模型存储地址为E:/99.Python_Develop/rotorVibration/clusterFitting/Cluster_0/netWork/, 上述路径下存有其它文件，如netParams.json、scalerInput、scalerTarget等
	"""

	def __init__(self, **kwargs):
		self.networkOutput = []
		# ===== 获取模型文件位置 ===== #
		if '_modelPath' in kwargs.keys():
			modelPath = kwargs['_modelPath']
		else:
			modelPath = os.getcwd()
		# ===== 从变量获取或从文件调用网络模型参数 ===== #
		if '_networkParams' in kwargs.keys():
			netParams = kwargs['_networkParams']
		else:
			# ===== 调用网络参数文件 ===== #
			with open(modelPath + 'netParams.json') as file:
				netParams_unseriesed = json.load(file)
			netParams = {}
			# ===== 解析网络参数 ===== #
			for item in netParams_unseriesed.keys():
				if '_shape' not in item:
					_data = netParams_unseriesed[item]
					_shape = netParams_unseriesed[item + '_shape']
					_data_transposed = np.reshape(_data, _shape)
					_cache = {item: _data_transposed}
					netParams = {**netParams, **_cache}
		# ===== 网络参数赋值 ===== #
		self.b = netParams['b']
		self.b0 = netParams['b0']
		self.b1 = netParams['b1']
		self.b2 = netParams['b2']
		self.iw0 = netParams['iw0']
		self.iw1 = netParams['iw1']
		self.iw2 = netParams['iw2']
		self.lw = netParams['lw']
		# ===== 调用scaler ===== #
		self.scalerInput = joblib.load(modelPath + 'scalerInput')
		self.scalerTarget = joblib.load(modelPath + 'scalerTarget')
		# ===== 网络输入赋值与标准化 ===== #
		inputSample = kwargs['_inputSample']
		self.inputSampleStd = self.scalerInput.transform(inputSample)

		def sigmoid(x_Array):
			res = np.zeros_like(x_Array)
			rows, cols = np.shape(x_Array)
			for col in range(cols):
				for row in range(rows):
					x = x_Array[row, col]
					res[row, col] = 1 / (1 + np.exp(-x))
			return res

		def tanh(x_Array):
			res = np.zeros_like(x_Array)
			rows, cols = np.shape(x_Array)
			for col in range(cols):
				for row in range(rows):
					x = x_Array[row, col]
					res[row, col] = (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))
			return res

		cache = sigmoid(np.add(np.matmul(self.inputSampleStd, self.iw0), self.b0))
		cache = sigmoid(np.add(np.matmul(cache, self.iw1), self.b1))
		cache = sigmoid(np.add(np.matmul(cache, self.iw2), self.b2))
		resFromFormula = tanh(np.add(np.matmul(cache, self.lw), self.b))
		self.networkOutput = self.scalerTarget.inverse_transform(resFromFormula).flatten().tolist()[0]
