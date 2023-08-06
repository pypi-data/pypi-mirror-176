# -*- coding: utf-8 -*-
"""
Recommended installs: pip install pytrends fredapi yfinance
Uses a number of live public data sources to construct an example production case.

While stock price forecasting is shown here, time series forecasting alone is not a recommended basis for managing investments!

This is a highly opinionated approach.
evolve = True allows the timeseries to automatically adapt to changes.

There is a slight risk of it getting caught in suboptimal position however.
It should probably be coupled with some basic data sanity checks.

cd ./AutoTS
conda activate py38
nohup python production_example.py > /dev/null &
"""
try:  # needs to go first
    from sklearnex import patch_sklearn

    patch_sklearn()
except Exception as e:
    print(repr(e))
import json
import datetime
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  # required only for graphs
from autots import AutoTS, load_live_daily, create_regressor


fred_key = "93873d40f10c20fe6f6e75b1ad0aed4d"  # https://fred.stlouisfed.org/docs/api/api_key.html
gsa_key = "zBYMGPb0bom4BEDsD8V0d3mwR6DnabT7Q9vkF1hz"  # https://open.gsa.gov/api/dap/
forecast_name = "example_0823"
graph = True  # whether to plot graphs
# https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects
frequency = (
    "D"  # "infer" for automatic alignment, but specific offsets are most reliable
)
forecast_length = 60  # number of periods to forecast ahead
drop_most_recent = 1  # whether to discard the n most recent records (as incomplete)
num_validations = (
    2  # number of cross validation runs. More is better but slower, usually
)
validation_method = "similarity"  # "similarity", "backwards", "seasonal 364"
n_jobs = "auto"  # or set to number of CPU cores
prediction_interval = (
    0.9  # sets the upper and lower forecast range by probability range. Bigger = wider
)
initial_training = "auto"  # set this to True on first run, or on reset, 'auto' looks for existing template, if found, sets to False.
evolve = True  # allow time series to progressively evolve on each run, if False, uses fixed template
archive_templates = True  # save a copy of the model template used with a timestamp
save_location = None  # "C:/Users/Colin/Downloads"  # directory to save templates to. Defaults to working dir
template_filename = f"autots_forecast_template_{forecast_name}.csv"
forecast_csv_name = None  # f"autots_forecast_{forecast_name}.csv"  # or None, point forecast only is written
model_list = "fast_parallel"
transformer_list = "fast"  # 'superfast'
transformer_max_depth = 5
models_mode = "default"  # "deep", "regressor"
initial_template = 'random'  # 'random' 'general+random'
preclean = None
{  # preclean option
    "fillna": 'ffill',
    "transformations": {"0": "EWMAFilter"},
    "transformation_params": {
        "0": {"span": 14},
    },
}

if save_location is not None:
    template_filename = os.path.join(save_location, template_filename)
    if forecast_csv_name is not None:
        forecast_csv_name = os.path.join(save_location, forecast_csv_name)

if initial_training == "auto":
    initial_training = not os.path.exists(template_filename)
    if initial_training:
        print("No existing template found.")
    else:
        print("Existing template found.")

# set max generations based on settings, increase for slower but greater chance of highest accuracy
# if include_ensemble is specified in import_templates, ensembles can progressively nest over generations
if initial_training:
    gens = 100
    models_to_validate = 0.35
    ensemble = ["horizontal-max", "dist", "simple"]  # , "mosaic", "mosaic-window"
elif evolve:
    gens = 10
    models_to_validate = 0.3
    ensemble = ["horizontal-max", "dist", "simple"]  # "mosaic", "mosaic-window", "subsample"
else:
    gens = 0
    models_to_validate = 0.99
    ensemble = ["horizontal-max", "dist", "simple"]  # "mosaic", "mosaic-window",

# only save the very best model if not evolve
if evolve:
    n_export = 30
else:
    n_export = 1  # wouldn't be a bad idea to do > 1, allowing some future adaptability

"""
Begin dataset retrieval
"""

df = load_live_daily(
    long=False,
    fred_key=fred_key,
    fred_series=[
        "DGS10",
        "T5YIE",
        "SP500",
        "DCOILWTICO",
        "DEXUSEU",
        "WPU0911",
        "DEXUSUK",
    ],
    tickers=["MSFT", "PG"],
    trends_list=["forecasting", "msft", "p&g"],
    earthquake_min_magnitude=5,
    weather_years=3,
    london_air_days=700,
    gsa_key=gsa_key,
    gov_domain_list=None,  # ['usajobs.gov', 'usps.com', 'weather.gov'],
    gov_domain_limit=700,
)
# remove "volume" data as it skews MAE (another solution is to adjust metric_weighting)
df = df[[x for x in df.columns if "_volume" not in x]]
# remove dividends and stock splits as it skews metrics (too intermittent)
df = df[[x for x in df.columns if "_dividends" not in x]]
df = df[[x for x in df.columns if "stock_splits" not in x]]

df = df[df.index.year > 1999]
start_time = datetime.datetime.now()
# remove any data from the future
df = df[df.index <= start_time]
# remove series with no recent data
df = df.dropna(axis="columns", how="all")
min_cutoff_date = start_time - datetime.timedelta(days=180)
most_recent_date = df.notna()[::-1].idxmax()
drop_cols = most_recent_date[most_recent_date < min_cutoff_date].index.tolist()
df = df.drop(columns=drop_cols)
print(
    f"Series with most NaN: {df.head(365).isnull().sum().sort_values(ascending=False).head(5)}"
)

