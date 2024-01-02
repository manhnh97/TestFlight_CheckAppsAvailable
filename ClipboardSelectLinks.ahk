F3:: Reload

F8::
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
    
    ; Define a regular expression pattern to capture the hashtag and TestFlight link
    pattern := "#.*\w"

    ; Use RegExMatch to extract the matched pattern from the input
    if (RegExMatch(input, pattern, match)) {
		Clipboard := match
    }

    if WinExist("ahk_exe Telegram.exe")
    {
        WinActivate ; Use the window found by WinExist.
        Sleep, 100
        Send, ^v
        Sleep, 100
        Send, {ENTER}
    }
    Return

F7::
	; Save the currently selected text to a variable
    Clipboard := ""  ; Clear the clipboard
    SendInput, ^c    ; Simulate Ctrl + C to copy selected text
    ClipWait, 1      ; Wait for 1 second for the clipboard to contain data

    Send, ^t
	Sleep, 100
	Send, ^v appstore{ENTER}
	return
