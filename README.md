# Unofficial Fork
**This is an unofficial fork of graphite-web used at Evernote. 
No support is provided for it. Use at your own risk.**

**For the official graphite-web repository:
[graphite-project/graphite-web](https://github.com/graphite-project/graphite-web)**

We have a cluster of graphite servers using apache, carbon-relay, carbon-cache, 
memcached, and mysql. Many of our metrics are supplied via collectd. 
For more information: [graphite at evernote blog](http://blog.evernote.com/tech/2013/07/29/graphite-at-evernote/)

Our version of graphite-web is based on **graphite-web 0.9.12**

## Evernote Changes for graphite-web

* UI changes
* Templated Dashboards 
* Multi-device Templated Dashboards
* Dashboard model change

## UI Changes
We only use the graphite dashboard and composer. We do not use login, flot,
and events. We use apache for authentication and access to graphite. Our
browserHeader.html differs from the one supplied here as this version restores
the components we removed, but we left in our preference to open components in 
'content' rather than '_top'. We default to the Dashboard UI navbar on the
left rather than top: Tree (left nav) in the Configure UI window.


## Dashboard Enhancements
### Templated Dashboards
We added templated dashboards to graphite. In our version of the dashboard, 
there are additional tabs for 'Devices' and 'Template Editor'. In the 
Devices tab, a 'Templates' drop-down list includes only dashboards marked as
templates. A dashboard's template status can be managed under the Template 
Editor tab. The Dashboard Finder under the Dashboard menu can be used to load
both types of dashboards. Templated dashboards in the Finder are marked with
'(templated)'.

Selecting both a template and device will load the templated dashboard and the
the automatic template variable '{{id}}' will be set to the selected device. 
Arbitrary variables wrapped with double braces can be managed in the Template
Editor. Variables can be used in template enabled dashboards:
    
    cactiStyle(aliasByNode(collectd.{{id}}.memory.memory-free.value,3))

### Multi-device Templated Dashboards
The dashboard list of devices supports multi-select. This is often used to 
quickly compare multiple devices that should have similar performance profiles. 
We create specific dashboards for this activity to reduce the number of metrics 
within graphs versus our more detailed single device dashboard templates. 

There are no special syntax changes required to support multi-device templates
in a dashboard. A single metric expression is dynamically updated. For example, 
here's how we can compare the CPU usage of multiple servers. Each device 
selected in the list will create a single metric in the graph:

    aliasByNode(sumSeries(collectd.{{id}}.cpu-avg.cpu-wait.value,collectd.{{id}}.cpu-avg.cpu-system.value,collectd.{{id}}.cpu-avg.cpu-user.value),1)

Note that using 'Share' with a multi-device dashboard, won't share all the currently
selected devices.

#### Devices
Our concept of 'devices' for the dashboard is based on our naming standards for
device metrics in graphite. 

We use the following pattern: *prefix.host.metric*

    collectd.host123.memory.memory-free.value
    network.lb123.snmp.a10_ax_ssl.connrate.value
    network.pdu123.snmp.temperature-A1.value

For the devices to appear in the devices list, the device directories **must** be
defined in webapp/graphite/local_settings.py. An example with two directories:

    METRICS_DIRS = [ '/opt/graphite/storage/whisper/collectd', '/opt/graphite/storage/whisper/network' ]


### Dashboard Model Change
To support dashboards, we've altered the dashboard model to include a new
BooleanField: templated. If you're attempting to use this version of graphite
with a pre-existing graphite installation, make sure this field is present in
your preferred data store. From models.py:

    templated = models.BooleanField(default = False)


---------

**Original README content begins here.**


## Overview

Graphite consists of two major components

1. the frontend Django webapp that runs under mod_python Apache
2. the backend carbon-cache.py daemon

Client applications connect to the running carbon-cache.py daemon on port 2003 and send it
lines of text of the following format:

    my.metric.name value unix_timestamp

For example:

    performance.servers.www01.cpuUsage 42.5 1208815315

The metric name is like a filesystem path that uses . as a separator instead of /
The value is some scalar integer or floating point value
The unix_timestamp is unix epoch time, as an integer

Each line like this corresponds to one data point for one metric.

Once you've got some clients sending data to carbon-cache, you can view
graphs of that data in the frontend webapp.


## Webapp Installation

Use the instructions in the INSTALL file.


## Running carbon-cache.py

First you must tell carbon-cache what user it should run as.
This must be a user with write privileges to `$GRAPHITE_ROOT/storage/whisper/`
Specify the user account in `$GRAPHITE_ROOT/carbon/conf/carbon.conf`

This user must also have write privileges to `$GRAPHITE_ROOT/storage/log/carbon-cache/`


## Writing a client

First you obviously need to decide what data it is you want to graph with
graphite. The script `examples/example-client.py` demonstrates a simple client
that sends loadavg data for your local machine to carbon on a minutely basis.

The default storage schema stores data in one-minute intervals for 2 hours.
This is probably not what you want so you should create a custom storage schema
according to the docs on the graphite wiki (http://graphite.wikidot.com)
