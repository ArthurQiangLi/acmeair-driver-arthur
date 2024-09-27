import time

# Mock-up values for the example, replace with actual values
total_duration = 5  # Total duration in seconds
collection_end_time = time.time() + total_duration  # End time for collection

# Loop to simulate your data collection with a progress bar
while time.time() < collection_end_time:
    # Replace this with your actual function call
    # ok, res = sdclient.get_data(metrics, start, end, sampling, filter=filter)

    # Calculate elapsed time and remaining time
    elapsed_time = int(time.time() - (collection_end_time - total_duration))
    remaining_time = total_duration - elapsed_time

    # Create a simple progress bar string
    progress_bar = '━' * (elapsed_time) + ' ' * (remaining_time)
    
    # Display the progress bar with elapsed time in seconds
    print(f"\r{progress_bar} [{elapsed_time}/{total_duration}sec]", end='') # [end=''] make it flush before print

    time.sleep(1)  # Wait for the next sampling interval, replace with your sampling rate

print("\nData collection complete.")



# Advanced version
# import time
# import sys

# # Simulating the existing variables
# collection_end_time = time.time() + 60  # For example, run for 60 seconds
# sampling = 1  # Default sampling interval in seconds

# # Calculate the total duration in seconds
# total_duration = int(collection_end_time - time.time())

# # Start the loop and implement the progress bar
# while time.time() < collection_end_time:
#     # Simulate your data collection step
#     ok, res = True, {}  # Placeholder for your sdclient.get_data(metrics, start, end, sampling, filter=filter)

#     # Calculate elapsed time and remaining time
#     elapsed_time = int(time.time() - (collection_end_time - total_duration))
#     remaining_time = total_duration - elapsed_time

#     # Create the progress bar
#     progress_length = 40  # Length of the progress bar
#     filled_length = int(progress_length * elapsed_time // total_duration)
#     bar = '━' * filled_length + ' ' * (progress_length - filled_length)

#     # Print the progress bar in a single line, updating in place
#     sys.stdout.write(f'\r[{bar}] [{elapsed_time}/{total_duration}sec]')
#     sys.stdout.flush()

#     time.sleep(sampling)  # Wait for the next sampling interval

# print("\nData collection complete.")
