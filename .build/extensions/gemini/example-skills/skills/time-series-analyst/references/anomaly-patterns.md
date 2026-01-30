# Time Series Anomaly Detection

## Anomaly Types

| Type | Description | Example |
|------|-------------|---------|
| Point | Single outlier | Spike in traffic |
| Contextual | Normal value, wrong context | High sales on holiday |
| Collective | Sequence of anomalies | Gradual drift |
| Seasonal | Violation of seasonal pattern | Missing weekly peak |

## Statistical Methods

### Z-Score

```python
def zscore_anomalies(series, threshold=3):
    mean = series.mean()
    std = series.std()
    z_scores = (series - mean) / std
    return abs(z_scores) > threshold
```

### Modified Z-Score (Robust)

```python
def modified_zscore_anomalies(series, threshold=3.5):
    median = series.median()
    mad = np.median(np.abs(series - median))
    modified_z = 0.6745 * (series - median) / mad
    return abs(modified_z) > threshold
```

### IQR Method

```python
def iqr_anomalies(series, multiplier=1.5):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - multiplier * IQR
    upper = Q3 + multiplier * IQR
    return (series < lower) | (series > upper)
```

### Rolling Statistics

```python
def rolling_anomalies(series, window=30, num_std=2):
    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()

    lower = rolling_mean - num_std * rolling_std
    upper = rolling_mean + num_std * rolling_std

    return (series < lower) | (series > upper)
```

## Machine Learning Methods

### Isolation Forest

```python
from sklearn.ensemble import IsolationForest

def isolation_forest_anomalies(series, contamination=0.01):
    # Create features
    df = pd.DataFrame({'value': series})
    df['hour'] = series.index.hour
    df['dayofweek'] = series.index.dayofweek
    df['rolling_mean'] = series.rolling(24).mean()
    df['rolling_std'] = series.rolling(24).std()
    df = df.dropna()

    model = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=100
    )

    predictions = model.fit_predict(df)
    return predictions == -1  # -1 = anomaly
```

### Local Outlier Factor

```python
from sklearn.neighbors import LocalOutlierFactor

def lof_anomalies(series, n_neighbors=20, contamination=0.01):
    # Reshape for sklearn
    X = series.values.reshape(-1, 1)

    lof = LocalOutlierFactor(
        n_neighbors=n_neighbors,
        contamination=contamination
    )

    predictions = lof.fit_predict(X)
    return predictions == -1
```

### DBSCAN

```python
from sklearn.cluster import DBSCAN

def dbscan_anomalies(series, eps=0.5, min_samples=5):
    X = series.values.reshape(-1, 1)

    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(X)

    # -1 label = noise/anomaly
    return labels == -1
```

## Seasonal Decomposition

```python
from statsmodels.tsa.seasonal import STL

def stl_anomalies(series, period=24, threshold=3):
    stl = STL(series, period=period, robust=True)
    result = stl.fit()

    # Anomalies in residual
    residual = result.resid
    residual_zscore = (residual - residual.mean()) / residual.std()

    return abs(residual_zscore) > threshold
```

## Threshold Selection

| Method | Sensitivity | Use Case |
|--------|-------------|----------|
| Z > 2 | High | Catch more anomalies |
| Z > 3 | Medium | Balanced |
| Z > 4 | Low | Only extreme outliers |
| IQR × 1.5 | High | With outliers |
| IQR × 3.0 | Low | Robust data |

## Evaluation Metrics

```python
from sklearn.metrics import precision_score, recall_score, f1_score

def evaluate_detector(y_true, y_pred):
    return {
        'precision': precision_score(y_true, y_pred),
        'recall': recall_score(y_true, y_pred),
        'f1': f1_score(y_true, y_pred),
        'false_positive_rate': sum((y_pred == 1) & (y_true == 0)) / sum(y_true == 0)
    }
```

## Alerting Thresholds

| Severity | Definition |
|----------|------------|
| Warning | 2-3 standard deviations |
| Critical | 3-4 standard deviations |
| Emergency | > 4 standard deviations |
