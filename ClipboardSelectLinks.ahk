F3:: Reload

; For gSheet camping
F6:: 
	Send, +{RIGHT}^{c}
	sleep, 100
	Send, ^{UP}
	sleep, 100
	Send, ^{UP}
	sleep, 100
	send, {DOWN}
	sleep, 100
	Send, ^{v}
	sleep, 100
	Send, {RIGHT}
	sleep, 100
	send, {RIGHT}
	sleep, 80
	Send, c
	sleep, 80
	send, {LEFT}
	sleep, 80
	send, ^{c}
	sleep, 200
	Send, ^{f}
	sleep, 200
	Send, ^{v}
	sleep, 100
	send, {ENTER}
	sleep, 100
	Send, {ESC}
	sleep, 50
	SendInput, {WheelDown}
	return

; Close Tab
F7::
	send, ^{w}
	
    return

; gSheet search app store
F8::
    Click, 1
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

	; Add " appstore" to the extracted text
	Clipboard := input . " appstore"
	
	Send, ^{t}
	Sleep, 100
	Send, ^{v}
	Sleep, 50
	Send, {ENTER}
    return

; For Telegram format
F9::
    Clipboard := ""  
    Click, 3
    Sleep, 50

    ; Save the currently selected text to a variable
    SendInput, ^c    
    ClipWait, 1      

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
        
    ; Ensure the window title is correct
    WinTitle := "ahk_exe Telegram.exe"
    
    ; Check if the Telegram window exists
    if WinExist(WinTitle)
    {
        ; Activate the Telegram window
		WinActivate, %WinTitle%
        WinWaitActive, %WinTitle%
        Sleep, 100
        
        ; Paste the modified text and press Enter
        Send, ^v
        Sleep, 100
        Send, {ENTER}
    }
    Return

; gAppstore
F10::
    Click, 3
	Sleep, 50
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
        Clipboard := extracted_text . " app store"
    }
	
	Send, ^{t}
	Sleep, 100
	Send, ^{v}
	Sleep, 50
	Send, {ENTER}
    return

; glinks
F11::
    Click, 3
	Sleep, 50
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