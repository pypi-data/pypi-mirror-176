# Copyright 2022 Alphamed

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Pretraining breast_density_classification models and schedulers.

Reference: https://arxiv.org/abs/2202.08238
"""

import importlib
import json
import os
import sys
from abc import ABCMeta
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Type, overload
from zipfile import ZipFile

import torch
import torch.nn.functional as F
from PIL import Image
from torch import nn, optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

from ... import logger
from ...contractor import TaskContractor
from ...fed_avg import FedAvgScheduler, SecureFedAvgScheduler
from ...scheduler import register_metrics
from ..auto_model import AutoMeta, AutoModel, AutoModelFamily, DatasetMode
from ..cv.auto_model_cv import AutoMetaImageInput, Preprocessor
from ..cvat.annotation import ImageAnnotationUtils
from ..exceptions import AutoModelError, ConfigError


class InceptionPreprocessor(Preprocessor):

    def _resize(self, image: torch.Tensor):
        image = image.permute(0, 2, 1)
        image = F.interpolate(input=image.unsqueeze(0), size=[299, 299], mode='area')
        return image.squeeze()

    def __init__(self, mode: DatasetMode) -> None:
        self. _transformer = (
            transforms.Compose([
                transforms.RandomAffine(degrees=10, translate=(0.02, 0.02)),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Lambda(lambda image: self._resize(image=image)),
            ])
            if mode == DatasetMode.TRAINING else
            transforms.Compose([
                transforms.ToTensor(),
                transforms.Lambda(lambda image: self._resize(image=image)),
            ])
        )

    def transform(self, image_file: str) -> torch.Tensor:
        """Transform an image object into an input tensor."""
        image = Image.open(image_file).convert('RGB')
        return self._transformer(image)


class InceptionDataset(Dataset):

    def __init__(self, image_dir: str, annotation_file: str, mode: DatasetMode) -> None:
        """Init a dataset instance for ResNet auto model families.

        Args:
            image_dir:
                The directory including image files.
            annotation_file:
                The file including annotation information.
            mode:
                One of training or validation or testing.
        """
        super().__init__()
        if not image_dir or not isinstance(image_dir, str):
            raise ConfigError(f'Invalid image directory: {image_dir}.')
        if not annotation_file or not isinstance(annotation_file, str):
            raise ConfigError(f'Invalid annotation file path: {annotation_file}.')
        assert mode and isinstance(mode, DatasetMode), f'Invalid dataset mode: {mode}.'
        if not os.path.exists(image_dir) or not os.path.isdir(image_dir):
            raise ConfigError(f'{image_dir} does not exist or is not a directory.')
        if not os.path.exists(annotation_file) or not os.path.isfile(annotation_file):
            raise ConfigError(f'{annotation_file} does not exist or is not a file.')

        self.image_dir = image_dir
        self.annotation_file = annotation_file
        self.transformer = InceptionPreprocessor(mode=mode)

        self.images, self.labels = ImageAnnotationUtils.parse_single_category_annotation(
            annotation_file=self.annotation_file, resource_dir=image_dir, mode=mode
        )

    def __getitem__(self, index: int):
        _item = self.images[index]
        return self.transformer(_item.image_file), _item.class_label

    def __len__(self):
        return len(self.images)


@dataclass
class AutoMetaInception(AutoMeta):

    input_meta: AutoMetaImageInput
    param_file: str
    model_class: str
    epochs: int
    batch_size: int
    lr: float
    model_file: str = None
    module_dir: str = None

    @classmethod
    def from_json(cls, data: dict) -> 'AutoMetaInception':
        assert data and isinstance(data, dict), f'Invalid meta data: {data}.'

        name = data.get('name')
        input_meta = data.get('input_meta')
        model_file = data.get('model_file')
        module_dir = data.get('module_dir')
        param_file = data.get('param_file')
        model_class = data.get('model_class')
        epochs = data.get('epochs')
        batch_size = data.get('batch_size')
        lr = data.get('lr')
        if (
            not name or not isinstance(name, str)
            or not input_meta or not isinstance(input_meta, dict)
            or (not model_file and not module_dir)
            or (model_file and not isinstance(model_file, str))
            or (module_dir and not isinstance(module_dir, str))
            or not param_file or not isinstance(param_file, str)
            or not model_class or not isinstance(model_class, str)
            or not epochs or not isinstance(epochs, int) or epochs < 1
            or not batch_size or not isinstance(batch_size, int) or batch_size < 1
            or not lr or not isinstance(lr, float) or lr <= 0
        ):
            raise ConfigError(f'Invalid meta data: {data}.')
        if (
            module_dir
            and (not os.path.exists(module_dir) or not os.path.isdir(module_dir))
        ):
            err_msg = f"Module directory doesn't exist or is not a directory: {module_dir}."
            raise ConfigError(err_msg)
        if (
            not module_dir and model_file
            and (not os.path.exists(model_file) or not os.path.isfile(model_file))
        ):
            err_msg = f"Model file doesn't exist or is not a file: {model_file}."
            raise ConfigError(err_msg)
        if not os.path.exists(param_file) or not os.path.isfile(param_file):
            err_msg = f"Param file doesn't exist or is not a file: {param_file}."
            raise ConfigError(err_msg)

        return AutoMetaInception(name=name,
                                 input_meta=AutoMetaImageInput.from_json(input_meta),
                                 param_file=param_file,
                                 epochs=epochs,
                                 batch_size=batch_size,
                                 lr=lr,
                                 model_class=model_class,
                                 model_file=model_file,
                                 module_dir=module_dir)


class AutoInceptionBase(AutoModel, metaclass=ABCMeta):
    """Define common parameters and actions here."""

    def __init__(self,
                 meta_data: dict,
                 resource_dir: str,
                 **kwargs) -> None:
        super().__init__(meta_data=meta_data, resource_dir=resource_dir)
        self._init_meta()
        self.epochs = self.meta.epochs
        self.batch_size = self.meta.batch_size
        self._lr = self.meta.lr
        self._epoch = 0
        self.is_cuda = torch.cuda.is_available()

        self.dataset_dir = None
        self.labels: List[str] = []

        self._best_result = 0
        self._best_state = None
        self._overfit_index = 0
        self._is_dataset_initialized = False
        self._save_root = os.path.join('models', self.meta.name)

    def _init_meta(self):
        model_file = self.meta_data.get('model_file')
        module_dir = self.meta_data.get('module_dir')
        param_file = self.meta_data.get('param_file')
        assert (
            (model_file and isinstance(model_file, str))
            or (module_dir and isinstance(module_dir, str))
        ), f'Invalid meta data: {self.meta_data}'
        assert param_file and isinstance(param_file, str), f'Invalid meta data: {self.meta_data}'
        if module_dir:
            self.meta_data['module_dir'] = os.path.join(self.resource_dir, module_dir)
        else:
            self.meta_data['model_file'] = os.path.join(self.resource_dir, model_file)
        self.meta_data['param_file'] = os.path.join(self.resource_dir, param_file)
        self.meta = AutoMetaInception.from_json(self.meta_data)

    def init_dataset(self, dataset_dir: str) -> bool:
        self.dataset_dir = dataset_dir
        try:
            if not self._is_dataset_initialized:
                self.training_loader
                self.validation_loader
                self.testing_loader
                if not self.training_loader and not self.testing_loader:
                    logger.error('Both training data and testing data are missing.')
                    return False

                self.num_classes = (len(self.training_loader.dataset.labels)
                                    if self.training_loader
                                    else len(self.testing_loader.dataset.labels))
            return bool(
                (self.training_loader and len(self.training_loader) > 0)
                or (self.testing_loader and len(self.testing_loader) > 0)
            )
        except Exception:
            logger.exception('Failed to initialize dataset.')
            return False

    @property
    def annotation_file(self):
        return os.path.join(self.dataset_dir, 'annotation.json') if self.dataset_dir else None

    @property
    def training_loader(self) -> DataLoader:
        """Return a dataloader instance of training data.

        Data augmentation is used to improve performance, so we need to generate a new dataset
        every epoch in case of training on a same dataset over and over again.
        """
        if not hasattr(self, "_training_loader") or self._training_loader_version != self._epoch:
            self._training_loader = self._build_training_data_loader()
            self._training_loader_version = self._epoch
        return self._training_loader

    def _build_training_data_loader(self) -> Optional[DataLoader]:
        dataset = InceptionDataset(image_dir=self.dataset_dir,
                                   annotation_file=self.annotation_file,
                                   mode=DatasetMode.TRAINING)
        if len(dataset) == 0:
            return None
        return DataLoader(dataset=dataset,
                          batch_size=self.batch_size,
                          shuffle=True)

    @property
    def validation_loader(self) -> DataLoader:
        """Return a dataloader instance of validation data."""
        if not hasattr(self, "_validation_loader"):
            self._validation_loader = self._build_validation_data_loader()
        return self._validation_loader

    def _build_validation_data_loader(self) -> DataLoader:
        dataset = InceptionDataset(image_dir=self.dataset_dir,
                                   annotation_file=self.annotation_file,
                                   mode=DatasetMode.VALIDATION)
        if len(dataset) == 0:
            return None
        return DataLoader(dataset=dataset, batch_size=self.batch_size)

    @property
    def testing_loader(self) -> DataLoader:
        """Return a dataloader instance of testing data."""
        if not hasattr(self, "_testing_loader"):
            self._testing_loader = self._build_testing_data_loader()
        return self._testing_loader

    def _build_testing_data_loader(self) -> DataLoader:
        dataset = InceptionDataset(image_dir=self.dataset_dir,
                                   annotation_file=self.annotation_file,
                                   mode=DatasetMode.TESTING)
        if len(dataset) == 0:
            return None
        return DataLoader(dataset=dataset, batch_size=self.batch_size)

    def _build_model(self):
        sys.path.insert(0, self.resource_dir)
        if self.meta.module_dir:
            module = importlib.import_module(os.path.basename(self.meta.module_dir),
                                             self.meta.module_dir)
        else:
            module = importlib.import_module(os.path.basename(self.meta.model_file)[:-3],
                                             self.meta.model_file[:-3])
        model_class = getattr(module, self.meta.model_class)
        _model: nn.Module = model_class(init_weights=False)

        origin_num_classes = 4
        num_classes = origin_num_classes
        fine_tuned_file = os.path.join(self.resource_dir, 'fine_tuned.json')
        if self.dataset_dir and os.path.isdir(self.dataset_dir):
            dataset = InceptionDataset(image_dir=self.dataset_dir,
                                       annotation_file=self.annotation_file,
                                       mode=DatasetMode.PREDICTING)
            self.labels = dataset.labels
            self.num_classes = len(self.labels)
        elif os.path.exists(fine_tuned_file):
            with open(fine_tuned_file, 'r') as f:
                fine_tuned_json: dict = json.load(f)
                self.labels = fine_tuned_json.get('labels')
                self.num_classes = len(self.labels)

        _model.fc = nn.Linear(2048, num_classes)
        with open(self.meta.param_file, 'rb') as f:
            state_dict = torch.load(f)
            if self.num_classes != origin_num_classes:
                state_dict.pop('fc.weight')
                state_dict.pop('fc.bias')
            _model.load_state_dict(state_dict, strict=False)

        return _model.cuda() if self.is_cuda else _model

    def _rebuild_model(self):
        """Rebuild model when context changes.

        The model should be able to be initialized without dataset resources, i.e. in
        predicting mode. However, it perhaps has to change in a later time, for example,
        when start to fine tune depending on user defined dataset and labels.
        """
        self._model = self._build_model()

    @property
    def model(self) -> nn.Module:
        if not hasattr(self, '_model'):
            self._model = self._build_model()
        return self._model

    @property
    def optimizer(self) -> optim.Optimizer:
        if not hasattr(self, '_optimizer'):
            self._optimizer = optim.RMSprop(self.model.parameters(),
                                            lr=self.lr,
                                            alpha=0.9,
                                            eps=1.0,
                                            momentum=0.9)
        else:
            # update lr
            latest_lr = self.lr
            for param_group in self._optimizer.param_groups:
                param_group['lr'] = latest_lr
        return self._optimizer

    @property
    def lr(self) -> float:
        return self._lr * 0.94**((self._epoch - 1) // 2)

    def train(self):
        self.model.train()

    def eval(self):
        self.model.eval()

    @overload
    def forward(self, input: torch.Tensor) -> str:
        """Predict an image's tensor and give its label."""

    @overload
    def forward(self, input: str) -> str:
        """Predict an image defined by a file path and give its label."""

    def forward(self, input):
        if not input or not isinstance(input, (str, torch.Tensor)):
            raise AutoModelError(f'Invalid input data: {input}.')
        if isinstance(input, str):
            if not os.path.isfile(input):
                raise AutoModelError(f'Cannot find or access the image file {input}.')
            preprocessor = InceptionPreprocessor(mode=DatasetMode.PREDICTING)
            input = preprocessor.transform(input)
            input.unsqueeze_(0)
        # TODO eval output unreasonable values, will be fixed later
        # self.model.eval()
        self.model.train()
        input = input.expand(2, 3, 299, 299)  # TODO train mode doesn't accept single input
        output, _ = self.model(input)
        predict = output.argmax(1)[0].item()
        if not self.labels:
            with open(os.path.join(self.resource_dir, 'fine_tuned.json')) as f:
                fine_tuned_json: dict = json.loads(f)
                self.labels = fine_tuned_json.get('labels')
        return self.labels[predict]

    def _train_an_epoch(self):
        self.train()
        for images, targets in self.training_loader:
            if self.is_cuda:
                images, targets = images.cuda(), targets.cuda()
            outputs, aux_outputs = self.model(images)
            loss_1 = F.cross_entropy(outputs, targets)
            loss_2 = F.cross_entropy(aux_outputs, targets)
            loss = loss_1 + 0.4 * loss_2
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    @torch.no_grad()
    def _run_test(self) -> Tuple[float, float]:
        """Run a test and report the result.

        Return:
            avg_loss, correct_rate
        """
        self.push_log(f'Begin testing of epoch {self._epoch}.')
        # TODO eval output unreasonable values, will be fixed later
        # self.eval()
        self.train()
        total_loss = 0
        total_correct = 0
        for images, targets in self.testing_loader:
            if self.is_cuda:
                images, targets = images.cuda(), targets.cuda()
            outputs, _ = self.model(images)
            loss = F.cross_entropy(outputs, targets, reduction='sum').item()
            total_loss += loss
            pred = outputs.max(1, keepdim=True)[1]
            total_correct += pred.eq(targets.view_as(pred)).sum().item()

        avg_loss = total_loss / len(self.testing_loader.dataset)
        correct_rate = total_correct / len(self.testing_loader.dataset) * 100
        logger.info(f'Average Loss: {avg_loss:.4f}')
        logger.info(f'Correct rate: {correct_rate:.2f}')
        self.push_log(f'Testing result:\navg_loss={avg_loss:.4f}\ncorrect_rate={correct_rate:.2f}')

        return avg_loss, correct_rate

    @torch.no_grad()
    def _is_finished(self) -> bool:
        """Decide if stop training.

        If there are validation dataset, decide depending on validatation results. If
        the validation result of current epoch is below the best record for 10 continuous
        times, then stop training.
        If there are no validation dataset, run for `epochs` (default 20) times.
        """
        if not self.validation_loader or len(self.validation_loader) == 0:
            if self._epoch >= self.epochs:
                self._best_state = deepcopy(self.model.state_dict())
            return self._epoch >= self.epochs
        # make a validation
        self.push_log(f'Begin validation of epoch {self._epoch}.')
        # TODO eval output unreasonable values, will be fixed later
        # self.eval()
        self.train()
        total_loss = 0
        total_correct = 0
        for images, targets in self.validation_loader:
            if self.is_cuda:
                images, targets = images.cuda(), targets.cuda()
            outputs, _ = self.model(images)
            loss = F.cross_entropy(outputs, targets, reduction='sum').item()
            total_loss += loss
            pred = outputs.max(1, keepdim=True)[1]
            total_correct += pred.eq(targets.view_as(pred)).sum().item()

        avg_loss = total_loss / len(self.validation_loader.dataset)
        correct_rate = total_correct / len(self.validation_loader.dataset) * 100
        logger.info(f'Average Loss: {avg_loss:.4f}')
        logger.info(f'Correct rate: {correct_rate:.2f}')
        msg = f'Validation result:\navg_loss={avg_loss:.4f}\ncorrect_rate={correct_rate:.2f}'
        self.push_log(msg)

        if correct_rate > self._best_result:
            self._overfit_index = 0
            self._best_result = correct_rate
            self._best_state = deepcopy(self.model.state_dict())
            self.push_log('Validation result is better than last epoch.')
            return False
        else:
            self._overfit_index += 1
            msg = f'Validation result gets worse for {self._overfit_index} consecutive times.'
            self.push_log(msg)
            return self._overfit_index >= 10


