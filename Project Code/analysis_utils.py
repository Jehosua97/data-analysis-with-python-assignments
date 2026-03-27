from __future__ import annotations

import csv
import re
from pathlib import Path

import pandas as pd
from pandas.errors import ParserError

DATA_FILE = Path(__file__).with_name("4110008001_databaseLoadingData.csv")

GENERAL_HEALTH_LEVELS = [
    "Self-perceived general health, excellent or very good",
    "Self-perceived general health, good",
    "Self-perceived general health, fair or poor",
]

MENTAL_HEALTH_LEVELS = [
    "Self-perceived mental health, excellent or very good",
    "Self-perceived mental health, good",
    "Self-perceived mental health, fair or poor",
]

REPAIR_LEVELS = [
    "No, only regular maintenance is needed",
    "Yes, minor repairs are needed",
    "Yes, major repairs are needed",
]

CROWDING_LEVELS = [
    "One person or fewer per room",
    "More than one but less than 1.5 persons per room",
    "1.5 persons or more per room",
]

SHORT_HEALTH_LABELS = {
    "Self-perceived general health, excellent or very good": "Excellent or very good",
    "Self-perceived general health, good": "Good",
    "Self-perceived general health, fair or poor": "Fair or poor",
    "Self-perceived mental health, excellent or very good": "Excellent or very good",
    "Self-perceived mental health, good": "Good",
    "Self-perceived mental health, fair or poor": "Fair or poor",
}

SHORT_REPAIR_LABELS = {
    "No, only regular maintenance is needed": "Regular maintenance only",
    "Yes, minor repairs are needed": "Minor repairs needed",
    "Yes, major repairs are needed": "Major repairs needed",
}

SHORT_CROWDING_LABELS = {
    "One person or fewer per room": "1 or fewer per room",
    "More than one but less than 1.5 persons per room": "More than 1 and less than 1.5",
    "1.5 persons or more per room": "1.5 or more per room",
}

REGION_COORDINATES = {
    "Atlantic provinces": {"lat": 46.5, "lon": -61.4, "level": "Region"},
    "Quebec": {"lat": 52.0, "lon": -71.7, "level": "Province/Territory"},
    "Ontario": {"lat": 50.0, "lon": -85.0, "level": "Province/Territory"},
    "Prairie provinces": {"lat": 54.5, "lon": -106.0, "level": "Region"},
    "Manitoba": {"lat": 54.8, "lon": -98.0, "level": "Province/Territory"},
    "Saskatchewan": {"lat": 54.5, "lon": -106.0, "level": "Province/Territory"},
    "Alberta": {"lat": 54.5, "lon": -114.0, "level": "Province/Territory"},
    "British Columbia": {"lat": 53.7, "lon": -124.7, "level": "Province/Territory"},
    "Territories": {"lat": 64.0, "lon": -118.0, "level": "Region"},
    "Yukon": {"lat": 64.2, "lon": -135.0, "level": "Province/Territory"},
    "Northwest Territories": {"lat": 64.8, "lon": -124.8, "level": "Province/Territory"},
    "Nunavut": {"lat": 66.0, "lon": -95.0, "level": "Province/Territory"},
}


def load_dataset(csv_path: str | Path = DATA_FILE) -> pd.DataFrame:
    try:
        data = pd.read_csv(csv_path)
        if "GEO" not in data.columns and "Geography" not in data.columns:
            raise ParserError("Wide StatCan layout detected.")
    except ParserError:
        return _load_wide_statcan_table(csv_path)

    if "GEO" in data.columns and "Geography" not in data.columns:
        data["Geography"] = data["GEO"]
    return _normalize_text_columns(data)


def _normalize_text_columns(data: pd.DataFrame) -> pd.DataFrame:
    text_columns = [
        "Geography",
        "Indigenous identity",
        "Age group",
        "Gender",
        "Overall health",
        "Housing - Needs repairs",
        "Persons per room (crowding)",
        "Statistics",
        "STATUS",
    ]
    for column in text_columns:
        if column in data.columns:
            data[column] = data[column].astype("string").str.strip()
    return data


def _clean_statcan_label(text: str) -> str:
    text = (text or "").strip().strip('"').replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+\d+(?=\s|$)", "", text)
    return text.strip()


def _parse_statcan_value(raw_value: str) -> tuple[float | None, str | pd._libs.missing.NAType]:
    raw_value = (raw_value or "").strip().replace(",", "")
    if not raw_value:
        return None, pd.NA
    if raw_value == "F":
        return None, "F"

    match = re.match(r"^([-+]?[0-9]*\.?[0-9]+)([A-Za-z]*)$", raw_value)
    if not match:
        return None, raw_value

    value = float(match.group(1))
    status = match.group(2) or pd.NA
    return value, status


