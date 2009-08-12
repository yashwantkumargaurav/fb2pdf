<?php
require_once 'awscfg.php';

// grab this with "pear install Crypt_HMAC"
require_once 'Crypt/HMAC.php';
// grab this with "pear install --onlyreqdeps HTTP_Request"
require_once 'HTTP/Request.php';

// Note that version HTTP_Request 1.3.0 has a BUG in it!  Change line
// 765 from:
//            (HTTP_REQUEST_METHOD_POST != $this->_method && empty($this->_postData) && empty($this->_postFiles))) {
// to:
//            (HTTP_REQUEST_METHOD_POST == $this->_method && empty($this->_postData) && empty($this->_postFiles))) {
// Without this change PUTs with non-empty content-type will fail!

// Helper function to create S3 object (see sqshelper.php)
function getS3Object()
{
    global $awsApiKey, $awsApiSecretKey;
    return new S3($awsApiKey, $awsApiSecretKey);
}

// Amazon S3 class
class S3
{
	var $serviceUrl = "http://s3.amazonaws.com/";
   	var $accessKeyId;
   	var $secretKey;
    
	var $request;
    
	var $responseCode;
	var $responseBody;
	var $responseHeader;
    
    // debug (set to false to remove echo)
    var $debug = false;

	function S3($accessKeyId, $secretKey) 
    {
		$this->accessKeyId = $accessKeyId;
		$this->secretKey   = $secretKey;
	}
    
	// Returns a list of buckets
    function listBuckets() 
    {
        $this->request =& new HTTP_Request($this->serviceUrl);
		$this->initRequest("GET", "", "private", "", "", "");
        $this->request->sendRequest();
        $this->gotResponse();
        return ($this->responseCode == 200) ? true : false;
	}

  	// Writes an object
    function writeObject($bucket, $object, $data, $contentType, $acl, $metadata = NULL, $extraHttpHeaders = NULL)
    {
        $resource = $bucket . "/" . $object;
        
        $this->request =& new HTTP_Request($this->serviceUrl . $resource);
		$this->initRequest("PUT", $resource, $contentType, $acl, $metadata, $extraHttpHeaders);
        
        // add data
        $this->request->setBody($data);
        
        $this->request->sendRequest();
        $this->gotResponse();
        return ($this->responseCode == 200) ? true : false;
    }
    
  	// Writes a file
    function writeFile($bucket, $object, $filename, $contentType, $acl, $metadata = NULL, $extraHttpHeaders = NULL)
    {
        // check file
        $fp = fopen ($filename, "r");
        if (!$fp)
            return false;
        
        $resource = $bucket . "/" . $object;
        
        $this->request =& new HTTP_Request($this->serviceUrl . $resource);
		$this->initRequest("PUT", $resource, $contentType, $acl, $metadata, $extraHttpHeaders);
        
        // read data from file
        while (!feof($fp))
        {
            $data = fread($fp, 8192);
            if (!$this->request->_body)
                $this->request->_body = $data;
            else
                $this->request->_body .= $data;
        }
        fclose ($fp);
        
        $this->request->sendRequest();
        $this->gotResponse();
        return ($this->responseCode == 200) ? true : false;
    }
    
  	// Object exists
    function objectExists($bucket, $object)
    {
        $resource = $bucket . "/" . $object;
        
        $this->request =& new HTTP_Request($this->serviceUrl . $resource);
		$this->initRequest("HEAD", $resource, "", "private", "", "");
        
        $this->request->sendRequest();
        $this->gotResponse();
        
        return ($this->responseCode == 200) ? true : false;
    }
    
