import pandas as pd
import numpy as np

# getting trade log data from the CSV file
trade_data = pd.read_csv('tradelog.csv')

initial_portfolio_value = 6500
risk_free_rate = 0.05

# Calculation of parameters
total_trades = len(trade_data)
profitable_trades = len(trade_data[trade_data['Exit Price'] > trade_data['Entry Price']])
loss_making_trades = total_trades - profitable_trades
win_rate = profitable_trades / total_trades

average_profit_per_trade = (trade_data['Exit Price'] - trade_data['Entry Price'])[trade_data['Exit Price'] > trade_data['Entry Price']].mean()
average_loss_per_trade = (trade_data['Entry Price'] - trade_data['Exit Price'])[trade_data['Exit Price'] < trade_data['Entry Price']].mean()
risk_reward_ratio = abs(average_profit_per_trade / average_loss_per_trade)
loss_rate = 1 - win_rate
expectancy = (win_rate * average_profit_per_trade) - (loss_rate * average_loss_per_trade)

#   average return per unit of volatility (average ROR)
average_return = (trade_data['Exit Price'] - trade_data['Entry Price']).mean()
volatility = (trade_data['Exit Price'] - trade_data['Entry Price']).std()
average_ror = average_return / volatility

#   Sharpe Ratio
sharpe_ratio = (average_return - risk_free_rate) / volatility

#  Max Drawdown and Max Drawdown Percentage
cumulative_returns = (trade_data['Exit Price'] - trade_data['Entry Price'] + initial_portfolio_value).cumsum()
max_drawdown = (cumulative_returns - cumulative_returns.expanding().max()).min()
max_drawdown_percentage = (max_drawdown / initial_portfolio_value) * 100

#   CAGR (Compound Annual Growth Rate)
ending_value = cumulative_returns.iloc[-1]
beginning_value = initial_portfolio_value
num_periods = len(trade_data)
cagr = (ending_value / beginning_value) ** (1 / num_periods) - 1

#   Calmar Ratio
calmar_ratio = cagr / abs(max_drawdown)

# Create a dictionary to store the results
results = {
    "Total Trades": total_trades,
    "Profitable Trades": profitable_trades,
    "Loss-Making Trades": loss_making_trades,
    "Win Rate": win_rate,
    "Average Profit per Trade": average_profit_per_trade,
    "Average Loss per Trade": average_loss_per_trade,
    "Risk Reward Ratio": risk_reward_ratio,
    "Expectancy": expectancy,
    "Average ROR per Trade": average_ror,
    "Sharpe Ratio": sharpe_ratio,
    "Max Drawdown": max_drawdown,
    "Max Drawdown Percentage": max_drawdown_percentage,
    "CAGR": cagr,
    "Calmar Ratio": calmar_ratio,
}

# converting results to a DataFrame and save to a CSV file
results_df = pd.DataFrame(results, index=[0])
results_df.to_csv('trade_results.csv', index=False)