def _load_wide_statcan_table(csv_path: str | Path) -> pd.DataFrame:
    with Path(csv_path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))

    geography_row = rows[8]
    identity_row = rows[9]
    age_row = rows[10]
    gender_row = rows[11]
    statistic_row = rows[12]

    column_meta: dict[int, dict[str, str]] = {}
    current_geography = None
    current_identity = None
    current_age = None
    current_gender = None

    for column_index in range(3, len(geography_row)):
        if geography_row[column_index].strip():
            current_geography = _clean_statcan_label(geography_row[column_index])
        if identity_row[column_index].strip():
            current_identity = _clean_statcan_label(identity_row[column_index])
        if age_row[column_index].strip():
            current_age = _clean_statcan_label(age_row[column_index])
        if gender_row[column_index].strip():
            current_gender = _clean_statcan_label(gender_row[column_index])

        column_meta[column_index] = {
            "Geography": current_geography,
            "Indigenous identity": current_identity,
            "Age group": current_age,
            "Gender": current_gender,
            "Statistics": _clean_statcan_label(statistic_row[column_index]),
        }

    records: list[dict[str, object]] = []
    current_health = None
    current_repairs = None

    for row in rows[15:]:
        if len(row) != len(geography_row):
            break

        health_value = _clean_statcan_label(row[0])
        repairs_value = _clean_statcan_label(row[1])
        crowding_value = _clean_statcan_label(row[2])

        if health_value:
            current_health = health_value
        if repairs_value:
            current_repairs = repairs_value

        for column_index in range(3, len(row)):
            value, status = _parse_statcan_value(row[column_index])
            if value is None and pd.isna(status):
                continue

            metadata = column_meta[column_index]
            records.append(
                {
                    "Geography": metadata["Geography"],
                    "Indigenous identity": metadata["Indigenous identity"],
                    "Age group": metadata["Age group"],
                    "Gender": metadata["Gender"],
                    "Overall health": current_health,
                    "Housing - Needs repairs": current_repairs,
                    "Persons per room (crowding)": crowding_value,
                    "Statistics": metadata["Statistics"],
                    "VALUE": value,
                    "STATUS": status,
                }
            )

    return _normalize_text_columns(pd.DataFrame(records))


def _filter_valid_rows(data: pd.DataFrame, statistic: str) -> pd.DataFrame:
    filtered = data[data["Statistics"] == statistic].copy()
    filtered = filtered[filtered["STATUS"].fillna("") != "F"].copy()
    return filtered


def get_story_metrics(data: pd.DataFrame) -> dict[str, object]:
    rows = _filter_valid_rows(data, "Number of persons")

    total_population = rows[
        (rows["Geography"] == "Canada")
        & (rows["Overall health"] == "Total, self-perceived general health")
        & (rows["Housing - Needs repairs"] == "Total, housing - Needs repairs")
        & (rows["Persons per room (crowding)"] == "Total, Persons per room (crowding)")
    ]["VALUE"].iloc[0]

    major_repairs = get_national_housing_distribution(data, "repairs")
    major_repairs_share = major_repairs.loc[
        major_repairs["Category"] == "Major repairs needed", "Share"
    ].iloc[0]

    crowding = get_national_housing_distribution(data, "crowding")
    severe_crowding_share = crowding.loc[
        crowding["Category"] == "1.5 or more per room", "Share"
    ].iloc[0]

    mental_mix = get_overall_health_mix(data)
    mental_fair_poor = mental_mix[
        (mental_mix["Health type"] == "Mental health")
        & (mental_mix["Category"] == "Fair or poor")
    ]["Share"].iloc[0]

    regional = get_geography_map_data(
        data,
        overall_health="Total, self-perceived general health",
        crowding_category="1.5 persons or more per room",
        statistic="Percent",
        include_canada=False,
        include_aggregate_regions=False,
    )
    top_region = regional.iloc[0]

    return {
        "total_population": total_population,
        "major_repairs_share": major_repairs_share,
        "severe_crowding_share": severe_crowding_share,
        "mental_fair_poor_share": mental_fair_poor,
        "top_region": top_region["Geography"],
        "top_region_value": top_region["VALUE"],
    }


def get_overall_health_mix(data: pd.DataFrame) -> pd.DataFrame:
    rows = _filter_valid_rows(data, "Number of persons")
    rows = rows[
        (rows["Geography"] == "Canada")
        & (rows["Housing - Needs repairs"] == "Total, housing - Needs repairs")
        & (rows["Persons per room (crowding)"] == "Total, Persons per room (crowding)")
        & (rows["Overall health"].isin(GENERAL_HEALTH_LEVELS + MENTAL_HEALTH_LEVELS))
    ].copy()

    rows["Health type"] = rows["Overall health"].map(
        lambda value: "General health"
        if value in GENERAL_HEALTH_LEVELS
        else "Mental health"
    )
    rows["Category"] = rows["Overall health"].map(SHORT_HEALTH_LABELS)
    rows["Share"] = rows.groupby("Health type")["VALUE"].transform(
        lambda values: values / values.sum() * 100
    )
    return rows[["Health type", "Category", "VALUE", "Share"]]


