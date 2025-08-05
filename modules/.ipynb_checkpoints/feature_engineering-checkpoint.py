# modules/feature_engineering.py

import pandas as pd

def engineer_features(df_ml):
    # Drop rows with missing Status
    df_ml = df_ml.dropna(subset=['Status'])

    # Extract hour, minute from Entry_Time
    df_ml['Hour'] = df_ml['Entry_Time'].apply(lambda x: x.hour if pd.notnull(x) else -1)
    df_ml['Minute'] = df_ml['Entry_Time'].apply(lambda x: x.minute if pd.notnull(x) else -1)

    # Create dummy variables for Status
    status_dummies = pd.get_dummies(df_ml['Status'], prefix='Status').astype(int)
    df_ml = pd.concat([df_ml, status_dummies], axis=1)

    # Define features and labels
    X = df_ml[['Late_Min', 'Hour', 'Minute']]
    y = df_ml['Status']

    return X, y, df_ml
