# Sentinel: Industrial Edge Systems & Process Governance

**Tech Stack:** `Python 3` | `AutoHotkey v2` | `Windows API (ntdll, kernel32)` | `REST APIs` | `ETL Pipelines`

## Executive Summary

**Sentinel** is a monorepo containing a suite of high-assurance automation tools, IoT telemetry pipelines, and kernel-level process governors. It was engineered to bridge the gap between Operational Technology (OT) and Information Technology (IT) on high-volume Surface-Mount Technology (SMT) manufacturing lines.

In legacy manufacturing environments, systems are often black boxes, APIs are undocumented, and race conditions between proprietary binaries can bring production to a halt. The tools in this repository were built to establish strict digital governance over these physical systems—reducing machine downtime, neutralizing configuration drift, and automating heavy data ingestion pipelines.

## Repository Architecture

This repository is divided into four distinct domain-specific modules:

### 1. [Warden](/warden) - *Kernel-Level Process Governance*

A high-assurance data sanitization proxy built to combat severe configuration drift in SMT inspection hardware.

* **The Engineering:** Utilizes `ntdll\NtSuspendProcess` to hijack and freeze proprietary C-binaries at the CPU level. This "nuclear" synchronization resolves non-deterministic race conditions, allowing Warden to safely sanitize, normalize, and inject overridden states into I/O files before releasing the process back to the system.
* **The Impact:** Prevented thousands of false-positive machine failures, saving the factory floor from years of manual configuration debt.

### 2. [Nozzle Suite](/nozzle) - *IoT Telemetry & Multithreaded Dashboards*

A complete IoT suite that reverse-engineers undocumented hardware APIs to provide real-time tooling tracking and ETL inventory reporting.

* **The Engineering:** Consumes deeply nested, undocumented JSON payloads from Fuji NXT machine REST APIs. Translates internal hexadecimal machine codes into human-readable inventory SKUs. Serves this data asynchronously to a multithreaded `tkinter` desktop GUI, completely decoupling heavy network I/O from the user interface.
* **The Impact:** Replaced manual tooling searches, significantly reducing Single-Minute Exchange of Die (SMED) downtime during PCB changeovers. Now serves as the mandatory Standard Operating Procedure (SOP) for all operators.

### 3. [Orchestrator](/orchestrator) - *Temporal Data Synthesis Pipeline*

An automation engine designed to rapidly clone, offset, and inject inspection metadata into highly rigid legacy SQL databases.

* **The Engineering:** Parses CSV metadata via RegEx and manipulates temporal data using custom base-60 math functions. Implements strict Buffer Overflow Protection/Temporal Normalization by mathematically handling 24-hour epoch rollovers, ensuring simulated timestamps never crash the database ingestion engine.
* **The Impact:** Turns hours of manual data entry ("carpetazo") into a sub-second, error-free automated process.

### 4. [KeepAwake](/keepawake) - *Session Persistence Daemon*

A lightweight daemon designed to bypass aggressive global group policies (GPO) on factory floor terminals.

* **The Engineering:** Directly interacts with the Windows API via `kernel32\SetThreadExecutionState` (`0x00000002`). By programmatically asserting the `ES_DISPLAY_REQUIRED` flag, it mimics human presence without relying on simulated keystrokes or mouse wiggles.
* **The Impact:** Prevents critical monitoring dashboards from locking out operators during live production runs.

## Core Engineering Philosophies

* **Pragmatic Problem Solving:** Solutions are dictated by physical factory constraints (e.g., frozen UIs, physical tool searches, database crashes), not academic theory.
* **System Observability:** Creating transparency in undocumented or legacy systems where none previously existed.
* **Defensive Architecture:** Using temporal offsets, kernel suspension, and strict network timeouts to ensure high-assurance stability in chaotic environments.

## Getting Started

Each module is self-contained. To explore the code or deploy a specific tool, navigate to its respective directory and review its localized `README.md` for specific configuration, dependencies, and execution instructions.



