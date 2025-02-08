from pathlib import Path

import pandas as pd
from tqdm import tqdm

YEARS = [2020, 2021, 2022, 2023]
COLUMN_MAPPING_FILE = "docs/dictionnaire_des_variables.csv"


def create_dataset() -> pd.DataFrame:
    """
    Creates a dataset from raw accident data files.

    Returns:
        pd.DataFrame: A DataFrame containing the merged accident data from all years.
    """
    all_years_data = _load_accident_files()
    combined_data = _combine_all_years(all_years_data)

    return combined_data


def _load_accident_files() -> dict:
    """
    Loads accident data for multiple years.
    """
    all_years_data = {}
    file_patterns = _get_file_patterns()

    for year in tqdm(YEARS, desc="Loading accident data"):
        year_data = _load_year_data(year, file_patterns)
        if year_data:
            all_years_data[year] = year_data

    return all_years_data


def _combine_all_years(all_years_data: dict) -> pd.DataFrame:
    """
    Combines data from all years into a single DataFrame.
    """
    all_years_merged = _merge_all_years_data(all_years_data)
    return _assemble_years_dataframe(all_years_merged)


def _merge_all_years_data(all_years_data: dict) -> list:
    """
    Merges data for each year and returns a list of merged DataFrames.
    """
    all_years_merged = []

    for year, year_data in tqdm(all_years_data.items(), desc="Combining accident data"):
        year_merged = _merge_year_data(year_data, year)
        if year_merged is not None:
            all_years_merged.append(year_merged)

    return all_years_merged


def _assemble_years_dataframe(all_years_merged: list) -> pd.DataFrame:
    """
    Creates the final DataFrame from the list of merged year data.
    """
    if all_years_merged:
        return pd.concat(all_years_merged, ignore_index=True)
    return pd.DataFrame()


def _get_file_patterns() -> dict:
    """
    Returns the file patterns for each table type.
    """
    return {
        "caracteristiques": ["caract-{}.csv"],
        "lieux": ["lieux-{}.csv"],
        "vehicules": ["vehicules-{}.csv"],
        "usagers": ["usagers-{}.csv"],
    }


def _load_year_data(year: int, file_patterns: dict) -> dict:
    """
    Loads data for a specific year.
    """
    year_data = {}

    for table, patterns in file_patterns.items():
        df = _load_table_data(year, patterns)
        if df is not None:
            year_data[table] = df

    return year_data


def _load_table_data(year: int, patterns: list) -> pd.DataFrame | None:
    """
    Loads data for a specific table.
    """
    for pattern in patterns:
        filename = _build_filename(year, pattern)
        if Path(filename).exists():
            try:
                return _load_and_preprocess_csv(filename)
            except Exception:
                continue
    return None


def _build_filename(year: int, pattern: str) -> str:
    """
    Builds the filename for a given year and pattern.
    """
    return f"data/raw/{pattern.format(year)}"


def _load_and_preprocess_csv(filename: str) -> pd.DataFrame:
    """
    Loads and preprocesses a CSV file.
    """
    df = pd.read_csv(filename, sep=";", low_memory=False, encoding="utf-8")
    return _preprocess_dataframe(df)


def _preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses a DataFrame by normalizing column names and converting ID columns to string.
    """
    df = _normalize_column_names(df)
    df = _standardize_id_columns(df)
    df = _convert_id_usagers_to_int(df)
    df = _convert_id_columns_to_string(df)
    return df


def _normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalizes column names to lowercase and strips whitespace.
    """
    df.columns = df.columns.str.lower().str.strip()
    return df


def _standardize_id_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes ID column names.
    """
    if "accident_id" in df.columns:
        df = df.rename(columns={"accident_id": "num_acc"})
    return df


def _convert_id_usagers_to_int(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts ID columns to string type.
    """
    id_columns = ["id_usager","pr"]
    for col in id_columns:
        if col in df.columns:
            print(col)
            df[col] = df[col].str.replace("\xa0", "").astype(str)
    return df


