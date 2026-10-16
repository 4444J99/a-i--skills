# ARIMA Model Guide

## Model Components

**ARIMA(p, d, q)**:
- **p**: Autoregressive order (past values)
- **d**: Differencing order (make stationary)
- **q**: Moving average order (past errors)

**SARIMA(p, d, q)(P, D, Q, m)**:
- Uppercase: Seasonal components
- **m**: Seasonal period (12 for monthly, 4 for quarterly)

## Model Selection Process

### 1. Check Stationarity

```python
from statsmodels.tsa.stattools import adfuller, kpss

def check_stationarity(series):
    # ADF Test (null: non-stationary)
    adf_result = adfuller(series, autolag='AIC')
    print(f'ADF Statistic: {adf_result[0]:.4f}')
    print(f'p-value: {adf_result[1]:.4f}')
    print('Stationary' if adf_result[1] < 0.05 else 'Non-stationary')

    # KPSS Test (null: stationary)
    kpss_result = kpss(series, regression='c', nlags='auto')
    print(f'KPSS Statistic: {kpss_result[0]:.4f}')
    print(f'p-value: {kpss_result[1]:.4f}')
```

### 2. Determine Differencing (d)

```python
from statsmodels.tsa.stattools import adfuller

def find_d(series, max_d=2):
    d = 0
    temp = series.copy()

    while d <= max_d:
        result = adfuller(temp.dropna())
        if result[1] < 0.05:  # Stationary
            return d
        temp = temp.diff()
        d += 1

    return max_d
```

### 3. Identify p and q from ACF/PACF

| Pattern | Indicates |
|---------|-----------|
| PACF cuts off at lag p | AR(p) model |
| ACF cuts off at lag q | MA(q) model |
| Both decay gradually | ARMA model |

```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
plot_acf(series_stationary, ax=ax1, lags=40)
plot_pacf(series_stationary, ax=ax2, lags=40)
plt.tight_layout()
```

### 4. Auto Selection with pmdarima

```python
from pmdarima import auto_arima

model = auto_arima(
    series,
    start_p=0, max_p=5,
    start_q=0, max_q=5,
    d=None,  # Auto-detect
    seasonal=True,
    m=12,  # Monthly seasonality
    start_P=0, max_P=2,
    start_Q=0, max_Q=2,
    D=None,  # Auto-detect seasonal differencing
    trace=True,
    error_action='ignore',
    suppress_warnings=True,
    stepwise=True,
    information_criterion='aic'
)

print(model.summary())
```

## Model Diagnostics

### Residual Analysis

```python
from statsmodels.stats.diagnostic import acorr_ljungbox

def check_residuals(model):
    residuals = model.resid

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Residual plot
    axes[0, 0].plot(residuals)
    axes[0, 0].set_title('Residuals')

    # Histogram
    axes[0, 1].hist(residuals, bins=30)
    axes[0, 1].set_title('Histogram')

    # ACF of residuals
    plot_acf(residuals, ax=axes[1, 0])

    # Q-Q plot
    from scipy import stats
    stats.probplot(residuals, plot=axes[1, 1])

    plt.tight_layout()

    # Ljung-Box test
    lb_test = acorr_ljungbox(residuals, lags=20)
    print("Ljung-Box test p-values:")
    print(lb_test)
```

### Good Model Indicators

1. **Residuals**: White noise (no autocorrelation)
2. **Ljung-Box**: p-values > 0.05 (no autocorrelation)
3. **Residual histogram**: Approximately normal
4. **AIC/BIC**: Lower is better

## Forecasting

```python
from statsmodels.tsa.arima.model import ARIMA

# Fit model
model = ARIMA(series, order=(2, 1, 2))
fitted = model.fit()

# Point forecast
forecast = fitted.forecast(steps=30)

# Forecast with confidence intervals
forecast_obj = fitted.get_forecast(steps=30)
mean = forecast_obj.predicted_mean
conf_int = forecast_obj.conf_int(alpha=0.05)

# Plot
plt.figure(figsize=(12, 6))
plt.plot(series.index, series, label='Historical')
plt.plot(forecast.index, forecast, label='Forecast', color='red')
plt.fill_between(conf_int.index,
                 conf_int.iloc[:, 0],
                 conf_int.iloc[:, 1],
                 alpha=0.3)
plt.legend()
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Non-stationary | Increase d |
| Residual autocorrelation | Adjust p or q |
| Seasonal patterns | Use SARIMA |
| High variance | Log transform |
| Model doesn't converge | Simplify (reduce p, q) |
