Plant Disease Detection

A Flutter mobile application that detects plant leaf diseases using a locally deployed **TensorFlow Lite (TFLite)** deep learning model. The application performs on-device image classification and can optionally retrieve disease information (causes, consequences, and treatment recommendations) through the OpenAI API.

---

# Project Overview

Plant diseases significantly reduce agricultural productivity and crop quality. Early disease detection allows farmers and agricultural professionals to take timely preventive measures.

This project combines:

* **Flutter** for the cross-platform mobile application
* **TensorFlow Lite** for fast on-device inference
* **TensorFlow/Keras** for training the Convolutional Neural Network (CNN)
* **OpenAI API** (optional) to provide additional information about detected diseases

The application allows users to:

* Capture a plant leaf image using the camera
* Select an existing image from the gallery
* Detect the disease locally without an internet connection
* Display the predicted disease and confidence score
* Optionally retrieve causes, consequences, and treatment recommendations using the OpenAI API

---

# Dataset

The CNN model was trained using the **Plant Disease Classification Merged Dataset** available on Kaggle.

**Dataset Source**

https://www.kaggle.com/datasets/alinedobrovsky/plant-disease-classification-merged-dataset

Approximate dataset size:

* **4 GB** (subset used for training)

A larger version of approximately **19 GB** was initially considered. However, due to limited computational resources, unstable electricity supply, and network interruptions during training on Google Colab, a smaller subset was selected to complete the project successfully.

---

# Model Training

The disease classifier is a **Convolutional Neural Network (CNN)** implemented using **TensorFlow/Keras**.

Training characteristics:

* Images resized to **128 × 128 pixels**
* Built using the **Keras Sequential API**
* Three convolutional layers
* TensorFlow/Keras implementation
* Training performed on Google Colab
* 10 training epochs were planned

Although the uploaded training history displays four epochs, this corresponds to an earlier experimental run. The final model was trained using ten epochs.

The training history file is included in the repository.

---

# Application Workflow

1. The user captures or selects a plant leaf image.
2. The image is preprocessed.
3. The TensorFlow Lite model performs local inference.
4. The predicted disease and confidence score are displayed.
5. The user may optionally request additional information from the OpenAI API, including:

   * Causes
   * Consequences
   * Treatment recommendations

> **Note:** The OpenAI integration was implemented but could not be fully tested because a valid API key was unavailable during development.

---

# Project Structure

```
lib/
│
├── main.dart
├── screens/
│   └── homepage.dart
├── services/
│   ├── model_service.dart
│   └── api_service.dart
├── constants/
│   └── api_constants.dart
│
assets/
└── models/
    └── plant_model.tflite
```

---

# Main Components

### `lib/main.dart`

Application entry point and theme configuration.

### `lib/screens/homepage.dart`

Contains the main user interface:

* Image picker
* Camera integration
* Disease prediction
* Result display
* Precaution dialog

### `lib/services/model_service.dart`

Responsible for:

* Loading the TensorFlow Lite model
* Image preprocessing
* Running inference
* Returning the predicted disease and confidence score

### `lib/services/api_service.dart`

Communicates with the OpenAI API to retrieve:

* Causes
* Consequences
* Treatment recommendations

### `assets/models/plant_model.tflite`

Contains the trained TensorFlow Lite model used for on-device inference.

---

# Installation

## Prerequisites

* Flutter SDK
* Android Studio or VS Code
* Android emulator or Android device

Clone the repository:

```bash
git clone https://github.com/Haseeb-Akhlaq/GPT4Vision-Flutter-Plant-Disease-Detechtor.git
cd GPT4Vision-Flutter-Plant-Disease-Detechtor
```

Install dependencies:

```bash
flutter pub get
```

Run the application:

```bash
flutter run
```

---

# TensorFlow Lite Model

Current implementation:

* Input size: **224 × 224**
* Pixel normalization: **[0,1]**
* Softmax applied to output scores
* Highest probability returned as prediction

The current `labelMap` contains placeholder labels (`class_0`, `class_1`, ...). These should be replaced with the actual class names generated during model training.

---

# OpenAI Integration

The application can optionally request structured disease information from the OpenAI API.

The expected response includes:

* Causes
* Consequences
* Treatment

If structured JSON is unavailable, the raw response is displayed instead.

**Security Note**

API keys should never be stored directly in the source code.

For production deployments, API keys should be supplied through:

* Environment variables
* Build-time configuration
* A secure backend service

---

# Development Notes

If model inference fails:

* Verify that the TensorFlow Lite input and output tensor shapes match those expected by `ModelService`.
* Ensure that the preprocessing pipeline matches the preprocessing used during training.
* Replace the placeholder labels with the actual disease classes.

---

# Screenshots

*(Insert screenshots of the application here.)*

Example:

```
screenshots/
    home_page.png
    prediction_result.png
    precautions_dialog.png
```

---

# Technologies Used

* Flutter
* Dart
* TensorFlow
* TensorFlow Lite
* TensorFlow/Keras
* Google Colab
* OpenAI API
* Dio
* Image Picker

---

# Future Improvements

* Improve classification accuracy using a larger dataset
* Train deeper CNN architectures
* Add support for more plant species
* Improve treatment recommendations
* Offline disease information database
* Multi-language support

---

# Acknowledgements

* Kaggle Plant Disease Classification Merged Dataset
* TensorFlow
* Flutter
* Google Colab
* OpenAI

---

# License

This project was developed for academic purposes as part of a university final-year project.
