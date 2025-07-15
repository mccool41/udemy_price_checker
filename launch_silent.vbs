Set shell = CreateObject("WScript.Shell") 
currentDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
batchFile = currentDir & "\run_price_checker.bat"
shell.Run Chr(34) & batchFile & Chr(34), 0
Set shell = Nothing