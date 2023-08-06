import abc
import cv2 as cv

from algorithms_extensions.loadable import ILoadable


class OCVModel(abc.ABC, ILoadable):

    def __init__(self, layer=None, output_trans=None):
        self._net = None
        self._layer = layer
        self._output_trans = output_trans if output_trans else self._flatten

        self._scale = None
        self._input_size = None
        self._mean = None
        self._swapRB = None
        self._crop = None

    @abc.abstractmethod
    def _get_model_path(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_deploy_path(self):
        raise NotImplementedError

    def is_loaded(self) -> bool:
        return self._net is not None

    def load(self):
        self._net = cv.dnn.readNet(model=self._get_model_path(), config=self._get_deploy_path())

    def unload(self):
        self._net = None

    def inference(self, net_input):
        self.load_if_not_loaded()

        kwargs = self._get_kwargs()
        blob = cv.dnn.blobFromImage(net_input, **kwargs)
        self._net.setInput(blob)

        if self._layer is None:
            output = self._net.forward()
        else:
            output = self._net.forward(self._layer)

        return self._output_trans(output)

    def _get_kwargs(self):
        kwargs = {}
        if self._scale is not None:
            kwargs['scalefactor'] = self._scale
        if self._input_size is not None:
            kwargs['size'] = self._input_size
        if self._mean is not None:
            kwargs['mean'] = self._mean
        if self._swapRB is not None:
            kwargs['swapRB'] = self._swapRB
        if self._crop is not None:
            kwargs['crop'] = self._crop

        return kwargs

    def _flatten(self, feats):
        return feats.flatten()
