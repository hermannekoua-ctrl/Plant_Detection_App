import tensorflow as tf

model = tf.keras.models.load_model("plant_disease_model_2.keras")

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

tflite_model = converter.convert()

with open("plant_model.tflite", "wb") as f:
    f.write(tflite_model)

print("Saved plant_model.tflite")