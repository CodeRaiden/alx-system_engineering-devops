# 0x19 Postmortem - WordPress Failure (incident #47)

:fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire:
![My first postmortem](https://www.google.com/url?sa=i&url=https%3A%2F%2Fpandorafms.com%2Fblog%2Fpost-mortem-incident%2F&psig=AOvVaw21t8OefJXvjOSHZEbaGONM&ust=1675637343336000&source=images&cd=vfe&ved=0CBAQjRxqFwoTCODP7tf5_PwCFQAAAAAdAAAAABAJ) 
:fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire:

## Date and Duration of Outage

2023-02-4 / 5:00 PM - 6:15 PM

## Authors

* samie

## Status

Resolved, action items in progress

## Summary

Our very popular and very useful site "Checker" which helps to indicate if other sites are down, went down. A 500 Internal Server Error disabled access for our users for about an hour while the issue was resolved. The irony was broadcast on Twitter in similar form and tone to the following one. An hour of server debugging led to a resolution.

### Impact

100% of users experienced inaccessibility to our site in the form of a 500 Internal Server Error.
The whole user-facing site was unable to be reached. Estimated 570M queries
lost, $1.5B of ad revenue foregone or requested back by companies whose ads could not be seen due to the massive downtime.

### Root Cause

500 Internal Server Error coming from PHP section of LAMP
(Linux Apache MySQL PHP) stack. Settings file contained a typo
which caused a **File Not Found** error on the PHP backend. It
was difficult to detect from the apache server because Apache lacks the alerting capabilities to signal issues with the content it was serving.

## Trigger

A call to the server would trigger it due to the fact that PHP is
halted by the error whenever it attempted to run.

## Resolution

The error was resolved by a correction to the typo. But the
debugging process however, took the better part of an hour. A 500 error
means anything can be wrong with the server including the files and databases
it pulls from. And so, the first step was to the check the apache logs.
Apache only showed being started and stopped which is normal also indicating
that apache is writing to the logs in fact. Next, MySQL was checked. Databases
can go down and cause issues. No issue were found in the
MySQL logs either. Therefore, the problem was expected to be in the PHP code.
To debug PHP the debug mode for the PHP config was turned on. This changed the
server's response from 500 to 200. So, we would expect the problem is fixed, right? well... Not! The server returned 200, but this was not because it was serving content. It was rather serving something else. The good news is it served us the error in the PHP files. It was a typo. On line 124 of the `wp-settings.php` file, a require directive was referencing `class-wp-locale.phpp`. This file did not exist. Why was this? Its extension was wrong. All PHP files have a `.php` extension.
`.phpp` is a silly oversight in typing the correct file name. Once the typo
was resolved the whole server was serving the correct website content.

## Detection

Anderson experienced a 500 Internal Server error when trying to access our site
for his own personal inquiry into the status of another site.

## Corrective and Preventative Action Items

| Action Item | Type | Owner | Bug |
| ----------- | ---- | ----- | --- |
| Setup automatic testing through Travis CI in github | mitigate | jennifer | n/a **DONE** |
| Develop code review framework which includes local test | prevent | martym | Bug 5554823 **TODO** |
| Develop dummy site for 500 Internal Server redirect, potentially using other website status apis for info rather than ours | alternative action | docbrown | n/a **TODO** |
| Use development site for real testing prior to production deployment| prevent | jennifer | Bug 5554824 **TODO** |
| Facilitate communication between SRE and backend departments for more robust development | prevent | agoogler | Bug 5554825 **DONE** |
| Deploy updated wordpress site to prod | prevent | jennifer | n/a **DONE** |
| Develop monitoring and detection tools for quicker detection of issue | mitigate | SRE Team | n/a **TODO** |

## Lessons Learned

* Never push untested or poorly tested code into production no matter how small the change

### What went well

* Debugging techniques were on point and used well and aided with development skills
* Production fix was fast

### What went wrong

* Debugging took too long
* Detection of the problem should have been much quicker

### Where we got lucky

* Twitter was a quick means of getting feedback from our users and someone was scrolling twitter instead of working

## Timeline

2023-02-4 (*all times PST*)

| Time  | Description |
| ----- | ----------- |
| 16:51 | Team comes back from happy hour at "Mr. YouWatzItz" on Canal |
| 16:53 | Team pushed code after a few modifications and code reviews |
| 16:54 | **OUTAGE BEGINS** -- Server is serving 500 Internal Server Error |
| 16:55 | docbrown receives pager storm, `ManyHttp500s` from all clusters |
| 16:57 | Checker is no longer informing users of site statuses because it is itself down |
| 16:58 | docbrown starts investigating, finds server error is indeed what the user sees |
| 17:01 | **INCIDENT BEGINS** docbrown declares incident #47 |
| 17:02 | someone coincidentally tweets at us about the irony of our situation |
| 17:06 | docbrown investigates apache logs |
| 17:07 | docbrown investigates mysql logs |
| 17:10 | martym investigates php in debug mode |
| 17:18 | clarac finds file where error is originating from |
| 17:20 | martym fixes typo in file |
| 17:35 | Production push of code and server succeeds after error fix |
| 17:36 | **OUTAGE MITIGATED**, Serving accurate webpage to all user-facing pages now |
| 17:55 | Conducted final check on stability of server and determined it is ok to be allowed to go |
| 18:00 | **OUTAGE ENDS**, all traffic balanced across all clusters |
| 18:15 | **INCIDENT ENDS**, reached exit criterion of 30 minutes nominal performance |
