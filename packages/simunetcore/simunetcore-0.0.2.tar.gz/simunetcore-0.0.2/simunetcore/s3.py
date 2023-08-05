import boto3
import boto3.session

def createS3Client(s3_endpoint):
    """
    Creates an S3 client.

    Returns
    -------
    s3_client :boto3.resource
        The S3 client.

    Parameters
    ----------
    s3_endpoint : dict{str: Any}
        The endpoint dictionary containing the S3 parameters.
        {
            "url": "https://s3.host.url",
            "bucket_name": "bucket",
            "access_key": "access_key",
            "secret": "secret"
        }

    See Also
    --------
    boto3 library : simunet uses boto3 for S3 communication.

    """
    
    # Create S3 resource
    s3_client = boto3.resource(
        service_name="s3", 
        aws_access_key_id=s3_endpoint["access_key"],
        aws_secret_access_key=s3_endpoint["secret"],
        endpoint_url=s3_endpoint["url"])
    
    # Return the S3 client
    return s3_client


class S3Proxy(object):
    """S3 communication proxy."""  
    
    def __init__(self, s3_endpoint):
        """
        Creates a new S3Proxy object.

        Parameters
        ----------
        s3_endpoint : dict{str: Any]
            The endpoint dictionary containing the S3 parameters.
            {
                "url": "https://s3.host.url",
                "bucket_name": "bucket",
                "access_key": "access_key",
                "secret": "secret"
            }

        """

        # Store the reader
        self.s3_client = createS3Client(s3_endpoint)
        self.bucket_name = s3_endpoint["bucket_name"]
        
    def read(self, obj_name):
        """
        Reads the content of the object with the given name.

        Parameters
        ----------
        obj_name : str
            The name of the object to read.

        Returns
        -------
        content : str
            The content of the object.

        """
        
        # Read object from S3
        s3_obj = self.s3_client.Object(self.bucket_name, obj_name)
        return s3_obj.get()["Body"].read()
    
    def write(self, obj_name, content):
        """
        Writes the content of the object with the given name.

        Parameters
        ----------
        obj_name : str
            The name of the object to write to.
        content : str
            The new content of the object.

        Returns
        -------
        status_code : int
            The http status code of the S3 answer.
        
        """
        
        # Write the buffer to S3
        s3obj = self.s3_client.Object(self.bucket_name, obj_name)
        res = s3obj.put(Body=content)
        return res["ResponseMetadata"]["HTTPStatusCode"]
    
    def delete(self, obj_name):
        """
        Deletes the object with the given name.

        Parameters
        ----------
        obj_name : str
            The name of the object to delete.
        
        Returns
        -------
        status_code : int
            The http status code of the S3 answer.
 
        """
        
        # Delete object from s3
        s3obj = self.s3_client.Object(self.bucket_name, obj_name)
        res = s3obj.delete()
        return res["ResponseMetadata"]["HTTPStatusCode"]
