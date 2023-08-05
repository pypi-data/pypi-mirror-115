PerfectoAI is an automated emailable analytics tool along with AI graphs & predictions specially designed for Perfecto's Smart Reports. Kindly reach out to Perfecto's Professional Services if interested.</br>
[![Downloads](https://pepy.tech/badge/perfectoai)](https://pepy.tech/project/perfectoai)

CHANGES
=======

1.0.34:
-------
- Support for Epoch time in ms for startDate and endDate parameters. This allows the ability to query results as accurate to two different timestamp with milliseconds
- Manual Interactive session results will no longer be included under top failed tests and top recommendations
- JobName and Job Number will now be empty if not applicable in failures html
- Important fix to handle multiple repetitive special characters in Smart Reporting's failure message
- Summary Report hyperlinks will now reach to applicable Smart Reporting urls when jobs=All Jobs
- Failure html files are renamed like unique_failures.html as they contain details of unique failures only
- All table layouts will follow responsive design even when test names or failures are very huge

1.0.32:
-------

- Clicking on header logo will navigate to perfecto cloud website
- Removed unnecessary logs, packages & non relevant code to improve speed by 20%
- Graphs have meaningful headings
- Deprecating tags of -e parameter and replaced it with addInfo to make it more meaningful
- Appending " -d true" parameter to your existing query will now enable downloading of .txt files and extra console statements
- Appending "|ci=false" to -e parameter will automatically open report post execution. It will not be opened automatically by default in order to provide a seamless devops experience.
