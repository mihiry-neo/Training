# Flight Data Analysis - Day08 - 16/06/2025

## Data Setup and Loading
### Tables and Files Used
- **Flights Data**: Main dataset with flight information (loaded as `flights_delta`)
- **Airlines Data**: Reference table with airline codes and full airline names
- **Airports Data**: CSV file containing airport codes, names, cities, and states

### Data Preparation Steps
- Combined date fields (year, month, day) with departure time to create proper datetime columns

## Data Quality Check and Cleaning
### What I Found
- Missing values in delay columns (weather delay, security delay, etc.)
- Missing tail numbers for some flights
- Missing arrival/departure times for some flights
- Some flights had incomplete time information

### How I Fixed It
- Replaced missing delay values with 0 (assuming no delay if not recorded)
- Filled missing tail numbers with "Unknown"
- Filled missing cancellation reasons with "Not Cancelled"
- Removed flights that were missing critical time data (departure time, arrival time, flight duration)

## Analysis Tasks Completed

### 1. Basic Flight Statistics
- **Delay Analysis**: Calculated average delays for each airline
- **Data Overview**: Got total row count, column information, and basic statistics

### 2. Airport and Route Analysis (Joins)
#### CVG Airport Focus
- Filtered all flights starting from CVG airport
- Added full airport names and city information for both origin and destination
- This showed where CVG connects to and with what frequency

#### Route Performance
- Calculated average delays for each route (origin-destination pair)
- Added this information back to individual flights to see how each flight compares to its route average
- Identified consistently delayed routes vs. reliable routes

#### Airport Congestion
- Measured average taxi-out time and departure delays at each origin airport
- Busier airports typically show longer taxi times and more delays
- Added this context to individual flight records

### 3. Weather Impact Analysis
- Focused on flights that had weather delays
- Calculated daily weather delay averages by airport
- Showed which airports and dates were most affected by weather

### 4. Ranking and Performance Analysis (Window Functions)
#### Airport Rankings
- Ranked airports by how many flights depart from them
- Created categories: Top 10, Top 50, Top 100, Top 150, Others
- This helps identify major vs. minor airports

#### Route Rankings
- Found the busiest flight routes by passenger volume
- Ranked routes and created similar categories
- Popular routes like major city pairs ranked highest

#### Airline Performance Rankings
- Ranked airlines by average arrival delay (best to worst punctuality)
- Used percentile rankings to group airlines into performance categories:
  - Best Performer, Top Performer, Above Average, Average, Below Average, Very Poor, Worst Performer

#### Flight-Level Rankings
- Within each airline, ranked individual flights by their departure delays
- This shows which specific flights are problematic for each carrier

#### Daily Patterns
- Found the busiest day for each airport (by flight count)
- Showed seasonal and daily variations in airport activity

#### Day-to-Day Comparisons
- Compared today's delays vs. yesterday's delays for each airport
- Tracked how delay patterns change from day to day
- Did the same analysis for specific flight numbers to see consistency

### 5. Filter, Contains, Like, Regex statements
#### Operational Filters
- **Late Night Flights**: Flights scheduled after 10 PM or before 5 AM
- **Weekend Delays**: Flights on Saturday/Sunday with delays over 30 minutes
- **Weather-Only Delays**: Flights delayed only by weather (no other delay causes)
- **Early Arrivals**: Flights that arrived 30+ minutes ahead of schedule
- **Short Flights**: Flights with less than 10 minutes of actual air time
- **Long Taxi Times**: Flights with more than 30 minutes of ground taxi time

#### Pattern Matching
- **Airport Codes**: Found airports starting with "S" or ending with "X"
- **Flight Numbers**: Located 4-digit flight numbers, palindrome numbers
- **Tail Numbers**: Aircraft registrations starting with "N" followed by digits
- **Airline Codes**: Found airlines with repeated letters (like "AA")

### 6. GroupBy, Aggregation functions
- Finding the Maximum, Minimum and Average Delay for Each Airline
- Avg Arr Delay for each Airlines
- Have used various groupBy, agg functions throughout the day

### 7. Data Transformation Techniques
#### Text Processing
- Converted airline codes to different cases (uppercase, lowercase, title case)
- Split airport codes into individual letters for detailed analysis
- Searched for specific letters within airport codes

#### Date Operations
- Calculated how many days ago flights occurred
- Added/subtracted days from flight dates
- Reformatted dates into different display formats

#### Array Operations
- Split text into arrays and worked with individual elements
- Expanded arrays into separate rows for detailed analysis
- Collected unique values across groups (like unique tail numbers per airline)

#### Cross-Tabulation
- Created pivot tables showing flight counts by airline and diversion status
- Generated monthly delay patterns for each airline
- Showed seasonal trends in airline performance

#### Categorization
- Created delay categories: "Early", "On Time", "Minor Delay", "Severe Delay"
- Based on arrival delay minutes to make data more interpretable

## Technical Skills Applied
- **Data Cleaning**: Handled missing values and data quality issues
- **Complex Joins**: Combined multiple tables in various ways
- **Window Functions**: Ranking, running totals, and comparisons across groups
- **Aggregations**: Calculated averages, counts, and statistical measures
- **Pattern Matching**: Used various text matching techniques
- **Time Series Analysis**: Tracked changes over time
- **Data Transformation**: Converted and restructured data for analysis
- **Statistical Analysis**: Percentile rankings and performance categorization

## Data Quality Improvements
- Started with raw flight data containing inconsistencies
- Ended with clean, enriched dataset ready for reporting
- Added meaningful categories and rankings for business interpretation
- Created reusable patterns for ongoing analysis