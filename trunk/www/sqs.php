<?php
// This software code is made available "AS IS" without warranties of any
// kind.  You may copy, display, modify and redistribute the software
// code either by itself or as incorporated into your code; provided that
// you do not remove any proprietary notices.  Your use of this software
// code is at your own risk and you waive any claim against Amazon
// Digital Services, Inc. or its affiliates with respect to your use of
// this software code. (c) 2006 Amazon Digital Services, Inc. or its
// affiliates.

// Notes:
// - This relies on HTTP_Request from pear.php.net, but the latest version
//   has a bug; see note below on how to fix it (one-character change).


/**
 * A PHP5 class for interfacing with the Amazon SQS REST API
*/
require_once 'Crypt/HMAC.php';    // grab this with "pear install Crypt_HMAC"
require_once 'HTTP/Request.php';  // grab this with "pear install --onlyreqdeps HTTP_Request"
// Note that version HTTP_Request 1.3.0 has a BUG in it!  Change line
// 765 from:
//            (HTTP_REQUEST_METHOD_POST != $this->_method && empty($this->_postData) && empty($this->_postFiles))) {
// to:
//            (HTTP_REQUEST_METHOD_POST == $this->_method && empty($this->_postData) && empty($this->_postFiles))) {
// Without this change PUTs with non-empty content-type will fail!

class SQS
{
	var $serviceUrl;
   	var $accessKeyId;
   	var $secretKey;
	var $responseString;
	var $responseCode;
	var $parsed_xml;
	var $request;
	
	/**
	 * Constructor
	 *
	 * Takes ($accessKeyId, $secretKey, $serviceUrl)
	 *
	 * - [str] $accessKeyId: Your AWS Access Key Id
	 * - [str] $secretKey: Your AWS Secret Access Key
	 * - [str] $serviceUrl: OPTIONAL: defaults: http://queue.amazonaws.com/
	 *
	*/
	function SQS($accessKeyId, $secretKey, $serviceUrl="http://queue.amazonaws.com/") {
		$this->serviceUrl=$serviceUrl;
		$this->accessKeyId=$accessKeyId;
		$this->secretKey=$secretKey;
	}
	
	/**
	 * createQueue -- creates a queue.
	 *
	 * Takes ($queue)
	 *
	 * - [str] $queue: the user-defined part of the QueueId
	*/		
	function createQueue($queue){
		$httpDate =  date("D, j M Y G:i:s T");
		$stringToSign = "POST\n\ntext/plain\n$httpDate\n/";
		$this->request =& new HTTP_Request("http://queue.amazonaws.com/?QueueName=".$queue);
		$this->initialize_request("POST", $httpDate, $stringToSign);
		$this->request->addPostData("something","something"); //can't have empty POST
		$this->request->addHeader("Content-Type", "text/plain");			
		$this->request->sendRequest();
		$this->responseCode=$this->request->getResponseCode();
		$this->responseString = $this->request->getResponseBody();
		//$this->parsed_xml = simplexml_load_string($this->responseString);
		if ($this->responseCode == 200) {
			return true;
		} else {
			return false;
		}		
	}
	
	/**
	 * deleteQueue -- deletes a queue.
	 *
	 * Takes ($queueId)
	 *
	 * - [str] $queueId: the $queueId of the queue you wish to delete 
	 * (Note: $queueId is AlphaNumericPrefix/UserAssignedQueueName. The AlphaNumericPrefix is automatically assigned when the queue is created.)
	*/		
	function deleteQueue($queueId){
		$httpDate = date("D, j M Y G:i:s T");
		$stringToSign = "DELETE\n\n\n$httpDate\n/$queueId";
		$this->request =& new HTTP_Request($this->serviceUrl . $queueId );
		$this->initialize_request("DELETE", $httpDate, $stringToSign);
		$this->request->sendRequest();
		$this->responseCode=$this->request->getResponseCode();
		$this->responseString = $this->request->getResponseBody();
		//$this->parsed_xml = simplexml_load_string($this->responseString);
		if ($this->responseCode == 200) {
			return true;
		} else {
			return false;
		}
	}
	
