## Orchestrator

**Orchestrator** is a high-assurance temporal data synthesis tool designed for SMT (Surface Mount Technology) manufacturing environments. It automates the recovery of missing inspection data by programmatically generating valid, time-shifted results based on a single "Golden" reference file.

### The Problem: MES Synchronization Gaps

In high-velocity production lines, proprietary inspection hardware sometimes fails to hand off data to the **Manufacturing Execution System (MES)**. When this synchronization breaks, a "Data Gap" occurs: the board is physically inspected and passed, but no digital record exists.

**Industrial Impact:** Historically, this forced the factory to either scrap functional hardware or issue manual quality deviations—both of which are costly, labor-intensive, and disruptive to production throughput.

### The Solution: Temporal Synthesis

Orchestrator resolves these gaps by "manufacturing time." It takes a validated reference inspection result and synthesizes a batch of new results for the missing serial numbers.

To bypass the aggressive verification logic of legacy servers, the tool implements **Temporal Interpolation**: it adds a calculated 7-second offset to each board in the batch (`A_Index * 7`). This prevents "Duplicate Timestamp" collisions in the database while maintaining a realistic production cadence.

### Technical Implementation

* **Atomic Buffer Management**: Utilizes a **Relative Temp Folder** for staging. This is critical because the downstream ingestion engine is a high-velocity C-binary (hot-folder watcher) with sub-millisecond consumption speed. Processing in a local `temp` directory ensures the engine never captures a partial or corrupted file handle.
* **State Recovery & Logic**: Converts `HH:MM:SS` strings to total seconds for arithmetic operations and re-encodes them, handling **24-hour rollover logic** to prevent data from drifting into the next calendar day.
* **RegEx Metadata Extraction**: Uses Regular Expressions to dynamically identify and extract original start/finish timestamps from proprietary CSV structures.
* **I/O Synchronization**: Implements a 20ms sleep cycle during the final `FileMove` to ensure the file system has fully released the file handle before the ingestion engine attempts to lock it.

### Configuration & Installation

#### 1. Configuration

Open `orchestrator.ahk` and define your environment paths:

* `Source`: Folder containing "Reference" or "Golden" files.
* `Target`: The ingestion point monitored by the MES-integration software.
* `Temp`: Set to `A_ScriptDir "\temp\"` by default for portability.

#### 2. Deployment

* **Standalone Binary**: Use `Ahk2Exe` to compile into a portable `.exe` (recommended for production).
* **AHK Runtime**: Run directly via [AutoHotkey v2](https://www.autohotkey.com/).

### Usage

1. **Launch** the script/binary.
2. **Trigger**: Press `Ctrl + Shift + K`.
3. **Selection**: Choose a "Good" reference file to act as the template.
4. **Input**: Provide the list of missing serial numbers (comma-separated).
5. **Execution**: The tool synthesizes data in `temp` and deploys it to the `Target` for immediate MES ingestion.

