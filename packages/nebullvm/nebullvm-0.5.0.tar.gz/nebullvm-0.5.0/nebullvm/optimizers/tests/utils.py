import os
from typing import Tuple

import torch
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import Model, layers
from transformers import AlbertModel, AlbertTokenizer

from nebullvm.api.functions import (
    _extract_info_from_data,
    _benchmark_original_model,
)
from nebullvm.api.huggingface import convert_hf_model
from nebullvm.base import ModelParams, DeepLearningFramework, Device
from nebullvm.config import TRAIN_TEST_SPLIT_RATIO
from nebullvm.converters.torch_converters import convert_torch_to_onnx
from nebullvm.measure import compute_relative_difference
from nebullvm.transformations.base import MultiStageTransformation
from nebullvm.utils.data import DataManager
from nebullvm.utils.general import gpu_is_available

INPUT_SHAPE = (3, 256, 256)
OUTPUT_SHAPE = (2,)
STATIC_BATCH_SIZE = 1
DYNAMIC_BATCH_SIZE = 2


class TestModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = torch.nn.Conv2d(
            in_channels=3, out_channels=64, kernel_size=3
        )
        self.relu1 = torch.nn.ReLU()
        self.conv2 = torch.nn.Conv2d(
            in_channels=64, out_channels=32, kernel_size=3
        )
        self.relu2 = torch.nn.ReLU()
        self.fcn = torch.nn.Linear(32, 2)

    def forward(self, input_tensor_0, input_tensor_1):
        x0 = self.relu2(self.conv2(self.relu1(self.conv1(input_tensor_0))))
        x1 = self.relu2(self.conv2(self.relu1(self.conv1(input_tensor_1))))
        x = x0 + x1
        x = self.fcn(x.mean(dim=(-2, -1)).view(-1, 32))
        return x


def tensorflow_model():
    input_0 = keras.Input(shape=(256, 256, 3))
    input_1 = keras.Input(shape=(256, 256, 3))
    x0 = layers.Conv2D(64, kernel_size=(3, 3), activation="relu")(input_0)
    x1 = layers.Conv2D(64, kernel_size=(3, 3), activation="relu")(input_1)
    x0 = layers.Conv2D(32, kernel_size=(3, 3), activation="relu")(x0)
    x1 = layers.Conv2D(32, kernel_size=(3, 3), activation="relu")(x1)
    x = x0 + x1
    y = layers.Dense(2, activation="softmax")(x)
    return Model(inputs=[input_0, input_1], outputs=y)


def _build_static_model(
    framework: DeepLearningFramework = DeepLearningFramework.PYTORCH,
) -> Tuple[torch.nn.Module, ModelParams]:
    model_params = {
        "batch_size": STATIC_BATCH_SIZE,
        "input_infos": [
            {"size": INPUT_SHAPE, "dtype": "float"},
            {"size": INPUT_SHAPE, "dtype": "float"},
        ],
        "output_sizes": [OUTPUT_SHAPE],
    }
    model_params = ModelParams(**model_params)
    if framework == DeepLearningFramework.PYTORCH:
        model = TestModel()
    elif framework == DeepLearningFramework.TENSORFLOW:
        model = tensorflow_model()
    else:
        raise NotImplementedError
    return model, model_params


def _build_dynamic_model(
    framework: DeepLearningFramework,
) -> Tuple[torch.nn.Module, ModelParams]:
    model_params = {
        "batch_size": DYNAMIC_BATCH_SIZE,
        "input_infos": [
            {"size": INPUT_SHAPE, "dtype": "float"},
            {"size": INPUT_SHAPE, "dtype": "float"},
        ],
        "output_sizes": [OUTPUT_SHAPE],
        "dynamic_info": {
            "inputs": [{0: "batch_size"}, {0: "batch_size"}],
            "outputs": [{0: "batch_size"}],
        },
    }
    if framework == DeepLearningFramework.PYTORCH:
        model = TestModel()
    elif framework == DeepLearningFramework.TENSORFLOW:
        model = tensorflow_model()
    else:
        raise NotImplementedError
    return model, ModelParams(**model_params)


