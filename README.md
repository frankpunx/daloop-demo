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