def get_national_housing_distribution(data: pd.DataFrame, dimension: str) -> pd.DataFrame:
    rows = _filter_valid_rows(data, "Number of persons")
    rows = rows[
        (rows["Geography"] == "Canada")
        & (rows["Overall health"] == "Total, self-perceived general health")
    ].copy()

    if dimension == "repairs":
        rows = rows[
            (rows["Persons per room (crowding)"] == "Total, Persons per room (crowding)")
            & (rows["Housing - Needs repairs"].isin(REPAIR_LEVELS))
        ].copy()
        rows["Category"] = rows["Housing - Needs repairs"].map(SHORT_REPAIR_LABELS)
        rows["Dimension"] = "Repair condition"
    else:
        rows = rows[
            (rows["Housing - Needs repairs"] == "Total, housing - Needs repairs")
            & (rows["Persons per room (crowding)"].isin(CROWDING_LEVELS))
        ].copy()
        rows["Category"] = rows["Persons per room (crowding)"].map(SHORT_CROWDING_LABELS)
        rows["Dimension"] = "Crowding"

    rows["Share"] = rows["VALUE"] / rows["VALUE"].sum() * 100
    return rows[["Dimension", "Category", "VALUE", "Share"]]


def _health_levels_for_type(health_type: str) -> list[str]:
    if health_type == "general":
        return GENERAL_HEALTH_LEVELS
    return MENTAL_HEALTH_LEVELS


def get_health_composition_by_repairs(
    data: pd.DataFrame,
    health_type: str,
    geography: str = "Canada",
) -> pd.DataFrame:
    health_levels = _health_levels_for_type(health_type)
    rows = _filter_valid_rows(data, "Number of persons")
    rows = rows[
        (rows["Geography"] == geography)
        & (rows["Persons per room (crowding)"] == "Total, Persons per room (crowding)")
        & (rows["Housing - Needs repairs"].isin(REPAIR_LEVELS))
        & (rows["Overall health"].isin(health_levels))
    ].copy()

    rows["Housing condition"] = rows["Housing - Needs repairs"].map(SHORT_REPAIR_LABELS)
    rows["Health category"] = rows["Overall health"].map(SHORT_HEALTH_LABELS)
    rows["Share"] = rows.groupby("Housing condition")["VALUE"].transform(
        lambda values: values / values.sum() * 100
    )
    return rows[
        ["Housing condition", "Health category", "VALUE", "Share"]
    ].sort_values(["Housing condition", "Health category"])


def get_health_composition_by_crowding(
    data: pd.DataFrame,
    health_type: str,
    geography: str = "Canada",
) -> pd.DataFrame:
    health_levels = _health_levels_for_type(health_type)
    rows = _filter_valid_rows(data, "Number of persons")
    rows = rows[
        (rows["Geography"] == geography)
        & (rows["Housing - Needs repairs"] == "Total, housing - Needs repairs")
        & (rows["Persons per room (crowding)"].isin(CROWDING_LEVELS))
        & (rows["Overall health"].isin(health_levels))
    ].copy()

    rows["Housing condition"] = rows["Persons per room (crowding)"].map(
        SHORT_CROWDING_LABELS
    )
    rows["Health category"] = rows["Overall health"].map(SHORT_HEALTH_LABELS)
    rows["Share"] = rows.groupby("Housing condition")["VALUE"].transform(
        lambda values: values / values.sum() * 100
    )
    return rows[
        ["Housing condition", "Health category", "VALUE", "Share"]
    ].sort_values(["Housing condition", "Health category"])


def get_fair_poor_trend(data: pd.DataFrame, dimension: str) -> pd.DataFrame:
    frames = []
    for health_type, label in [("general", "General health"), ("mental", "Mental health")]:
        if dimension == "repairs":
            composition = get_health_composition_by_repairs(data, health_type)
        else:
            composition = get_health_composition_by_crowding(data, health_type)
        fair_poor = composition[composition["Health category"] == "Fair or poor"].copy()
        fair_poor["Health type"] = label
        frames.append(fair_poor)
    return pd.concat(frames, ignore_index=True)


def get_geography_map_data(
    data: pd.DataFrame,
    overall_health: str,
    crowding_category: str,
    statistic: str,
    repairs_category: str = "Total, housing - Needs repairs",
    include_canada: bool = False,
    include_aggregate_regions: bool = True,
) -> pd.DataFrame:
    rows = _filter_valid_rows(data, statistic)
    rows = rows[
        (rows["Overall health"] == overall_health)
        & (rows["Persons per room (crowding)"] == crowding_category)
        & (rows["Housing - Needs repairs"] == repairs_category)
        & (rows["Geography"].isin(REGION_COORDINATES))
    ].copy()

    if not include_canada:
        rows = rows[rows["Geography"] != "Canada"].copy()

    coordinates = (
        pd.DataFrame.from_dict(REGION_COORDINATES, orient="index")
        .reset_index()
        .rename(columns={"index": "Geography"})
    )
    rows = rows.merge(coordinates, on="Geography", how="left")

    if not include_aggregate_regions:
        rows = rows[rows["level"] == "Province/Territory"].copy()

    return rows[
        [
            "Geography",
            "Overall health",
            "Housing - Needs repairs",
            "Persons per room (crowding)",
            "Statistics",
            "VALUE",
            "STATUS",
            "lat",
            "lon",
            "level",
        ]
    ].sort_values("VALUE", ascending=False)
