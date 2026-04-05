import pandas as pd
import numpy as np
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
from scipy.sparse import hstack
import utils

def train():
    # Load dataset
    print("Loading v3.14 dataset...")
    if not os.path.exists('dataset.csv'):
        print("Error: dataset.csv not found. Please run generate_dataset.py first.")
        return
        
    df = pd.read_csv('dataset.csv')
    X_text = df['email']
    y = df['label']
    
    # 1. TF-IDF Feature Extraction
    print("Vectorizing text (N-grams & IDF)...")
    vectorizer = TfidfVectorizer(
        stop_words='english', 
        max_features=1200, 
        ngram_range=(1, 3), # v3.14: Support trigrams
        use_idf=True,
        smooth_idf=True,
        sublinear_tf=True
    )
    X_tfidf = vectorizer.fit_transform(X_text)
    
    # 2. Structured Feature Extraction (Improved v3.14 features)
    print("Extracting 12 structured features (Readability, Sentiment, Personalization)...")
    X_structured = np.array([utils.extract_features(text) for text in X_text])
    
    # 3. Combine Features
    X_combined = hstack([X_tfidf, X_structured])
    
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42, stratify=y)
    
    # Define Base Estimators for Stacking
    print("Building v3.14 Ensemble Model (StackingClassifier)...")
    
    base_estimators = [
        ('lr', LogisticRegression(class_weight='balanced', max_iter=2000, C=0.5)),
        ('rf', RandomForestClassifier(n_estimators=150, max_depth=10, random_state=42, class_weight='balanced')),
        ('xgb', XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42, eval_metric='logloss'))
    ]
    
    # Meta-Learner (Logistic Regression is a standard choice)
    meta_learner = LogisticRegression()
    
    stacking_clf = StackingClassifier(
        estimators=base_estimators, 
        final_estimator=meta_learner,
        cv=5,
        passthrough=True # Allows the meta-learner to see the original features too
    )
    
    print("Training ensemble (this may take a few seconds)...")
    stacking_clf.fit(X_train, y_train)
    
    # Evaluation
    y_pred = stacking_clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    
    print(f"\nEnsemble Metrics -> Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save artifacts
    print("Saving v3.14 model as model.pkl...")
    with open('model.pkl', 'wb') as f:
        pickle.dump(stacking_clf, f)
    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
        
    print("Model Upgrade Complete. Deployment Ready.")

if __name__ == "__main__":
    train()
