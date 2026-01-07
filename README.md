# UrbanEV Project Summary

**UrbanEV** is a benchmark dataset and prediction framework for electric vehicle (EV) charging demand forecasting in Shenzhen, China. It contains 6 months of data (Sept 2022 - Feb 2023) from 1,362 charging stations across 275 zones, including charging occupancy, duration, volume, weather, spatial features, and pricing data.

## Models Used and Their Purpose

### Traditional Baselines (`code/baselines.py`)

- **Last Observation (LO)**: Simple persistence model using the most recent value
- **Auto-Regressive (AR)**: Time series model using lagged observations
- **ARIMA**: Statistical model combining auto-regression, differencing, and moving average for demand forecasting

### Deep Learning Models (`code/baselines.py`)

- **FCNN** (Fully Connected Neural Network): Basic feed-forward network for sequence prediction
- **LSTM** (Long Short-Term Memory): Captures temporal dependencies in charging patterns

### Additional Deep Learning Models
- **GCN** (Graph Convolutional Network): Models spatial relationships between zones using adjacency matrices
- **GCN-LSTM**: Combines spatial (GCN) and temporal (LSTM) modeling
- **ASTGCN** (Attention-based Spatial-Temporal GCN): Advanced model with attention mechanisms for capturing both spatial and temporal charging patterns

### Transformer-based Models (`code-transformer/models/`)

- **TimesNet**: Uses FFT to detect periodic patterns in charging demand and applies inception blocks for multi-scale temporal modeling
- **TimeXer**: Transformer with inverted architecture, using patching and attention mechanisms for long-term forecasting

## Model Complexity Progression

The models progressively increase in complexity from simple statistical methods to sophisticated deep learning architectures that capture both spatial dependencies (between charging zones) and temporal patterns (hourly/daily cycles) in EV charging demand.

## Dataset Details

- **Coverage**: 275 zones, 1,362 charging stations, 17,532 charging piles
- **Time Period**: September 1, 2022 - February 28, 2023
- **Data Types**: Charging occupancy, duration, volume, weather conditions, spatial features (adjacency matrices, distances), POIs, and pricing
- **Resolution**: Hourly and 5-minute aggregations available

## Project Structure

- `code/`: Traditional and deep learning baseline models
- `code-transformer/`: Transformer-based models for time-series forecasting
- `data/`: Preprocessed zone-level dataset
- `result/`: Output directory for experimental results


## Model Architecture Details

### 1. Last Observation (LO)
**How it works:** Predicts future values by repeating the most recent observation.

**Dataflow:**
```
Historical: [t-12, t-11, ..., t-1, t] → Prediction: t+pred_len = t
```

**Example:** If occupancy at 2:00 PM = 50 vehicles, predict 3:00 PM = 50 vehicles

**Architecture:** No training required; direct value lookup

---

### 2. ARIMA (AutoRegressive Integrated Moving Average)
**How it works:** Statistical model using past values (AR), differencing (I), and past errors (MA).

**Dataflow:**
```
Historical: [t-n, ..., t-1] → ARIMA(p,d,q) → Forecast: [t+1, t+2, ...]
```

**Components:**
- **AR(p)**: Uses p past observations (e.g., p=1 uses previous hour)
- **I(d)**: Differences data d times to remove trends
- **MA(q)**: Uses q past forecast errors

**Example:** ARIMA(1,1,1) with occupancy = [40, 45, 48]
- AR: weighs t-1 (48)
- I: considers change (48-45 = +3)
- MA: adjusts for previous prediction error
- Result: predicts ~50

---

### 3. LSTM (Long Short-Term Memory)
**How it works:** Recurrent neural network that learns temporal patterns through memory cells.

**Architecture:**
```
Input: [batch, nodes, seq] → [32, 331, 12]
  ↓
Reshape: [batch*nodes, seq, features] → [10592, 12, 3]
  ↓
LSTM: 2 layers, 16 hidden units → [10592, 12, 16]
  ↓
Flatten: [batch, nodes, seq*16] → [32, 331, 192]
  ↓
Linear Layer → [32, 331, 1]
  ↓
Output: [batch, nodes] → [32, 331] predictions
```

**Dataflow Example:**
```
Station 1068, past 12 hours: [40, 42, 45, 50, 55, 60, 58, 52, 48, 45, 43, 41]
  ↓ LSTM processes temporal sequence
Hidden states capture: morning rise → noon peak → afternoon decline
  ↓ Linear layer predicts
Next hour: 39 vehicles
```

**Key Features:**
- Processes each station independently (no spatial awareness)
- Memory cells retain long-term patterns (daily cycles)
- Handles variable-length sequences

---
