#from gvars import HMG_ANBIMA
#import pieces

def get_calendario_anbima_api():
    anbima = {
    "holidays": [
                {
                    "Holiday": "2024-04-21T00:00:00",
                    "NextWorkDay": "2024-04-22T00:00:00"
                },
                {
                    "Holiday": "2024-05-01T00:00:00",
                    "NextWorkDay": "2024-05-02T00:00:00"
                },
                {
                    "Holiday": "2024-05-30T00:00:00",
                    "NextWorkDay": "2024-05-31T00:00:00"
                }
            ]
        }

        
    return anbima.json()
    
