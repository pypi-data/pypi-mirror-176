import abc
from algorithms import IDescriptor
import cv2 as cv
from easydict import EasyDict as edict
import mxnet as mx
import numpy as np
import sklearn.preprocessing
import threading

from algorithms_extensions.loadable import ILoadable


class DescriptorMxnet(IDescriptor, ILoadable):

	def __init__(self):
		self._net = None
		self._thread_loaded = None  # thread en que fue cargado el modelo

	@abc.abstractmethod
	def _get_prefix(self):
		raise NotImplementedError

	@abc.abstractmethod
	def _get_epoch(self):
		raise NotImplementedError

	@abc.abstractmethod
	def _get_input_shape(self):
		raise NotImplementedError

	def is_loaded(self) -> bool:
		model_loaded = self._net is not None
		current_thread_is_main = threading.current_thread() == threading.main_thread()
		current_thread_equals_loaded_thread = threading.current_thread() == self._thread_loaded
		return model_loaded and (current_thread_is_main or current_thread_equals_loaded_thread)

	def load(self):
		self._thread_loaded = threading.current_thread()
		ctx = [mx.cpu()]
		self._net = edict()
		self._net.ctx = ctx
		self._net.sym, self._net.arg_params, self._net.aux_params = mx.model.load_checkpoint(self._get_prefix(), self._get_epoch())
		# net.arg_params, net.aux_params = ch_dev(net.arg_params, net.aux_params, net.ctx)
		all_layers = self._net.sym.get_internals()
		self._net.sym = all_layers['fc1_output']  # TODO cambiar esto para que la capa sea un parámetro de la clase
		self._net.model = mx.mod.Module(symbol=self._net.sym, context=self._net.ctx, label_names=None)
		self._net.model.bind(data_shapes=[('data', (1, 3, self._get_input_shape()[0], self._get_input_shape()[1]))])
		self._net.model.set_params(self._net.arg_params, self._net.aux_params)

	def unload(self):
		self._net = None
		self._thread_loaded = None

	def features(self, img):
		self.load_if_not_loaded()

		input_blob = np.zeros((1, 3, self._get_input_shape()[0], self._get_input_shape()[1]))
		timg = cv.resize(img, self._get_input_shape())
		timg = np.transpose(timg, (2, 0, 1))
		input_blob[0] = timg
		data = mx.nd.array(input_blob)
		db = mx.io.DataBatch(data=(data,))
		self._net.model.forward(db, is_train=False)
		feats = self._net.model.get_outputs()[0].asnumpy()
		feats = sklearn.preprocessing.normalize(feats)
		return feats.squeeze()

