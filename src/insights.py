import pandas as pd
from src.visualization import detect_datetime_columns


def generate_dataset_insights(df):

    all_insights = []
    story_context = {}

    analyses = [
        analyze_basic(df),
        analyze_missing_values(df),
        analyze_duplicates(df),
        analyze_column_statistics(df),
        analyze_categories(df),
        analyze_correlations(df),
        analyze_outliers(df),
        analyze_time_series(df)
    ]

    for analysis in analyses:
        all_insights.extend(analysis["insights"])
        story_context.update(analysis["context"])

    return {
        "insights": all_insights,
        "story_context": story_context
    }



def analyze_basic(df):
    """Analyze basic dataset information."""

    rows, columns = df.shape

    numeric_columns = len(df.select_dtypes(include="number").columns)
    categorical_columns = len(df.select_dtypes(exclude="number").columns)

    insights = [
        {
            "type": "info",
            "title": "Dataset Size",
            "message": f"The dataset contains {rows:,} rows and {columns} columns."
        },
        {
            "type": "info",
            "title": "Column Types",
            "message": (
                f"{numeric_columns} numeric column(s) and "
                f"{categorical_columns} categorical column(s) detected."
            )
        }
    ]

    context = {
        "dataset": {
            "rows": rows,
            "columns": columns,
            "numeric_columns": numeric_columns,
            "categorical_columns": categorical_columns
        }
    }

    return {
        "insights": insights,
        "context": context
    }

def analyze_missing_values(df):
    """Analyze missing values in the dataset."""

    missing_counts = df.isnull().sum()
    missing_counts = missing_counts[missing_counts > 0]

    insights = []

    if missing_counts.empty:
        insights.append({
            "type": "success",
            "title": "Missing Values",
            "message": "No missing values found in the dataset."
        })

        context = {
            "missing_values": {
                "total_missing": 0,
                "columns": []
            }
        }

    else:
        columns = []

        total_missing = int(missing_counts.sum())

        for column, count in missing_counts.items():
            percentage = round((count / len(df)) * 100, 2)

            insights.append({
                "type": "warning",
                "title": "Missing Values",
                "message": f"{column} contains {count} missing values ({percentage}%)."
            })

            columns.append({
                "column": column,
                "count": int(count),
                "percentage": percentage
            })

        context = {
            "missing_values": {
                "total_missing": total_missing,
                "columns": columns
            }
        }

    return {
        "insights": insights,
        "context": context
    }
def analyze_duplicates(df):
    """Analyze duplicate rows in the dataset."""

    duplicate_count = int(df.duplicated().sum())
    duplicate_percentage = round((duplicate_count / len(df)) * 100, 2) if len(df) > 0 else 0

    if duplicate_count == 0:
        insights = [
            {
                "type": "success",
                "title": "Duplicate Rows",
                "message": "No duplicate rows found."
            }
        ]
    else:
        insights = [
            {
                "type": "warning",
                "title": "Duplicate Rows",
                "message": (
                    f"{duplicate_count} duplicate row(s) found "
                    f"({duplicate_percentage}% of the dataset)."
                )
            }
        ]

    context = {
        "duplicates": {
            "count": duplicate_count,
            "percentage": duplicate_percentage
        }
    }

    return {
        "insights": insights,
        "context": context
    }

import pandas as pd

def analyze_column_statistics(df):
    """Analyze descriptive statistics for numeric columns."""

    numeric_df = df.select_dtypes(include="number")

    insights = []
    statistics = []

    if numeric_df.empty:
        insights.append({
            "type": "info",
            "title": "Statistics",
            "message": "No numeric columns found."
        })

        return {
            "insights": insights,
            "context": {
                "statistics": []
            }
        }

    for column in numeric_df.columns:

        stats = {
            "column": column,
            "mean": round(float(numeric_df[column].mean()), 2),
            "median": round(float(numeric_df[column].median()), 2),
            "minimum": round(float(numeric_df[column].min()), 2),
            "maximum": round(float(numeric_df[column].max()), 2),
            "std_dev": round(float(numeric_df[column].std()), 2),
            "range": round(float(
                numeric_df[column].max() -
                numeric_df[column].min()
            ), 2)
        }

        statistics.append(stats)

    insights.append({
        "type": "info",
        "title": "Statistics",
        "message": f"Statistical summary generated for {len(statistics)} numeric column(s)."
    })

    return {
        "insights": insights,
        "context": {
            "statistics": statistics
        }
    }

def analyze_categories(df):
    """Analyze categorical columns."""

    categorical_df = df.select_dtypes(exclude="number")

    insights = []
    categories = []

    if categorical_df.empty:

        insights.append({
            "type": "info",
            "title": "Categories",
            "message": "No categorical columns found."
        })

        return {
            "insights": insights,
            "context": {
                "categories": []
            }
        }

    for column in categorical_df.columns:

        value_counts = categorical_df[column].value_counts()

        top_value = value_counts.index[0]
        top_count = int(value_counts.iloc[0])

        percentage = round(
            (top_count / len(df)) * 100,
            2
        )

        categories.append({
            "column": column,
            "unique_values": int(categorical_df[column].nunique()),
            "top_category": str(top_value),
            "count": top_count,
            "percentage": percentage
        })

    insights.append({
        "type": "info",
        "title": "Categories",
        "message": f"Analyzed {len(categories)} categorical column(s)."
    })

    return {
        "insights": insights,
        "context": {
            "categories": categories
        }
    }

