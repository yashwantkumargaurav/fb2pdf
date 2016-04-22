Since PDF generation from FB2 is CPU intensive process we are designed it to use distributed processing architecture, with multiple backend computers doing conversion.

## Processing Flow ##

  1. Web UI accepts task from user. FB2 file is uploaded either via form or URL
  1. Web UI uploads file to Amazon S3 storage. Additionally it creates on S3 placehoolder key (filename) for results.
  1. Web UI adds taks to Amazong Simple Queue with small XML task (see test/sample\_message.xml in SVN). Thask specify URL on S3 with FB4 file and S3 key where to put results.
  1. The page is shown to user, saying that his task is being processed, please wait. Page auto-reloads every 10 seconds. User can also bookmark it and check later or reload manually. On each reload page checks key file on S3, extacts metadata and check is it has 'status=done' filed. It if does, message is shown to user that processing is finished and he is given download link. In status is 'error' user is informed that processing failed and given a chance to send bug report to developers, which will contain link to log file.
  1. Multiple conversion workers are periodically checking amazong queue for new events. Once event is received one of them picks it up, download and process file. If processing was successful, result is uploaded to S3 using key provided in task and in meta information for this key status field is set to 'done'. In case of non-recoverable error (e.g. TeX syntax error), log file is uploaded to this key and status is set to 'error'.
  1. After file conversion backend optionally calls back URL provided in XML task file. This URL current updates book status in DB.

## Notes ##

  * Even if user uploads file via specifying URL we always cache it copy on S3 to ensure it is avaliable later when processing would happen
  * Resulting files (along with FB2) are stored on S3 permanently
  * We also have implemented smart checking (comparing MD5 of newly requested conversion source with once we already had connected and return results immediately if they are already avialiable on S3).
  * Log files are also uploaded to S3. This would allow developers later to have both Fb4 and log file to debug conversion bugs.