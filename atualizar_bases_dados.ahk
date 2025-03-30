#Requires AutoHotkey v2.0
#SingleInstance Force

roda_codigo_python(){
    ; path to Python interpreter
    pythonPath := "`"C:/Program Files/Python313/python.exe`""

    ; path to Python script
    scriptPath := "`"C:/Users/ricardopeloi/OneDrive - falconi365/Data Science/O_Mais_Novo_Day_Trader_do_Brasil/o_mais_novo_day_trader_do_brasil/main.py`""

    RunWait pythonPath . "" . " " . "" . scriptPath . " & cmd /k" 
}


^F1::
{
roda_codigo_python

; SetTimer roda_codigo_python, 24*60*60*1000 ; Uma vez por dia
; SetTimer roda_codigo_python, 60*1000 ; Uma vez por minuto
; SetTimer roda_codigo_python, 3*60*1000 ; Uma vez a cada 3 minutos
SetTimer roda_codigo_python, 60*60*1000 ; Uma vez por hora
return
}