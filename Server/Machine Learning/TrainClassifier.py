import tensorflow as tf
from tensorflow import keras
import json
import matplotlib.pyplot as plt
from Model import Model
from Dataset import Dataset

with open("config.json", "r") as f:
    config = json.load(f)

class TrainingInstance:    
    """
    Trains a Tensorflow image classifier and saves the model to a file.
    """
    
    def __init__(self):
        """
        Initialize the training session.  Creates a dataset object from the available data, trains a model, and then visualizes the results.
        """
        with open("config.json", "r") as f:
            self.config = json.load(f)
        self.initializeDatasets()
        self.trainModel()
        self.visualizeResults()
        
    def initializeDatasets(self):
        """
        Loads the image data and saves it as a class object
        """
        inputDir = self.config["genusPath"]
        self.dataset = Dataset(inputDir, self.config)
    
    def trainModel(self):
        """
        Initialize the model and train it on the dataset, saving each epoch.
        """
        self.model = Model(self.config, len(self.dataset.classNames))
        self.model.compile(optimizer='adam', loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
        
        saveCallback = tf.keras.callbacks.ModelCheckpoint("model")
        
        self.history = self.model.fit(self.dataset.train, validation_data=self.dataset.validation, epochs=self.config["training"]["epochs"], callbacks = [saveCallback])
        
        tf.saved_model.save(self.model, 'model_prod')
        
    def visualizeResults(self):
        """
        Display plots of the accuracy and loss of both datasets over the course of the training session.
        """
        acc = self.history.history['accuracy']
        val_acc = self.history.history['val_accuracy']

        loss = self.history.history['loss']
        val_loss = self.history.history['val_loss']

        epochs_range = range(self.config["training"]["epochs"])

        plt.figure(figsize=(8, 8))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, acc, label='Training Accuracy')
        plt.plot(epochs_range, val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')

        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label='Training Loss')
        plt.plot(epochs_range, val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')
        plt.show()
        

def main():
    instance = TrainingInstance()

if __name__ == "__main__":
    main()