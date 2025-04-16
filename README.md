Picked up and Updated... Old Repo (https://github.com/ananingfosu/rice-parakeet)

# Rice Disease Prediction GUI

A modern, user-friendly desktop application for predicting rice leaf diseases from images using a trained machine learning model.

## Features

- **Image Upload:** Image upload and processing capabilities. Easily upload rice leaf images (PNG or JPG) for analysis.
- **Disease Prediction:** Real-time disease prediction. Instantly predicts one of three common rice diseases using a pre-trained model.
- **Responsive Modern GUI:**
  - Clean, two-column layout with dynamic resizing and responsive elements.
  - User-friendly graphical interface using Tkinter
  - Dark mode toggle and modern sans-serif font for improved readability.
  - Button hover effects and clear visual feedback.
- **Prediction Feedback:** Results are displayed in a styled, resizable info box.
- **Error Handling:** User-friendly pop-up dialogs for errors and issues.
- **Restart Functionality:** Restart the application at any time for a fresh session.
- **Accuracy:** - High accuracy rate (80.56%)

## Supported Rice Diseases
- Bacterial leaf blight
- Brown spot
- Leaf smut

### Model
- Uses Support Vector Machine (SVM) algorithm
- Trained on a dataset of rice leaf images
- Achieves 80.56% accuracy
- Model is saved as `rice_pred.pkl`

### Dependencies
- Python 3.9 or 3.10
- scikit-learn
- PIL (Python Imaging Library)
- skimage
- tkinter
- numpy
- Recommended: Use a virtual environment (e.g., `venv` or `conda`).

## Getting Started

### Usage

## What its about
1. Run the GUI:
   ```bash
   python rice_disease_pred_GUI.py
   ```
2. In the application:
   - Upload a rice leaf image (PNG or JPG).
   - Click **Predict Disease** to see the result.
   - Click **Restart** to restart the application, or simply upload another image to predict again.
  
## Environment Setup and Running

If you want to contribute or run this project on your own machine, follow these steps:

### 1. Clone the Repository
```bash
git clone <repo-url>
cd rice-parakeet-main
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
# For Windows
python -m venv rice_env
rice_env\Scripts\activate

# For macOS/Linux
python3 -m venv rice_env
source rice_env/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the GUI Application
```bash
python rice_disease_pred_GUI.py
```

### 5. Edit and Retrain the Model (Jupyter Notebook)
- Open the provided Jupyter notebook (e.g., `Rice_Disease_Training.ipynb`) in the repo or create your own.
- Make sure your virtual environment is activated, then launch Jupyter:
  ```bash
  jupyter notebook
  ```
- Use the notebook to retrain or update the model as needed.
- Save the trained model as `rice_pred.pkl` in the `model/` directory.
- Restart the GUI to use the updated model.

### 6. Additional Tips
- Always keep your dependencies up-to-date by running `pip install -r requirements.txt` after pulling new changes.
- If you add new dependencies, update `requirements.txt`.
- Use version control best practices (branches, pull requests, etc.) when contributing.

---

### Folder Structure
```
rice-parakeet-main/
├── model/
│   └── rice_pred.pkl           # Trained ML model (required)
├── images/
│   └── rice.png                # Default preview image
├── rice_disease_pred_GUI.py    # Main GUI application
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

### Notes
- Ensure that `model/rice_pred.pkl` exists for predictions to work.
- The GUI is responsive and will adjust to different window sizes.
- All error messages are shown as pop-up dialogs for clarity.

## Customization
- You can modify the color palette and fonts in `rice_disease_pred_GUI.py` for a different look.
- Add more disease classes by updating the model and label list.

## Jupyter Notebook Reference
- The main notebook for model training and updates is: `Rice_Disease_Training.ipynb`
- Use this notebook to preprocess data, train the classifier, evaluate performance, and export the trained model as `rice_pred.pkl` into the `model/` directory.
- Ensure your environment matches the requirements in `requirements.txt` before running the notebook.

## Model Details
- **Model Type:** Scikit-learn classifier (e.g., RandomForestClassifier or similar)
- **Input:** RGB image of a rice leaf (PNG or JPG)
- **Image Preprocessing:** Images are resized to 128x128 pixels and normalized before prediction.
- **Classes:**
  - Bacterial leaf blight
  - Brown spot
  - Leaf smut
- **Output:** Predicted disease label
- **Accuracy:**  80% on validation set
- **Updating the Model:** Retrain using the notebook and overwrite `model/rice_pred.pkl` with the new model.

## Screenshots
![Main GUI -- Light theme](images/screenshot_main_gui_light_theme.png)
![Main GUI -- Dark theme](images/screenshot_main_gui_dark_theme.png)
![Predicted Disease GUI -- Light theme](images/screenshot_pred_light_theme.png)
![Predicted Disease GUI -- Dark theme](images/screenshot_pred_dark_theme.png)

## Troubleshooting
- **Model not found:** Ensure `model/rice_pred.pkl` exists.
- **Tkinter error:** Make sure Python was installed with Tkinter support.
- **Image not loading:** Only PNG or JPG formats are supported.

## Accuracy Metrics

- Overall accuracy: 80.56%
- Macro average precision: 0.80
- Macro average recall: 0.82
- Macro average F1-score: 0.81

## License
This project is for educational and research purposes. Made as my final year project for my computer science degree in KNUST with a coursemate. 

---

**Developed with ❤️ for modern, accessible plant disease diagnosis.**
