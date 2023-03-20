import matplotlib.pyplot as plt
import pandas as pd
from prophet import Prophet
from fbprophet.plot import add_changepoints_to_plot, plot_components_plotly

# Load the CSV file
df = pd.read_csv('dates.csv', skip_blank_lines=False)
blank_df = df.loc[df.isnull().all(1)]
if len(blank_df) > 0:
    first_blank_index = blank_df.index[0]
    df = df[:first_blank_index]
#print(df.tail())

df['ds'] = pd.to_datetime(df['ds'], format='%d/%m/%Y')

m = Prophet(seasonality_mode='multiplicative', 
            seasonality_prior_scale=0.1,
            changepoint_prior_scale=0.5)
m.add_seasonality(name='daily', period=24, fourier_order=10)

m.fit(df)
    
# Generate predictions for the next 30 days
future = m.make_future_dataframe(periods=30*12, freq='D')
forecast = m.predict(future)

# Plot the forecast
fig = m.plot(forecast, xlabel='Date', ylabel='Temperature (°C)')

# Get the index of the last observed date in the original dataframe
last_date_index = df.index[-1]

# Subset the forecast dataframe to only include predicted values
forecast_subset = forecast.iloc[last_date_index:]

# Plot the predicted values with a different color
plt.plot(forecast_subset['ds'], forecast_subset['yhat'], color='red', label='Predicted', linewidth=2)

plt.legend(loc='upper left')
plt.show()



#USEFUL CODE SNIPPETS

#------------------------------------------------------------

# Change the y-axis title
#fig_yearly.update_layout(yaxis_title='Temperature (°C)')

#------------------------------------------------------------

# Plot specific components
#fig_trend = plot_forecast_component_plotly(m, forecast, 'trend')
#fig_trend.show()

#------------------------------------------------------------

# Add extra regressors
# Example: Add holiday information
# future['holiday'] = pd.Series([1 if date.month == 12 else 0 for date in future['ds']])

#------------------------------------------------------------

# Plot the forecast with changepoints
# fig = m.plot(forecast, xlabel='Date', ylabel='Temperature (°C)')
# a = add_changepoints_to_plot(fig.gca(), m, forecast)

#------------------------------------------------------------

# print the predicted values and write them to a txt file
# f = open("teste.txt", "w")
# f.write(str(forecast_subset[['ds', 'yhat']]))
# f.close()