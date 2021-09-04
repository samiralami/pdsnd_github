import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ["chicago", "new york city", "washington" ]
MONTHS =  ["all", "january", "february", "march", "april", "may", "june", "july",
           "ausust", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday","all"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    valid_city, valid_month, valid_day = False, False, False

    print('Hello! Let\'s explore some US bikeshare data!!!!!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        while not valid_city:
            try:
                city = (input("enter a city to explore: (chicago, new york city, washington)")).lower().replace(" ","")
                if city == "newyorkcity":
                    city = CITIES[1]
                if city in CITIES:
                    valid_city = True
                    continue
                else:
                    print("enter a city chicago, new york city or washington ")
            except ValueError:
                print("enter a valid city name")


    # get user input for month (all, january, february, ... , june)
        while not valid_month:
            try:
                month = (input("enter a month to explore: (all, january, february, ...)")).lower().strip(' ')
                if month in MONTHS:
                    valid_month = True
                    continue
                else:
                    print("enter a valid months ")
            except ValueError:
                print("enter a valid month name")

    # get user input for day of week (all, monday, tuesday, ... sunday)
        while not valid_day:
            try:
                day = (input("enter a day to explore: (all, monday, tuesday, ...)")).lower().strip(' ')
                if day in DAYS:
                    valid_day = True
                    break
                else:
                    print("enter a valid day ")
            except ValueError:
                print("enter a valid day name")

        if valid_city and valid_month and valid_day:
            break

    print('-'*40)
    print ("your selected:", city, ", ", month, ", ", day)
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
    months_dict = {
        "january" : 1,
        "february" : 2,
        "march" : 3,
        "april" : 4,
        "may" : 5,
        "june" : 6,
        "july" : 7,
        "august" : 8,
        "september" : 9,
        "october" : 10,
        "november" : 11,
        "december" : 12
    }
    days_dict = {
        "monday" : 0,
        "tuesday" : 1,
        "wednesday" : 2,
        "thursday" : 3,
        "friday" : 4,
        "saturday" :5,
        "sunday" : 6,
    }

    all = "all"

    df = pd.read_csv(CITY_DATA[city])

    print("data loaded")

    # replace NaN values with the previous value in the column
    df.fillna(method = 'ffill', axis = 0,inplace=True)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    if (month != all and day != all):
        selection = (df['Start Time'].dt.dayofweek == days_dict[day]) & (df['Start Time'].dt.month == months_dict[month])
        df = df.loc[selection]
    else:
        if (month == all and day != all):
            selection = (df['Start Time'].dt.dayofweek == days_dict[day])
            df = df.loc[selection]
        else:
            if (day == all and month != all):
                selection = (df['Start Time'].dt.month == months_dict[month])
                df = df.loc[selection]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    if (df.month.mode().count()):
        print("\nMost common month : ", MONTHS[df.month.mode().iat[0]] )
    else:
         print("\nMost common month does not exit for selected period " )

    # display the most common day of week
    if (df.day.mode().count()):
        print("\nMost common day : ", DAYS[ df.day.mode().iat[0] ] )
    else:
        print("\nMost common day does not exit in selected period " )

    # display the most common start hour
    if(df.hour.mode().count()):
        print("\nMost common start hour : ", df.hour.mode().iat[0], "hrs" )
    else:
        print("\nMost common start hour does not exit in selected period " )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    if ( df['Start Station'].mode().count()):
        print("\nMost common used Start Station : ", df['Start Station'].mode().iat[0] )
    else:
        print("\nNo data for most common used Start Station : " )

    # display most commonly used end station
    if (df['End Station'].mode().count()):
        print("\nMost common used End Station : ", df['End Station'].mode().iat[0] )
    else:
         print("\nNo data for most common used End Station : " )
    # display most frequent combination of start station and end station trip
    print("\nMost common combo Start/End Station : ")

    output = df.groupby(['Start Station','End Station']) \
                             .size() \
                             .reset_index(name='count') \
                             .sort_values(['count'], ascending=False)  \
                             .head(1)
    print( output)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("\nTotal travel time = ",df['Trip Duration'].sum())


    # display mean travel time
    print("\nMean travel time = ",df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if ('User Type' in df.columns):
        print("\nThere are", df.groupby(['User Type'])['User Type'].size().count()," User Types")
    else:
        print("\nNo User Type data available")

    # Display counts of gender
    if ('Gender' in df.columns):
         print("\nGender count : \n", df.groupby(['Gender'])['Gender'].count())
    else:
         print("\nNo Gender data available")

    # Display earliest, most recent, and most common year of birth
    if ('Birth Year' in df.columns):
        print("\nEarliest year of birth: ", df['Birth Year'].min())
        print("\nMost common year of birth: ", df['Birth Year'].mode().iloc[0])
        print("\nMost resent year of birth: ", df['Birth Year'][(df['Start Time'].idxmax())])
    else:
        print("\nNo Birth Year data available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data to users."""

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    view_data = view_data.lower()
    start_loc = 0
    while view_data == "yes":
        print(df.iloc[start_loc])
        start_loc += 5
        view_display = input("Do you wish to continue?: “)
        view_data = view_data.lower()
    return

def main():
    try:
        while True:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            if(not df.empty):
                time_stats(df)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)
                display_raw_data(df)
            else:
                print("\nNo data available for this period")

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
    except KeyboardInterrupt:
        print("\ngood bye")
if __name__ == "__main__":
	main()
