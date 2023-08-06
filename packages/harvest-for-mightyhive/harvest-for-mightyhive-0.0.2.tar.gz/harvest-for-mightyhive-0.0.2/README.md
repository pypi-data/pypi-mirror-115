## About The Package
The package aims to automate the process of updating time entries in harvest.
Although harvest provides APIs to do so, it requires superuser access. For
regular users, those APIs are not accessible. That is why I created this
package, just to make life easier.

## Dependencies

* [selenium](https://selenium-python.readthedocs.io/)
* [chrome-driver](https://chromedriver.chromium.org/): You should have this if you use chrome.


## Installation
```sh
pip install harvest-mightyhive
```
<!-- USAGE EXAMPLES -->
## Usage

Initialize a Harvest client:
```python
harvest = Harvest(username, password)
```

Populate the class variables and submit.
```python
harvest.date = date.today()
harvest.project = Project.INTERNAL
harvest.task = Task.MEETING
harvest.note = "Kick off meeting"
harvest.duration = "0:30"
harvest.submit()
```
