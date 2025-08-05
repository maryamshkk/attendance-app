import pandas as pd
from typing import Tuple


def calculate_leaves_from_lates(
    df_ml: pd.DataFrame,
    lates_to_leave: int = 2
) -> pd.DataFrame:
    """
    Summarize leaves based on 'Late' status in the attendance dataframe.
    Rule: Every `lates_to_leave` late entries = 1 leave.

    Args:
        df_ml: DataFrame containing columns ['Employee ID','Name','Status']
        lates_to_leave: Number of late entries that count as one leave (default=2)

    Returns:
        leave_summary: DataFrame with ['Employee ID','Name','Total_Lates','Total_Leaves']
    """
    # Validate required columns
    required = {'Employee ID', 'Name', 'Status'}
    missing = required - set(df_ml.columns)
    if missing:
        raise ValueError(f"Missing required columns for leave calculation: {missing}")

    # Count late entries per employee
    late_df = df_ml[df_ml['Status'] == 'Late']
    late_counts = (
        late_df
        .groupby(['Employee ID', 'Name'])
        .size()
        .reset_index(name='Total_Lates')
    )

    # Apply leave rule
    late_counts['Total_Leaves'] = (late_counts['Total_Lates'] // lates_to_leave).astype(int)

    # Ensure every employee appears
    all_employees = df_ml[['Employee ID', 'Name']].drop_duplicates()
    leave_summary = all_employees.merge(
        late_counts,
        on=['Employee ID', 'Name'],
        how='left'
    )

    # Fill missing with zeros
    leave_summary['Total_Lates'] = leave_summary['Total_Lates'].fillna(0).astype(int)
    leave_summary['Total_Leaves'] = leave_summary['Total_Leaves'].fillna(0).astype(int)

    return leave_summary