class AutoInception(AutoInceptionBase):

    def fine_tune(self,
                  id: str,
                  task_id: str,
                  dataset_dir: str,
                  is_initiator: bool = False,
                  is_debug_script: bool = False):
        self.id = id
        self.task_id = task_id
        self.is_initiator = is_initiator
        self.is_debug_script = is_debug_script

        if not self.init_dataset(dataset_dir):
            raise AutoModelError('Failed to initialize dataset.')
        self._rebuild_model()

        self._save_root = (os.path.join('/data/alphamed-federated', task_id)
                           if not self.is_debug_script
                           else os.path.join('models', 'breast_density_classification'))

        self._epoch = 0
        is_finished = False
        while not is_finished:
            self._epoch += 1
            self.push_log(f'Begin training of epoch {self._epoch}.')
            self._train_an_epoch()
            self.push_log(f'Complete training of epoch {self._epoch}.')
            is_finished = self._is_finished()

        self._save_fine_tuned()
        self._run_test()

    def _save_fine_tuned(self):
        """Save the best or final state of fine tuning."""
        save_dir = os.path.join(self._save_root, 'result')
        os.makedirs(save_dir, exist_ok=True)
        with open(os.path.join(save_dir, 'fine_tuned.pt'), 'wb') as f:
            torch.save(self._best_state, f)
        with open(os.path.join(save_dir, 'fine_tuned.json'), 'w') as f:
            f.write(json.dumps({'labels': self.labels}, ensure_ascii=False))


