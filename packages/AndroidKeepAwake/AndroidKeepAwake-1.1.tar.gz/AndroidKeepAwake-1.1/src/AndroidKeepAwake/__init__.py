from kivy import platform, Logger

if platform == "android":
    try:
        from jnius import autoclass, cast, PythonJavaClass, java_method
        from android.runnable import run_on_ui_thread

        activity = autoclass("org.kivy.android.PythonActivity")
        View = autoclass('android.view.View')
        Params = autoclass('android.view.WindowManager$LayoutParams')

    except Exception as err:
        Logger.error("KeepAwake: " + str(err))
else:

    def run_on_ui_thread(x):
        pass


class WakeLockBridge:
    def __init__(self):
        pass

    def android_setflag(self):
        pass

    def android_clearflag(self):
        pass


class WakeLock(WakeLockBridge):
    @run_on_ui_thread
    def __init__(self):
        super().__init__()
        Logger.info("KeepAwake: __init__ called.")

    @run_on_ui_thread
    def android_setflag(self):
        activity.mActivity.getWindow().addFlags(Params.FLAG_KEEP_SCREEN_ON)
        Logger.info("KeepAwake: android_setflag called.")

    @run_on_ui_thread
    def android_clearflag(self):
        activity.mActivity.getWindow().clearFlags(Params.FLAG_KEEP_SCREEN_ON)
        Logger.info("KeepAwake: android_clearflag called.")


class AndroidKeepAwake:
    def __init__(self):
        if platform == "android":
            # Setting below to True, will override your appID and bannerID to use test ads :)
            self.bridge = WakeLock()
        else:
            Logger.warning("KeepAwake: This only runs on Android devices")

    def android_setflag(self):
        if platform == "android":
            self.bridge.android_setflag()

    def android_clearflag(self):
        if platform == "android":
            self.bridge.android_clearflag()
