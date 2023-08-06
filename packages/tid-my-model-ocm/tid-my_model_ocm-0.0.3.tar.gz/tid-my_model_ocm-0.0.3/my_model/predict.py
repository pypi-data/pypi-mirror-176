import pandas as pd

from my_model import __version__ as _version
from my_model.config.core import config
from my_model.processing.data_manager import load_pipeline

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_survived_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(
    input_data: pd.DataFrame,
):
    """Make a prediction using a saved model pipeline."""
    data = pd.DataFrame(input_data)
    return _survived_pipe.predict(data)
