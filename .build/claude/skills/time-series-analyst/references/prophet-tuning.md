# Prophet Tuning Guide

## Basic Setup

```python
from prophet import Prophet
import pandas as pd

# Data must have 'ds' (datetime) and 'y' (value) columns
df = pd.DataFrame({
    'ds': dates,
    'y': values
})

model = Prophet()
model.fit(df)

# Create future dataframe
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)
```

## Seasonality Configuration

### Built-in Seasonalities

```python
model = Prophet(
    yearly_seasonality=True,   # Default: auto
    weekly_seasonality=True,   # Default: auto
    daily_seasonality=False,   # Default: auto
    seasonality_mode='additive'  # or 'multiplicative'
)
```

### Custom Seasonality

```python
# Monthly seasonality
model.add_seasonality(
    name='monthly',
    period=30.5,
    fourier_order=5
)

# Quarterly seasonality
model.add_seasonality(
    name='quarterly',
    period=91.25,
    fourier_order=8
)

# Business day pattern (weekdays only)
def is_weekday(ds):
    return ds.weekday() < 5

df['weekday'] = df['ds'].apply(is_weekday)
model.add_seasonality(
    name='weekday',
    period=5,
    fourier_order=3,
    condition_name='weekday'
)
```

### Fourier Order Selection

| Period | Suggested Order |
|--------|-----------------|
| Yearly | 10 |
| Monthly | 3-5 |
| Weekly | 3 |
| Daily | 4 |

Higher = more flexible, risk overfitting.

## Trend Configuration

```python
model = Prophet(
    growth='linear',           # or 'logistic', 'flat'
    changepoint_prior_scale=0.05,  # Flexibility (default 0.05)
    changepoints=None,         # Auto-detect or specify dates
    n_changepoints=25,         # Number of potential changepoints
)

# Logistic growth requires cap (and optionally floor)
df['cap'] = 1000
df['floor'] = 0
model = Prophet(growth='logistic')
model.fit(df)
```

### Changepoint Tuning

```python
# More changepoints = more flexibility
model = Prophet(
    changepoint_prior_scale=0.5,  # Higher = more flexible
    n_changepoints=50
)

# Visualize changepoints
from prophet.plot import add_changepoints_to_plot

fig = model.plot(forecast)
add_changepoints_to_plot(fig.gca(), model, forecast)
```

## Holiday Effects

```python
# Define holidays
holidays = pd.DataFrame({
    'holiday': 'black_friday',
    'ds': pd.to_datetime(['2023-11-24', '2024-11-29']),
    'lower_window': -1,  # Days before
    'upper_window': 1,   # Days after
})

# Add more holidays
christmas = pd.DataFrame({
    'holiday': 'christmas',
    'ds': pd.to_datetime(['2023-12-25', '2024-12-25']),
    'lower_window': -2,
    'upper_window': 1,
})

holidays = pd.concat([holidays, christmas])

model = Prophet(holidays=holidays)
```

### Country Holidays

```python
model = Prophet()
model.add_country_holidays(country_name='US')
```

## Regressors

```python
# Add external regressors
model = Prophet()
model.add_regressor('temperature')
model.add_regressor('is_promotion', standardize=False)

# Training data must include regressor columns
df['temperature'] = temp_values
df['is_promotion'] = promo_flags

model.fit(df)

# Future must also include regressors
future['temperature'] = future_temp
future['is_promotion'] = future_promo
forecast = model.predict(future)
```

## Cross-Validation

```python
from prophet.diagnostics import cross_validation, performance_metrics

# Time series cross-validation
df_cv = cross_validation(
    model,
    initial='730 days',    # Training period
    period='180 days',     # Space between cutoffs
    horizon='365 days'     # Forecast horizon
)

# Calculate metrics
df_p = performance_metrics(df_cv)
print(df_p[['horizon', 'mape', 'rmse', 'mae']])

# Plot cross-validation results
from prophet.plot import plot_cross_validation_metric

fig = plot_cross_validation_metric(df_cv, metric='mape')
```

## Hyperparameter Tuning

```python
import itertools

param_grid = {
    'changepoint_prior_scale': [0.001, 0.01, 0.1, 0.5],
    'seasonality_prior_scale': [0.01, 0.1, 1.0, 10.0],
    'seasonality_mode': ['additive', 'multiplicative']
}

all_params = [dict(zip(param_grid.keys(), v))
              for v in itertools.product(*param_grid.values())]

rmses = []
for params in all_params:
    model = Prophet(**params)
    model.fit(df)
    df_cv = cross_validation(model, initial='730 days',
                            period='180 days', horizon='365 days')
    df_p = performance_metrics(df_cv)
    rmses.append(df_p['rmse'].mean())

best_params = all_params[np.argmin(rmses)]
```

## Uncertainty Intervals

```python
model = Prophet(
    interval_width=0.95,      # 95% intervals (default 0.80)
    uncertainty_samples=1000  # MCMC samples (default 1000)
)
```
