import time
import datetime
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington']

months = ['all', 'jan', 'feb', 'mar', 'apr', 'may', 'jun']

day_of_week = ['all', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    name = input('Please enter your name: ').title()
    print('Hello {}! Let\'s explore some US bikeshare data!'.format(name))
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to ha

    while True:
        city = input('Would you like to see data for Chicago, New York City or Washington? ').lower()
        if city not in cities:
            print('You can only review data for Chicago, New York City or Washington. \nPlease try again!')
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month would you like to see? \nPlease input Jan, Feb, Mar, Apr, May, Jun or all to see all months. ').lower()
        if month not in months:
            print('That is not a valid entry. Please try again')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input('Which day of the week would you like to see? Mon, Tue, Wed, Thu, Fri, Sat, Sun or all for all days. ').lower()
        if day not in day_of_week:
            print('That is not a valid entry. Please try again. ')
        else:
            break

    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns. use abbr days mon tue etc
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%a')

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding in
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month and create dict to convert month number to month
    common_month = df['month'].mode()[0]
    months = {  1: 'January',
                2: 'February',
                3: 'March',
                4: 'April',
                5: 'May',
                6: 'June'}
    print('Most Popular Month:', months[common_month])


    # display the most common day of week

    common_day = df['day_of_week'].mode()[0]
    print('Most Popular Day of Week:', common_day)


    # display the most common start hour


    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nFinding The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular station to start from is:\n ',popular_start_station)

    # find 5 most popular start stations
    print('\nThe 5 Most Popular Start Stations are: \n{}\n'.format(df['Start Station'].value_counts().head(5)))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular station to finish at is:\n ',popular_end_station)

    # find 5 most popular end stations
    print('\nThe 5 Most Popular End Stations are: \n{}\n'.format(df['End Station'].value_counts().head(5)))

    # display most frequent combination of start station and end station trip
    combination = (df['Start Station'] + df['End Station']).mode()[0]
    print('The most combination of start station and end station trip is\n {}'.format(combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time = df['Trip Duration'].sum()
    time_convert = datetime.timedelta(seconds = int(total_travel_time))
    print('Total travel time is: \n', time_convert)

    # display mean travel time

    mean_travel_time = df['Trip Duration'].mean()
    mean_convert = datetime.timedelta(seconds = int(mean_travel_time))
    print('Average travel time is :\n', mean_convert)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types: \n{}\n'.format(df['User Type'].value_counts()))

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Counts of users by gender: \n{}\n'.format(df['Gender'].value_counts()))
    else:
        print('There is no gender data for your selection.')

    # Display earliest, most recent, and most common year of birth
    if 'Gender' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode([0]))
        print('Birth Year Data: ')
        print('Earliest Year: ', earliest_year)
        print('Most Recent Year: ', most_recent)
        print('Most Common Year: ', most_common)
    else:
        print('There is no birth date data for your selection')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data_limit(df):
    trip_data = input('\nDo you want to see 5 rows of individual trip data? \n').lower()
    start_loc = 0
    while True:
        if trip_data in ('yes', 'y'):
            print('\nShowing individual trip data:\n')
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            trip_data = input('\nDo you wish to see 5 more rows?:\n ').lower()
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_limit(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
