import win32com.client

word = win32com.client.Dispatch("Word.Application")
word.Visible = True
word.WindowState = 1
word.Activate()

doc = word.Documents.Add()
word.ActiveWindow.Activate()

print("Word opened and activated.")