class AutoInceptionFedAvg(AutoInceptionBase):

    def fine_tune(self,
                  id: str,
                  task_id: str,
                  dataset_dir: str,
                  is_initiator: bool = False,
                  is_debug_script: bool = False):
        self.is_debug_script = is_debug_script

        if not self.init_dataset(dataset_dir):
            raise AutoModelError('Failed to initialize dataset.')
        self._rebuild_model()

        task_contractor = TaskContractor(task_id=task_id)
        self.clients = task_contractor.query_nodes(is_auto_ml=True)

        self.scheduler = InceptionFedAvgScheduler(auto_proxy=self)
        self.scheduler._setup_context(id=id, task_id=task_id, is_initiator=is_initiator)
        self._save_root = self.scheduler._save_root
        if self.is_debug_script:
            self.scheduler.data_channel._ports = [i for i in range(21000, 21010)]
        self.scheduler._launch_process()

    def _save_fine_tuned(self):
        """Save the best or final state of fine tuning."""
        save_dir = os.path.join(self._save_root, 'result')
        os.makedirs(save_dir, exist_ok=True)
        with open(os.path.join(save_dir, 'fine_tuned.pt'), 'wb') as f:
            torch.save(self._best_state, f)
        with open(os.path.join(save_dir, 'fine_tuned.json'), 'w') as f:
            f.write(json.dumps({'labels': self.labels}, ensure_ascii=False))

    def push_log(self, message: str):
        return self.scheduler.push_log(message)

    def _is_finished(self) -> bool:
        if not self.validation_loader or len(self.validation_loader) == 0:
            percent = self._epoch * 100 // self.epochs
            percent = min(percent, 99)
            self.scheduler.contractor.report_progress(percent=percent)
        return super()._is_finished()


