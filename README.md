# kore_aggregator
Working on making a basic SIEM with entity resolution

## Basic Hypothesis

Security solutions cost too much for SMB.  This means that many times these companies will 
either minimally invest or not invest at all in proper tooling.  When the company gets breached, 
it will make it near impossible to find IOCs in their network.

But what if... we can build a crowd sourced platform that has minimum to no cost for bringing in 
many of the common data sources that they will need/want.

When we break down a basic SIEM we come to a few common features:

- A standardized way of bringing in the data from the originating data source [collector]
- A standardized way of parsing the data into a backend which can be latter searched or have 
applications built on top of [connector]
- A way to search this data [query language]
- A way to visualize or aggregate the data into information [applications]

### SPLUNK

Most people I find that use Splunk have a love/hate relationship with the product.  They use it
because they have invested numerous hours into learning the syntax and being able to query the 
data.  They love that a lot of the connectors are already created and just need to be installed.

They hate the pricing model and the inability to save queries into an "alerting" workflow.  Typically,
I will find that a Splunk poweruser will have 5-10 tabs open per investigation.  This is extremely
painful and impedes an analysts time to remediation/detection.

### How can we change the price point?

I am working with some friends to build a prototype that runs in our public domains that collects
and aggregates this data into a easily searchable UX.  The goal is to use Neo4j as the backend,
some Bootstrap + React UX for searching and application building.  To have the best chance of 
standardizing this into a framework that others may use, we are going to adhere our object model
to the same one use by [BloodHound](https://github.com/BloodHoundAD/BloodHound).  This will make
sure that anything that any data that we bring in can only enrich current BloodHound offerings and 
vice versa.

Will this fail? Probably, this is a side project that has no real end goal. Keeping things honest here :)


## How to contribute

- Build a collector and add to [kore_collector](https://github.com/Cr0n1c/kore_collector)
- Build a connector and add the collector to [/connectors](connectors). Use [ldap.py](connectors/ldap.py) 
as a reference.
- Add your connector to `run_connectors` function inside [kore_aggregator.py](kore_aggregator.py).
- Run `kore_aggregator.py` to validate things are working.
 
