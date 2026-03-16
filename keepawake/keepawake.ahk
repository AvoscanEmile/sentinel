#Requires AutoHotkey v2.0
#SingleInstance Force

/**
 * Sentinel Heartbeat
 * Uses SetThreadExecutionState to reset the display idle timer.
 * 0x00000002 = ES_DISPLAY_REQUIRED
 */

; Minimalist Tray Icon to show it's active
TraySetIcon("shell32.dll", 44) ; The 'Star' icon

Loop {
    ; DllCall to kernel32
    ; This tells Windows: "Someone is still looking at this screen."
    DllCall("kernel32\SetThreadExecutionState", "UInt", 0x00000002)
    
    ; Wait 45 seconds before poking the OS again
    ; Most GPO-enforced locks happen at 1, 5, or 10 minutes.
    Sleep(45000) 
}

; Exit the script: Ctrl + Shift + E
^+e::ExitApp()
