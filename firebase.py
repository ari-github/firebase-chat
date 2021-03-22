import pyrebase

config = {
            "apiKey": "your data",
            "authDomain": "your data",
            "databaseURL": "your data",
            "projectId": "your data",
            "storageBucket": "your data",
            "messagingSenderId": "your data",
            "appId": "your data"
        }

firebase = pyrebase.initialize_app(config)

db = firebase.database()
auth = firebase.auth()
