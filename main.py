# llibreries (imports)
import pandas as pd
import os
import numpy as np
import re
from collections import Counter

# df

csv_file = "data/attacks.csv"
df = pd.read_csv(csv_file, encoding = "ISO-8859-1")

#encapsulation

def clean_rows_columns (df):
    df.dropna(how= "all")
    df[df.drop("Case Number", axis = 1).isna().all(axis= 1)]
    df[(df["Case Number"] != "0") & (df["Case Number"] != "xx")]
    df.dropna(axis=1, how='all')

    return df

df_clean = clean_rows_columns (df)

def column_names(df_clean):
    df_clean.rename(columns={"Sex ":"Sex"}, inplace= True)
    df_clean.rename(columns={"Species ":"Species"}, inplace= True)

    return df_clean

rename_columns = column_names(df_clean)

def column_names_2(rename_columns):
    comp_dict = {i : i.lower().replace(" ", "_") for i in df_clean.columns}
    rename_columns.rename(columns = comp_dict, inplace=True)

    return rename_columns

change_names = column_names(rename_columns)

def check_duplicates(change_names):
    change_names.drop_duplicates(subset=change_names.columns.difference(["original_order"]))
    
    return change_names

drop_duplicates = check_duplicates(change_names)
print(drop_duplicates)

def drop_unuseful_col(drop_duplicates):
    drop_duplicates.drop(columns=["href", "href_formula", "case_number.1", "case_number.2", "unnamed:_22" , "unnamed:_23", "original_order", "pdf"], inplace = True)

    return drop_duplicates

final_col = drop_unuseful_col(drop_duplicates)

def sex_clean(final_col):
        
    def filter_sex(x):
        if x != "M" and x != "F" and x != "M ":
            return "unknown"
        elif x == "M ":
            return "M"
        else:
            return x

    final_col["sex"] = final_col["sex"].apply(filter_sex)

    return filter_sex

clean_sex = sex_clean(final_col)

def fatal_clean(clean_sex):
        
    def filter_fatal(x):
        if x != "N" and x != "Y" and x != "N " and x != " N" and x != "y":
            return "unknown"
        elif x == "N " or x == " N":
            return "N"
        elif x == "y":
            return "Y"
        else:
            return x

    clean_sex["sex"] = clean_sex["sex"].apply(filter_fatal)

    return clean_sex

clean_fatal = fatal_clean(clean_sex)

def cleaning_type(clean_fatal):
    pattern = r'\w*[Bb]oat\w*'
    clean_fatal["type"] = clean_fatal['type'].str.replace(pattern, 'Boat', regex=True)

    return clean_fatal

type_clean = cleaning_type(clean_fatal)

#Not finished, had  to go for the resentation and read me. And too much debbugging.

