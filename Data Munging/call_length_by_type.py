#!/usr/local/bin/python3

import collections
import pandas as pd


def get_sec(timestamp):
    """
    This function receives a timestamp in HH:MM:SS format
    and returns the number of seconds
    :param timestamp: the timestamp (i.e. call duration)
    """
    call_length = timestamp.split(':')  # Split timestamp on colon
    return int(call_length[0]) * 3600 + int(call_length[1]) * 60 + int(call_length[2])

# Read CSV file into Pandas DataFrame object
df = pd.read_csv('fire_clean.csv')

# Isolate relevant columns and sort by type
df = df[['duration', 'type']]
df.sort_values(by='type')

# Create empty dict for data accumulation
durations_by_type = {}

"""
Loop through DataFrame to reset the duration for each row from
HH:MM:SS timestamp to seconds, and populate durations_by_type dict
"""
for i in df.index:
    # Reset call duration for current row to seconds
    df.loc[i, 'duration'] = get_sec(df['duration'][i])

    # Create variables for readability
    call_type = df['type'][i]
    call_duration = df['duration'][i]

    if call_type not in durations_by_type:
        durations_by_type[call_type] = {'total_duration': 0,
                                        'count': 0,
                                        'avg_duration': 0}

    """
    1. Increment number of calls for this call_type
    2. Add current duration to total_duration
    3. Update average duration, rounding to two decimal places
    """
    durations_by_type[call_type]['count'] += 1
    durations_by_type[call_type]['total_duration'] += call_duration
    durations_by_type[call_type]['avg_duration'] = round(
        durations_by_type[call_type]['total_duration'] / durations_by_type[call_type]['count']
    )

# Create OrderedDict for sorting of keys
durations_by_type = collections.OrderedDict(sorted(durations_by_type.items()))

# Print average duration for each call type
for key, value in durations_by_type.items():
    print('Average duration for call of type {0}: {1} seconds.'.format(key,
                                                                       value['avg_duration']))
