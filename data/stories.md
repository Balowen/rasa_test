## happy_path
* greet
    - find_facility_types
* inform{"facility_type": "xubh-q36u"}    
    - facility_form
    - form{"name": "facility_form"}
    - form{"name": null}
* inform{"facility_id": 4245}
    - find_healthcare_address
    - utter_address
* thanks
    - utter_noworries

## happy_path2
* search_provider{"location": "Austin", "facility_type": "xubh-q36u"}
    - facility_form
    - form{"name": "facility_form"}
    - form{"name": null}
* inform{"facility_id": "450871"}
    - find_healthcare_address
    - utter_address
* thanks
    - utter_noworries
    
## happy_path_multi_requests
* greet
  - find_facility_types
* inform{"facility_type": "b27b-2uc7"}
  - facility_form
  - form{"name": "facility_form"}
  - form{"name": null}
* inform{"facility_id": "747604"}
  - find_healthcare_address
  - utter_address
* search_provider{"facility_type": "9wzi-peqs"}
  - facility_form
  - form{"name": "facility_form"}
  - form{"name": null}
* inform{"facility_id": 4245}   
    - find_healthcare_address
    - utter_address
  
  
## story_thankyou
* thanks
  - utter_noworries

## say goodbye
* goodbye
  - utter_goodbye

