from abc import ABC
from pathlib import Path

import pydantic
from pydantic import Field

from ecgai_ai_training.model_base import MyBaseModel

# class MyBaseModel(MyBaseModel):
#     def __hash__(self):  # make hashable BaseModel subclass
#         return hash((type(self),) + tuple(self.__dict__.values()))


class TrainerParameters(MyBaseModel, ABC):
    random_state: int
    crop: int
    cbam: bool = Field(description="to use or not use the Convolution Block Attention Module")
    model_name: str
    n_epochs: int = Field(
        description="The is the number of complete passes through the training dataset. The size of "
        "a batch must be more than or equal to one and less than or equal to the number "
        "of samples in the training dataset"
    )
    batch_size: int
    lr: float = Field(description="Adam learning rate (default: 1e-3)")
    weight_decay: float = (
        Field(
            description="Weight decay is a regularization technique by adding a small penalty, "
            "usually the L2 norm of the weights (all the weights of the model), "
            "to the loss function. loss = loss + weight decay parameter * L2 norm of "
            "the weights"
        ),
    )
    training_set_file_path: Path
    validation_set_file_path: Path
    ai_model_save_directory: Path

    @classmethod
    def create(
        cls,
        random_state: int,
        crop: int,
        cbam: bool,
        model_name: str,
        n_epochs: int,
        batch_size: int,
        lr: float,
        weight_decay: float,
        training_set_file_path: Path,
        validation_set_file_path: Path,
        ai_model_save_directory: Path,
    ):
        try:
            d = dict(
                RandomState=random_state,
                Crop=crop,
                Cbam=cbam,
                ModelName=model_name,
                NEpochs=n_epochs,
                BatchSize=batch_size,
                Lr=lr,
                WeightDecay=weight_decay,
                TrainingSetFilePath=training_set_file_path,
                ValidationSetFilePath=validation_set_file_path,
                AiModelSaveDirectory=ai_model_save_directory,
            )
            return cls.from_dict(d)
        except pydantic.ValidationError as e:
            # logging.error(e)
            raise e


class BuilderParameters(MyBaseModel, ABC):
    ai_model_save_directory: Path = Field(description="path model will be saved from the default path")
    ecg_image_directory: Path
    ai_model_directory: Path
    base_directory: Path
    training_set_file_path: Path
    validation_set_file_path: Path
    cv: int = Field(
        description="Cross-validation is a statistical method used to estimate the skill of machine " "learning models."
    )
    random_state: int

    @classmethod
    def create(
        cls,
        random_state: int,
        ai_model_save_directory: Path,
        ecg_image_directory: Path,
        ai_model_directory: Path,
        base_directory: Path,
        training_set_file_path: Path,
        validation_set_file_path: Path,
        cv: int,
    ):
        try:
            d = dict(
                RandomState=random_state,
                AiModelSaveDirectory=ai_model_save_directory,
                EcgImageDirectory=ecg_image_directory,
                AiModelDirectory=ai_model_directory,
                BaseDirectory=base_directory,
                TrainingSetFilePath=training_set_file_path,
                ValidationSetFilePath=validation_set_file_path,
                Cv=cv,
            )
            return cls.from_dict(d)
        except pydantic.ValidationError as e:
            # logging.error(e)
            raise e


#
# class Resunet10(BuilderParameters):
#     """
#     The default values of the Resunet10 neural model
#     """
#
#     lr = 1e-4
#     crop = 128
#     cbam = False
#     n_epochs = 10
#     batch_size = 32
#     model_name = "resunet10"
#     weight_decay = 1e-5
#     random_state = 42
#     cv = 5
#     base_directory: Path
#     ai_model_directory: Path
#     # = Path(base_directory, 'ai-models')
#     # ai_model_directory = os.path.abspath(, "ai-models"))
#     ai_model_save_directory: Path
#     # = Path(base_directory, "ai-models", "resunet10")
#     # os.path.abspath(        os.path.join(Path(Path.cwd()), "ai-models", "resunet10")
#     # )
#     ecg_image_directory = os.path.abspath(os.path.join(Path(Path.cwd()), "test_data/ecg_training_printout/"))
#
#     def __init__(self, base_directory: Path = Path(Path.cwd())):
#         self.base_directory = base_directory
#         self.ai_model_directory = Path(base_directory, "ai-models")
#         # self.ai_model_directory = os.path.abspath(, "ai-models"))
#         self.ai_model_save_directory = Path(base_directory, "ai-models", "resunet10")
#         super().__init__()
