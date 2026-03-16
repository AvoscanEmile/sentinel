#Requires AutoHotkey v2.0
#SingleInstance Force

/**
 * Sentinel | Orchestrator
 * High-assurance temporal data synthesis for SMT inspection results.
 */

; --- Configuration ---
Source := "Source/File/Folder/Example"
Target := "Target/File/Folder/Example"
Temp   := A_ScriptDir "\temp\"

; --- Main Automation ---
^+K::
{
    ; Ensure the relative temp folder exists
    if !DirExist(Temp)
        DirCreate(Temp)

    ; 1. Select Reference File
    SourceFile := FileSelect(1, Source, , "All files (*.*)")
    if (SourceFile = '') {
        MsgBox "No se eligio un archivo base. Por favor seleccione un archivo base."
        Reload
    }

    ; 2. Collect Target Serials
    Prompt := "Escriba los serial de las tablillas para darles proceso.`n" 
            . "Enlistelos separandolos por coma y espacio (e.g. ECBD123, XILC345)."
    TargetBarcodes := InputBox(Prompt, "KOH-YOUNG Carpeteo Automatico", "w290 h180")

    if (TargetBarcodes.Result = "Cancel" OR TargetBarcodes.Value = "") {
        MsgBox "No se introdujo ninguna serial. Es necesario introducir seriales para darles proceso."
        Reload
    }

    ; 3. Extract Source Metadata
    Loop Files SourceFile {
        SourceTitle := A_LoopFileName
        titleArray := StrSplit(SourceTitle, "_")
        SourceNumber := titleArray[1]
    }

    openSource := FileOpen(SourceFile, "rw")
    sourceString := openSource.Read()
    
    ; Extract original timestamps via RegEx
    RegExMatch(sourceString, "\d\d:\d\d:\d\d,\d\d:\d\d:\d\d", &clock)
    sourceClock := clock[]
    splitedClock := StrSplit(sourceClock, ",")
    
    sourceStartTime  := splitedClock[1]
    sourceFinishTime := splitedClock[2]
    
    sourceStartSec  := clockTSec(sourceStartTime)
    sourceFinishSec := clockTSec(sourceFinishTime)

    ; 4. Synthesis Loop
    TBArray := StrSplit(TargetBarcodes.Value, ", ")
    
    Loop TBArray.length
    {
        ; Create a new filename and copy base file to temp
        newName := StrReplace(SourceTitle, SourceNumber, TBArray[A_Index])
        FileCopy(SourceFile, Temp . newName, 1)
        
        tempFile := FileOpen(Temp . newName, "rw")
        fileString := tempFile.Read()
        
        ; Replace Serial ID
        newFile := StrReplace(fileString, SourceNumber, TBArray[A_Index])
        
        ; Calculate 7-second temporal offset to prevent DB collisions
        newStart  := sourceStartSec  + (A_Index * 7)
        newFinish := sourceFinishSec + (A_Index * 7)
        
        newStartClock  := secTClock(newStart)
        newFinishClock := secTClock(newFinish)
        
        ; Inject new timestamps
        newFile1 := StrReplace(newFile, sourceStartTime, newStartClock)
        newFile2 := StrReplace(newFile1, sourceFinishTime, newFinishClock)
        
        tempFile.Seek(0, 0)
        tempFile.Write(newFile2)
        tempFile.Close()
    }

    ; 5. Deploy to Ingestion Pipeline
    Loop Files Temp . "*.csv" {
        FileMove(A_LoopFilePath, Target)
        Sleep(20) ; Safety buffer for high-velocity preparser handles
    }

    MsgBox "Programa terminado. Se le dio proceso a " . TBArray.length . " seriales."
}

; --- Helper Functions ---

; Converts HH:MM:SS string to total seconds.
clockTSec(string) {
    splitClock := StrSplit(string, ":") 
    seconds := (splitClock[1] * 3600) + (splitClock[2] * 60) + splitClock[3] 
    return seconds
}


; Converts seconds to HH:MM:SS string, handling 24h roll-over.
secTClock(n) {
    while (n > 86399) {
        n -= 86400
    }
    
    H  := Format("{:02}", n // 3600)
    HR := Mod(n, 3600)
    M  := Format("{:02}", HR // 60)
    S  := Format("{:02}", Mod(HR, 60))
    
    return H . ":" . M . ":" . S 
}
