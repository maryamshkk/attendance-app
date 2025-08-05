import pandas as pd

def predict_attendance(df: pd.DataFrame, model) -> (pd.DataFrame, pd.DataFrame):
    """
    Given a raw daily attendance DataFrame and a trained model, this function:
      1. Cleans and converts entry times
      2. Computes late minutes
      3. Extracts ML features (Hour, Minute)
      4. Predicts attendance status
      5. Calculates leave summary (2 late = 1 leave)
    Returns:
      - df_predictions: DataFrame with ['Employee ID','Name','Date','Entry_Time','Late_Min','Status']
      - leave_summary: DataFrame with ['Employee ID','Name','Total_Lates','Total_Leaves']
    """
    # Lazy imports of your modules
    from modules.data_cleaning import convert_to_time, get_late_minutes
    from modules.feature_engineering import engineering_features
    from modules.leave_calculator import calculate_leaves_from_lates

    # 1. Clean entry times
    df = df.copy()
    df['Entry_Time'] = df['Entry_Time'].apply(convert_to_time)

    # 2. Compute late minutes
    df['Late_Min'] = df['Entry_Time'].apply(get_late_minutes)

    # 3. Feature engineering to get X_test
    X_test, df = engineering_features(df)

    # 4. Predict status
    df['Status'] = model.predict(X_test)

    # 5. Drop internal columns
    if 'Hour' in df and 'Minute' in df:
        df.drop(columns=['Hour', 'Minute'], inplace=True)

    # 6. Prepare predictions output
    df_predictions = df[['Employee ID', 'Name', 'Date', 'Entry_Time', 'Late_Min', 'Status']].copy()

    # 7. Calculate leave summary on predictions
    leave_summary = calculate_leaves_from_lates(df_predictions)

    return df_predictions, leave_summary

# Example usage:
# import joblib
# model = joblib.load('models/best_rf_model.pkl')
# df_raw = pd.read_csv('data/today_attendance.csv')
# df_pred, summary = predict_attendance(df_raw, model)
# df_pred.head(), summary.head()