class InceptionFedAvgScheduler(FedAvgScheduler):

    def __init__(self, auto_proxy: AutoInceptionFedAvg) -> None:
        super().__init__(min_clients=len(auto_proxy.clients) - 1,
                         max_clients=len(auto_proxy.clients) - 1,
                         max_rounds=auto_proxy.epochs,
                         log_rounds=5,
                         calculation_timeout=3600,
                         data_channel_timeout=(600, 600))
        self.auto_proxy = auto_proxy
        self._is_finished = False

    def build_model(self) -> nn.Module:
        return self.auto_proxy.model

    def build_optimizer(self, model: nn.Module) -> optim.Optimizer:
        return self.auto_proxy.optimizer

    def build_train_dataloader(self) -> DataLoader:
        return self.auto_proxy.training_loader

    def build_validation_dataloader(self) -> DataLoader:
        return self.auto_proxy.validation_loader

    def build_test_dataloader(self) -> DataLoader:
        return self.auto_proxy.testing_loader

    def state_dict(self) -> Dict[str, torch.Tensor]:
        return self.model.state_dict()

    def load_state_dict(self, state_dict: Dict[str, torch.Tensor]):
        self.model.load_state_dict(state_dict)

    def validate_context(self):
        super().validate_context()
        if self.is_initiator:
            assert self.test_loader and len(self.test_loader) > 0, 'failed to load test data'
            self.push_log(f'There are {len(self.test_loader.dataset)} samples for testing.')
        else:
            assert self.train_loader and len(self.train_loader) > 0, 'failed to load train data'
            self.push_log(f'There are {len(self.train_loader.dataset)} samples for training.')

    def train_an_epoch(self):
        self.auto_proxy._epoch = self._round
        self.auto_proxy._train_an_epoch()

    @register_metrics(name='test_results', keys=['average_loss', 'correct_rate'])
    def test(self):
        self.auto_proxy._epoch = self._round
        avg_loss, correct_rate = self.auto_proxy._run_test()
        self.get_metrics('test_results').append_metrics_item({
            'average_loss': avg_loss,
            'correct_rate': correct_rate
        })

    def is_task_finished(self) -> bool:
        return self._is_finished

    def _check_and_run_test(self):
        self.auto_proxy._epoch = self._round
        self._is_finished = self.auto_proxy._is_finished()
        super()._check_and_run_test()

    def _save_model(self):
        self.auto_proxy._save_fine_tuned()

    def _prepare_task_output(self) -> Tuple[str, str]:
        """Generate final output files of the task.

        Return:
            Local paths of the report file and model file.
        """
        self.push_log('Uploading task achievement and closing task ...')

        save_dir = os.path.join(self._save_root, 'result')
        os.makedirs(save_dir, exist_ok=True)

        metrics_files = []
        for _name, _metrics in self._metrics_bucket.items():
            _file = f'{os.path.join(save_dir, _name)}.csv'
            _metrics.to_csv(_file)
            metrics_files.append(_file)
        report_file = os.path.join(save_dir, "report.zip")
        with ZipFile(report_file, 'w') as report_zip:
            for _file in metrics_files:
                report_zip.write(_file, os.path.basename(_file))
        report_file_path = os.path.abspath(report_file)

        # torch.jit doesn't work with a TemporaryFile
        resource_dir = self.auto_proxy.resource_dir
        resource_zip_file = os.path.join(save_dir, 'model.zip')
        with ZipFile(resource_zip_file, 'w') as resource_zip:
            resource_zip.write(os.path.join(save_dir, 'fine_tuned.pt'),
                               self.auto_proxy.meta.param_file)
            resource_zip.write(os.path.join(save_dir, 'fine_tuned.json'),
                               'fine_tuned.json')
            for path, _, filenames in os.walk(resource_dir):
                for _file in filenames:
                    if os.path.join(path, _file) == self.auto_proxy.meta.param_file:
                        continue  # don't save the original params
                    inner_path = path[len(resource_dir):]
                    resource_zip.write(os.path.join(path, _file),
                                       os.path.join(inner_path, _file))
        resource_file_path = os.path.abspath(resource_zip_file)

        self.push_log('Task achievement files are ready.')
        return report_file_path, resource_file_path


