import tensorflow as tf
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2
import os

# Path to your SavedModel directory (adjust if different)
saved_model_dir = "plant_disease_saved_model"
# Output TFLite path
out_tflite = os.path.join("assets", "models", "plant_model.tflite")

# Load the SavedModel
print('Loading SavedModel from', saved_model_dir)
loaded = tf.saved_model.load(saved_model_dir)

# Choose a serving signature
if "serving_default" in loaded.signatures:
    concrete_func = loaded.signatures["serving_default"]
else:
    sigs = list(loaded.signatures.keys())
    print('Available signatures:', sigs)
    concrete_func = loaded.signatures[sigs[0]]

print('Freezing variables to constants...')
frozen_func = convert_variables_to_constants_v2(concrete_func)
print('Frozen function inputs:', [t.name for t in frozen_func.inputs])
print('Frozen function outputs:', [t.name for t in frozen_func.outputs])

print('Converting to TFLite...')
converter = tf.lite.TFLiteConverter.from_concrete_functions([frozen_func])

# If conversion fails with unsupported ops, uncomment the following two lines:
# converter.target_spec.supported_ops = [
#     tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS
# ]

# Optional: enable optimizations/quantization
# converter.optimizations = [tf.lite.Optimize.DEFAULT]

try:
    tflite_model = converter.convert()
    os.makedirs(os.path.dirname(out_tflite), exist_ok=True)
    with open(out_tflite, 'wb') as f:
        f.write(tflite_model)
    print('Wrote', out_tflite)
except Exception as e:
    print('Conversion failed:', e)
    raise
