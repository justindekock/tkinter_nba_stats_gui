import pandas as pd

def clean_floats(df):
    num_df = df.select_dtypes(include='Float64')
    notnum_df = df.select_dtypes(exclude='Float64')
    pcts = ['FGP', 'F3P', 'FTP']
    for i in range(len(num_df.columns)):
        if num_df.columns[i] in pcts:
            num_df[num_df.columns[i]] = (num_df[num_df.columns[i]].round(4) * 100).to_string(index=False) + '%'
        else:
            num_df[num_df.columns[i]] = num_df[num_df.columns[i]].round(2)
            
    clean_df = pd.concat([notnum_df, num_df], axis=1) # axis=1 makes it concat along columns instead of rows
    
    return clean_df

def clean_string_list(string_list):
    clean_strings = []
    chars = ["'", '[', ']']
    for string in string_list:
        for char in chars:
            string = str(string).replace(char, '')
        clean_strings.append(string)
            
    return clean_strings

def clean_df(df):
    chars = ["'", '[', ']']
    for val in df.values:
        for char in chars:
            val = str(val).replace(char, '')
    return df
        
        
    