class InceptionSecureFedAvgScheduler(SecureFedAvgScheduler):

    def __init__(self, auto_proxy: AutoInceptionFedAvg) -> None:
        super().__init__(min_clients=len(auto_proxy.clients) - 1,
                         max_clients=len(auto_proxy.clients) - 1,
                         t=len(auto_proxy.clients) - 2,
                         log_rounds=5,
                         calculation_timeout=3600,
                         data_channel_timeout=(600, 600))
        self.auto_proxy = auto_proxy
        self._is_finished = False

    def build_model(self) -> nn.Module:
        return self.auto_proxy.model

    def build_optimizer(self, model: nn.Module) -> optim.Optimizer:
        return self.auto_proxy.optimizer

    def build_train_dataloader(self) -> DataLoader:
        return self.auto_proxy.training_loader

    def build_validation_dataloader(self) -> DataLoader:
        return self.auto_proxy.validation_loader

    def build_test_dataloader(self) -> DataLoader:
        return self.auto_proxy.testing_loader

    def state_dict(self) -> Dict[str, torch.Tensor]:
        return self.model.state_dict()

    def load_state_dict(self, state_dict: Dict[str, torch.Tensor]):
        self.model.load_state_dict(state_dict)

    def validate_context(self):
        super().validate_context()
        if self.is_initiator:
            assert self.test_loader and len(self.test_loader) > 0, 'failed to load test data'
            self.push_log(f'There are {len(self.test_loader.dataset)} samples for testing.')
        else:
            assert self.train_loader and len(self.train_loader) > 0, 'failed to load train data'
            self.push_log(f'There are {len(self.train_loader.dataset)} samples for training.')

    def train_an_epoch(self):
        self.auto_proxy._epoch = self._round
        self.auto_proxy._train_an_epoch()

    @register_metrics(name='test_results', keys=['average_loss', 'correct_rate'])
    def test(self):
        self.auto_proxy._epoch = self._round
        avg_loss, correct_rate = self.auto_proxy._run_test()
        self.get_metrics('test_results').append_metrics_item({
            'average_loss': avg_loss,
            'correct_rate': correct_rate
        })

    def is_task_finished(self) -> bool:
        return self._is_finished

    def _check_and_run_test(self):
        self.auto_proxy._epoch = self._round
        self._is_finished = self.auto_proxy._is_finished()
        super()._check_and_run_test()

    def _save_model(self):
        self.auto_proxy._save_fine_tuned()

    def _prepare_task_output(self) -> Tuple[str, str]:
        """Generate final output files of the task.

        Return:
            Local paths of the report file and model file.
        """
        self.push_log('Uploading task achievement and closing task ...')

        save_dir = os.path.join(self._save_root, 'result')
        os.makedirs(save_dir, exist_ok=True)

        metrics_files = []
        for _name, _metrics in self._metrics_bucket.items():
            _file = f'{os.path.join(save_dir, _name)}.csv'
            _metrics.to_csv(_file)
            metrics_files.append(_file)
        report_file = os.path.join(save_dir, "report.zip")
        with ZipFile(report_file, 'w') as report_zip:
            for _file in metrics_files:
                report_zip.write(_file, os.path.basename(_file))
        report_file_path = os.path.abspath(report_file)

        # torch.jit doesn't work with a TemporaryFile
        resource_dir = self.auto_proxy.resource_dir
        resource_zip_file = os.path.join(save_dir, 'model.zip')
        with ZipFile(resource_zip_file, 'w') as resource_zip:
            resource_zip.write(os.path.join(save_dir, 'fine_tuned.pt'),
                               self.auto_proxy.meta.param_file)
            resource_zip.write(os.path.join(save_dir, 'fine_tuned.json'),
                               'fine_tuned.json')
            for path, _, filenames in os.walk(resource_dir):
                for _file in filenames:
                    if os.path.join(path, _file) == self.auto_proxy.meta.param_file:
                        continue  # don't save the original params
                    inner_path = path[len(resource_dir):]
                    resource_zip.write(os.path.join(path, _file),
                                       os.path.join(inner_path, _file))
        resource_file_path = os.path.abspath(resource_zip_file)

        self.push_log('Task achievement files are ready.')
        return report_file_path, resource_file_path


class BreastDensityClassificationFamily(AutoModelFamily):

    BREAST_DENSITY_CLASSIFICATION = 'breast_density_classification'
    BREAST_DENSITY_CLASSIFICATION_FED_AVG = 'breast_density_classification_fed_avg'

    _NAME_MAP = {
        BREAST_DENSITY_CLASSIFICATION: AutoInception,
        BREAST_DENSITY_CLASSIFICATION_FED_AVG: AutoInceptionFedAvg,
    }

    @classmethod
    def get_auto_model(cls, name: str) -> Optional[Type[AutoModel]]:
        return cls._NAME_MAP.get(name)
