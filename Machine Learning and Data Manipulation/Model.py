from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

class Model(Sequential):
    def __init__(self, config, numClasses):
        super().__init__()
        self.add(layers.Rescaling(1./255, input_shape=(config["imageSize"]["height"], config["imageSize"]["width"], 3)))
        self.add(layers.Conv2D(16, 3, padding='same', activation='relu'))
        self.add(layers.MaxPooling2D())
        self.add(layers.Conv2D(32, 3, padding='same', activation='relu'))
        self.add(layers.MaxPooling2D())
        self.add(layers.Conv2D(64, 3, padding='same', activation='relu'))
        self.add(layers.MaxPooling2D())
        self.add(layers.Flatten())
        self.add(layers.Dense(128, activation='relu'))
        self.add(layers.Dropout(0.5))
        self.add(layers.Dense(numClasses))