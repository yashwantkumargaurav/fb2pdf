#import <Foundation/Foundation.h>

#include <CoreFoundation/CoreFoundation.h>
#include <CoreServices/CoreServices.h> 

#import <Foundation/NSXMLDocument.h>
#import <CoreFoundation/CFURL.h>

/* -----------------------------------------------------------------------------
   Step 1
   Set the UTI types the importer supports
  
   Modify the CFBundleDocumentTypes entry in Info.plist to contain
   an array of Uniform Type Identifiers (UTI) for the LSItemContentTypes 
   that your importer can handle
  
   ----------------------------------------------------------------------------- */

/* -----------------------------------------------------------------------------
   Step 2 
   Implement the GetMetadataForURL function
  
   Implement the GetMetadataForURL function below to scrape the relevant
   metadata from your document and return it as a CFDictionary using standard keys
   (defined in MDItem.h) whenever possible.
   ----------------------------------------------------------------------------- */

/* -----------------------------------------------------------------------------
   Step 3 (optional) 
   If you have defined new attributes, update schema.xml and schema.strings files
   
   The schema.xml should be added whenever you need attributes displayed in 
   Finder's get info panel, or when you have custom attributes.  
   The schema.strings should be added whenever you have custom attributes. 
 
   Edit the schema.xml file to include the metadata keys that your importer returns.
   Add them to the <allattrs> and <displayattrs> elements.
  
   Add any custom types that your importer requires to the <attributes> element
  
   <attribute name="com_mycompany_metadatakey" type="CFString" multivalued="true"/>
  
   ----------------------------------------------------------------------------- */



/* -----------------------------------------------------------------------------
    Get metadata attributes from file
   
   This function's job is to extract useful information your file format supports
   and return it as a dictionary
   ----------------------------------------------------------------------------- */

Boolean GetMetadataForURL(void* thisInterface, 
                          CFMutableDictionaryRef attributes, 
                          CFStringRef contentTypeUTI,
                          CFURLRef urlForFile)
{
    /* Pull any available metadata from the file at the specified path */
    /* Return the attribute keys and attribute values in the dict */
    /* Return TRUE if successful, FALSE if there was no data provided */
    
    NSXMLDocument *xmlDoc;
    NSError *err=nil;
    
    xmlDoc = [[NSXMLDocument alloc] initWithContentsOfURL:(NSURL*)urlForFile
                                                  options:(NSXMLNodePreserveWhitespace|NSXMLNodePreserveCDATA)
                                                    error:&err];
    if (xmlDoc == nil) 
        xmlDoc = [[NSXMLDocument alloc] initWithContentsOfURL:(NSURL*)urlForFile
                                                      options:NSXMLDocumentTidyXML
                                                        error:&err];
    if (xmlDoc == nil)  
    {
        return FALSE;
    }
    
    if (err)  
    {
        [xmlDoc release];
        return FALSE;
    }

    // Title
    NSArray *nodes = [xmlDoc nodesForXPath:@"/FictionBook/description/title-info/book-title/text()"
                                          error:&err];
    
    if(err || [nodes count]<=0)
    {
        [xmlDoc release];
        return FALSE;
    }
    
    NSXMLNode *titleNode = [nodes objectAtIndex:0];
    NSString *title = [titleNode stringValue];
    [(NSMutableDictionary*)attributes setObject:title forKey:@"com_fb2pdf_fb2_title"];
    
    
    // Authors
    NSArray *result = [xmlDoc objectsForXQuery:@"string-join(/FictionBook/description/title-info/author/first-name/text()|/FictionBook/description/title-info/author/first-name/text()|/FictionBook/description/title-info/author/middle-name/text(),' ')"
                                     constants:nil error:&err];
    
    if(err)
    {
        [xmlDoc release];
        return FALSE;
    }
    
    if([result count]<=0)
    {
        [xmlDoc release];
        return FALSE;
    }
    
    [(NSMutableDictionary *)attributes setObject:result
                                          forKey:@"com_fb2pdf_fb2_author"];

    [xmlDoc release];
    return TRUE;
}
