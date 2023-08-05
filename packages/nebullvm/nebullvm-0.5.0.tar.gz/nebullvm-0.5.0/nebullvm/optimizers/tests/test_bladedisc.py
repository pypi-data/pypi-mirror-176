from tempfile import TemporaryDirectory

import pytest
import torch

from nebullvm.base import DeepLearningFramework, QuantizationType, Device
from nebullvm.inference_learners.blade_disc import BladeDISCInferenceLearner
from nebullvm.installers.installers import _get_os, get_cpu_arch
from nebullvm.optimizers import BladeDISCOptimizer
from nebullvm.optimizers.tests.utils import initialize_model
from nebullvm.utils.compilers import bladedisc_is_available
from nebullvm.utils.general import gpu_is_available


@pytest.mark.parametrize(
    (
        "output_library",
        "dynamic",
        "quantization_type",
        "metric_drop_ths",
        "metric",
    ),
    [
        (DeepLearningFramework.PYTORCH, True, None, None, None),
        (DeepLearningFramework.PYTORCH, False, None, None, None),
        (
            DeepLearningFramework.PYTORCH,
            False,
            QuantizationType.DYNAMIC,
            2,
            "numeric_precision",
        ),
        (
            DeepLearningFramework.PYTORCH,
            False,
            QuantizationType.HALF,
            2,
            "numeric_precision",
        ),
        (
            DeepLearningFramework.PYTORCH,
            False,
            QuantizationType.STATIC,
            2,
            "numeric_precision",
        ),
    ],
)
@pytest.mark.skipif(
    not bladedisc_is_available(),
    reason="Can't test bladedisc if it's not installed.",
)
def test_bladedisc(
    output_library: DeepLearningFramework,
    dynamic: bool,
    quantization_type: QuantizationType,
    metric_drop_ths: int,
    metric: str,
):
    if (
        _get_os() == "Darwin"
        and get_cpu_arch() == "arm"
        and quantization_type is not None
    ):
        # Quantization doesn't work on M1 chips
        return
    elif (
        not torch.cuda.is_available()
        and quantization_type == QuantizationType.HALF
    ):
        # Half quantization fails on CPU
        return
    elif torch.cuda.is_available() and quantization_type in [
        QuantizationType.STATIC,
        QuantizationType.DYNAMIC,
    ]:
        # Quantization is not supported on GPU
        return

    with TemporaryDirectory() as tmp_dir:
        (
            model,
            input_data,
            model_params,
            input_tfms,
            model_outputs,
            metric,
        ) = initialize_model(dynamic, metric, output_library)

        device = Device.GPU if gpu_is_available() else Device.CPU

        optimizer = BladeDISCOptimizer()
        model, metric_drop = optimizer.optimize(
            model=model,
            output_library=output_library,
            model_params=model_params,
            input_tfms=input_tfms,
            metric_drop_ths=metric_drop_ths,
            quantization_type=quantization_type,
            metric=metric,
            input_data=input_data,
            model_outputs=model_outputs,
            device=device,
        )
        assert isinstance(model, BladeDISCInferenceLearner)
        assert isinstance(model.get_size(), int)

        # Test save and load functions
        model.save(tmp_dir)
        loaded_model = BladeDISCInferenceLearner.load(tmp_dir)
        assert isinstance(loaded_model, BladeDISCInferenceLearner)

        inputs_example = model.get_inputs_example()
        res = model(*inputs_example)
        assert res is not None

        if dynamic:
            inputs_example = [
                input_[: len(input_) // 2] for input_ in inputs_example
            ]
            res = model(*inputs_example)
            assert res is not None
