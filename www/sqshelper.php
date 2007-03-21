<?php
require_once 'awscfg.php';
require_once 'sqs.php';

function sqsPutMessage($id, $sourceUrl, $name, $callbackUrl, $callbackPassword, $email)
{
    global $awsApiKey, $awsApiSecretKey, $awsSQSQueue, $awsSQSTimeout;

    $sqs = new SQS($awsApiKey, $awsApiSecretKey);
    if (!$sqs->createQueue($awsSQSQueue))
        return false;

    $queueUrl = parseCreateQueueResponse($sqs->responseString);
    $queueUrl = str_replace("http://queue.amazonaws.com/","",$queueUrl);

    $message = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><fb2pdfjob version=\"3\">" . 
        "<source url=\"$sourceUrl\" type=\"application/fb2+xml\" name=\"$name\"/>" .
        "<result key=\"$id.zip\" encoding=\"application/zip\"/>" .
        "<log key=\"$id.txt\"/>" .
        "<callback url=\"$callbackUrl\" method=\"POST\" params=\"pass=$callbackPassword&amp;email=$email\"/>" .
        "</fb2pdfjob>";

    if (!$sqs->putMessage(base64_encode($message), $queueUrl, $awsSQSTimeout))
        return false;

    return true;
}

$sqsProcessQueueUrl=false;
$sqsQueueUrl=null;

function parseCreateQueueResponse($response)
{
    global $sqsQueueUrl;
    
    // Initialize the XML parser
    $parser=xml_parser_create();
    xml_set_element_handler($parser,"sqs_element_start","sqs_element_end");
    xml_set_character_data_handler($parser,"sqs_element_data");    
    
    $error = false;
    if (!xml_parse($parser,$response,true))
        $error = true;
    
    xml_parser_free($parser);
    return (!$error) ? $sqsQueueUrl : null;
}
// Function to use at the start of an element
function sqs_element_start($parser,$element_name,$element_attrs)
{
    global $sqsProcessQueueUrl;
    
    if ($element_name == "QUEUEURL")
        $sqsProcessQueueUrl = true;
}

// Function to use at the end of an element
function sqs_element_end($parser,$element_name)
{
    global $sqsProcessQueueUrl;
    
    if ($element_name == "QUEUEURL")
        $sqsProcessQueueUrl = false;
}

function sqs_element_data($parser,$data)
{
    global $sqsProcessQueueUrl, $sqsQueueUrl;
    
    if ($sqsProcessQueueUrl)
        $sqsQueueUrl = $data;
}
?>