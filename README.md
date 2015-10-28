# kisi-python
Python client and scripts for talking to the KISI lock API

## `kisi_unlock.py`
`kisi_unlock.py` is a wrapper for `KisiApi` to have an all-in-one script to unlock a lock.

### Example
```bash
$ ./kisi_unlock.py -e foo@bar.com -p PASSWORD -l 'My Door'
2015-10-28 12:48:43,121 root INFO Found lock: "My Door 2.0" (ID: 12345)
2015-10-28 12:48:43,844 root INFO {u'message': u'Unlocked!'}
```

If no password is provided, it will be prompted:
```bash
$ ./kisi_unlock.py -e foo@bar.com -l 'My Door'
Password:
2015-10-28 12:48:43,121 root INFO Found lock: "My Door 2.0" (ID: 12345)
2015-10-28 12:48:43,844 root INFO {u'message': u'Unlocked!'}
```

## `api.py`
`api.py` can be imported and used from outside scripts, for example:

```python
In [1]: from api import KisiApi

In [2]: api = KisiApi('foo@bar.com', 'PASSWORD')

In  [3]: api.unlock('My Door')
Out [3]: {u'message': u'Unlocked!'}
```

The `send_api()` method can be used to send raw API calls to KISI:
```python
In [4]: api.send_api('GET', 'keys')
Out[4]: <Response [200]>

In [5]: api.send_api('GET', 'keys').json()
Out[5]:
...omitted...
```
