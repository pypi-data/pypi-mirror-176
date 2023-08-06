
## PyCaptcha

Simple captcha harvester for python. Supporting Hcapctha and RecaptchaV2

![Example](https://media.discordapp.net/attachments/957767715655925780/1041025966887153724/image.png?width=1314&height=906)


## Install dependencies

```bash
pip install -r requirements.txt
```
## Usage

```python
from pycaptcha import harvester

#Create a new harvester instace 

solver = harvester.new(solver_type="hcaptcha", url="https://discord.com/register", site_key="4c672d35-0701-42b2-88c3-78380b0db560")

#Start a new solve
captcha_token = solver.solve(timeout=20)

print(captcha_token)

```

## Working on

- Proxy support

- Support for importing chrome profiles

- Adding more captcha types (RecaptchaV3, Amazon,...)

