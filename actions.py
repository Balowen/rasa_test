# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"


from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Any, Text, Dict, List, Union

import requests
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction


# We use the medicare.gov database to find information about 3 different
# healthcare facility types, given a city name, zip code or facility ID
# the identifiers for each facility type is given by the medicare database
# xubh-q36u is for hospitals
# b27b-2uc7 is for nursing homes
# 9wzi-peqs is for home health agencies

ENDPOINTS = {
    "base": "https://data.medicare.gov/resource/{}.json",
    "xubh-q36u": {
        "city_query": "?city={}",
        "zip_code_query": "?zip_code={}",
        "id_query": "?provider_id={}"
    },
    "b27b-2uc7": {
        "city_query": "?provider_city={}",
        "zip_code_query": "?provider_zip_code={}",
        "id_query": "?federal_provider_number={}"
    },
    "9wzi-peqs": {
        "city_query": "?city={}",
        "zip_code_query": "?zip={}",
        "id_query": "?provider_number={}"
    }
}

FACILITY_TYPES = {
    "hospital":
        {
            "name": "hospital",
            "resource": "xubh-q36u"
        },
    "nursing_home":
        {
            "name": "nursing home",
            "resource": "b27b-2uc7"
        },
    "home_health":
        {
            "name": "home health agency",
            "resource": "9wzi-peqs"
        }
}


class ActionFacilitySearch(Action):

    def name(self) -> Text:
        return "action_facility_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # tracker keeps track of the slots in specific action
        facility = tracker.get_slot("facility_type")

        # for the sake of symplicity, hardcoded address
        address = "300 Hyde St. San Francisco"
        dispatcher.utter_message(f"Here is the address of the {facility}:{address}")

        return [SlotSet("address", address)]


class FacilityForm(FormAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "facility_form"

    @staticmethod
    def required_slots(tracker: "Tracker") -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["facility_type", "location"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {"facility_type": self.from_entity(entity="facility_type",
                                                  intent=["inform",
                                                          "search_provider"]),
                "location": self.from_entity(entity="location",
                                             intent=["inform",
                                                     "search_provider"])}


    def submit(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Once required slots are filled, print buttons for found facilities"""

        location = tracker.get_slot('location')
        facility_type = tracker.get_slot('facility_type')

        results = _find_facilities(location, facility_type)
        button_name = _resolve_name(FACILITY_TYPES, facility_type)
        if len(results) == 0:
            dispatcher.utter_message(
                f"Sorry, we could not find a {button_name} in {location.title()}")
            return []
        # limit number of results to 3 for clear presentation purposes
        for r in results[:3]:
            if facility_type == FACILITY_TYPES["hospital"]["resource"]:
                facility_id = r.get("provider_id")
                name = r["hospital_name"]
            elif facility_type == FACILITY_TYPES["nursing_home"]["resources"]:
                facility_id = r["federal_provider_number"]
                name = r["provider_name"]
            else:
                facility_id = r["provider_number"]
                name = r["provider_name"]

            payload = "/inform{\"facility_id\":\"" + facility_id + "\"}"
            buttons.append(
                {"title": f"{name.title()}",
                 "payload": payload})

        if len(buttons) == 1:
            message = f"Here is a {button_name} near you:"
        else:
            if button_name == "home health agency":
                button_name = "home health agencie"
            message = f"Here are {len(buttons)} {button_name}s near you:"

        # TODO: update rasa core version for configurable `button_type`
        dispatcher.utter_button_message(message, buttons)
        return []