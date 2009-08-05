<?php
require_once 'awscfg.php';
require_once 'sqs.client.php';
require_once 'utils.php';

function sqsPutMessage($id, $sourceUrl, $name, $callbackUrl, $callbackPassword, $email, $format, $formatParams)
{
    global $awsApiKey, $awsApiSecretKey, $awsSQSQueue, $awsSQSTimeout;

    $sqs = new SQSClient($awsApiKey, $awsApiSecretKey, 'http://queue.amazonaws.com');
    
	try
    {
        // Create the queue.  TODO: If the queue has recently been deleted, the application needs to wait for 60 seconds before
        $sqs->CreateQueue($awsSQSQueue);

        $zipName = getStorageName($id, $format, ".zip");
        $logName = getStorageName($id, $format, ".txt");
            
        // Send a message to the queue
        $message = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><fb2pdfjob version=\"3\">" . 
            "<source url=\"$sourceUrl\" type=\"application/fb2+xml\" name=\"$name\"/>" .
            "<result key=\"$id\" encoding=\"application/zip\" name=\"$zipName\"/>" .
            "<log key=\"$logName\"/>" .
   	    "<callback url=\"$callbackUrl\" method=\"POST\" params=\"pass=$callbackPassword&amp;email=$email&amp;format=$format\"/>";
            foreach(array_keys($formatParams) as $name)
            {
                $value = $formatParams[$name];
                $message .= "<parameter name=\"$name\" value=\"$value\"/>";
	    }
            $message .= "</fb2pdfjob>";

        $sqs->SendMessage(base64_encode($message));
    }
    catch(Exception $e)
    {
        $err_str = $e->getMessage();
        error_log("FB2PDF ERROR. sqshelper: " . $err_str); 
        return false;
    }
    
    return true;
}
?>