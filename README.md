
# Finance Toolkit

`finance_toolkit` is a Python library designed to provide essential financial tools for analyzing financial instruments. It includes functions to calculate key metrics such as beta, Sharpe ratio, maximum drawdown, and more.

## Features

- **Beta**: Measures an asset's sensitivity to market movements.
- **Theta**: Calculates the average return of a financial instrument over a specified period.
- **Sigma**: Calculates the average volatility of a financial instrument over a specified period.
- **Max Drawdown**: Measures the largest loss from a peak to a trough in a financial instrument's historical performance.
- **Jensen Alpha**: Measures an asset's performance relative to the market, adjusted for risk.
- **Alpha**: Measures an asset's performance relative to the market.
- **Sharpe Ratio**: Evaluates the risk-adjusted return of a financial instrument.
- **Calmar Ratio**: Evaluates the risk-adjusted return using maximum drawdown as the measure of risk.
- **Indexing**: Calculates indexed values based on percentage changes in input data.
- **Historical VaR**: Calculates Value at Risk (VaR) based on historical performance.
- **Momentum**: Calculates the momentum of a time series over a specified period.

## Installation

To install `finance_toolkit`, you can use pip:

```bash
pip install git+https://github.com/votre_utilisateur/finance_toolkit.git
```

## Usage

Here is an example of how to use some of the library's functions:

```python
import pandas as pd
import numpy as np
from finance_toolkit import beta, theta, sigma, max_drawdown, sharpe_ratio

# Sample data
asset_returns = pd.Series([0.01, -0.02, 0.03, 0.04, -0.01])
market_returns = pd.Series([0.02, -0.01, 0.03, 0.02, -0.02])

# Calculate beta
beta_value = beta(asset=asset_returns, market=market_returns)
print(f"Beta: {beta_value}")

# Calculate average return
average_return = theta(history=asset_returns)
print(f"Average Return: {average_return}")

# Calculate volatility
volatility = sigma(history=asset_returns)
print(f"Volatility: {volatility}")

# Calculate maximum drawdown
max_dd = max_drawdown(history=asset_returns)
print(f"Max Drawdown: {max_dd}")

# Calculate Sharpe ratio
risk_free_rate = 0.01
sharpe = sharpe_ratio(history=asset_returns, risk_free=risk_free_rate)
print(f"Sharpe Ratio: {sharpe}")
```

## Contributing

Contributions are welcome! If you would like to contribute to `finance_toolkit`, please follow these steps:

1. Fork the repository.
2. Create a branch for your feature (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or suggestions, please contact [votre_email@example.com](mailto:votre_email@example.com).
