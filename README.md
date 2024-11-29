python中需要提前pip的库

1.selenium
2.time

selenium所需要的chromedriver需要匹配自己电脑里chrome的版本才行。

第九行 service = Service('C:\Program Files\Google\Chrome\Application\chromedriver.exe')，改为自己电脑中chromedriver.exe所在的位置，防止每次运行都需要重新缓冲。

运行后需要扫码登录一次，后续无需操作



Packages that need to be pip installed in advance

1.selenium
2.time

The chromedriver required by selenium needs to match the version of chrome in your computer.

Line 9 service = Service('C:\Program Files\Google\Chrome\Application\chromedriver.exe'), change it to the location of chromedriver.exe on your computer to prevent the need to re-buffer every time you run it.

After running, you need to scan the QR code to log in once, and no subsequent operations are required.
