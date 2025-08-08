# 7-Day Machine Learning Journey: From Basics to Advanced

Welcome to your structured ML learning path! This project contains a week-by-week progression that will take you from ML basics to advanced concepts, perfectly designed for returning learners who want to get future-ready.

## 🎯 Week 1: ML Fundamentals (Days 1-7)

**Current Status: Day 1 Complete ✅**

This week covers the complete machine learning workflow using the famous Titanic dataset:

### Day 1: Data Loading & Exploratory Data Analysis ✅
- **Notebook**: `day1_data_loading_and_eda.ipynb`
- **Focus**: Understanding data before modeling
- **Topics**: Dataset loading, missing data analysis, feature distributions, correlations
- **Key Skills**: Pandas, Seaborn, statistical analysis

### Day 2: Data Cleaning & Feature Engineering (Coming Next)
- **Focus**: Preparing data for machine learning
- **Topics**: Missing value imputation, feature creation, data encoding

### Days 3-7: Model Building Through Deployment
- Day 3: First ML Model (Logistic Regression)
- Day 4: Classification Metrics Deep Dive  
- Day 5: Tree-Based Models (Decision Trees, Random Forest)
- Day 6: Hyperparameter Tuning
- Day 7: End-to-End ML Pipeline

## 🚀 Quick Start for Day 1

### Option A: Easy Launch (Recommended for macOS)
```bash
# One-command setup and launch
./setup_and_launch.sh
```

### Option B: Manual Setup (All Systems)
```bash
# Create virtual environment
python3 -m venv ml_env
source ml_env/bin/activate  # On Windows: ml_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Jupyter
jupyter notebook day1_data_loading_and_eda.ipynb
```

### Option C: Alternative for macOS with Homebrew Issues
```bash
# If you get "externally-managed-environment" error
python3 -m venv ml_env
source ml_env/bin/activate
pip install -r requirements.txt
jupyter notebook day1_data_loading_and_eda.ipynb
```

## 📋 Prerequisites

- Python 3.7+ installed on your system
- Basic familiarity with Python (variables, functions, loops)
- High school level statistics knowledge helpful but not required

## 🛠️ Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd ML-Learning
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv ml_env
   source ml_env/bin/activate  # On Windows: ml_env\Scripts\activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

## 📚 Day 1 Notebook Structure

The Day 1 notebook (`day1_data_loading_and_eda.ipynb`) contains 13 comprehensive sections:

1. **Environment Setup** - Library imports and configuration
2. **Dataset Loading** - Understanding the Titanic dataset
3. **First Look at Data** - Basic dataset information
4. **Missing Data Analysis** - Identifying data quality issues
5. **Target Variable Analysis** - Understanding what we're predicting
6. **Categorical Features** - Exploring non-numerical data
7. **Numerical Features** - Analyzing continuous variables
8. **Correlation Analysis** - Finding relationships between features
9. **Advanced Relationships** - Deep-dive into feature interactions
10. **Feature Engineering Preview** - Identifying opportunities for tomorrow
11. **Data Quality Assessment** - Comprehensive quality review
12. **Key Insights Summary** - Main findings from analysis
13. **Tomorrow's Roadmap** - Preview of Day 2 activities

## 🎓 Key Concepts Covered

### Machine Learning Fundamentals
- **Supervised Learning** - Learning from labeled data
- **Binary Classification** - Predicting two possible outcomes
- **Train/Test Split** - Evaluating model performance
- **Feature Engineering** - Creating useful features from raw data

### Data Science Skills
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Matplotlib/Seaborn** - Data visualization
- **Scikit-learn** - Machine learning algorithms

### Model Evaluation
- **Accuracy** - Overall prediction correctness
- **Confusion Matrix** - Detailed prediction breakdown
- **Classification Report** - Precision, recall, and F1-score
- **Feature Importance** - Understanding model decisions

## 🔍 Dataset Information

The Titanic dataset contains information about passengers on the Titanic and whether they survived the disaster. This is a classic binary classification problem where we predict survival (1) or death (0) based on passenger characteristics.

**Features include:**
- Passenger class, gender, age
- Number of siblings/spouses aboard
- Number of parents/children aboard
- Fare paid, port of embarkation
- And more...

## 🚀 Next Steps After Completing the Notebook

1. **Try Different Algorithms**
   - Logistic Regression
   - Support Vector Machines (SVM)
   - Neural Networks

2. **Advanced Techniques**
   - Hyperparameter tuning
   - Cross-validation
   - Ensemble methods

3. **Real-World Projects**
   - Housing price prediction
   - Customer churn analysis
   - Image classification

4. **Deep Learning**
   - Neural networks with TensorFlow/PyTorch
   - Computer vision
   - Natural language processing

## 💡 Tips for Learning

- **Run each cell** and understand what it does before moving to the next
- **Experiment** with the code - try changing parameters and see what happens
- **Take notes** on concepts you find challenging
- **Practice** with other datasets to reinforce your learning
- **Join communities** like Kaggle, Reddit r/MachineLearning, or local meetups

## 🤝 Contributing

Feel free to:
- Report issues or bugs
- Suggest improvements
- Add more examples or explanations
- Share your own learning experiences

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Learning! 🎉**

Remember: Machine learning is a journey, not a destination. Keep practicing, experimenting, and building projects to strengthen your skills!
