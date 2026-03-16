#Requires AutoHotkey v2.0
#SingleInstance Force

Source := "C:\Kohyoung\Preparser\InputFiles"
Temp := "C:\Users\aSpire3\Documents\KY_UTILS\temp\"
Target := "C:\Kohyoung\KY-3030\AutoExport"

clockTSec(string) {
splitClock := StrSplit(string, ":") 
seconds := (splitClock[1] * 3600) + (splitClock[2] * 60) + splitClock[3] 
return seconds
}

secTClock(n) {
loop {
if (n > 86399) {
n := n - 86400
continue
} else {
break
}
}
H := format("{:02}", n//3600)
HR := Mod(n, 3600)
M := format("{:02}", HR//60)
S := format("{:02}", Mod(HR, 60))
clock := H . ":" . M . ":" . S 
return clock
}

^+K::
{
SourceFile := FileSelect(1, Source, ,"All files (*.*)")
if (SourceFile = '') {
MsgBox "No se eligio un archivo base. Por favor seleccione un archivo base."
Reload
}
TargetBarcodes := InputBox("Escriba los serial de las tablillas para darles proceso, si es mas de un serial enlistelos separandolos por una coma y un espacio (ECBD123456, XILC345698, ZEBD239845, etc.).", "KOH-YOUNG Carpeteo Automatico", "w290 h180")
if (TargetBarcodes.Result = "Cancel" OR TargetBarcodes.Value = "") {
MsgBox "No se introdujo ninguna serial. Es necesario introducir seriales para darles proceso"
Reload
}
Loop Files SourceFile {
SourceTitle := A_LoopFileName
titleArray := StrSplit(SourceTitle, "_")
SourceNumber := titleArray[1]
}

openSource := FileOpen(SourceFile, "rw")
sourceString := openSource.Read()
RegExMatch(sourceString, "\d\d:\d\d:\d\d,\d\d:\d\d:\d\d", &clock)
sourceClock := clock[]
splitedClock := StrSplit(sourceClock, ",")
sourceStartTime := splitedClock[1]
sourceFinishTime := splitedClock[2]
sourceStartSec := clockTSec(sourceStartTime)
sourceFinishSec := clockTSec(sourceFinishTime)

TBArray := StrSplit(TargetBarcodes.Value, ", ")
Loop TBArray.length
{
newName := StrReplace(SourceTitle, SourceNumber, TBArray[A_Index])
FileCopy SourceFile, Temp . newName, 1
tempFile := FileOpen(Temp . newName, "rw")
fileString := tempFile.Read()
newFile := StrReplace(fileString, SourceNumber, TBArray[A_Index])
newStart := sourceStartSec+(A_Index*7)
newFinish := sourceFinishSec+(A_Index*7)
newStartClock := secTClock(newStart)
newFinishClock := secTClock(newFinish)
newFile1 := StrReplace(newFile, sourceStartTime, newStartClock)
newFile2 := StrReplace(newFile1, sourceFinishTime, newFinishClock)
tempFile.Seek(0, 0)
tempFile.write(newFile2)
tempFile.close()
}

Loop Files Temp . "*.csv" {
FileMove A_LoopFilePath, Target
Sleep 20 
}

MsgBox "Programa terminado. Se le dio proceso a " . TBArray.length . " seriales."
}	