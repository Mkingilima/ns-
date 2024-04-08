import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('device_sending_tracker.csv')

# Separate data for devices 0 and 1
df_dev0 = df[df['dev_id'] == 0]
df_dev1 = df[df['dev_id'] == 1]

# Plotting
plt.figure(figsize=(12, 6))

# Plot packet sending events for device 0
plt.scatter(df_dev0['sim_time'], df_dev0['packet'], label='Device 0 (Sending)', marker='o', color='blue')

# Plot packet receiving events for device 1
plt.scatter(df_dev1['sim_time'], df_dev1['packet'], label='Device 1 (Receiving)', marker='x', color='green')

# Set labels and title
plt.xlabel('Simulation Time (seconds)')
plt.ylabel('Packet Identifier')
plt.title('Real-time Data Sending and Receiving Events')

# Add legend
plt.legend()

# Show the plot
plt.show()
