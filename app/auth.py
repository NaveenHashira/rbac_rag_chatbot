import pandas as pd
import streamlit as st

def verify_user(hr_df_path: str, name: str, department: str) -> bool:
    """
    Verify user against HR database
    
    Args:
        hr_df_path: Path to HR CSV file
        name: User's full name
        department: Department name
        
    Returns:
        bool: True if valid user, False otherwise
    """
    try:
        hr_df = pd.read_csv(hr_df_path)
        n = name.strip().lower()
        d = department.strip().lower()
        
        match = hr_df[
            (hr_df['full_name'].str.strip().str.lower() == n) &
            (hr_df['department'].str.strip().str.lower() == d)
        ]
        return not match.empty
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return False