def analyze_correlations(df, threshold=0.7):
    """Analyze strong correlations between numeric columns."""

    numeric_df = df.select_dtypes(include="number")

    insights = []
    correlations = []

    if numeric_df.shape[1] < 2:
        insights.append({
            "type": "info",
            "title": "Correlations",
            "message": "Not enough numeric columns to analyze correlations."
        })

        return {
            "insights": insights,
            "context": {
                "correlations": []
            }
        }

    corr_matrix = numeric_df.corr()

    columns = corr_matrix.columns

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):

            value = corr_matrix.iloc[i, j]

            if abs(value) >= threshold:

                correlations.append({
                    "column1": columns[i],
                    "column2": columns[j],
                    "correlation": round(float(value), 2),
                    "relationship": (
                        "positive"
                        if value > 0
                        else "negative"
                    )
                })

    if correlations:

        insights.append({
            "type": "success",
            "title": "Correlations",
            "message": f"Found {len(correlations)} strong correlation(s)."
        })

    else:

        insights.append({
            "type": "info",
            "title": "Correlations",
            "message": "No strong correlations found."
        })

    return {
        "insights": insights,
        "context": {
            "correlations": correlations
        }
    }

def analyze_outliers(df):
    """Analyze outliers in numeric columns using the IQR method."""

    numeric_df = df.select_dtypes(include="number")

    insights = []
    outliers = []

    if numeric_df.empty:
        insights.append({
            "type": "info",
            "title": "Outliers",
            "message": "No numeric columns found."
        })

        return {
            "insights": insights,
            "context": {
                "outliers": []
            }
        }

    for column in numeric_df.columns:

        q1 = numeric_df[column].quantile(0.25)
        q3 = numeric_df[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        mask = (numeric_df[column] < lower) | (numeric_df[column] > upper)

        count = int(mask.sum())

        if count > 0:

            percentage = round((count / len(df)) * 100, 2)

            outliers.append({
                "column": column,
                "count": count,
                "percentage": percentage,
                "lower_bound": round(float(lower), 2),
                "upper_bound": round(float(upper), 2)
            })

    if outliers:

        insights.append({
            "type": "warning",
            "title": "Outliers",
            "message": f"Outliers detected in {len(outliers)} numeric column(s)."
        })

    else:

        insights.append({
            "type": "success",
            "title": "Outliers",
            "message": "No significant outliers detected."
        })

    return {
        "insights": insights,
        "context": {
            "outliers": outliers
        }
    }


def analyze_time_series(df):
    """Analyze trends in time-series data."""

    insights = []
    context = {
        "time_series": []
    }

    
    

    
           

    # Detect datetime columns
    datetime_columns = detect_datetime_columns(df)

    if not datetime_columns:

        insights.append({
            "type": "info",
            "title": "Time Series",
            "message": "No date/time column detected."
        })

        return {
            "insights": insights,
            "context": context
        }

    # Use the first detected datetime column
    date_column = datetime_columns[0]
    # Sort dataset chronologically
    df = df.sort_values(by=date_column).reset_index(drop=True)

    numeric_columns = df.select_dtypes(include="number").columns

    if len(numeric_columns) == 0:

        insights.append({
            "type": "info",
            "title": "Time Series",
            "message": "No numeric columns available for time-series analysis."
        })

        return {
            "insights": insights,
            "context": context
        }
    
    for column in numeric_columns:

        # Skip columns with fewer than 2 valid values
        temp_df = df[[date_column, column]].dropna()
        temp_df = (
            df[[date_column, column]]
            .dropna()
            .reset_index(drop=True)
        )
        if len(temp_df) < 2:
            continue

        values = temp_df[column]

        if len(values) < 2:
            continue

        highest_index = values.idxmax()
        lowest_index = values.idxmin()

        highest = {
            "period": str(df.loc[highest_index, date_column]),
            "value": float(values.max())
        }

        lowest = {
            "period": str(df.loc[lowest_index, date_column]),
            "value": float(values.min())
        }
        percentage_change = values.pct_change() * 100

        valid_changes = percentage_change.dropna()

        if valid_changes.empty:
            continue

        max_index = valid_changes.idxmax()

        largest_increase = {
            "from": str(temp_df.loc[max_index - 1, date_column]),
            "to": str(temp_df.loc[max_index, date_column]),
            "percent": round(float(valid_changes.loc[max_index]), 2)
        }
        min_index = valid_changes.idxmin()

        largest_decrease = {
            "from": str(temp_df.loc[min_index - 1, date_column]),
            "to": str(temp_df.loc[min_index, date_column]),
            "percent": round(float(valid_changes.loc[min_index]), 2)
        }

        first_value = values.iloc[0]
        last_value = values.iloc[-1]

        change_percent = ((last_value - first_value) / first_value) * 100

        if change_percent >= 20:
            trend = "Strong Growth"

        elif change_percent >= 5:
            trend = "Moderate Growth"

        elif change_percent <= -20:
            trend = "Strong Decline"

        elif change_percent <= -5:
            trend = "Moderate Decline"

        else:
            trend = "Stable"

        mean = values.mean()

        if mean != 0:

            cv = values.std() / mean

        else:
            cv = 0

        if cv < 0.10:
            volatility = "Low"

        elif cv < 0.30:
            volatility = "Moderate"

        else:
            volatility = "High"

        context["time_series"].append({

            "metric": column,

            "highest": highest,

            "lowest": lowest,

            "largest_increase": largest_increase,

            "largest_decrease": largest_decrease,

            "overall_trend": trend,

            "volatility": volatility
        })

    if context["time_series"]:

        insights.append({
            "type": "success",
            "title": "Time Series",
            "message": (
                f"Analyzed {len(context['time_series'])} "
                "time-series metric(s)."
            )
        })

    else:

        insights.append({
            "type": "info",
            "title": "Time Series",
            "message": (
                "No suitable time-series metrics were found."
            )
        })

    return {
    "insights": insights,
    "context": context
    }