	/**
	 * listQueues -- lists all your queues.
	 *
	 * Takes ($queueNamePrefix)
	 *
	 * - [str] $queueNamePrefix (OPTIONAL): lists all queues where the queue name begines with $queueNamePrefix
	*/
	function listQueues($queueNamePrefix){
		$httpDate = date("D, j M Y G:i:s T");
		$stringToSign = "GET\n\n\n$httpDate\n/";
		$this->request = & new HTTP_Request($this->serviceUrl."?QueueNamePrefix=$queueNamePrefix");
		$this->initialize_request("GET", $httpDate, $stringToSign);
		$this->request->sendRequest();
		$this->responseCode=$this->request->getResponseCode();
		$this->responseString = $this->request->getResponseBody();
		//$this->parsed_xml = simplexml_load_string($this->responseString);
		if ($this->responseCode == 200) {
			return true;
		} else {
			return false;
		}
	}		
	
	/**
	 * putMessage -- Puts a messages to a queue.
	 *
	 * Takes ($message, $queueId, $visibilityTimeout)
	 *
	 * - [str] $message: message to be put to the queue
	 * - [str] $queueId: queueId to which message it to be put
	 * - [int] $visibilityTimeout (OPTIONAL): if not deleted after this time, the message will return to the queue
	*/		
	function putMessage($message, $queueId, $visibilityTimeout){
		$message = "<?xml version='1.0' encoding='UTF-8'?>".$message;
		$httpDate = date("D, j M Y G:i:s T");
		$stringToSign = "PUT\n\ntext/plain\n$httpDate\n/$queueId/back";
		$this->request =& new HTTP_Request($this->serviceUrl . "$queueId/back?VisibilityTimeout=$visibilityTimeout");
		$this->initialize_request("PUT", $httpDate, $stringToSign);
		$this->request->addHeader("Content-Type", "text/plain");
		$this->request->addHeader("Content-Length", strlen($message));
		$this->request->setBody($message);
		$this->request->sendRequest();
		$this->responseCode=$this->request->getResponseCode();
		$this->responseString = $this->request->getResponseBody();
		//$this->parsed_xml = simplexml_load_string($this->responseString);
		if ($this->responseCode == 200) {
			return true;
		} else {
			return false;
		}
	}      
	
	/**
	 * receiveMessage -- Receives a message(s) from a queue.
	 *
	 * Takes ($queueId, $visibilityTimeout, $numberOfMessages)
	 *
	 * - [str] $queueId: the queue from which messages(s) will be taken
	 * - [int] $visibilityTimeout (OPTIONAL): if not deleted after this time, the message will return to the queue
	 * - [int] $numberOfMessages (OPTIONAL): number of messages to be received
	*/
	function receiveMessage($queueId, $visibilityTimeout, $numberOfMessages){
		$httpDate = date("D, j M Y G:i:s T");
		$stringToSign = "GET\n\n\n$httpDate\n/$queueId/front";
		$url = $this->serviceUrl.$queueId."/front";
		if($numberOfMessages == '')
			$numberOfMessages = 1;
		$url.="?NumberOfMessages=$numberOfMessages";
		if($visibilityTimeout != '')
			$url.="&VisibilityTimeout=$visibilityTimeout";
		$this->request =& new HTTP_Request($url);
		$this->initialize_request("GET", $httpDate, $stringToSign);	
		$this->request->sendRequest();
		$this->responseCode=$this->request->getResponseCode();
		$this->responseString = $this->request->getResponseBody();
		//$this->parsed_xml = simplexml_load_string($this->responseString);
		if ($this->responseCode == 200) {
			return true;
		} else {
			return false;
		}
	}		
	
	/**
	 * getVisibilityTimeout -- gets the visibility timeout for a specified queue.
	 *
	 * Takes ($queueId)
	 *
	 * - [str] $queueId: queueId for which visibility timeout is sought
	*/
	function getVisibilityTimeout($queueId){
		$httpDate = date("D, j M Y G:i:s T");
		$stringToSign = "GET\n\n\n$httpDate\n/$queueId";
		$this->request =& new HTTP_Request($this->serviceUrl.$queueId);
		$this->initialize_request("GET", $httpDate, $stringToSign);
		$this->request->sendRequest();
		$this->responseCode=$this->request->getResponseCode();
		$this->responseString = $this->request->getResponseBody();
		//$this->parsed_xml = simplexml_load_string($this->responseString);
		if ($this->responseCode == 200) {
			return true;
		} else {
			return false;
		}
	}				
	
