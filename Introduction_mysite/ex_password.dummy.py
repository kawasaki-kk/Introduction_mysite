# -*- coding: utf-8 -*-
u"""機密情報
    データベース、及びdjangoシークレットキー情報の管理
    ''内部にご自身で設定した情報をご記入ください
    ご使用の際には、このファイルの".dummy"部分を削除してください

    また、debug_modeはdjangoのデバックモードを有効化するかどうかのフラグとなります
    無効にしたい場合には、現在"True"となっている箇所を"False"に設定してください

    settings.py内ですでにimportされているため、上記編集を行わない場合、正常に動作しません
"""
database_password = 'password here'
database_user = 'your database user name here'
database_name = 'your database name here'
debug_mode = True
secret_key = 'django secret key here'
