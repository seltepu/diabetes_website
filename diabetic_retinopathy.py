import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator


train_datagen = ImageDataGenerator(rescale=1./255,  
                                   validation_split=0.1)  

train = train_datagen.flow_from_directory('C:/Users/shive/Downloads/archive', 
                                                    target_size=(128, 128), 
                                                    batch_size=32,
                                                    class_mode='categorical',
                                                    subset='training')

validation = train_datagen.flow_from_directory('C:/Users/shive/Downloads/archive',  
                                                         target_size=(128, 128),
                                                         batch_size=32,
                                                         class_mode='categorical',
                                                         subset='validation')

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),  
    layers.MaxPooling2D((2, 2)),  
    layers.Conv2D(64, (3, 3), activation='relu'),  
    layers.MaxPooling2D((2, 2)),  
    layers.Conv2D(128, (3, 3), activation='relu'), 
    layers.MaxPooling2D((2, 2)),  
    layers.Flatten(),  
    layers.Dense(128, activation='relu'),  
    layers.Dense(3, activation='softmax')  
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(train,
                    epochs=10,  
                    validation_data=validation)

model.save('diabetic_retinopathy_classifier.keras')
