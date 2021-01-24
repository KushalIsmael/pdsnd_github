import time
import pandas as pd
import numpy as np

city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Check that city input is one of the possible options
    while True:
        try:
            city = input('Type the name of the city you would like to analyze:').lower()
            city not in city_data[city]
        except:
            print("This is not a valid city, please try one of the following cities: washington, chicago, or new york city\n")
        else:
            print("Looks like you would like to explore bikeshare data for: ",city)
            break

    # Check that month input is one of the possible options
    months_options = ['all','january','february','march','april','may','june']
    month = input('Type the name of the month you would like analyze or type all for all months:').lower()
    while month not in months_options:
        print('This is not a valid month, please type one of the following months: january, february, march, april, may, june, or all\n')
        month = input('Type the name of the month you would like analyze or type all for all months: ').lower()
    else:
        if month == 'all':
            print('Looks like you would like to explore bikeshare data for all months')
        else:
            print('Looks like you would like to explore bikeshare data for the month of ',month)
    #Check that day input is one of possible options
    days_options = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day = input('Type the day of the week you would like to anaylze:').lower()

    while day not in days_options:
        print('This is not a valid day, please type another day or write all for all days\n')
        day = input('Type the day of the week you would like to anaylze:').lower()
    else:
        if day == 'all':
            print('Looks like you would like to explore bikeshare data for all days')
        else:
            print('Looks like you would like to explore bike share data for ', day)
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
    #Read in data for city
    df = pd.read_csv(city_data[city])
    #Rename blank column
    df = df.rename(columns={'Unnamed: 0':'Trip ID'})
    #Convert start time to datetime type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #Create column for month name
    df['Start Month'] = df['Start Time'].dt.month_name().str.lower()
    #Create column for day name
    df['Start Day'] = df['Start Time'].dt.day_name().str.lower()
    #Filter city data based on month input
    if month == 'all':
        pass
    else:
        df = df.loc[df['Start Month'] == month]

    #filter data based on day input
    if day == 'all':
        pass
    else:
        df = df.loc[df['Start Day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Display the most common month
    common_month = df['Start Month'].mode()[0]
    print("The most common month is: ", common_month)
    #Display the most common start week day
    common_day = df['Start Day'].mode()[0]
    print("The most common day is: ", common_day)

    #Display the most common start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    print("The most common hour is: ", common_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Display most common start station
    common_start = df['Start Station'].mode()[0]
    print('The most common start station is: ', common_start)

    #Display most common end station
    common_end = df['End Station'].mode()[0]
    print('The most common end station is: ', common_end)

    #Create new column that combines start and end station
    df['Station Combo'] = df['Start Station'] + ' to ' + df['End Station']
    #Display most common start and end station combination
    common_combo = df['Station Combo'].mode()[0]
    print('The most frequent station to station trip is: ', common_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Convert total travel time
    total_time = df['Trip Duration'].sum()
    total_hours = int(total_time//3600)
    total_minutes = int((total_time//60) - (total_hours*60))
    total_seconds = int(total_time - ((total_minutes*60)+(total_hours*3600)))
    print('The total trip travel time is: ', total_hours, ' hours, ', total_minutes, ' minutes, and ', total_seconds, 'seconds')

    #Convert mean travel time
    mean_time = df['Trip Duration'].mean()
    mean_hours = int(mean_time//3600)
    mean_minutes = int((mean_time//60) - (mean_hours*60))
    mean_seconds = int(mean_time - ((mean_minutes*60)+(mean_hours*3600)))
    print('The mean travel time is:', mean_hours, 'hours, ', mean_minutes, 'minutes, and ', mean_seconds, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    print('The counts for each user type are:\n',df.groupby('User Type').size().to_string(header=None),'\n')

    #Display counts by gender if data available
    if 'Gender' not in df.columns:
        print('There is no gender information availabe in the data set.\n')
    else:
        df['Count'] = 1
        gender = df.groupby('Gender').count()
        print('The counts for each gender are:\n',gender['Count'].to_string(header=None),'\n')


    #Display max, min, and most common birth year if data available
    if 'Birth Year' not in df.columns:
        print('There is no birth year information available in this data set.\n')
    else:
        earliest_birth = int(df['Birth Year'].min())
        recent_birth = int(df['Birth Year'].max())
        common_birth = int(df['Birth Year'].mode())
        print('The earliest birth year is: ',earliest_birth,'\nThe most recent birth year is: ',recent_birth,'\nThe most common birth year is: ',common_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Display 5 lines of data until user inputs no"""
    #Ask user if they want to see the individual trip data
    view_data = str(input('\nWould you like to view 5 rows of individual trip data?\n')).lower()
    #Set the start location to 6 to show the first 5 rows of data
    start_loc = 6
    #Remove columns created in analysis
    df = df.drop(columns = ['Station Combo','Count'])
    #Show the first 5 rows of data and ask the user if they would like to see 5 more rows.
    while view_data == 'yes':
        print("\nHere is the individual bikeshare data:")
        print(df.iloc[0:start_loc])
        more_data = str(input('\nWould you like to see the following 5 rows of data?\n')).lower()
        if more_data == 'yes':
            start_loc += 5
            print(print(df.iloc[0:start_loc]))
            print(more_data)
        else:
            print('\nOkay, you can always view more data later by restarting the program.')
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
