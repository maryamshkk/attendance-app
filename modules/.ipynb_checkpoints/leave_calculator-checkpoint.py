# modules/leave_calculator.py

import pandas as pd

def calculate_leaves_from_lates(df_ml):
    """
    Calculate total leaves based on 'Late' status in the attendance ML-format dataframe.
    Rule: Every 2 late entries = 1 leave
    """

    # Step 1: Filter rows where status is "Late"
    late_df = df_ml[df_ml['Status'] == 'Late']

    # Step 2: Count number of "Late" entries per employee
    late_counts = (
        late_df
        .groupby(['Employee ID', 'Name'])
        .size()
        .reset_index(name='Total_Lates')
    )

    # Step 3: Apply rule — every 2 lates = 1 leave
    late_counts['Total_Leaves'] = late_counts['Total_Lates'] // 2

    # Step 4: Get full employee list
    all_employees = df_ml[['Employee ID', 'Name']].drop_duplicates()

    # Step 5: Merge with late counts
    leave_summary = all_employees.merge(late_counts, on=['Employee ID', 'Name'], how='left')

    # Step 6: Fill NaNs with 0 and cast to int
    leave_summary[['Total_Lates', 'Total_Leaves']] = leave_summary[['Total_Lates', 'Total_Leaves']].fillna(0).astype(int)

    return leave_summary