	/**
	 * getMessage -- "Peeks" at a message (message is not "locked" - it can be received by another call).
	 *
	 * Takes ($queueId, $messageId)
	 *
	 * - [str] $queueId: queueId in which message is to be found
	 * - [str] $messageId: the Id of the message to be seen
	*/
	function getMessage($queueId, $messageId){
		$httpDate = date("D, j M Y G:i:s T");
		$stringToSign = "GET\n\n\n$httpDate\n/$queueId/$messageId";
		$this->request =& new HTTP_Request($this->serviceUrl.$queueId."/".$messageId);
		$this->initialize_request("GET", $httpDate, $stringToSign);	
		$this->request->sendRequest();
		$this->responseCode=$this->request->getResponseCode();
		$this->responseString = $this->request->getResponseBody();
		//$this->parsed_xml = simplexml_load_string($this->responseString);
		if ($this->responseCode == 200) {
			return true;
		} else {
			return false;
		}
	}
	
	/**
	 * deleteMessage -- Deletes a message.
	 *
	 * Takes ($queueId, $messageId)
	 *
	 * - [str] $queueId: queueId from which message is to be deleted
	 * - [str] $messageId: the Id of the message to be deleted
	*/
	function deleteMessage($queueId, $messageId){
		$httpDate = date("D, j M Y G:i:s T");
		$stringToSign = "DELETE\n\n\n$httpDate\n/$queueId/$messageId";
		$this->request =& new HTTP_Request($this->serviceUrl.$queueId."/".$messageId);
		$this->initialize_request("DELETE", $httpDate, $stringToSign);	
		$this->request->sendRequest();
		$this->responseCode=$this->request->getResponseCode();
		$this->responseString = $this->request->getResponseBody();
		//$this->parsed_xml = simplexml_load_string($this->responseString);
		if ($this->responseCode == 200) {
			return true;
		} else {
			return false;
		}
	}
	
	/**
	 * setVisibilityTimeout -- sets the visibility timeout for a specified queue.
	 *
	 * Takes ($queueId, $visibilityTimeout)
	 *
	 * - [str] $queueId: queueId for which visibility timeout is to be set
	 * - [int] $visibilityTimeout: if messages are received but not deleted before this time, they will be returned to the queue
	*/
	function setVisibilityTimeout($queueId, $visibilityTimeout){
		$httpDate = date("D, j M Y G:i:s T");
		$stringToSign = "PUT\n\n\n$httpDate\n/$queueId";
		$this->request =& new HTTP_Request($this->serviceUrl . "$queueId?VisibilityTimeout=$visibilityTimeout");
		$this->initialize_request("PUT", $httpDate, $stringToSign);
		$this->request->sendRequest();
		$this->responseCode=$this->request->getResponseCode();
		$this->responseString = $this->request->getResponseBody();
		//$this->parsed_xml = simplexml_load_string($this->responseString);
		if ($this->responseCode == 200) {
			return true;
		} else {
			return false;
		}
	}
	
	//Note that all "grant" related functions utilize the Query interface as they are not available via the REST interface
	
