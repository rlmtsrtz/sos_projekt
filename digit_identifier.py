import os
import time
import torch
import matplotlib.pyplot as plt
from model_functions import NeuralNet, get_loss_fn, get_memory_usage, save_all, get_optimizer
from torchvision import datasets
from torchvision.transforms import ToTensor
from torch.utils.data import DataLoader


class DigitIdentifier:
    def __init__(self, train_data=None, test_data=None, batch_size=64, load=False, csv_index=0, forward_dict=None,
                 loss_fn=None, optimizer=None, lr=0.1, momentum=0.8, weight_decay=0.0001, info=False):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.info = info
        self.csv_path = 'panda_tables/runs_digit_identifier.csv'
        self.dict_path = 'dictionarys/digit_identifier/forward_dictionary'
        self.model_path = 'models/digit_identifier/digit_identifier'
        if self.info:
            print(f"Using {self.device} device")
        self.epochs = None
        self.train_data = self.get_data(train_data, train=True)
        self.test_data = self.get_data(test_data, train=False)
        self.batch_size = batch_size
        self.forward_dict = forward_dict
        self.train_dataloader = DataLoader(self.train_data, batch_size=self.batch_size)
        self.test_dataloader = DataLoader(self.test_data, batch_size=self.batch_size)
        self.model = self.get_model(forward_dict=forward_dict, load=load, csv_index=csv_index)
        self.best_model = None
        if load is False:
            self.loss_fn = get_loss_fn(loss_fn)
            self.lr = lr
            self.momentum = momentum
            self.weight_decay = weight_decay
            self.optimizer = get_optimizer(model=self, optimizer=optimizer)
        self.needed_time = None
        self.memory_total = None
        self.memory_used = None
        self.memory_free = None
        self.average_accuracy_train = None
        self.average_accuracy_test = 0
        self.average_loss_train = None
        self.average_loss_test = None

    # Das neuronale Netz wird erstellt oder geladen. Hier pictureSize für jeden Datensatz Hard-Coden.
    def get_model(self, forward_dict=None, load=False, csv_index=0):
        path = f"models/digit_identifier/digit_identifier{csv_index}.pt"
        if load is True and os.path.isfile(path) is True:
            model = torch.load(path).to(self.device)
        else:
            model = NeuralNet(forward_dict=forward_dict, picture_size=28).to(self.device)
        return model

    # Das Netz wird trainiert und gestoppt, sobald es 4 mal schlechter als das bisher beste Ergebnis war (early-stopping)
    def train_model(self, stop_counter_max=3):
        start_time = time.time()
        correct = None
        train_loss = None
        average_accuracy_test_best = -1
        epoch = -1
        stop_counter = 0
        while stop_counter <= stop_counter_max:
            epoch += 1
            self.model.train()
            train_loss, correct = 0, 0
            for batch_id, (data, target) in enumerate(self.train_dataloader):
                data, target = data.to(self.device), target.to(self.device)
                self.optimizer.zero_grad()
                prediction = self.model(data)

                loss = self.loss_fn(prediction, target)
                loss.backward()
                self.optimizer.step()

                train_loss += loss.item()
                correct += (prediction.argmax(1) == target).type(torch.float).sum().item()
                if batch_id % 200 == 0 and self.info:
                    print(f"current loss: {loss.item()} ")
            train_loss /= len(self.train_data)
            correct /= len(self.train_dataloader.dataset)
            if self.info:
                print(f"Train Error (epoch: {epoch + 1}): Average accuracy: {(100 * correct)}%, "
                      f"Average loss: {train_loss}\n")
            self.test_model()
            if average_accuracy_test_best < self.average_accuracy_test:
                average_accuracy_test_best = self.average_accuracy_test
                save_all(model=self, model_save=True, rest_save=False)
                self.epochs = epoch + 1
                stop_counter = 0
            else:
                stop_counter += 1

        self.average_accuracy_test = average_accuracy_test_best
        self.needed_time = time.time() - start_time
        self.memory_total = get_memory_usage('total')
        self.memory_used = get_memory_usage('used')
        self.memory_free = self.memory_total - self.memory_used
        self.average_accuracy_train = 100 * correct
        self.average_loss_train = train_loss
        save_all(model=self, model_save=False, rest_save=True)

    # Das Netz wird bisher unbekannten Daten getestet
    def test_model(self):
        self.model.eval()
        test_loss, correct = 0, 0
        with torch.no_grad():
            for data, target in self.test_dataloader:
                data, target = data.to(self.device), target.to(self.device)
                prediction = self.model(data)
                test_loss += self.loss_fn(prediction, target).item()
                correct += (prediction.argmax(1) == target).type(torch.float).sum().item()
        test_loss /= len(self.test_dataloader)
        correct /= len(self.test_dataloader.dataset)
        if self.info:
            print(f"Test Error: Accuracy: {(100 * correct)}%, Average loss: {test_loss} \n")
        self.average_accuracy_test = 100 * correct
        self.average_loss_test = test_loss

    # Das Netz kann mit visualisierung der Bilder ausprobiert werden.
    # show ist die Anzahl der Bilder, die gezeigt werden sollen.
    def try_model(self, show=5):
        shown = 0
        self.model.eval()
        images, labels = next(iter(self.test_dataloader))
        with torch.no_grad():
            for data, target in self.test_dataloader:
                data, target = data.to(self.device), target.to(self.device)
                prediction = self.model(data)
                for i in range(data.size()[0]):
                    if prediction[i].argmax(0) == target[i]:
                        plt.title(f'Prediction: {prediction[i].argmax(0)} -> Correct!')
                        plt.imshow(images[i].numpy()[0], cmap="summer")
                        plt.show()
                    else:
                        plt.title(f'Prediction: {prediction[i].argmax(0)} -> Not correct!')
                        plt.imshow(images[i].numpy()[0], cmap="autumn")
                        plt.show()
                    shown += 1
                    if shown >= show:
                        break
                if shown >= show:
                    break

    # Hier werden die Daten geladen
    @staticmethod
    def get_data(data, train=True):
        if data is None:
            data = datasets.MNIST(
                root="data",
                train=train,
                download=True,
                transform=ToTensor(),
            )
        return data
