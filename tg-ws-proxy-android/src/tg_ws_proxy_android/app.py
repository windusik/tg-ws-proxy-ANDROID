"""
WebSocket proxy for Telegram, based on Flowseal's solution
"""

import toga
from toga import validators
from concurrent.futures import Future
import tg_ws_proxy_android.proxy_backend.tg_ws_proxy_NEW as backend
from toga.style.pack import COLUMN, ROW


class TelegramWSProxyforAndroid(toga.App):
    port = 1080
    host = "127.0.0.1"
    dc_ip = ["2:149.154.167.220", "4:149.154.167.220"]
    proxy_launched = False
    proxy = None
    completion_future = Future()
    def met(self, bool_iter, ifnot):
        for b in bool_iter:
            if not b:
                return ifnot
        return None
    def apply_dcip(self, dcip):
        self.dc_ip = dcip.value.split(";")
        print(self.dc_ip)
    def apply_port(self, port):
        self.port = int(port.value)
    def apply_host(self, host):
        self.host = host.value
    def startup(self):
        async def do_proxy_stuff(btn):
            if not self.proxy_launched:
                self.apply_dcip(dcip_inp)
                self.apply_port(port_inp)
                command = ["--host", self.host, "--port", str(self.port)]
                for ip in self.dc_ip:
                    command.append("--dc-ip")
                    command.append(ip)
                self.proxy = backend.main(command)
                self.proxy_launched = True
            else:
                if self.proxy:
                    backend.STOP_EVENT.set()
                    self.proxy = None
                    self.proxy_launched = False
                    backend.STOP_EVENT.clear()
                    print("PROXY OFF")
            btn.text=f"{'Turn proxy OFF' if self.proxy_launched else 'Turn proxy ON'}"
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        port_label = toga.Label("Port",font_size=9)
        port_inp = toga.TextInput(validators=[validators.Integer(error_message="Port should be a number from 1-65535", allow_empty=False), lambda x: None if 0 < int(x) < 65536 else "Port should be a number from 1-65535"],margin_bottom=20, on_change=self.apply_port)
        port_inp.value = str(self.port)
        dcip_label = toga.Label("DC:IP list (separated by \";\")",font_size=9)
        dcip_inp = toga.TextInput(validators=[validators.Contains(substring=":", error_message="DC IP is in format of DC:IP;DC:IP;..etc.", allow_empty=False)], on_change=self.apply_dcip,margin_bottom=20)
        dcip_inp.value = ";".join(self.dc_ip)
        host_label = toga.Label("Host IP",font_size=9)
        host_inp = toga.TextInput(validators=[validators.MatchRegex(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", allow_empty = False, error_message="Host IP should be 4 numbers between 1-255 (0.0.0.0 to listen on all hosts)"), lambda x: self.met([0 <= int(y) <= 255  for y in x.split('.')], "Host IP should be 4 numbers between 1-255 (0.0.0.0 to listen on all hosts)")], on_change=self.apply_host,margin_bottom=20)
        host_inp.value = "127.0.0.1"
        start_stop_btn = toga.Button(text=f"{'Turn proxy OFF' if self.proxy_launched else 'Turn proxy ON'}", on_press=do_proxy_stuff)
        main_box = toga.Column(margin=20)

        #subprocess.run()
        
        main_box.add(dcip_label)
        main_box.add(dcip_inp)
        main_box.add(host_label)
        main_box.add(host_inp)
        main_box.add(port_label)
        main_box.add(port_inp)
        main_box.add(start_stop_btn)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return TelegramWSProxyforAndroid()
