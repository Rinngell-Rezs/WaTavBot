
def Fire():
    from firebase import firebase
    fire = firebase.FirebaseApplication("https://watavbot.firebaseio.com",None)
    return fire
