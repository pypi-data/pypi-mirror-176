import glob
from pathlib import Path

from ecgai_ai_training.models import BuilderParameters, TrainerParameters

RANDOM_STATE = 42


def create_res10(
    ai_model_save_directory: Path, training_set_file_path: Path, validation_set_file_path: Path
) -> TrainerParameters:
    c = TrainerParameters.create(
        random_state=RANDOM_STATE,
        lr=1e-4,
        crop=128,
        cbam=False,
        n_epochs=10,
        batch_size=32,
        model_name="resunet10",
        weight_decay=1e-5,
        ai_model_save_directory=ai_model_save_directory,
        training_set_file_path=training_set_file_path,
        validation_set_file_path=validation_set_file_path,
    )
    return c


def create_builder_parameters(ecg_image_path: Path, base_directory: Path) -> BuilderParameters:
    ai_model_directory = Path(base_directory, "ai-models")
    training_set_file_path = Path(ai_model_directory, "train_set.json.zip")
    validation_set_file_path = Path(ai_model_directory, "valid_set.json.zip")
    ai_model_save_directory = Path(base_directory, "ai-models", "resunet10")
    parameters = BuilderParameters.create(
        random_state=RANDOM_STATE,
        ai_model_save_directory=ai_model_save_directory,
        ecg_image_directory=ecg_image_path,
        ai_model_directory=ai_model_directory,
        base_directory=base_directory,
        training_set_file_path=training_set_file_path,
        validation_set_file_path=validation_set_file_path,
        cv=5,
    )
    if len(glob.glob1(str(parameters.ecg_image_directory), "*.png")) == 0:
        raise ValueError(f"{parameters.ecg_image_directory} does not contain any .png images")
    _create_dir(parameters.ai_model_directory)
    _create_dir(parameters.ai_model_save_directory)

    return parameters


def _create_dir(dir_path: Path):
    if not dir_path.is_dir():
        dir_path.mkdir()
    return
