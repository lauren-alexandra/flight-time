"""
SOLID Design Principles

- Single Responsibility Principle
- Open Closed Principle
- Liskov's Substitutability Principle
- Interface Segregation Principle
- Dependency Inversion Principle
"""

# Original Code we'll apply principles to:
class FTPClient:
  def __init__(self, **kwargs):
    self._ftp_client = FTPDriver(kwargs['host'], kwargs['port'])
    self._sftp_client = SFTPDriver(kwargs['sftp_host'], kwargs['user'], kwargs['pw'])

  def upload(self, file:bytes, **kwargs):
    is_sftp = kwargs['sftp']
    if is_sftp:
      with self._sftp_client.Connection() as sftp:
        sftp.put(file)
    else:
      self._ftp_client.upload(file)

  def download(self, target:str, **kwargs) -> bytes:
    is_sftp = kwargs['sftp']
    if is_sftp:
      with self._sftp_client.Connection() as sftp:
        return sftp.get(target)
    else:
      return self._ftp_client.download(target)


"""
Single Responsibility Principle

every module/class should only have one responsibility and therefore
only one reason to change

increases cohesion, decreases coupling

think of responsibilities as use cases. each case should only
be handled in one place.
"""

# Examining our original code we can see the class does not have a 
# single responsibility because it has to manage connection details 
# for an FTP, and SFTP server. Fixed here:

class FTPClient:
  def __init__(self, host, port):
    self._client = FTPDriver(host, port)

  def upload(self, file:bytes):
    self._client.upload(file)

  def download(self, target:str) -> bytes:
    return self._client.download(target)


class SFTPClient(FTPClient):
  def __init__(self, host, user, password):
    self._client = SFTPDriver(host, username=user, password=password)

  def upload(self, file:bytes):
    with self._client.Connection() as sftp:
      sftp.put(file)

  def download(self, target:str) -> bytes:
    with self._client.Connection() as sftp:
      return sftp.get(target)


"""
Open Closed Principle

software entities (classes, functions, modules) should be open for
extension but closed to change.

extension doesnt change a function signature but allows for new
functionality without changing the code.
e.g.
This could be renaming a parameter, adding a new parameter with a 
default value, or adding the *arg, or **kwargs parameters.
"""

# you can also extend a class with functions
class FTPClient:
  def __init__(self, host, port):
      ... # For this example the __init__ implementation is not significant

  def upload(self, file:bytes):
      ... # For this example the upload implementation is not significant

  def download(self, target:str) -> bytes:
      ... # For this example the download implementation is not significant

  def upload_bulk(self, files:List[str]):
    for file in files:
      self.upload(file)

  def download_bulk(self, targets:List[str]) -> List[bytes]:
    files = []
    for target in targets:
      files.append(self.download(target))

    return files


"""
Liskov's Substituitability Principle


"""























