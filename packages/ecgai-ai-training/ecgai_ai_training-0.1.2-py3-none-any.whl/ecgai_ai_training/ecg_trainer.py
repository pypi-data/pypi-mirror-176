from pathlib import Path

import numpy as np
import pandas as pd
import torch
from adabound import AdaBound
from sklearn.metrics import f1_score

from ecgai_ai_training.ecg_loader import ECGDataLoader
from ecgai_ai_training.models import TrainerParameters
from ecgai_ai_training.neural_losses import ComboLoss
from ecgai_ai_training.neural_models import build_model

# from adabound import AdaBound
# from sklearn.metrics import f1_score
#
# from ecg_loader import ECGDataLoader
# from ecg_losses import ComboLoss
# from ecg_models import build_model


class ECGTrainer(object):
    # lr: float = 1e-4
    # crop: int = 128
    # cbam: bool = False
    # n_epochs: int = 100
    # batch_size: int = 32
    # model_name: str = 'resunet10'
    # weight_decay: float = 1e-5
    # random_state: int = 42
    # def __init__(self, random_state: int, crop: int, cbam: bool, model_name: str, n_epochs: int, batch_size: int,
    #              lr: float, weight_decay: float):
    def __init__(self, trainer_parameters: TrainerParameters):

        if not trainer_parameters.training_set_file_path.is_file():
            raise ValueError(f"{trainer_parameters.training_set_file_path} does not contain a training set file")
        if not trainer_parameters.validation_set_file_path.is_file():
            raise ValueError(f"{trainer_parameters.validation_set_file_path} does not contain a validation set file")

        self.training_set_file_path = trainer_parameters.training_set_file_path
        self.validation_set_file_path = trainer_parameters.validation_set_file_path
        torch.set_num_threads(3)
        np.random.seed(trainer_parameters.random_state)
        torch.manual_seed(trainer_parameters.random_state)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        #
        # self.training_set_file_path = trainer_parameters.training_set_file_path
        # self.validation_set_file_path = trainer_parameters.validation_set_file_path
        self.ai_model_save_directory = trainer_parameters.ai_model_save_directory
        if not self.ai_model_save_directory.is_dir():
            self.ai_model_save_directory.mkdir()

        self.crop = trainer_parameters.crop
        self.cbam = trainer_parameters.cbam
        self.model_name = trainer_parameters.model_name
        self.n_epochs = trainer_parameters.n_epochs
        self.batch_size = trainer_parameters.batch_size

        self.cuda = torch.cuda.is_available()
        self.model = self.__build_model()
        self.criterion = self.__get_criterion()
        self.opt, self.sche = self.__get_optimizer(
            lr=trainer_parameters.lr, weight_decay=trainer_parameters.weight_decay
        )
        return

    def __build_model(self):
        model = build_model(self.model_name, self.cbam)
        if self.cuda:
            model.cuda()
        return model

    @staticmethod
    def __get_criterion():
        criterion = ComboLoss(
            weights={"dice": 1, "focal": 1}, channel_weights=[1], channel_losses=[["dice", "focal"]], per_image=False
        )
        return criterion

    def __get_optimizer(self, lr, weight_decay):
        optimizer = AdaBound(amsbound=True, lr=lr, params=self.model.parameters(), weight_decay=weight_decay)

        scheduler = None
        # scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        #     optimizer, 'min', factor=0.5,
        #     patience=10, verbose=True, min_lr=1e-5
        # )
        # scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=25, gamma=0.5)
        return optimizer, scheduler

    def run(self):
        print("=" * 100)
        print("TRAINING MODEL - {}".format(self.model_name))
        print("-" * 100 + "\n")
        train_set = self.read_json(file_path=self.training_set_file_path)
        valid_set = self.read_json(file_path=self.validation_set_file_path)
        model_path = Path(self.ai_model_save_directory, "model_name.pth")
        # loader_params = {'batch_size': self.batch_size, 'crop': self.crop}
        dataloader = {
            "train": ECGDataLoader(train_set, batch_size=self.batch_size, crop=self.crop, augment=True).build(),
            "valid": ECGDataLoader(valid_set, batch_size=self.batch_size, crop=self.crop, augment=False).build(),
        }

        best_loss = None
        for epoch in range(self.n_epochs):
            e_message = "[EPOCH {:0=3d}/{:0=3d}]".format(epoch + 1, self.n_epochs)

            for phase in ["train", "valid"]:
                ep_message = e_message + "[" + phase.upper() + "]"
                if phase == "train":
                    self.model.train()
                else:
                    self.model.eval()

                f1s, losses = [], []
                batch_num = len(dataloader[phase])

                batch_num = len(dataloader[phase])
                for ith_batch, data in enumerate(dataloader[phase]):
                    patches, masks = [d.cuda() for d in data] if self.cuda else data
                    patches = patches.squeeze(0)
                    masks = masks.squeeze(0)

                    pred = self.model(patches)
                    loss = self.criterion(pred, masks)

                    pred = torch.sigmoid(pred)
                    pred[pred > 0.5] = 1
                    pred[pred <= 0.5] = 0
                    pred = pred.cpu().detach().numpy().flatten()
                    label = masks.cpu().detach().numpy().flatten()
                    f1 = f1_score(label, pred, average="macro")

                    f1s.append(f1)
                    losses.append(loss.item())

                    if phase == "train":
                        self.opt.zero_grad()
                        loss.backward()
                        self.opt.step()

                    sr_message = "[STEP {:0=3d}/{:0=3d}]-[F1: {:.6f} LOSS: {:.6f}]"
                    sr_message = ep_message + sr_message
                    print(sr_message.format(ith_batch + 1, batch_num, f1, loss), end="\r")

                avg_f1 = np.mean(f1s)
                avg_loss = np.mean(losses)

                er_message = "[AVERAGE][F1: {:.6f} LOSS: {:.6f}]"
                er_message = "\n\033[94m" + ep_message + er_message + "\033[0m"
                print(er_message.format(avg_f1, avg_loss))

                if phase == "valid":
                    if self.sche is not None:
                        # self.sche.step(avg_loss)
                        self.sche.step()

                    if best_loss is None or best_loss > avg_loss:
                        best_loss = avg_loss
                        best_loss_mtc = [epoch + 1, avg_f1, avg_loss]
                        torch.save(self.model.state_dict(), model_path)
                        print("[Best validation loss, model_name: {}]".format(model_path))

                    print()

        res_message = (
            "VALIDATION PERFORMANCE: BEST LOSS"
            + "\n"
            + "[EPOCH:{} F1: {:.6f} LOSS:{:.6f}]\n".format(best_loss_mtc[0], best_loss_mtc[1], best_loss_mtc[2])
            + "=" * 100
            + "\n"
        )

        print(res_message)
        return

    @staticmethod
    def read_json(file_path: Path) -> list:
        if not file_path.is_file():
            raise ValueError(f"{file_path} does not contain a file")
        df = pd.read_json(path_or_buf=file_path)
        return df.values.tolist()
