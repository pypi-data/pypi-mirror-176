import logging
import random
import string
from pathlib import Path

import numpy as np
import pandas as pd
from numpy import ndarray
from skimage.io import imread

from ecgai_ai_training.images import (
    create_binary_image,
    invert_image,
    save_image_as_ubyte,
)
from ecgai_ai_training.models import BuilderParameters
from ecgai_ai_training.service import IService


class ECGTrainerBuilder(IService):
    def __init__(self, builder_parameters: BuilderParameters):
        self.builder_parameters = builder_parameters

    def build(self):
        dataset = self._load_images_data()
        for i in range(1, self.builder_parameters.cv + 1):
            training_data_set, validation_data_set = self._split_dataset(dataset=dataset, position=i)
            self.serialize_data_sets(training_data_set, validation_data_set)
            break

        super(ECGTrainerBuilder, self).build()

    def run(self):
        pass
        # super(ECGTrainerBuilder, self).run()
        # self.__train()

    def load(self):
        self._load_images_data()

    def _load_images_data(self) -> list:
        dataset: list = []
        self.convert_to_binary()

        image_files = [
            f for f in self.builder_parameters.ecg_image_directory.iterdir() if not f.stem.startswith("mask")
        ]

        mask_files = [f for f in self.builder_parameters.ecg_image_directory.iterdir() if f.stem.startswith("mask")]

        for image_file in image_files:
            file_name = image_file.stem
            record_id = self.get_record_number(file_name)

            # find mask image_file by record_id
            mask_file_file_path = [x for x in mask_files if record_id in x.stem]
            # if no mask image found log warning
            if len(mask_file_file_path) != 1:
                logging.warning(f"No mask image found for {file_name}")
                continue

            mask_image = imread(mask_file_file_path[0]) / 255.0
            # TODO check what this function is for
            if np.sum(mask_image) == 0:
                continue

            image = imread(image_file) / 255.0

            image_set = self._create_image_set(image=image, mask_image=mask_image)
            dataset.append(image_set)
        random.seed(self.builder_parameters.random_state)
        random.shuffle(dataset)
        return dataset

    @staticmethod
    def _create_image_set(image: ndarray, mask_image: ndarray) -> list:
        l: list = [image, mask_image]
        return l

    @staticmethod
    def get_record_number(file_name):
        translation_table_letters = str.maketrans("", "", string.ascii_letters)
        translation_table_punctuation = str.maketrans("", "", string.punctuation)
        file_name = file_name.translate(translation_table_letters)
        file_name = file_name.translate(translation_table_punctuation)
        return file_name

    def convert_to_binary(self):
        for image_path in Path.iterdir(self.builder_parameters.ecg_image_directory):
            # print(image_path)
            image = create_binary_image(image_path=image_path)

            if image_path.stem.startswith("mask"):
                print(f"found mask file {image_path.stem}")
                image = invert_image(image=image)

            save_image_as_ubyte(image=image, image_path=image_path)

    def _split_dataset(self, dataset: list, position: int):
        n = len(dataset)
        cv_subjects = int(n / self.builder_parameters.cv) + 1

        idx1 = cv_subjects * (position - 1)
        idx2 = cv_subjects * position if position != self.builder_parameters.cv else n

        train_set = dataset[0:idx1] + dataset[idx2:]
        valid_set = dataset[idx1:idx2]
        return train_set, valid_set

    # def __train(
    #     self,
    # ):
    #     self._create_dir(self.model_save_directory)
    #
    #     with open(self.training_set_file_path, "rb") as f:
    #         training_data_set = pickle.load(f)
    #     with open(self.validation_set_file_path, "rb") as f:
    #         validation_data_set = pickle.load(f)
    #
    #     trainer = ECGTrainer(self.builder_parameters)
    #     trainer.run(training_data_set, validation_data_set, self.model_save_directory)
    #     return

    # def run(self, data_dir, models_dir):
    #     self._load(data_dir)
    #
    #     for i in range(1, self.cv + 1):
    #         train_set, valid_set = self.__split(self.dataset, i)
    #
    #         self._serialize_data_sets(models_dir, train_set, valid_set)
    #
    #         cv_model_dir = os.path.join(models_dir, self.model_path)
    #
    #         self.__train(train_set, valid_set, cv_model_dir)
    #         break
    #     return

    def serialize_data_sets(self, training_data_set: list, validation_data_set: list):
        # "w" - Write - Opens a file for writing, creates the file if it does not exist
        # "b" - Binary - Binary mode (e.g. images)
        # source https://www.w3schools.com/python/python_file_handling.asp
        training_data = pd.DataFrame(training_data_set)
        validation_data = pd.DataFrame(validation_data_set)
        training_data.to_json(path_or_buf=self.builder_parameters.training_set_file_path)
        # training_data.to_pickle(path=self.builder_parameters.training_set_file_path, protocol=4)
        validation_data.to_json(path_or_buf=self.builder_parameters.validation_set_file_path)
        # validation_data.to_pickle(path=self.builder_parameters.validation_set_file_path, protocol=4)
        # with open(self.training_set_file_path, "wb") as f:
        #     pickle.dump(training_data_set, f)
        # with open(self.validation_set_file_path, "wb") as f:
        #     pickle.dump(validation_data_set, f)
