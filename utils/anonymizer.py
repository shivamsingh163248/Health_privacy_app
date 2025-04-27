import pandas as pd

# --- Helper Functions ---

def generalize_age(age):
    try:
        age = int(age)
        if age < 30:
            return "18-29"
        elif age < 50:
            return "30-49"
        else:
            return "50+"
    except:
        return "Unknown"

def mask_email(email):
    try:
        user, domain = email.split('@')
        return "xxxx@" + domain
    except:
        return "xxxx@domain.com"

def generalize_column(df, column):
    if column == 'name':
        return df[column].apply(lambda x: f"Name_{x[0].upper()}***" if pd.notna(x) and len(str(x)) > 0 else "Name_***")
    elif column == 'age':
        return df[column].apply(generalize_age)
    elif column == 'city':
        return df[column].apply(lambda x: "City_***")
    elif column == 'state':
        return df[column].apply(lambda x: "State_***")
    elif column == 'mobile':
        return df[column].astype(str).apply(lambda x: x[:4] + "******")
    elif column == 'email':
        return df[column].apply(mask_email)
    else:
        return df[column]

# --- K-Anonymity ---

def apply_k_anonymity(df, selected_columns, k=2):
    df_copy = df.copy()

    for col in selected_columns:
        if col in df_copy.columns:
            df_copy[col] = generalize_column(df_copy, col)

    grouped = df_copy.groupby(selected_columns)
    valid_groups = [group for _, group in grouped if len(group) >= k]

    if not valid_groups:
        return pd.DataFrame(columns=df.columns)

    return pd.concat(valid_groups).reset_index(drop=True)

# --- L-Diversity ---

def apply_l_diversity(df, selected_columns, k=2, l=2, sensitive_column='blood_group'):
    df_copy = df.copy()

    for col in selected_columns:
        if col in df_copy.columns:
            df_copy[col] = generalize_column(df_copy, col)

    grouped = df_copy.groupby(selected_columns)
    valid_groups = []

    for _, group in grouped:
        if len(group) >= k:
            if group[sensitive_column].nunique() >= l:
                valid_groups.append(group)

    if not valid_groups:
        return pd.DataFrame(columns=df.columns)

    return pd.concat(valid_groups).reset_index(drop=True)

# --- Data Masking ---

def apply_data_masking(df, selected_columns):
    df_copy = df.copy()

    for col in selected_columns:
        if col in df_copy.columns:
            df_copy[col] = generalize_column(df_copy, col)

    return df_copy