	/**
	 * addGrant -- adds permissions for a user to a queue.
	 *
	 * Takes ($queueId, $grantee, $permission)
	 *
	 * - [str] $queueId: queueId for which permission is granted
	 * - [str] $grantee: e-mail address or canonical user id of person being granted permission
	 * - [str] $permission: type of permission being granted
	*/
	function addGrant($queueId, $grantee, $permission){//add expiration parameter
		$date = gmdate('Y-m-d\TH:i:s\Z');
		$signature = urlencode($this->constructSig("AddGrant".$date));
		if(!strpos($grantee,'@')){
			$params = "Action=AddGrant&Version=2006-04-01&AWSAccessKeyId=$this->accessKeyId&Timestamp=$date&Grantee.ID=$grantee&Permission=$permission&Signature=$signature";
		} else {
			$params = "Action=AddGrant&Version=2006-04-01&AWSAccessKeyId=$this->accessKeyId&Timestamp=$date&Grantee.EmailAddress=$grantee&Permission=$permission&Signature=$signature";
		}
		$req = & new HTTP_Request($this->serviceUrl.$queueId);
   		$req->setMethod('GET');
    	$req->addRawQueryString($params);
	    $req->sendRequest();
		$this->responseCode=$req->getResponseCode();
		$this->responseString = $req->getResponseBody();
		//$this->parsed_xml = simplexml_load_string($this->responseString);
		if ($this->responseCode == 200) {
			return true;
		} else {
			return false;
		}	
	}
	
	/**
	 * listGrants - Lists all grantees and permissions for a queue.
	 *
	 * Takes ($queueId)
	 *
	 * - [str] $queueId: queueId for which grant list is sought
	*/
	function listGrants($queueId){
		$date = gmdate('Y-m-d\TH:i:s\Z');
		$signature = urlencode($this->constructSig("ListGrants".$date)); 
		$params = "Action=ListGrants&Version=2006-04-01&AWSAccessKeyId=$this->accessKeyId&Timestamp=$date&Signature=$signature";
		$req = & new HTTP_Request($this->serviceUrl.$queueId);
   		$req->setMethod('GET');
    	$req->addRawQueryString($params);
	    $req->sendRequest();
		$this->responseCode=$req->getResponseCode();
		$this->responseString = $req->getResponseBody();
		//$this->parsed_xml = simplexml_load_string($this->responseString);
		if ($this->responseCode == 200) {
			return true;
		} else {
			return false;
		}	
	}
	
	/**
	 * removeGrant -- removes permissions from a user to a queue.
	 *
	 * Takes ($queueId, $grantee, $permission)
	 *
	 * - [str] $queueId: queueId for which permission is removed
	 * - [str] $grantee: e-mail address or canonical user id of person whose permission is being removed
	 * - [str] $permission: type of permission being removed
	*/
	function removeGrant($queueId, $grantee, $permission){
		$date = gmdate('Y-m-d\TH:i:s\Z');
		$signature = urlencode($this->constructSig("RemoveGrant".$date));
		if(!strpos($grantee,'@')){
			$params = "Action=RemoveGrant&Version=2006-04-01&AWSAccessKeyId=$this->accessKeyId&Timestamp=$date&Grantee.ID=$grantee&Permission=$permission&Signature=$signature";
		} else {
			$params = "Action=RemoveGrant&Version=2006-04-01&AWSAccessKeyId=$this->accessKeyId&Timestamp=$date&Grantee.EmailAddress=$grantee&Permission=$permission&Signature=$signature";
		}
		$req = & new HTTP_Request($this->serviceUrl.$queueId);
   		$req->setMethod('GET');
    	$req->addRawQueryString($params);
	    $req->sendRequest();
		$this->responseCode=$req->getResponseCode();
		$this->responseString = $req->getResponseBody();
		//$this->parsed_xml = simplexml_load_string($this->responseString);
		if ($this->responseCode == 200) {
			return true;
		} else {
			return false;
		}	
	}    
	
	//initializes common elements of all REST requests
	function initialize_request($verb, $httpDate, $stringToSign){
		$this->request->setMethod($verb);
		$this->request->addHeader("Date", $httpDate);
		$signature = $this->constructSig($stringToSign);
		$this->request->addHeader("Authorization", "AWS " . $this->accessKeyId . ":" . $signature);
		$this->request->addHeader("AWS-Version", "2006-04-01");
	}
				
	function hex2b64($str) {
		$raw = '';
		for ($i=0; $i < strlen($str); $i+=2) {
			$raw .= chr(hexdec(substr($str, $i, 2)));
		}
			return base64_encode($raw);
	}
		 
	function constructSig($str) {
		$hasher =& new Crypt_HMAC($this->secretKey, "sha1");
		$signature = $this->hex2b64($hasher->hash($str));
		return($signature);
	}
}
?>