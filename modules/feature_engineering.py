import pandas as pd
from typing import Tuple


def engineer_features(df_ml: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """
    Engineer features for ML model training:
      - Drop rows with missing Status
      - Extract Hour and Minute from Entry_Time
      - One-hot encode Status for training
    Returns:
      - X: DataFrame of features ['Late_Min', 'Hour', 'Minute']
      - y: Series of target labels ('Status')
      - df_ml: original DataFrame augmented with new columns
    """
    df = df_ml.copy()
    # Validate required columns
    required_cols = {'Entry_Time', 'Late_Min', 'Status'}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns for feature engineering: {missing}")

    # Drop rows missing status
    df = df.dropna(subset=['Status'])

    # Extract hour and minute
    df['Hour'] = df['Entry_Time'].apply(lambda x: x.hour if pd.notnull(x) else -1)
    df['Minute'] = df['Entry_Time'].apply(lambda x: x.minute if pd.notnull(x) else -1)

    # One-hot encode status
    status_dummies = pd.get_dummies(df['Status'], prefix='Status').astype(int)
    df = pd.concat([df, status_dummies], axis=1)

    # Define features and labels
    X = df[['Late_Min', 'Hour', 'Minute']]
    y = df['Status']
    return X, y, df


def engineering_features(df_ml: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Engineer features for inference (no label y):
      - Extract Hour and Minute from Entry_Time
      - Return feature matrix X and augmented DataFrame
    Returns:
      - X: DataFrame of features ['Late_Min', 'Hour', 'Minute']
      - df_ml: DataFrame augmented with 'Hour' and 'Minute'
    """
    df = df_ml.copy()
    required_cols = {'Entry_Time', 'Late_Min'}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns for inference feature engineering: {missing}")

    df['Hour'] = df['Entry_Time'].apply(lambda x: x.hour if pd.notnull(x) else -1)
    df['Minute'] = df['Entry_Time'].apply(lambda x: x.minute if pd.notnull(x) else -1)

    X = df[['Late_Min', 'Hour', 'Minute']]
    return X, df
