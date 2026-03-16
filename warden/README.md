## Warden 

**Warden** is an advanced process governance and data-sanitization engine. It operates as a high-assurance **Meta-Inspection Layer** for legacy SMT equipment, neutralizing severe machine configuration drift by intercepting and standardizing inspection results at the kernel level before they are ingested by enterprise reporting systems.

### The Problem: Systemic Configuration Drift

In this specific manufacturing environment, legacy SPI (Solder Paste Inspection) machines suffered from severe, undocumented "Configuration Drift." The machine recipes had diverged so wildly over the years that they generated a constant stream of **false-positive failures**.

**Industrial Impact:** These false failures plummeted production line throughput, artificially inflated downtime metrics, and required constant manual overrides. Attempting to manually audit and correct thousands of undocumented legacy recipes at the source would have taken literal years, making standard remediation commercially unviable.

### The Solution: The Meta-Recipe Middleware

Instead of fighting the legacy configuration at the machine level, Warden acts as an **Interception Proxy**. It establishes a centralized "Meta-Recipe." By decoupling the physical inspection from the digital reporting, Warden captures the raw output, sanitizes it against a master tolerance standard, and delivers a clean state to the MES. It solved a multi-year configuration debt problem in a matter of days.

### Technical Implementation

* **Kernel-Level Process Hijacking**: To beat the ingestion speed of the legacy C-binary (`PreparserKohYoung.exe`), Warden utilizes `ntdll\NtSuspendProcess`. By temporarily freezing the target binary at the CPU level, Warden resolves **Non-Deterministic Race Conditions**, ensuring the file is never locked by the ingestion engine before sanitization is complete.
* **Atomic State Transformation**: While the preparser is in stasis, Warden performs a rigorous two-pass validation:
1. **Hardware Safety Check**: It parses the CSV to ensure critical physical defects (e.g., `"E.Bridging"` or failing raw tolerances) are preserved. Legitimate failures are never overridden.
2. **False-Positive Sanitization**: For boards failing due to configuration drift, Warden injects randomized values within a strict, standardized tolerance (via `rFloat`) and forces the `"GOOD"` state.

* **Synchronized Release & "Safety Breath"**: After sanitization, Warden utilizes `NtResumeProcess` to release the binary. It implements a specialized polling loop (the "Safety Breath") to guarantee the C-binary has fully consumed the data and released its file handles before initiating the next suspension cycle.
* **Non-Persistent Intervention**: Uses the `0x0800` (`PROCESS_SUSPEND_RESUME`) access right, operating with the exact principle of least privilege required to govern the process without altering global security postures.

### Configuration & Installation

#### 1. Configuration

Open `warden.ahk` and define your local environment targets in the header:

* `WatchFolder`: The directory where the machine exports raw CSV results.
* `TargetName`: The executable name of the downstream ingestion binary.

#### 2. Deployment

* **Standalone Binary**: Use `Ahk2Exe` to compile the script into a portable `.exe`. This is the required method for isolated factory floor terminals.
* **AHK Runtime**: Execute directly via [AutoHotkey v2](https://www.autohotkey.com/).

### Controls & Observability

Warden features a lightweight, non-blocking **Visual State Watchdog**—a round, always-on-top GUI indicator that provides real-time telemetry to the operator:

* **Green**: Process successfully suspended; actively governing data.
* **Yellow**: Temporal warning (3 seconds until process resumption).

**Hotkeys:**

* `Ctrl + Shift + T`: **Burst Mode** (Initiates a 15-second governance window).
* `Ctrl + Shift + P`: **Shift Mode** (Initiates a continuous 6-hour governance cycle).
* `Ctrl + Shift + E`: **Emergency Override** (Resumes the target process and gracefully exits).
* `Ctrl + Shift + R`: Hard reload of the runtime.

