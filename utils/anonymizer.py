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

def mask_mobile(mobile):
    try:
        mobile = str(mobile)
        return mobile[:4] + "******"
    except:
        return "**********"

def mask_zip(zip_code):
    try:
        zip_code = str(zip_code)
        return zip_code[:3] + "**"
    except:
        return "*****"

def mask_blood_group(blood_group):
    try:
        blood_group = str(blood_group)
        return "Group_*"
    except:
        return "Group_*"

def mask_city(city):
    return "City_***"

def mask_state(state):
    return "State_***"

def mask_donation_date(donation_date):
    try:
        # Example: 2023-03-12 --> 2023-03
        return str(donation_date)[:7]
    except:
        return "2023-XX"

def generalize_column(df, column):
    if column == 'name':
        return df[column].apply(lambda x: f"Name_{x[0].upper()}***" if pd.notna(x) and len(str(x)) > 0 else "Name_***")
    elif column == 'age':
        return df[column].apply(generalize_age)
    elif column == 'email':
        return df[column].apply(mask_email)
    elif column == 'mobile':
        return df[column].apply(mask_mobile)
    elif column == 'zip_code':
        return df[column].apply(mask_zip)
    elif column == 'blood_group':
        return df[column].apply(mask_blood_group)
    elif column == 'city':
        return df[column].apply(mask_city)
    elif column == 'state':
        return df[column].apply(mask_state)
    elif column == 'donation_date':
        return df[column].apply(mask_donation_date)
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
