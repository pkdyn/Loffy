from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials( client_id=  "9f133c4fea4142498c182dc76383ce4d",
                                                            client_secret= "84511eaa3a0c4ef6aaf6350ec8ff4d1b"))

def predict_single(samp, dv, rf): 
    X = dv.transform([samp]) 
    y_pred = rf.predict_proba(X)[0, 1] 
    return y_pred

def track_info(tracks) :
            audio_features = sp.audio_features(tracks)[0]
            samp={
            'bpm':  round(audio_features['tempo']),
            'energy': round(audio_features['energy']*100),
            'dance': round(audio_features['danceability']*100),
            'loud': round(audio_features['loudness']),
            'valence':  round(audio_features['valence']*100),
            'lens': round(audio_features['duration_ms']/1000), 
            'acoustic':round(audio_features['acousticness']*100)
            }
            return samp

with open('actions/lofi.bin', 'rb') as f_in:
   dv, rf = pickle.load(f_in)

class ActionQueryPred(Action):
    def name(self) -> Text:
        return "action_query_pred"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        text_link = tracker.get_slot('link')
        tracks=[text_link]
        samp={}
        samp=track_info(tracks)
        samp
        predict_single(samp, dv, rf)
        predict = predict_single(samp, dv, rf)
        if predict >= 0.5:
            predict_string = "yes, it's lofi"
        else:
            predict_string = "nah, it's not lofi"

        dispatcher.utter_message(text = predict_string)

        return []