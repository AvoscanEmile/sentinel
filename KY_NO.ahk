#Requires AutoHotkey v2.0
#SingleInstance Force

; --- NoLock ---

WatchFolder := "C:\Kohyoung\KY-3030\AutoExport"
TargetName  := "PreparserKohYoung.exe"

PP := ProcessExist(TargetName)
OnExit(CleanUp)

Indicator := Gui("+AlwaysOnTop -Caption +ToolWindow")
Indicator.BackColor := "Lime"
Indicator.Show("x1200 y760 w15 h15 NoActivate")
WinSetRegion("0-0 w15 h15 E", Indicator.Hwnd)
Indicator.Hide()

Watcher(Duration) {
    Indicator.BackColor := "Lime"
    Indicator.Show("NoActivate")
    startTime := A_TickCount
    Loop {

	if (A_TickCount - startTime > Duration - 3000) { 
		Indicator.BackColor := "Yellow"
	}

	if (A_TickCount - startTime > Duration) {
		ResumeProcess(PP)
		Indicator.Hide()
		break
	}

        ; Check if folder is empty (optimized)
        AnyFiles := false
        Loop Files, WatchFolder "\*.*", "F" {
            AnyFiles := true
            break
        }

        if !AnyFiles {
            Sleep(100)
            continue
        }

        ; Process everything in the Folder
        Loop Files, WatchFolder "\*.*", "F" {
            if WaitForFile(A_LoopFileFullPath) {
                ProcessCSV(A_LoopFileFullPath)
            }
        }

        ResumeProcess(PP)
        innerStart := A_TickCount

        Loop {
            Remaining := false
            Loop Files, WatchFolder "\*.*", "F" {
                Remaining := true
                break
            }

            if !Remaining {
                Sleep(200) ; The "Safety Breath" for C-cleanup
                break
            }

            if (A_TickCount - innerStart > 1500) {
                break
            }
            Sleep(10)
        }

        SuspendProcess(PP)
    }
}

ProcessCSV(FilePath) {
    FileData := FileRead(FilePath)
    Lines := StrSplit(FileData, "`n", "`r")
    NewFile := ""

    for LineNum, CurrentRow in Lines {
        Cols := StrSplit(CurrentRow, ",")
        if (LineNum > 3 && (Cols[4] < 20 || Cols[5] < 10 || Cols[8] == "E.Bridging"))  {
		return
        } 
    }

    for LineNum, CurrentRow in Lines {
        Cols := StrSplit(CurrentRow, ",")
        if (LineNum == 2) {
            Cols := StrSplit(CurrentRow, ",")
            Cols[8] := "GOOD"
            NewFile .= JoinCol(Cols) "`r`n"
        } 
        else if (LineNum > 3 && Cols[8] != "GOOD") {
            Cols[4] := rFloat(Cols[13], Cols[14])     
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

; --- Helper Functions ---

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

CleanUp(*) {
    ResumeProcess(PP)
    ExitApp()
}

rFloat(start, end) {
    return Round(Random(Float(start), Float(end)),3)
}

; --- Hotkeys ---

^+e::CleanUp()
^+t:: { 
SuspendProcess(PP)
Watcher(15000)
}
^+r:: { 
ResumeProcess(PP)
Reload
}
^+p:: { 
SuspendProcess(PP)
Watcher(21600000)
}