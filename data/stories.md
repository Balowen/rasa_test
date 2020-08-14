## happy path
* greet
  - find_facility_types
* inform{"facility_type: "rbry-mqwu"}
  - facility_form
  - form{"name": "facility_form"}
  - form{"name": null}
* inform{"facility_id": 4245}
  - find_healthcare_address
  - utter_address
* thankyou
  - utter_goodbye

## happy_path2
* search_provider{"location": "Austin", "facility_type": "rbry-mqwu"}
  - facility_form
  - form{"name": "facility_form"}
  - form{"name": null}
* inform{"facility_id": "450871"}
  - find_healthcare_address
  - utter_address
* thankyou
    - utter_noworries
    
## happy_path_multi_requests
* greet
  - find_facility_types
* inform{"facility_type: "rbry-mqwu"}
  - facility_form
  - form{"name": "facility_form"}
  - form{"name": null}
* inform{"facility_id": "747604"}
  - find_healthcare_address
  - utter_address
* search_provider{"facility_type: "rbry-mqwu"}
  - facility_form
  - form{"name": "facility_form"}
  - form{"name": null}
  
## search hospital happy path
* greet
  - utter_how_can_i_help
* search_provider{"facility_type":"hospital", "location":"San Francisco"}
  - action_facility_search
  - slot{"address":"300 Hyde St. San Francisco"}
* thanks
  - utter_goodbye
  
 ## search hospital + location
* greet
  - utter_how_can_i_help
* search_provider{"facility_type":"hospital"}
  - utter_ask_location
* inform{"location":"San Francisco"}
  - action_facility_search
* thanks
  - utter_goodbye
  

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
