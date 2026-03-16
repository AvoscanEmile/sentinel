# keepawake

## The Problem: The GPO Labyrinth

In an industrial environment with two decades of operational history, system fragmentation is a significant challenge. This tool was developed to address a situation where multiple, conflicting Group Policy Objects (GPOs) from various legacy servers were active simultaneously on the same network.

The complexity of identifying which specific server imposed a lock policy—and the administrative difficulty of isolating mission-critical machines from these conflicting rules—created a situation where screen visibility could not be guaranteed through standard IT channels. When administrative intervention reached a bottleneck, a programmatic solution became necessary to ensure that essential production dashboards remained visible.

## The Solution: The Kernel Heartbeat

`keepawake` does not attempt to fight the Group Policy or modify the system registry. Instead, it bypasses the administrative layer by communicating directly with the Windows Power Management API.

By issuing a periodic "heartbeat" signal, the script informs the operating system that the display is actively required. This resets the local idle timer at a kernel level, preventing the screen from locking regardless of the conflicting GPOs being pushed to the machine from the legacy network.

## Technical Implementation

* **API Call**: Utilizes `SetThreadExecutionState` via `kernel32.dll`.
* **Flag**: Uses `0x00000002` (`ES_DISPLAY_REQUIRED`) to specifically reset the display idle timer.
* **Mechanism**: A lightweight loop pokes the OS every 45 seconds, ensuring that even aggressive GPO-enforced timeouts are never reached.
* **Minimal Impact**: This approach does not alter global power states or persistent settings; it simply resets the timer for as long as the script is active.

## Installation & Deployment

This tool is designed for flexible deployment across diverse industrial environments. Two primary methods are supported:

1. **Standalone Executable**: Use the `Ahk2Exe` compiler to package `keepawake.ahk` into a portable `.exe`. This is the recommended approach for mission-critical workstations or locked-down environments where installing a scripting runtime is not feasible or permitted.
2. **Script Execution**: Install the [AutoHotkey v2](https://www.autohotkey.com/) runtime and run `keepawake.ahk` directly. This allows for rapid iteration and transparency for users who wish to inspect the source logic before execution.

Both methods are fully valid and maintain the kernel-level heartbeat functionality.

## Controls

* **Startup**: Execute the file to initiate the heartbeat. A star icon will appear in the system tray to indicate that the tool is active and the idle timer is being managed.
* **Exit**: Press `Ctrl + Shift + E` to terminate the process and return the system to its default power management state.
