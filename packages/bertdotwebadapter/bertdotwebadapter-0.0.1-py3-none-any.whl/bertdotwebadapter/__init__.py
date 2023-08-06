import datetime
from bertdotwebadapter.logger import Logger
import os
import re
import requests
from requests.auth import HTTPBasicAuth

logger = Logger().init_logger(__name__)

class WebAdapter:

  def __init__(self):
    pass

  def write_cache_file(self, response_obj, cache_file_path):

    if not os.path.isfile(cache_file_path):
      try:
        with open(cache_file_path, 'wb') as f:
            for chunk in response_obj.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
        logger.info('Wrote cache file at %s' % cache_file_path)
      except Exception as e:
        logger.warning("Error: Failed to cache content at {url}, error code was {code}".format(
          url=url,
          code=response_obj.status_code
          )
        )

  def get(self, url, **kwargs):

    username = kwargs.get('username')
    password = kwargs.get('password') 
    cache = kwargs.get('cache', False)
    cache_path = kwargs.get('cache_path', '/tmp')
    cache_time_limit = kwargs.get('cache_time', 60)

    if username and password:
      response = requests.get(url, auth=HTTPBasicAuth(username, password))
    else:
      response = requests.get(url)

    if response.status_code == 200:
      if cache:
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
          remote_filename = re.findall("filename=(.+)", d)[0]
        else:
          remote_filename = url.split('/')[-1]
        cache_file = '%s/%s' % (cache_path, remote_filename)
        if not os.path.isfile(cache_file):
          self.write_cache_file(response, cache_file)
        else:
          logger.info('Found cache file at %s' % cache_file)
          cache_file_modified = datetime.datetime.fromtimestamp(
            os.path.getmtime(cache_file)
            )
          cache_time_limit = datetime.timedelta(minutes=cache_time_limit)
          if datetime.datetime.now() - file_modified > cache_time_limit:
            logger.info('Cache time for file at %s has expired' % cache_file)
            self.write_cache_file(response, cache_file)
          else:
            return open(cache_file).read()
      return(response.text)
    else:
      return "Error: Call to {url} failed with error code {code}".format(
        url=url,
        code=response.status_code
        )