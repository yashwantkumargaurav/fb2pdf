<?php
require_once 'awscfg.php';
require_once 'sqs.php';

function sqsPutMessage($id, $url, $name)
{
global $awsApiKey, $awsApiSecretKey, $awsSQSQueue, $awsSQSTimeout;

$sqs = new SQS($awsApiKey, $awsApiSecretKey);
if (!$sqs->createQueue($awsSQSQueue))
    return false;

$queueUrl = parseCreateQueueResponse($sqs->responseString);
$queueUrl = str_replace("http://queue.amazonaws.com/","",$queueUrl);

$message = "<fb2pdfjob version=\"2\">" . 
    "<source url=\"$url\" type=\"application/fb2+xml\" name=\"$name\"/>" .
    "<result key=\"$id.pdf\"/>" .
    "<log key=\"$id.txt\"/>" .
    "</fb2pdfjob>";

if (!$sqs->putMessage($message, $queueUrl, $awsSQSTimeout))
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
