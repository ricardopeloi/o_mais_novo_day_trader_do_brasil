^F1::
{
#Requires AutoHotkey v2.0
#SingleInstance Force
; Persistent

roda_codigo_python

; https://www.autohotkey.com/board/topic/35626-auto-launch-a-program-at-a-certain-time/
SetTimer WorkProgram, 1000

WorkProgram(){
   If (A_Hour = 9 && A_WDay = 1) {
    SetTimer WorkProgram, 0
    roda_codigo_python
    SetTimer WorkProgram, 1000
   }
; return
}

roda_codigo_python(){
    ; Define the path to your Python interpreter (adjust if needed)
    pythonPath := "`"C:/Program Files/Python313/python.exe`""

    ; Define the path to your Python script
    scriptPath := "`"C:/Users/ricardopeloi/OneDrive - falconi365/Data Science/O_Mais_Novo_Day_Trader_do_Brasil/o_mais_novo_day_trader_do_brasil/main.py`""

    RunWait pythonPath . "" . " " . "" . scriptPath . " & cmd /k" 
}

return
}