df.to_csv(f"training_data_{forecast_name}.csv")
# df = pd.read_csv(f"training_data_{forecast_name}.csv", index_col=0, parse_dates=[0])

# example future_regressor with some things we can glean from data and datetime index
# note this only accepts `wide` style input dataframes
# and this is optional, not required for the modeling
regr_train, regr_fcst = create_regressor(
    df,
    forecast_length=forecast_length,
    frequency=frequency,
    drop_most_recent=drop_most_recent,
    scale=True,
    summarize="auto",
    backfill="bfill",
    fill_na="spline",
    holiday_countries={"US": None},  # requires holidays package
    encode_holiday_type=True,
    # datepart_method="simple_2",
)

# remove the first forecast_length rows (because those are lost in regressor)
df = df.iloc[forecast_length:]
regr_train = regr_train.iloc[forecast_length:]

print("data setup completed, beginning modeling")
"""
Begin modeling
"""

metric_weighting = {
    'smape_weighting': 1,
    'mae_weighting': 3,
    'rmse_weighting': 1,
    'made_weighting': 1,
    'mage_weighting': 0,
    'mle_weighting': 0,
    'imle_weighting': 0,
    'spl_weighting': 2,
    'containment_weighting': 0,
    'contour_weighting': 0,
    'runtime_weighting': 0.05,
}

model = AutoTS(
    forecast_length=forecast_length,
    frequency=frequency,
    prediction_interval=prediction_interval,
    ensemble=ensemble,
    model_list=model_list,
    transformer_list=transformer_list,
    transformer_max_depth=transformer_max_depth,
    max_generations=gens,
    metric_weighting=metric_weighting,
    initial_template=initial_template,
    aggfunc="sum",
    models_to_validate=models_to_validate,
    model_interrupt=True,
    num_validations=num_validations,
    validation_method=validation_method,
    constraint=None,
    drop_most_recent=drop_most_recent,  # if newest data is incomplete, also remember to increase forecast_length
    preclean=preclean,
    models_mode=models_mode,
    # no_negatives=True,
    # subset=100,
    # prefill_na=0,
    # remove_leading_zeroes=True,
    current_model_file=f"current_model_{forecast_name}",
    n_jobs=n_jobs,
    verbose=1,
)

if not initial_training:
    if evolve:
        model.import_template(template_filename, method="addon")
    else:
        model.import_template(template_filename, method="only")

model = model.fit(
    df,
    future_regressor=regr_train,
)

prediction = model.predict(
    future_regressor=regr_fcst, verbose=2, fail_on_forecast_nan=True
)

# Print the details of the best model
print(model)

"""
Process results
"""

# point forecasts dataframe
forecasts_df = prediction.forecast  # .fillna(0).round(0)
if forecast_csv_name is not None:
    forecasts_df.to_csv(forecast_csv_name)

forecasts_upper_df = prediction.upper_forecast
forecasts_lower_df = prediction.lower_forecast

# accuracy of all tried model results
model_results = model.results()
validation_results = model.results("validation")

# save a template of best models
if initial_training or evolve:
    model.export_template(
        template_filename,
        models="best",
        n=n_export,
        max_per_model_class=6,
        include_results=True,
    )
    if archive_templates:
        arc_file = f"{template_filename.split('.csv')[0]}_{start_time.strftime('%Y%m%d%H%M')}.csv"
        model.export_template(arc_file, models="best", n=1)

print(f"Model failure rate is {model.failure_rate() * 100:.1f}%")
print(f'The following model types failed completely {model.list_failed_model_types()}')
print("Slowest models:")
print(
    model_results[model_results["Ensemble"] < 1]
    .groupby("Model")
    .agg({"TotalRuntimeSeconds": ["mean", "max"]})
    .idxmax()
)

model_parameters = json.loads(model.best_model["ModelParameters"].iloc[0])

if graph:
    model.export_template("all_results.csv", models='all')
    column_indices = [0, 1]  # change columns here
    column_indices = list(range(model.df_wide_numeric.shape[1]))
    for plt_col in column_indices:
        prediction.plot(
            model.df_wide_numeric.clip(lower=0),
            series=model.df_wide_numeric.columns[plt_col],
            remove_zeroes=True,
            interpolate="linear",
            start_date="2021-01-01",
        )
        # plt.savefig("model.png", dpi=300)
        plt.show()

    with plt.style.context("seaborn-white"):
        ax = model.plot_per_series_smape()
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        plt.show()

    model.plot_backforecast()
    plt.show()

    if model.best_model_ensemble == 2:
        plt.subplots_adjust(bottom=0.5)
        model.plot_horizontal_transformers()
        # plt.savefig("transformers.png", dpi=300, bbox_inches="tight")
        plt.show()
        model.plot_horizontal_model_count()
        plt.show()

        model.plot_horizontal()
        plt.show()
        # plt.savefig("horizontal.png", dpi=300, bbox_inches="tight")

        if str(model_parameters["model_name"]).lower() in ["mosaic", "mosaic-window"]:
            mosaic_df = model.mosaic_to_df()
            print(mosaic_df[mosaic_df.columns[0:5]].head(5))

print(f"Completed at system time: {datetime.datetime.now()}")
