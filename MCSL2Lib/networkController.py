'''绕过代理保证程序联网正常'''
from requests import Session

Session = Session()
Session.trust_env = False
