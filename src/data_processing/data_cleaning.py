import pandas as pd

class DataCleaning:
    @staticmethod
    def handle_missing_values(df, strategy="drop", fill_value=None):
        if strategy == "drop":
            return df.dropna()
        elif strategy == "fill":
            return df.fillna(fill_value)
        else:
            raise ValueError("Invalid strategy")

    @staticmethod
    def remove_duplicates(df):
        return df.drop_duplicates()

    @staticmethod
    def convert_data_types(df, column_types):
        for column, dtype in column_types.items():
            df[column] = df[column].astype(dtype)
        return df
