# Linux Reliability Agent

## Overview
The Linux Reliability Agent is a lightweight monitoring tool that evaluates the operational health of a Linux system. It continuously collects system metrics, calculates a reliability score, and identifies degraded or unstable conditions.

---

## Features
- Continuous system health monitoring
- Reliability scoring and mode classification
- Alert generation and incident correlation
- Structured JSON logging
- Local web-based status interface
- Splunk Enterprise integration
- User-level systemd service support

---

## Logs
- **health.json** – periodic system health snapshots  
- **alerts.log** – individual alert events  
- **incidents.log** – correlated reliability incidents  

All logs are written in structured JSON format.

---

## Usage
The agent runs continuously in the background, evaluates system conditions at fixed intervals, and records reliability data for local viewing or centralized analysis.

---

## Technologies
Python, Flask, systemd, Splunk Enterprise, Linux

---

## Purpose
This project demonstrates system reliability monitoring, structured logging, and observability integration on Linux systems.
