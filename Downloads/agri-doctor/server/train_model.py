# train_model.py

import os
import json
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam

# Paths
dataset_dir = "dataset"
train_dir = os.path.join(dataset_dir, "train")
test_dir = os.path.join(dataset_dir, "test")
model_dir = "model"
os.makedirs(model_dir, exist_ok=True)

# Image parameters
IMG_SIZE = (224, 224)
BATCH_SIZE = 16

# Data generators
train_datagen = ImageDataGenerator(rescale=1./255, horizontal_flip=True, rotation_range=20)
test_datagen = ImageDataGenerator(rescale=1./255)

train_gen = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

test_gen = test_datagen.flow_from_directory(
    test_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# Save class indices
with open(os.path.join(model_dir, "class_indices.json"), "w") as f:
    json.dump(train_gen.class_indices, f)

# Build model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224,224,3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
predictions = Dense(len(train_gen.class_indices), activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=predictions)

# Freeze base layers
for layer in base_model.layers:
    layer.trainable = False

# Compile
model.compile(optimizer=Adam(1e-4), loss='categorical_crossentropy', metrics=['accuracy'])

# Train
model.fit(train_gen, validation_data=test_gen, epochs=5)

# Save model
model.save(os.path.join(model_dir, "plant_disease_model.h5"))

print("Training complete! Model saved in 'model/plant_disease_model.h5'")
