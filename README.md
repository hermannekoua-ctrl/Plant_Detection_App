Plant-Disease-Detection

A Flutter mobile app for identifying plant leaf diseases using a local TensorFlow Lite model and (optionally) fetching structured care/precaution guidance from the OpenAI API.

Quick start

Prerequisites:
- Flutter SDK installed and configured
- A connected device or emulator

Setup and run:

```bash
git clone https://github.com/Haseeb-Akhlaq/GPT4Vision-Flutter-Plant-Disease-Detechtor.git
cd GPT4Vision-Flutter-Plant-Disease-Detechtor
flutter pub get
flutter run
```

Replace the OpenAI API key before using remote API features.

1. How the model was TRAINED //

   Thanks to the google colab resources, we were able to train our model on a dataset from kaggle 'link https://www.kaggle.com/datasets/alinedobrovsky/plant-disease-classification-merged-dataset //'
   it is a convolutional Neural Network (CNN) implemented with TensorFlow/Keras for plant disease image classification. 
   images are resized to 128*128 pixels. the Model is built using Keras Sequentiel API.
   We used 3 CNN layers with the hope of redusing underfitting and overfitting errors. we wanted to go with a large dataset of 19go. After uploading the datasets on two different google drive accounts. After a month of unstable electricity supply plus a disturbing network issue we decided to train a much smaller model.
   The history of the training is listed amongs the files uploaded. we went for 10 epochs thought the file shows 4 due to a trial that failed as we hoped to train it better. 

What this app does (high-level)

- Pick or capture an image of a plant leaf in the UI.
- Run local inference using the bundled TFLite model (`assets/models/plant_model.tflite`) via `tflite_flutter`.
- Display the predicted label and confidence.
- Optionally request structured precautions (causes, consequences, treatment) from OpenAI and display them in a dialog.
- unfortunately we where not able to test this option with a functional openai key.


Key files and responsibilities

- `lib/main.dart`: application entry and theme.
- `lib/screens/homepage.dart`: main UI — image picker, run detection, show results and precautions.
- `lib/services/model_service.dart`: loads the TFLite model, preprocesses images, runs inference, returns label + confidence.
- `lib/services/api_service.dart`: sends requests to OpenAI to obtain structured precaution data or (unused in UI) to call a vision endpoint.
- `lib/constants/api_constants.dart`: contains `baseUrl` and `apiKey` used by `ApiService`.
- `assets/models/plant_model.tflite`: bundled TensorFlow Lite model used for on-device inference.

Model details & implementation notes

- Input size: `ModelService` defaults to `inputSize = 224` and normalizes pixel values to [0,1]. If your model uses a different size or normalisation, update `ModelService` accordingly.
- Labels: `ModelService` currently contains a placeholder `labelMap` (`class_0`, `class_1`, ...). Replace `labelMap` with the real class names produced by your training pipeline so displayed labels are meaningful.
- Output handling: the code expects the model to return logits or scores, applies softmax to compute probabilities, and returns the top class and confidence.

OpenAI usage

- `lib/services/api_service.dart` uses `https://api.openai.com/v1` endpoints via `dio`.
- IMPORTANT: The repository currently contains a plaintext OpenAI API key in `lib/constants/api_constants.dart`. Treat API keys as sensitive secrets. Do NOT commit real keys to a public repo. Replace the hard-coded key with one of these safer options before publishing:
   - Provide the key via CI or build-time environment variables and inject into the app (for development, use a local secrets file excluded from version control).
   - Use a lightweight backend service to proxy requests to OpenAI (recommended for production).

How the precautions flow works

- After local detection, tapping `PRECAUTION` calls `ApiService.sendMessageGPT(diseaseName: ...)` which asks the model to return a JSON object with keys `causes`, `consequences`, and `treatment` (each an array of short sentences).
- If the OpenAI model returns non-JSON text, the app stores the raw text under the `raw` key and displays it.

Development and debugging 

- If inference fails, confirm the TFLite model input/output shapes match `ModelService` expectations. You can print `_interpreter!.getInputTensors()` and output tensor shapes during development.
- To get correct human-readable labels: open the original training pipeline or dataset labels file and paste the class names into `labelMap` in `lib/services/model_service.dart`.
- To test OpenAI calls safely, remove the API key from `lib/constants/api_constants.dart` and instead set it at runtime via environment or a local-only file.






## My working directory C:\Users\EKOUA II\Desktop\GPT4Vision-Flutter-Plant-Disease-Detechtor-main



