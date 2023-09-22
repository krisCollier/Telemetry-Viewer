# Telemetry-Viewer

## What?

Quick and dirty alternative to Motec's telemetry software for use with .ld files (assetto corsa). 

## Why?

Motec requires a pro license (>1000$) to add custom math channels and also doesn't present things in a non-race engineer friendly way.

## Future improvements

- Add the ld2csv package to remove the need of manual exporting stints from motec.
  - ISSUE: Need to investigate adding distance and time channels with custom Hz rate otherwise useless.
- Add .html and .pdf exporting functionality 

## How to use

### Prerequisites

1. [JupyterLabs](https://jupyter.org/)
2. [Acti telemetry interface (for recording telem)](https://www.racedepartment.com/downloads/acti-assetto-corsa-telemetry-interface.3948/)
3. [Motec i2 Standard (Data analysis software)](https://www.motec.com.au/software/latestreleases/)

### Step-by-step

1. Complete a stint in Assetto Corsa (Needs to include out-in laps).
2. Open the stint .ld file in motec then export the entire stint to .csv with 20hz (Works best for now... until we've tested different frequencies).
TBC.
