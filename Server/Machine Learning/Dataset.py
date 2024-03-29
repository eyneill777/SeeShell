import tensorflow as tf

class Dataset:
    """
    Represents the image dataset used in SeeShell
    """
    
    def __init__(self, folderPath, config):
        """
        Loads the dataset and split into separate class objects for training and validation.
        """
        self.folderPath = folderPath
        self.train = tf.keras.utils.image_dataset_from_directory(
            folderPath,
            labels='inferred', 
            label_mode='categorical', 
            color_mode='rgb', 
            subset="training",
            batch_size=128, 
            image_size=(config["imageSize"]["height"], config["imageSize"]["width"]), 
            shuffle=True, 
            seed=123,
            validation_split=.1
            )

        self.validation = tf.keras.utils.image_dataset_from_directory(
            folderPath,
            labels='inferred', 
            label_mode='categorical', 
            color_mode='rgb', 
            subset="validation",
            batch_size=128, 
            image_size=(config["imageSize"]["height"], config["imageSize"]["width"]), 
            shuffle=True, 
            seed=123,
            validation_split=.1
            )
        self.classNames = self.train.class_names
        
        #self.showFirst9Images(self.train)
        
        #Buffered prefetching to speed up I/O
        # AUTOTUNE = tf.data.AUTOTUNE
        # self.train = self.train.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        # self.validation = self.validation.cache().prefetch(buffer_size=AUTOTUNE)
        
    def showFirst9Images(self, dataset):
        """
        Show a plot of the first 9 images in the dataset.
        """
        plt.figure(figsize=(10, 10))
        for images, labels in dataset.take(1):
          for i in range(9):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.axis("off")
        plt.show()
