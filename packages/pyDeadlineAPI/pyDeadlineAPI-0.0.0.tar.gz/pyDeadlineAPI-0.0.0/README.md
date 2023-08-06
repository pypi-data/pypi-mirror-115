# pyDeadlineAPI

This is the first implemention of the [DeadlineAPI](https://DeadlineAPI.org) for python. It implement the whole functionality of the api plus some additional features. It also runs extensive validity checks before loading successfully loading a file.

The following classes are provided:
+ Endpoint
+ DeadlineObject
+ Location
+ Contact


## Install

You can easily install pyDeadlineAPI via pip:
```
pip install pyDeadlineAPI
```

## The API
In this section we describe how the API works. 

### How to load a directory?
Loading a directory is easy. You can use the following code to load the default directory at `directory.deadlineapi.org/directory.json`:

```python
import deadlineapi
directory = deadlineapi.Loader.load_directory_by_url(loadDirectly=True)
```

Alternatively you can load from a specific url, a string or a local file on your computer/server:
```python
import deadlineapi
deadlineapi.Loader.load_directory_by_url("https://directory.deadlineapi.org/directory.json",loadDirectly=True)
deadlineapi.Loader.load_directory_by_string("{ "endpointname": "url" }",loadDirectly=True)
deadlineapi.Loader.load_directory_by_path(os.path.join("my","path"),loadDirectly=True)
```

The `loadDirectly=True` (default) makes sure that the endpoints get loaded directly and provides you with a list of [Endpoints](Endpoints). This may take some time. You can also set `loadDirectly=False`. In this case you will get a list of [DirectoryItem](DirectoryItem)s instead. You can use `endpoint = directoryitem.load()` to load the endpoint afterwards. 

### Endpoints
Endpoints represent the endpoints of the api. You can use all the fields specified in the JSON schema. E.g.:
```python
import deadlineapi
directory = deadlineapi.Loader.load_directory_by_url(loadDirectly=True)
for endpoint in directory:
    print(f"Endpoint is compatible to: {endpoint.api_compatibility}")
    print(f"Deadlines provide by {endpoint.name}:")
    for d in endpoint.deadlines:
        print(f"{d.name}: {d.deadline}")
```


In the following table we list all the functionality that is on top of the API fields.


| Name                   | Description                                           |
| ---------------------- | ----------------------------------------------------- |
| `endpointname`         | key in the directory file                             |
| `endpointurl`          | value (url) in the directory file                     |

Note further that you can also load endpoints directly. E.g. 
```python
import deadlineapi
deadlineapi.Loader.load_endpoint_by_string(s)
deadlineapi.Loader.load_endpoint_by_path(path)
deadlineapi.Loader.load_endpoint_by_url(url)
```

Endpoints get automatically validated against the [JSON schema](https://schema.deadlineapi.org/) and other requirements, like url in url field, emails in email field and so on. If you think that something is wrong with the schema files please discuss in the [schema repository](https://github.com/DeadlineAPI/Schema).


### DirectoryItem
A DirectoryItem is simple the representation of a key-value pair of the directory. It only hast two fields:

| Name                   | Description                                           |
| ---------------------- | ----------------------------------------------------- |
| `endpointname`         | key in the directory file                             |
| `endpointurl`          | value (url) in the directory file                     |

You can use `endpoint = directoryitem.load()` to load it and turn it into an [Endpoint](Endpoint) with all the deadline and fields attached. This will also set `endpointname` and `endpointurl` in the Endpoint object.


### DeadlineObject
The DeadlineObject correspond to the individual deadlines. They also got all field provided by API. 

```pyhton
import deadlineapi
directory = deadlineapi.Loader.load_directory_by_url()
for endpoint in directory:
        for d in endpoint.deadlines:
                print(f"{d.name}: {d.deadline} ({d.daysleft()}d)")
```

Note the DeadlineObject also provides some additional functionality:
 
| Name                   | Description                                               |
| ---------------------- | --------------------------------------------------------- |
|  `days_left()`         | How many (full) days are left until the deadline.         |
|  `hours_left()`        | How many (full) hours are left until the deadline.        |
|  `minutes_left()`      | How many (full) minutes are left until the deadline.      |
|  `countdown()`         | How much time is left in a useful format (string)         |
|  `timediff()`         | Provides the time diff as python object                   |

### Location
This class just wraps the location. It provides the following additional methods:

| Name                   | Description                                                               |
| ---------------------- | ------------------------------------------------------------------------- |
|  `to_str()`            | Provides the location as string, e.g.`virtual` or `Germany, Karlsruhe`    |

### Contact
The last class is Concat. This also provides a `toStr()` function:

| Name                   | Description                                                               |
| ---------------------- | ------------------------------------------------------------------------- |
|  `to_str()`            | Provides the contact as string, e.g.`info@kit.edu, @kitde`                |

## Contribute
Clone this repo and run

```bash
python3 -m venv venv
source venv/bin/activate
pip -r requirements.txt
```

We use the GitFlow method to organize our branches. Please work with PullRequests.


## Credits
Many many credits for [SpaceAPI](https://spaceapi.io/), who are the ultimative inspiration for this project also provided a lot of the code. E.g. our website is completely adapted by theirs. THANKS!