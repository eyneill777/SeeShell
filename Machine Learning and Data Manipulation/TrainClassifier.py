import tensorflow as tf
from tensorflow import keras

with open("config.json", "r") as f:
    config = json.load(f)
    
inputDir = config["genusPath"]

tf.keras.utils.image_dataset_from_directory(
    inputDir,
    labels='inferred', 
    label_mode='categorical', 
    color_mode='rgb', 
    batch_size=32, 
    image_size=(config["imageSize"]["width"], config["imageSize"]["height"]), 
    shuffle=True, 
    validation_split=.1
    )

tf.keras.preprocessing.image.ImageDataGenerator(
    featurewise_center=False,
    samplewise_center=False,
    featurewise_std_normalization=False,
    samplewise_std_normalization=False,
    zca_whitening=False,
    zca_epsilon=1e-06,
    rotation_range=0,
    width_shift_range=0.0,
    height_shift_range=0.0,
    brightness_range=None,
    shear_range=0.0,
    zoom_range=0.0,
    channel_shift_range=0.0,
    fill_mode='nearest',
    cval=0.0,
    horizontal_flip=False,
    vertical_flip=False,
    rescale=None,
    preprocessing_function=None,
    data_format=None,
    validation_split=0.0,
    interpolation_order=1,
    dtype=None
)