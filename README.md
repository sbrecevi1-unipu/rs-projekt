# rs-projekt
Repozitorij za projekt iz RS-a


## Cilj projekta

 - spojiti se na razne API-je (MoonPhase, plima-oseka, meteorološke, ...) sa nekim vrstama (ponajprije invazivnim) riba i njihovim navikama hranjenja/bivanja/napadanja kako bi im se smanjio broj i potaknuo izlov vrsta koje nemaju prirodnih neprijatelja 

 ## HOW TO
 - pip install -r requirements.txt
 - run main.py as: robyn --dev main.py #to auto reload it when files are changed
 - send post requests with postman or other tools to http://localhost:8000/ - just add example data to body: 
 ```
 {
        "email": "user@example.com",
        "latitude": 43.5,
        "longitude": 16.0,
        "location_name": "Plomin Luka",
        "target_species": ["mahi-mahi", "strijelka"]
    }
 ```

 - usage endpoints : 
 ```
"endpoints": {
            "POST /api/subscribe": "Kreiraj pretplatu",
            "GET /api/subscriptions": "Sve pretplate",
            "GET /api/subscriptions/:id": "Specifična pretplata",
            "DELETE /api/subscriptions/:id": "Deaktiviraj pretplatu",
        },
 ```