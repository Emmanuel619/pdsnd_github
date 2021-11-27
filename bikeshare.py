import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    #city = input('Please enter the City  ')
    city_name = ''
    while city_name.lower() not in ['chicago','washington','new york city']:
        city_name = input("\nWhich of the cities(chicago, washington, new york city) do you want analyze data?  ")
        if city_name.lower() in ['chicago','washington','new york city']:
            city = city_name.lower()
            print('Alright! Let\'s explore data from {}'.format(city_name))
        else:
            print("Sorry you entered an invalid city. Please input either chicago, washington or new york city.")

    # get user input for month (all, january, february, ... , june)
    month_name = ''
    while month_name.lower() not in MONTH_DATA:
        month_name = input("\nWhich month(all, january, february, ... , june) would you like to filter data for? \n")
        if month_name.lower() in MONTH_DATA:
            month = month_name.lower()
            if month == 'all':
                print('Great! No filter will be applied to the months')
            print('GOTCHA! Data will be filtered to obtain results for {}'.format(month))
        else:
            print("Sorry you entered an invalid month. Please input either january, february, ... , june.\n")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_name = ''
    while day_name.lower() not in ['all', 'monday', 'tuesday', 'wednesday', 'friday', 'saturday', 'sunday']:
        day_name = input("\nWhich day(all, monday, tuesday, ... sunday) would you like to filter data for? \n")
        if day_name.lower() in ['all', 'monday', 'tuesday', 'wednesday', 'friday', 'saturday', 'sunday']:
            day = day_name.lower()
            if day == 'all':
                print('Great! No filter will be applied to the day')
            print('GOTCHA! filter will be applied to obtain results for {}'.format(day))
        else:
            print("Sorry you entered an invalid day. Please input either monday, tuesday, ... sunday.\n")

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
    df = pd.read_csv(CITY_DATA[city])
    df.dropna(axis = 0, inplace = True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df.insert(3, 'Month', df['Start Time'].dt.month)
    df.insert(4, 'Day', df['Start Time'].dt.day_name())
    df.insert(5, 'Hour', df['Start Time'].dt.hour)
    if month != 'all':
        month = MONTH_DATA.index(month)
        df = df.loc[df['Month'] == month]
    if day != 'all':
        df = df.loc[df['Day'] == day.title()]
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        common_month = df['Month'].mode()[0]
        print('The most common month is: {}'.format(common_month))

    # display the most common day of week
    if day == 'all':
        print('The most common day of the week is: ' + df['Day'].mode()[0])

    # display the most common start hour
    print('The most common start hour is: ' + str(df['Hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most commonly used end station is: {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print('The most frequent combination of start and end station used is: {}'.format((df['Start Station'] + "||" + df['End Station']).mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The most total travel time is: {}'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('the mean travel time is: {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The count by user type is: {}'.format(df['User Type'].value_counts()))

    # Display counts of gender
    if city == 'chicago' or city == 'new york city':
        print('Number of users by gender: {}'.format(df['Gender'].value_counts()))

    # Display earliest, most recent, and most common year of birth
        print('Earliest birth  is: {}'.format(df['Birth Year'].min()))
        print('Most recent birth is: {}'.format(df['Birth Year'].max()))
        print('Most common birth is: {}'.format(df['Birth Year'].mode()[0]) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays raw data on user request.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print(df.head())
    next = 0
    while True:
        view_raw_data = input('\nWould you like to view next five row of raw data? Enter yes or no.\n')
        if view_raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        while True:
            view_raw_data = input('\nWould you like to view first five row of raw data? Enter yes or no.\n')
            if view_raw_data.lower() != 'yes':
                break
            display_raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