def get_onnx_model(temp_dir: str, dynamic: bool = False):
    model_path = os.path.join(temp_dir, "test_model.onnx")
    if dynamic:
        model, model_params = _build_dynamic_model()
    else:
        model, model_params = _build_static_model()
    device = Device.GPU if gpu_is_available() else Device.CPU
    convert_torch_to_onnx(model, model_params, model_path, device)
    return model_path, model_params


def get_torch_model(dynamic: bool = False):
    if dynamic:
        model, model_params = _build_dynamic_model(
            DeepLearningFramework.PYTORCH
        )
    else:
        model, model_params = _build_static_model(
            DeepLearningFramework.PYTORCH
        )
    return model, model_params


def get_tensorflow_model(dynamic: bool = False):
    if dynamic:
        model, model_params = _build_dynamic_model(
            DeepLearningFramework.TENSORFLOW
        )
    else:
        model, model_params = _build_static_model(
            DeepLearningFramework.TENSORFLOW
        )
    return model, model_params


def get_huggingface_model(temp_dir: str, dl_framework: DeepLearningFramework):
    tokenizer = AlbertTokenizer.from_pretrained("albert-base-v1")
    model = AlbertModel.from_pretrained("albert-base-v1")

    text = "Short text you wish to process"
    encoded_input = tokenizer(text, return_tensors="pt")
    device = Device.GPU if gpu_is_available() else Device.CPU

    (
        model,
        input_data,
        input_names,
        output_structure,
        output_type,
    ) = convert_hf_model(model, [encoded_input], device=device)

    input_data = DataManager(input_data)
    input_data.split(TRAIN_TEST_SPLIT_RATIO)

    model_outputs, _ = _benchmark_original_model(
        model,
        input_data.get_split("test"),
        dl_framework,
        compute_output=True,
        device=device,
    )

    model_path = os.path.join(temp_dir, "test_model.onnx")

    model_params = _extract_info_from_data(
        model, input_data, dl_framework, None, device
    )

    device = Device.GPU if gpu_is_available() else Device.CPU
    convert_torch_to_onnx(model, model_params, model_path, device, input_data)

    return (
        model_path,
        model_params,
        output_structure,
        input_names,
        output_type,
        input_data,
        model_outputs,
    )


def initialize_model(
    dynamic: bool,
    metric: str,
    output_library: DeepLearningFramework,
):
    device = Device.GPU if gpu_is_available() else Device.CPU
    batch_size = DYNAMIC_BATCH_SIZE if dynamic else STATIC_BATCH_SIZE

    if output_library == DeepLearningFramework.PYTORCH:
        model, model_params = get_torch_model(dynamic)

        input_data = DataManager(
            [
                (
                    (
                        torch.randn(batch_size, *INPUT_SHAPE),
                        torch.randn(batch_size, *INPUT_SHAPE),
                    ),
                    torch.zeros(batch_size, dtype=torch.long),
                )
            ]
        )
    elif output_library == DeepLearningFramework.TENSORFLOW:
        model, model_params = get_tensorflow_model(dynamic)
        input_data = DataManager(
            [
                (
                    (
                        tf.random_normal_initializer()(
                            shape=(
                                batch_size,
                                *INPUT_SHAPE[1:],
                                INPUT_SHAPE[0],
                            )
                        ),
                        tf.random_normal_initializer()(
                            shape=(
                                batch_size,
                                *INPUT_SHAPE[1:],
                                INPUT_SHAPE[0],
                            )
                        ),
                    ),
                    [0 for _ in range(batch_size)],
                )
            ]
        )

    input_data.split(TRAIN_TEST_SPLIT_RATIO)
    input_tfms = MultiStageTransformation([])

    model_outputs, _ = _benchmark_original_model(
        model,
        input_data.get_split("test"),
        output_library,
        compute_output=True,
        device=device,
    )

    if metric is not None:
        metric = compute_relative_difference

    return model, input_data, model_params, input_tfms, model_outputs, metric
