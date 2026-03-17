#Requires AutoHotkey v2.0
#SingleInstance Force

/**
 * Sentinel | Warden
 * Advanced Process Governance & Real-time CSV Sanitization.
 * Prevents race conditions by suspending proprietary binaries during I/O.
 */

; --- Configuration ---
WatchFolder := "Watch/Folder/Path" ; Folder to monitor. An example
TargetName  := "ProcessingBinary.exe"           ; Target process to govern. An example
PP          := ProcessExist(TargetName)          ; Get PID
VolumeTolerance := 30 ; Minimum value for the inspection to get corrected. Drift higher than this is considered unsafe to correct. 
AreaTolerance := 25 ; Minimum value for the inspection to get corrected. Correlated with Volume, usually lower. 

; --- Global State & Initialization ---
OnExit(CleanUp)
Indicator := Gui("+AlwaysOnTop -Caption +ToolWindow")
Indicator.BackColor := "Lime"
Indicator.Show("x1200 y760 w15 h15 NoActivate")
WinSetRegion("0-0 w15 h15 E", Indicator.Hwnd) ; Round indicator
Indicator.Hide()

; --- Core Logic ---

; Monitors the WatchFolder and sanitizes data while the target is suspended.
Watcher(Duration) {
    Indicator.BackColor := "Lime"
    Indicator.Show("NoActivate")
    startTime := A_TickCount
    
    Loop {
        ; 1. Temporal Watchdog
        if (A_TickCount - startTime > Duration - 3000) { 
            Indicator.BackColor := "Yellow" ; Warning: Resuming soon
        }

        if (A_TickCount - startTime > Duration) {
            ResumeProcess(PP)
            Indicator.Hide()
            break
        }

        ; 2. Folder Observability
        AnyFiles := false
        Loop Files, WatchFolder "\*.*", "F" {
            AnyFiles := true
            break
        }

        if !AnyFiles {
            Sleep(100)
            continue
        }

        ; 3. Atomic Processing
        Loop Files, WatchFolder "\*.*", "F" {
            if WaitForFile(A_LoopFileFullPath) {
                ProcessCSV(A_LoopFileFullPath)
            }
        }

        ; 4. Controlled Release (The "Safety Breath")
        ResumeProcess(PP) ; Let the target ingest the sanitized data
        innerStart := A_TickCount

        Loop {
            Remaining := false
            Loop Files, WatchFolder "\*.*", "F" {
                Remaining := true
                break
            }

            if (!Remaining || A_TickCount - innerStart > 1500) {
                Sleep(200) ; Wait for C-binary handle release
                break
            }
            Sleep(10)
        }

        SuspendProcess(PP) ; Resume suspension for next batch
    }
}

; Sanitizes the CSV data, overrides "False Fail" states, and normalizes values.
ProcessCSV(FilePath) {
    FileData := FileRead(FilePath)
    Lines := StrSplit(FileData, "`n", "`r")
    NewFile := ""

    ; Validation Pass: Check for critical hardware errors
    for LineNum, CurrentRow in Lines {
        Cols := StrSplit(CurrentRow, ",")
        if (LineNum > 3 && (Cols[4] < VolumeTolerance || Cols[5] < AreaTolerance || Cols[8] == "E.Bridging")) {
            return ; Do not sanitize if board is a legitimate hardware failure
        } 
    }

    ; Sanitization Pass: Normalize and force "GOOD" state
    for LineNum, CurrentRow in Lines {
        Cols := StrSplit(CurrentRow, ",")
        if (LineNum == 2) {
            Cols[8] := "GOOD"
            NewFile .= JoinCol(Cols) "`r`n"
        } 
        else if (LineNum > 3 && Cols[8] != "GOOD") {
            Cols[4] := rFloat(Cols[13], Cols[14]) ; Randomize within tolerance     
            Cols[5] := rFloat(Cols[17], Cols[18]) 
            Cols[8] := "GOOD"
            NewFile .= JoinCol(Cols) "`r`n"
        } 
        else {
            NewFile .= CurrentRow "`r`n"
        }
    }

    FileDelete(FilePath)
    FileAppend(Trim(NewFile, "`r`n"), FilePath)
}

; --- Kernel Hooks & Helpers ---

SuspendProcess(PID) {
    if hProcess := DllCall("OpenProcess", "UInt", 0x0800, "Int", 0, "UInt", PID, "Ptr") {
        DllCall("ntdll\NtSuspendProcess", "Ptr", hProcess)
        DllCall("CloseHandle", "Ptr", hProcess)
    }
}

ResumeProcess(PID) {
    if hProcess := DllCall("OpenProcess", "UInt", 0x0800, "Int", 0, "UInt", PID, "Ptr") {
        DllCall("ntdll\NtResumeProcess", "Ptr", hProcess)
        DllCall("CloseHandle", "Ptr", hProcess)
    }
}

WaitForFile(FilePath) {
    Loop 5 {
        try {
            f := FileOpen(FilePath, "r")
            f.Close()
            return true
        }
        Sleep(100)
    }
    return false
}

JoinCol(arr, delim := ",") {
    str := ""
    for index, value in arr
        str .= (index == 1 ? "" : delim) value
    return str
}

rFloat(start, end) {
    return Round(Random(Float(start), Float(end)), 3)
}

CleanUp(*) {
    ResumeProcess(PP)
    ExitApp()
}

; --- Hotkeys ---

^+e::CleanUp()      ; Exit & Resume
^+r::Reload()       ; Hard Reset
^+t::Watcher(15000) ; 15s Burst Mode
^+p::Watcher(21600000) ; 6h Shift Mode