    // Gets array of object's filename
    function getObjectFilename($bucket, $object)
    {
        $resource = $bucket . "/" . $object;
        
        $this->request =& new HTTP_Request($this->serviceUrl . $resource);
		$this->initRequest("HEAD", $resource, "", "private", "", "");
        
        $this->request->sendRequest();
        $this->gotResponse();

        $filename = null;
        if ($this->responseCode == 200) {
            foreach ($this->responseHeader as $key => $value) 
            {
                if (stristr($key, "Content-Disposition"))
                {
                    $values = array();
                    $values = explode("\"", strstr($value, "filename="));
                    $filename = $values[1];
                }
            }
        }

        return $filename;
    }
    
  	// Gets array of object's metadata
    function getObjectMetadata($bucket, $object)
    {
        $resource = $bucket . "/" . $object;
        
        $this->request =& new HTTP_Request($this->serviceUrl . $resource);
		$this->initRequest("HEAD", $resource, "", "private", "", "");
        
        $this->request->sendRequest();
        $this->gotResponse();
        
        if ($this->responseCode == 200)
        {
	    $metadata = array();
            $metaPrefix = "x-amz-meta-";
            foreach ($this->responseHeader as $key => $value) 
            {
                if (strstr($key, $metaPrefix))
                {
                    $i = str_replace($metaPrefix, "", $key);
                    $metadata[$i] = trim($value);
                }
            }
            return $metadata;
        }
        else
            return false;
    }
    
  	// Delete object
    function deleteObject($bucket, $object)
    {
        $resource = $bucket . "/" . $object;
        
        $this->request =& new HTTP_Request($this->serviceUrl . $resource);
		$this->initRequest("DELETE", $resource, "", "private", "", "");
        
        $this->request->sendRequest();
        $this->gotResponse();
        
        return ($this->responseCode == 200 or $this->responseCode == 204) ? true : false;
    }
    
    //initializes common elements of all REST requests
	function initRequest($verb, $resource, $contentType, $acl, $metadata, $extraHttpHeaders)
    {
        $date_rfc822 = "D, d M Y H:i:s T";
        $httpDate = gmdate($date_rfc822);
        
        $this->request->setMethod($verb);
        $this->request->addHeader("content-type", $contentType);
        $this->request->addHeader("Date", $httpDate);
        $this->request->addHeader("x-amz-acl", $acl);
        		
        // add metadata
        $metadatastring = "";
        if (is_array($metadata)) 
        {
            ksort($metadata);
			foreach ($metadata as $key => $value) 
            {
				$this->request->addHeader("x-amz-meta-".$key, trim($value));
				$metadatastring .= "x-amz-meta-".$key.":".trim($value)."\n";
            }
        }
        
        // add extra http headers
        if (is_array($extraHttpHeaders)) 
        {
			foreach ($extraHttpHeaders as $key => $value) 
            {
				$this->request->addHeader($key, trim($value));
            }
        }
        
        // auth
        $stringToSign = "$verb\n\n$contentType\n$httpDate\nx-amz-acl:$acl\n$metadatastring/$resource";
		$hasher =& new Crypt_HMAC($this->secretKey, "sha1");
		$signature = $this->hex2b64($hasher->hash($stringToSign));

        $this->request->addHeader("Authorization", "AWS " . $this->accessKeyId . ":" . $signature);
	}
				
	function gotResponse()
    {
   		$this->responseCode   = $this->request->getResponseCode();
		$this->responseHeader = $this->request->getResponseHeader();
		$this->responseBody   = $this->request->getResponseBody();
		
        $this->debugText("responseCode=", $this->responseCode);
		$this->debugText("responseHeader=" , $this->responseHeader);
		$this->debugText("responseBody=" , $this->responseBody);
    }
    
    function hex2b64($str) 
    {
		$raw = '';
		for ($i=0; $i < strlen($str); $i+=2) {
			$raw .= chr(hexdec(substr($str, $i, 2)));
		}
			return base64_encode($raw);
	}
		 
	function debugText($text, $var) 
    {
        if ($this->debug) 
        {
			print("<pre>");
			print($text);
			print_r($var);
			print("</pre>");
		}
	}
}
?>