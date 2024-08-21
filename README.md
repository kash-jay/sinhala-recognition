# Sinhala Recognition

## Description
This project focuses on recognizing handwritten Sinhala characters using a CNN model. It addresses the challenge of digitizing handwritten Sinhala script, an area underrepresented in OCR technology. A web app was created to allow users to interact with the model to digitize handwritten Sinhala characters in image form.

## Features
1. **Handwritten Character Recognition**: The app can recognize individual Sinhala characters from handwritten inputs.
2. **File Upload**: Users can upload images of handwritten text for recognition.
3. **Canvas Option**: Allows users to draw characters directly on a canvas within the app for instant recognition.
4. **Word-Level Recognition**: Ability to recognize entire words by segmenting them into individual characters.

## Technology Stack
- **Frontend**: React.js with TailwindCSS, optimized using Vite.
- **Backend**: Node.js with Express.js.
- **Machine Learning**: Python, employing libraries for CNN and image processing.

## Model Information
- A multi-layered CNN, with convolutional layers, batch normalization, ReLU activation, and max pooling.
- Utilized the Adam optimizer and categorical cross-entropy loss function. Employed early stopping to prevent overfitting.
- A comprehensive dataset from [Kaggle](https://www.kaggle.com/datasets/sathiralamal/sinhala-letter-454) with over 81,000 images across 454 classes.
- Included binarization, thinning, skeletonization, contour detection, centering, and normalization.
- High accuracy, precision, recall, and F1 Score, indicating effective learning and generalization capabilities.
