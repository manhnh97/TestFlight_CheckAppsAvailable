F3:: Reload

F8::
	Click, 3
	Sleep, 150
    ; Save the currently selected text to a variable
    Clipboard := ""  ; Clear the clipboard
    SendInput, ^c    ; Simulate Ctrl + C to copy selected text
    ClipWait, 1      ; Wait for 1 second for the clipboard to contain data

    ; Check if text is copied successfully
    If ErrorLevel
    {
        MsgBox, No text was selected!
        Return
    }
    
    ; Save the copied text into a variable
    input := Clipboard
    
    ; Define a regular expression pattern to capture the hashtag and TestFlight link
    pattern := "#.*\w"

    ; Use RegExMatch to extract the matched pattern from the input
    if (RegExMatch(input, pattern, match)) {
		; Use RegExReplace to remove square brackets and extract the data
		pattern1 := "<br />"
        extracted_text := RegExReplace(match, pattern1, "`n`n")
			Clipboard := extracted_text
    }
	
    if WinExist("ahk_exe Telegram.exe")
    {
        WinActivate, "ahk_exe Telegram.exe" ; Use the window found by WinExist.
		WinWaitActivate, "ahk_exe Telegram.exe"
        Sleep, 100
        Send, ^v
        Sleep, 100
        Send, {ENTER}
    }
    Return

F6::
    Click, 3
	Sleep, 150
    ; Save the currently selected text to a variable
    Clipboard := ""  ; Clear the clipboard
    SendInput, ^c    ; Simulate Ctrl + C to copy selected text
    ClipWait, 1      ; Wait for 1 second for the clipboard to contain data

    ; Check if text is copied successfully
    If ErrorLevel
    {
        MsgBox, No text was selected!
        Return
    }
    
    ; Save the copied text into a variable
    input := Clipboard

    ; Define a regular expression pattern to capture text within square brackets and remove the brackets
    patternGetName := "\*\*(.*)\*\*"
	
    ; Use RegExMatch to extract the matched pattern from the input
    if (RegExMatch(input, patternGetName, Name)) {
		; Define a regular expression pattern to capture text within square brackets and remove the brackets
        pattern := "\*"
        
        ; Use RegExReplace to remove square brackets and extract the data
        extracted_text := RegExReplace(Name, pattern)
        ; Add " appstore" to the extracted text
        Clipboard := extracted_text . " appstore"
    }
	
	Send, ^{t}
	Sleep, 100
	Send, ^{v}
	Sleep, 50
	Send, {ENTER}
    return

F7::
    Click, 3
	Sleep, 150
    ; Save the currently selected text to a variable
    Clipboard := ""  ; Clear the clipboard
    SendInput, ^c    ; Simulate Ctrl + C to copy selected text
    ClipWait, 1      ; Wait for 1 second for the clipboard to contain data

    ; Check if text is copied successfully
    If ErrorLevel
    {
        MsgBox, No text was selected!
        Return
    }
    
    ; Save the copied text into a variable
    input := Clipboard

    ; Define a regular expression pattern to capture text within square brackets and remove the brackets
    patternGetName := "https?.* "
	
    ; Use RegExMatch to extract the matched pattern from the input
    if (RegExMatch(input, patternGetName, testflight_link)) {
		
        Clipboard := testflight_link
    }
	
	Send, ^{t}
	Sleep, 100
	Send, ^{v}
	Sleep, 50
	Send, {ENTER}
	
    return
