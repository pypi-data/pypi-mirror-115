# AndroidKeepAwake

Keep your Android device awake when running Kivy Apps

## Example usage

```
class Screen1(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.myApp = AndroidKeepAwake()
        
    def on_enter(self):
        # Turn on AndroidKeepAwake on Enter
        self.myApp.android_setflag()

    def on_leave(self, *args):
        # Turn off AndroidKeepAwake on Leave
        self.myApp.android_clearflag()
```