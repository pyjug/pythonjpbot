
# 環境設定

1. 次のURLを参考に、Google Cloud Datastore のキーファイルを作成する

    https://cloud.google.com/datastore/docs/reference/libraries

2. 作成したキーファイルのファイル名を、次のように環境変数に指定する

    export GOOGLE_APPLICATION_CREDENTIALS="[PATH_TO_CERTFILE]"

    ex)
        export GOOGLE_APPLICATION_CREDENTIALS="%HOME/proj_xxxxx.json"


3. Discord bot のトークンを、任意のファイルに保存する

     ex)
         $ echo asdf89as9d8fndfssa8.asfasf98f7isaidfuhasf > $HOME/mybottoken

4. 作成したDiscord bot トークンファイルのファイル名を、次のように環境変数に指定する


    export DISCORD_BOT_KEYFILE="[KEY]"

    ex)
        export DISCORD_BOT_KEYFILE="%HOME/mybottoken"

5. 実行環境を作成する

```
$ pip install pipenv
$ git clone https://github.com/pyjug/pythonjpbot.git
$ pythonjpbot
$ pipenv install --three
```

6. 実行する


```
$ pipenv run python -m pythonjpbot
```

