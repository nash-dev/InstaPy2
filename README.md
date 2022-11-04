<img src="https://raw.githubusercontent.com/InstaPy2/InstaPy2/main/instapy2.png" width="44px"></img>
# InstaPy2
Automation script for Instagram that *farms* comments, follows and likes.

<span>
    <img src="https://img.shields.io/static/v1?label=Built%20with&message=Instagrapi&color=red"/>
    <img src="https://img.shields.io/static/v1?label=Built%20with&message=Python%203.11.0rc2&color=red"/>
    <a href="https://discord.gg/TY8pt8e5Xg" style="text-decoration: none; border: none; outline: 0;">
        <img src="https://img.shields.io/static/v1?label=Connect%20via&message=Discord&color=5865F2"/>
    </a>
    <img src="https://img.shields.io/static/v1?label=License&message=GPLv3&color=blue"/>
</span>
<br/>
<span>
    <a href="https://buymeacoffee.com/antiquecodes" style="text-decoration: none; border: none; outline: 0;">
        <img src="https://img.shields.io/static/v1?label=Support&message=Buy%20Me%20A%20Coffee&color=yellow"/>
    </a>
    <a href="https://paypal.com/paypalme/officialantique" style="text-decoration: none; border: none; outline: 0;">
        <img src="https://img.shields.io/static/v1?label=Support&message=PayPal&color=009cde"/>
    </a>
</span>

<br/>

# 2FA
> Instagrapi will fail when using 2FA. I've made a PR to fix that issue. Please wait until then to use 2FA.

2FA support has been introduced in `2fa-features` however, use it at your own risk.

## Using 2FA
```py
    from instapy2 import InstaPy2

    session = InstaPy2(username='<USERNAME_HERE>', password='<PASSWORD_HERE>', verification_code='<2FA_CODE_HERE>') # Tested and working with Apple Verification Code
```