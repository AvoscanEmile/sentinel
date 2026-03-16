## Nozzle Suite 

**Tech Stack:** `Python 3` | `Multithreading` | `REST APIs` | `tkinter` | `ETL Pipelines` | `IoT Telemetry`

**Nozzle Suite** is a real-time IoT tooling dashboard and automated ETL inventory pipeline for Fuji NXT SMT machines. It was engineered to eliminate critical bottlenecks during high-frequency PCB changeovers by providing operators with a multithreaded, real-time "radar" for physical machine tooling.As well as automating the inventory process for this expensive tooling. 

### The Problem: Changeover Downtime & Inventory Blind Spots

In high-mix manufacturing, PCB changeovers occur multiple times a day. Each recipe changeover requires specific nozzles (micro-tooling). Previously, locating the exact physical location of these tools across multiple factory lanes was a manual, error-prone process that significantly increased machine downtime. Additionally, the factory lacked any automated inventory tracking system for this highly specialized, expensive hardware.

### The Solution: Real-Time IoT Telemetry

Rather than relying on manual searches, **Nozzle Suite** interfaces directly with the undocumented REST APIs of the Fuji NXT machines. It aggregates live hardware telemetry, translating internal machine codes into human-readable inventory SKUs, and serves this data to technicians via a zero-latency, multithreaded desktop dashboard.

### Technical Highlights

* **Undocumented API Reverse-Engineering:** The Fuji API returned deeply nested, undocumented JSON structures. This project required manually reverse-engineering the payload, mapping internal hexadecimal machine codes (`H16`) to physical factory SKUs (`R047-010-035`) to create a relational translation matrix.
* **Concurrency & Non-Blocking UI:** Designed with Python's `threading` module to decouple heavy network I/O from the main GUI loop. This ensures the dashboard remains responsive even if a machine drops from the network or a request times out.
* **Complex Data Aggregation:** Utilizes hierarchical data structures (nested `defaultdict`s) to dynamically sort telemetry into a `Head Type -> Nozzle Size -> Machine Lane -> Module` schema in real-time.

### Core Architecture

The suite is structured as a modular Python package, separating data mapping, real-time UI, and ETL reporting:

* **`nozzle_mapping.py` (Single Source of Truth)**
Acts as the master translation matrix. It establishes a centralized configuration for the entire suite, ensuring that if a hardware SKU changes, it only needs to be updated in one place.
* **`nozzle_search.pyw` (Real-Time Changeover Dashboard)**
A multithreaded `tkinter` desktop application that serves as the primary operational tool for technicians.
* **Asynchronous I/O:** Network requests run on background threads with strict timeouts to prevent UI locking.
* **Predictive State Warning (`?` Flag):** Analyzes the machine's active job recipe (`JobUse` vs `NzlPosition`). If a nozzle is physically present but currently unassigned, the system flags it with a `?`. This acts as a critical warning to technicians: *"The machine is not currently using this, but the active recipe still expects it to be here. Do not remove."*


* **`nozzle_counter.py` (ETL Inventory Pipeline)**
A spin-off of the core telemetry logic. This script runs an asynchronous Extract, Transform, and Load (ETL) process to audit the exact count of every nozzle currently loaded in the factory, outputting a timestamped CSV report for daily inventory management.

### Business Impact

* **SMED / Downtime Reduction:** Fully automated the tooling search process, drastically reducing PCB changeover times and eliminating the "Where is this tool?" bottleneck.
* **100% SOP Adoption:** `nozzle_search.pyw` completely replaced the manual search process and remains the mandatory Standard Operating Procedure (SOP) for all technicians on the floor today.
* **Automated Auditing:** Transformed a non-existent inventory tracking process into a single-click, highly accurate automated report.

### Configuration, Deployment & Usage

Requires Python 3.x and the `requests` library.

#### 1. Environment Configuration

Before deploying, you **must** tailor the Single Source of Truth to your factory's specific layout. Open `nozzle_mapping.py` and modify the environment constants:

* `MACHINE_LIST` & `MACHINE_DICT`: Update these placeholders with your actual Fuji NXT machine hostnames/IPs and their corresponding physical factory lanes.
* `HEAD_DICT`: Adjust to match your specific machine head configurations.
* *Note: The `NOZZLE_DICT` contains highly accurate, reverse-engineered baseline SKU mappings for Fuji hardware and will likely work out-of-the-box, but should be verified against your local inventory.*

#### 2. Execution

```bash
# Install dependencies
pip install requests

# Launch the real-time Operator Dashboard (background process)
pythonw nozzle_search.pyw

# Run a point-in-time Inventory ETL Audit (CLI)
python nozzle_counter.py

```
