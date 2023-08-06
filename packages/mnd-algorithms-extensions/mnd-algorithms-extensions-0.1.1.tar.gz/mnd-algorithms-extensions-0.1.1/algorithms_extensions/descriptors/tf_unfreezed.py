import abc
from algorithms import IDescriptor
import cv2 as cv
import os
import re
import tensorflow as tf

from algorithms_extensions.loadable import ILoadable


def load_tensorflow_model(sess, model):
	"""
	Cargar modelo de Tensorflow con formato .index, .meta, .ckpt
	:param model:
	:return:
	"""

	# Check if the model is a model directory (containing a metagraph and a checkpoint file)
	#  or if it is a protobuf file with a frozen graph
	def get_model_filenames(model_dir):
		files = os.listdir(model_dir)
		meta_files = [s for s in files if s.endswith('.meta')]
		if len(meta_files) == 0:
			raise ValueError('No meta file found in the model directory (%s)' % model_dir)
		elif len(meta_files) > 1:
			raise ValueError('There should not be more than one meta file in the model directory (%s)' % model_dir)
		meta_file = meta_files[0]
		ckpt = tf.train.get_checkpoint_state(model_dir)
		if ckpt and ckpt.model_checkpoint_path:
			ckpt_file = os.path.basename(ckpt.model_checkpoint_path)
			return meta_file, ckpt_file

		meta_files = [s for s in files if '.ckpt' in s]
		max_step = -1
		for f in files:
			step_str = re.match(r'(^model-[\w\- ]+.ckpt-(\d+))', f)
			if step_str is not None and len(step_str.groups()) >= 2:
				step = int(step_str.groups()[1])
				if step > max_step:
					max_step = step
					ckpt_file = step_str.groups()[0]
		return meta_file, ckpt_file

	model_exp = os.path.expanduser(model)
	if os.path.isfile(model_exp):
		print('Model filename: %s' % model_exp)
		with tf.gfile.FastGFile(model_exp, 'rb') as f:
			graph_def = tf.GraphDef()
			graph_def.ParseFromString(f.read())
			tf.import_graph_def(graph_def, name='')
	else:
		print('Model directory: %s' % model_exp)
		meta_file, ckpt_file = get_model_filenames(model_exp)

		print('Metagraph file: %s' % meta_file)
		print('Checkpoint file: %s' % ckpt_file)

		saver = tf.train.import_meta_graph(os.path.join(model_exp, meta_file))
		# saver.restore(tf.get_default_session(), os.path.join(model_exp, ckpt_file))
		saver.restore(sess, os.path.join(model_exp, ckpt_file))


class DescriptorFromTFUnfreezed(IDescriptor, ILoadable):

	def __init__(self):
		self._sess = None
		self._inputs_placeholder = None
		self._embeddings = None

	@abc.abstractmethod
	def _get_model_path(self):
		raise NotImplementedError

	def is_loaded(self) -> bool:
		return self._inputs_placeholder is not None

	def load(self):
		self._sess = tf.Session() if tf.get_default_session() is None else tf.get_default_session()
		load_tensorflow_model(self._sess, self._get_model_path())
		self._inputs_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
		self._embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")

	def unload(self):
		self._sess = None
		self._inputs_placeholder = None
		self._embeddings = None

	def features(self, img):
		self.load_if_not_loaded()

		nimg = img

		shape = self._inputs_placeholder.shape
		nimg = cv.resize(nimg, (shape[1], shape[2]))
		nimg = nimg - 127.5
		nimg = nimg * 0.0078125
		feed_dict = {self._inputs_placeholder: [nimg]}
		return self._sess.run(self._embeddings, feed_dict=feed_dict).flatten()
