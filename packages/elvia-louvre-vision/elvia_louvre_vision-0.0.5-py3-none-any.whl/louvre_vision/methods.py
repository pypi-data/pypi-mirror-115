from io import BytesIO
import os
import requests
from typing import Union


class Methods():
    """
    Helper methods.
    """
    @staticmethod
    def extract_filename(file_path: str) -> str:
        """
        Extract the file name from a file path.

        :param str file_path:
        :rtype: str
        """
        file_name, file_extension = os.path.splitext(
            file_path.rsplit('/', 1)[-1])
        return file_name + file_extension

    @classmethod
    def fetch_file_from_url(cls, file_url: str) -> BytesIO:
        """
        Fetch file from URL, return a stream object.

        :param str file_url:
        :rtype: BytesIO
        :raises RequestException:
        """
        _response = requests.get(url=file_url)
        _file_bytes = BytesIO(_response.content)
        return _file_bytes

    @classmethod
    def get_remote_file_size(cls, file_url: str) -> Union[int, None]:
        """
        Return remote file size, if possible.
        
        :param str file_url:
        :rtype: int | None
        """
        try:
            response = requests.head(file_url).headers['Content-Length']
            return int(response)
        except:  # NOSONAR, Same functionality regardless of exception thrown
            # TODO: We should probably do something useful here
            return None

    @classmethod
    def is_file_empty(cls,
                      stream: BytesIO,
                      min_size_bytes: int = 1000) -> bool:
        """
        Check whether the file size is larger than a threshold value.
        
        :param BytesIO stream:
        :param int min_size_bytes:
        :rtype: bool
        """
        try:
            if stream.getbuffer().nbytes < min_size_bytes:
                return True
            return False
        except:  #NOSONAR, No matter what exception is thrown here we will label the file as empty
            # TODO: We should probably do something useful here
            return True

    @staticmethod
    def is_string_url(input_str: str) -> bool:
        """Check if a string is a URL."""
        return bool('https://' in input_str)
