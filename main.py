from robyn import Robyn
from datetime import datetime


app = Robyn(__file__)

subscriptions = []
users = {}


@app.post("/api/subscribe")
async def subscribe(request):
    """
    Endpoint za kreiranje subscription-a.
    Body:
    {
        "email": "user@example.com",
        "latitude": 43.5,
        "longitude": 16.0,
        "location_name": "Plomin Luka",
        "target_species": ["mahi-mahi", "strijelka"]
    }
    """

    try:
        data = request.json()
        # Validacija
        email = data.get("email", "").strip()
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        location_name = data.get("location_name", "").strip()
        target_species = data.get("target_species", [])

        # Provjere
        if not email or "@" not in email:
            return {"error": "Valjan email je obavezan"}

        if latitude is None or longitude is None:
            return {"error": "Latitude i longitude su obavezni"}

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (ValueError, TypeError):
            return {"error": "Latitude i longitude moraju biti brojevi"}

        # Osiguraj da je lista
        if not isinstance(target_species, list):
            target_species = [target_species]

        target_species = [s for s in target_species if s]
        print("\n DEBUG - Primljeni podaci:")
        print(f"   tip target_species: {type(data.get('target_species'))}")

        if not target_species or not isinstance(target_species, list):
            return {"error": "Barem jedna vrsta ribe je obavezna"}

        # Kreiraj ili dohvati user_id
        if email not in users:
            users[email] = len(users) + 1
        user_id = users[email]

        # Kreiraj subscription
        subscription = {
            "id": len(subscriptions) + 1,
            "user_id": user_id,
            "email": email,
            "latitude": latitude,
            "longitude": longitude,
            "location_name": location_name,
            "target_species": target_species,  # Lista kao što je primljena
            "active": True,
            "created_at": datetime.now().isoformat(),
        }

        subscriptions.append(subscription)

        print("\n" + "=" * 60)
        print(f"NOVA PRETPLATA (ID: {subscription['id']})")
        print("=" * 60)
        print(f"Email:     {email}")
        print(f"Lokacija:  {latitude:.6f}, {longitude:.6f}")

        if location_name:
            print(f"Naziv:     {location_name}")

        print(f"Vrste:     {', '.join(target_species)}")
        print(f"Ukupno:    {len(subscriptions)} pretplata(e)")
        print("=" * 60 + "\n")

        return {
            "status": "success",
            "message": "Subscription kreiran",
            "subscription_id": subscription["id"],
        }

    except Exception as e:
        print(f"\n❌ GREŠKA pri subscription-u: {str(e)}\n")
        return {"error": str(e)}


# robyn main.py --dev

@app.get("/api/subscriptions")
async def get_subscriptions(request):
    """Debug endpoint - prikaži sve aktivne subscriptions."""

    try:
        active_subs = [s for s in subscriptions if s["active"]]
        return {
            "status": "success",
            "subscriptions": active_subs,
            "count": len(active_subs),
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/subscriptions/:subscription_id")
async def get_subscription(request):
    """Pregled specifične subscription-e."""
    try:
        sub_id = int(request.path_params.get("subscription_id"))
        # Pronađi subscription
        sub = next((s for s in subscriptions if s["id"] == sub_id), None)
        if not sub:
            return {"error": "Subscription not found"}
        return {"status": "success", "subscription": sub}
    except ValueError:
        return {"error": "ID mora biti broj"}
    except Exception as e:
        return {"error": str(e)}


@app.delete("/api/subscriptions/:subscription_id")
async def delete_subscription(request):
    """Deaktivira subscription."""
    try:
        sub_id = int(request.path_params.get("subscription_id"))
        # Pronađi i deaktiviraj
        sub = next((s for s in subscriptions if s["id"] == sub_id), None)
        if not sub:
            return {"error": "Subscription not found"}
        elif sub["active"] == False:
            
            return {
                "status": "success",
                "message": f"Subscription {sub_id} already deactivated (done nothing).",
            }
        else:
            sub["active"] = False
            return {
                "status": "success",
                "message": f"Subscription {sub_id} deactivated",
            }

    except ValueError:
        return {"error": "ID mora biti broj"}

    except Exception as e:
        return {"error": str(e)}


@app.get("/")
async def home(request):
    """Root endpoint - info o API-ju."""
    return {
        "app": "Fishing Forecast API",
        "version": "0.1.0",
        "endpoints": {
            "POST /api/subscribe": "Kreiraj pretplatu",
            "GET /api/subscriptions": "Sve pretplate",
            "GET /api/subscriptions/:id": "Specifična pretplata",
            "DELETE /api/subscriptions/:id": "Deaktiviraj pretplatu",
        },
    }


if __name__ == "__main__":
    print("\n" + "=" * 72)
    print("ROBYN BACKEND - PROGNOZA PECANJA".center(72))
    print("=" * 72)
    print("\n📡 API Endpoints:\n")
    print("   POST   /api/subscribe                - Kreiraj subscription")
    print("   GET    /api/subscriptions            - Sve subscriptions")
    print("   GET    /api/subscriptions/:id        - Specifična subscription")
    print("   DELETE /api/subscriptions/:id        - Deaktiviraj subscription")
    print("\n" + "=" * 72)
    print("Backend server: http://localhost:8000")
    print("=" * 72 + "\n")
    app.start(port=8000)
