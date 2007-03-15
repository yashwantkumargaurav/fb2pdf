<?php

  /**
   * Command-line script to test SQS message sending
   */

require_once 'awscfg.php';
require_once 'sqshelper.php';

// send SQS message
if(!sqsPutMessage('testid', "http://s3.amazonaws.com/test_bucker/test.fb2", 'test.fb2', "http://www.codeminders.com/fb2pdf/conv_callback.php", uniqid(""),"vb@gg"))
{
    echo "Error sending message\n";
} else
{
    echo "Message sent\n";
}

?>