def _convert_id_columns_to_string(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts ID columns to string type.
    """
    id_columns = ["num_acc", "id_vehicule"]
    for col in id_columns:
        if col in df.columns:
            df[col] = df[col].astype(str)
    return df


def _merge_year_data(year_data: dict, year: int) -> pd.DataFrame | None:
    """
    Merges tables for a given year.
    """
    try:
        merged = _merge_tables(year_data)
        merged = _add_year_column(merged, year)
        return merged
    except Exception:
        return None


def _add_year_column(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """
    Adds a year column to the DataFrame.
    """
    df["annee_accident"] = year
    return df


def _merge_tables(year_data: dict) -> pd.DataFrame:
    """
    Merges all tables in the correct order.
    """
    merged = _merge_caracteristiques_and_lieux(year_data)
    merged = _merge_vehicules(merged, year_data)
    merged = _merge_usagers(merged, year_data)
    merged = _clean_merged_columns(merged)

    return merged


def _merge_caracteristiques_and_lieux(year_data: dict) -> pd.DataFrame:
    """
    Merges caracteristiques and lieux tables.
    """
    return _merge_tables_on_columns(
        year_data["caracteristiques"],
        year_data["lieux"],
        on=["num_acc"],
    )


def _merge_vehicules(merged: pd.DataFrame, year_data: dict) -> pd.DataFrame:
    """
    Merges vehicules table with the existing merged data.
    """
    return _merge_tables_on_columns(
        merged,
        year_data["vehicules"],
        on=["num_acc"],
        suffixes=("", "_vehicules"),
    )


def _merge_usagers(merged: pd.DataFrame, year_data: dict) -> pd.DataFrame:
    """
    Merges usagers table with the existing merged data.
    """
    return _merge_tables_on_columns(
        merged,
        year_data["usagers"],
        on=["num_acc", "id_vehicule"],
        suffixes=("", "_usagers"),
    )


def _merge_tables_on_columns(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    on: list[str],
    suffixes: tuple[str, str] = ("", ""),
) -> pd.DataFrame:
    """
    Merges two DataFrames on specified columns with optional suffixes.
    """
    return pd.merge(left_df, right_df, on=on, how="left", suffixes=suffixes)


def _clean_merged_columns(merged: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans up merged columns by dropping duplicates and ensuring correct column names.
    """
    merged = _drop_duplicate_columns(merged)
    merged = _standardize_column_names(merged)
    merged = _rename_columns_to_new_format(merged)
    return merged


def _rename_columns_to_new_format(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renames columns according to the new format defined in the mapping file.
    """
    column_mapping = _load_column_mapping()
    return df.rename(columns=column_mapping)


def _drop_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drops columns that were duplicated during merges.
    """
    columns_to_drop = _get_duplicate_column_names(df)
    return df.drop(columns=columns_to_drop)


def _get_duplicate_column_names(df: pd.DataFrame) -> list[str]:
    """
    Gets the list of duplicate column names from merges.
    """
    return [col for col in df.columns if col.endswith(("_vehicules", "_usagers"))]


def _standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes column names after merges.
    """
    if "num_veh" not in df.columns and "num_veh_x" in df.columns:
        df = df.rename(columns={"num_veh_x": "num_veh"})
    return df


def _load_column_mapping() -> dict:
    """
    Loads the column mapping from the CSV file.
    """
    mapping_df = pd.read_csv(COLUMN_MAPPING_FILE, sep=";")
    mapping = dict(zip(mapping_df["nom_original"], mapping_df["nouveau_nom"]))
    mapping["annee"] = "annee_accident"  # Add the year column mapping
    return mapping


if __name__ == "__main__":
    df = create_dataset()
    df["nombre_voies"] = df["nombre_voies"].astype(str)  # Prevents error when saving to parquet
    df.to_parquet("data/processed/dataset.parquet", index=False)
