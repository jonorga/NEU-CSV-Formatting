# NEU-CSV-Formatting
Overview: Creates a formatted file for each raw data file as well as an aggregate

General operation of this Python file:
1. Scan local directory and collect all file names that match naming convention for raw data files
2. Each raw data file gets:
    * Scanned for all needed values/metrics
    * A new outputted file with the values/metrics neatly formatted
    * Their values temporarily stored to be added to the aggregate file
3. Create aggregate file with data from all raw data files
4. Output message to the console indiciating:
    * how many files found, read, and formatted. 
    * which files found, read, and formatted. 
