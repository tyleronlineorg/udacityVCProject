import time
import pandas as pd
import numpy as np

#global lists to check inputs and use in methods
CITY_DATA = { 'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv' }
monthsList = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
daysList = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    ui = ''#user input placeholder
    while (ui not in CITY_DATA):
        print("Would you like to look at Chicago, New York City, or Washington")
        ui = input().lower() #only stores lowercase string that is in CITY_DATA list
        if (ui not in CITY_DATA):
            print("Input not accepted")
    city = ui
    
    while ui not in monthsList[:7]:
        print("Choose a Month; January, February, March, April, May, June, or All")
        ui = input().strip().lower() #only stores lowercase string that is in monthsList
        if (ui not in monthsList):
            print("Input not accepted")
    month = ui
    ui = '' #reset ui incase all was selected last time

    while (ui not in daysList):
        print("Choose a day of the week; Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All")
        ui = input().strip().lower() #only stores lowercase string that is in daysList
        if (ui not in daysList):
            print("Input not accepted")
    day = ui
          
    print('-'*40)
    print("Looking at data from: \n City = {} \n Month = {} \n Day = {}".format(city.title(), month.title(), day.title()))
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
    df = pd.read_csv(CITY_DATA[city.lower()]) #reads csv for the city chosen by user
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    if month != 'all': #if user selected a month, set df to just that month
        monthInt = monthsList.index(month) + 1
        df = df[df['month'] == monthInt]

    if day!= 'all': #if user selected a day, set df to just that day
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    mcm = df['month'].mode()[0]#finds most common month, takes first if there is a tie
    print(f"Most Common Month: {monthsList[mcm - 1].title()}")

    mcd = df['day_of_week'].mode()[0]#takes first item returned from mode()
    print(f"Most Common Day: {mcd}")

    mch = df['Start Time'].dt.hour.mode()[0]
    print(f"Most Common Start Hour: {mch}:00")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print(f"Most used Start Station is {df['Start Station'].mode()[0]}")

    print(f"Most used End Station is {df['End Station'].mode()[0]}")

    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"Most common trip: {most_common_trip[0]} → {most_common_trip[1]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    totalDuration = df['Trip Duration'].sum()
    days = totalDuration //86400 #floor of duration / seconds in day
    hours = (totalDuration%86400)//3600 #floor of duration minus full days / seconds in hour
    minutes = (totalDuration%3600)//60  #floor of duration minus full days and hours / seconds in minute
    seconds = totalDuration%60
    print("Total travel time is {} day(s) {} hour(s), {} minute(s), and {} second(s)." .format(days,hours, minutes, seconds))

    avgDuration = df['Trip Duration'].mean()
    avgMins = avgDuration // 60
    avgSec = avgDuration % 60
    print("Average travel time is {} minutes and {} seconds" .format(avgMins, avgSec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type_counts = df['User Type'].value_counts()
    print("Counts of User Types:")
    print(user_type_counts.to_string())

    if 'Gender' in df.columns: #check for gender data before attempting to count
        gender_counts = df['Gender'].value_counts()
        print("Counts of each gender:")
        print(gender_counts.to_string())
    else:
        print("No gender data available for this city.")

    if 'Birth Year' in df.columns:
        print("\nBirth Year Stats:")
        print(f"Earliest Birth Year: {int(df['Birth Year'].min())}")
        print(f"Most Recent Birth Year: {int(df['Birth Year'].max())}")
        print(f"Most Common Birth Year: {int(df['Birth Year'].mode()[0])}")
    else:
        print("\nNo birth year data available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df.empty: #if df is empty, offer to restart, don't run any methods
            print("\nNo data available for the selected filters. Please try different filters.")
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        row = 0
        showData = ''
        while showData != 'no' and showData != 'yes':
            showData = input("\nWould you like to see 5 rows of raw data? Enter yes or no: ").lower()
        while showData == 'yes':
               print(df.iloc[row: row + 5])  # Show next 5 rows
               print('-'*40)
               row += 5
               if row >= len(df):
                    print("No more raw data to display.")
                    break
               showData = input("\nWould you like to see 5 more rows of raw data? Enter yes or no: ").lower()
                  
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = ''
        while restart != 'yes' and restart != 'no':
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()

