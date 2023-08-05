import logging
from abc import abstractmethod, ABC
from pathlib import Path
from typing import Any, List

from nebullvm.base import ModelParams, Device
from nebullvm.converters.tensorflow_converters import (
    convert_tf_to_onnx,
    convert_keras_to_onnx,
)
from nebullvm.converters.torch_converters import convert_torch_to_onnx
from nebullvm.optional_modules.onnx import onnx
from nebullvm.optional_modules.tensorflow import tensorflow as tf
from nebullvm.optional_modules.torch import Module
from nebullvm.utils.data import DataManager

logger = logging.getLogger("nebullvm_logger")


class BaseConverter(ABC):
    """Base class for converters.

    Attributes:
        model_name (str, optional): name of the model. If not given 'temp' will
            be used as model name.
    """

    def __init__(self, model_name: str = None):
        self.model_name = model_name or "temp"

    @abstractmethod
    def convert(
        self,
        model: Any,
        model_params: ModelParams,
        save_path: Path,
        device: Device,
        input_data: DataManager = None,
    ):
        raise NotImplementedError


class ONNXConverter(BaseConverter):
    """Class for converting models from a supported framework to ONNX.

    Attributes:
        model_name (str, optional): name of the model. If not given 'temp' will
            be used as model name.
    """

    ONNX_MODEL_EXTENSION = ".onnx"

    def convert(
        self,
        model: Any,
        model_params: ModelParams,
        save_path: Path,
        device: Device,
        input_data: DataManager = None,
    ):
        """Convert the input model in ONNX.

        Args:
            model (any, optional): Model to be converted. The model can be in
                either the tensorflow or pytorch framework.
            model_params (ModelParams): Model Parameters as input sizes and
                dynamic axis information.
            save_path (Path): Path to the directory where saving the onnx
                model.
            device (Device): Device where the model will be run.
            input_data (DataManager, optional): Custom data provided by user to
                be used as input for the converter.

        Returns:
            Path: Path to the onnx file.
        """
        onnx_name = f"{self.model_name}{self.ONNX_MODEL_EXTENSION}"
        if isinstance(model, Module):
            convert_torch_to_onnx(
                torch_model=model,
                model_params=model_params,
                output_file_path=save_path / onnx_name,
                input_data=input_data,
                device=device,
            )
            return save_path / onnx_name
        elif isinstance(model, tf.Module) and model is not None:
            convert_tf_to_onnx(
                model=model,
                output_file_path=save_path / onnx_name,
            )
            return save_path / onnx_name
        elif isinstance(model, tf.keras.Model) and model is not None:
            convert_keras_to_onnx(
                model=model,
                model_params=model_params,
                output_file_path=save_path / onnx_name,
            )
            return save_path / onnx_name
        else:
            raise NotImplementedError(
                f"The ONNX conversion from {type(model)} hasn't "
                f"been implemented yet!"
            )


class CrossConverter(BaseConverter):
    ONNX_EXTENSION = ".onnx"
    TORCH_EXTENSION = ".pt"
    TF_EXTENSION = ".pb"

    def convert(
        self,
        model: Any,
        model_params: ModelParams,
        save_path: Path,
        device: Device,
        input_data: DataManager = None,
    ) -> List[Any]:
        # TODO: Add cross conversion torch-tf
        onnx_path = save_path / f"{self.model_name}{self.ONNX_EXTENSION}"
        if isinstance(model, Module):
            logger.info("Converting the torch model to onnx")
            onnx_path = convert_torch_to_onnx(
                torch_model=model,
                model_params=model_params,
                output_file_path=onnx_path,
                input_data=input_data,
                device=device,
            )

            return (
                [model, str(onnx_path)] if onnx_path is not None else [model]
            )
        elif isinstance(model, tf.Module) and model is not None:
            logger.info("Converting the tensorflow model to onnx")
            onnx_path = convert_tf_to_onnx(
                model=model,
                output_file_path=onnx_path,
            )
            return (
                [model, str(onnx_path)] if onnx_path is not None else [model]
            )

        else:
            # Copy onnx provided model into the tmp dir
            # Loading and saving the model to the new directory
            # enables support also for onnx external data format
            try:
                model_onnx = onnx.load(str(model))
                onnx.save(model_onnx, str(onnx_path))
            except Exception:
                logger.error(
                    "The provided onnx model path is invalid. Please provide"
                    " a valid path to a model in order to use Nebullvm."
                )
                return []

            return [str(onnx_path)]
