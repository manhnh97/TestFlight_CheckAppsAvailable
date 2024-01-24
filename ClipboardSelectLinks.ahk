F3:: Reload

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

F7::
	send, ^{w}
	
    return

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