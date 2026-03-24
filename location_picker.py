# pip install nicegui==2.24.2
from nicegui import ui
from functools import partial
import httpx

marker = None
coords_text = ""


def on_map_click(e):
    """Single-click handler: one pin only."""
    global marker, coords_text, current_lat, current_lng

    # inicijalizacija koordinata
    lat = e.args["latlng"]["lat"]
    lng = e.args["latlng"]["lng"]
    coords_text = f"{lat:.6f}, {lng:.6f}"
    current_lat = lat
    current_lng = lng

    # brisi stari marker ako postoji
    if marker:
        map.remove_layer(marker)

    # Dodavanje novog markera
    marker = map.marker(latlng=(lat, lng))
    coord_label.set_text(f"📍 {coords_text}")
    print(coords_text)
    ui.notify(
        f"Lokacija označena! {coords_text}", position="top", color="blue", timeout=2000
    )


async def submit_subscription():
    """Pošalji subscription na Robyn backend."""
    email = email_input.value
    location_name = location_input.value
    species = species_select.value
    if not email:
        ui.notify("Molim unesite email!", color="negative")
        return
    if current_lat is None or current_lng is None:
        ui.notify("Molim prvo odaberite lokaciju na karti!", color="negative")
        return
    if not species:
        ui.notify("Molim odaberite barem jednu vrstu ribe!", color="negative")
        return

    payload = {
        "email": email,
        "latitude": current_lat,
        "longitude": current_lng,
        "location_name": location_name,
        "target_species": species,  # lista
    }
    try:
        async with httpx.AsyncClient() as client:
            print(payload)
            response = await client.post(
                "http://localhost:8000/api/subscribe", json=payload, timeout=10.0
            )

        if response.status_code == 200:
            ui.notify(
                "✅ Uspješno pretplaćeno! Dobit ćete email kada su uvjeti idealni.",
                color="positive",
                position="top",
                timeout=4000,
            )
            # Reset forma
            email_input.value = ""
            location_input.value = ""
            species_select.value = []
        else:

            ui.notify(f"❌ Greška: {response.text}", color="negative")
    except Exception as e:
        ui.notify(f"❌ Greška u komunikaciji s backendom: {str(e)}", color="negative")


# ---------- UI ----------
ui.page_title("One-click Coordinate Picker")

with ui.footer().classes("bg-blue-6 text-white"):
    ui.label(
        "💡 Klikom na kartu označiti lokaciju • Koordinate će se kopirati u međuspremnik"
    )

with ui.row().classes("w-full h-[90vh] gap-4 p-4"):
    # LIJEVA STRANA: Forma
    with ui.column().classes("w-1/3 gap-4"):
        ui.label("📋 Pretplata na Notifikacije").classes("text-h6 q-mb-sm")
        email_input = ui.input(
            label="Email Adresa", placeholder="vas.email@example.com"
        ).classes("w-full")
        location_input = ui.input(
            label="Naziv Lokacije (opcionalno)", placeholder="npr. Plomin Luka"
        ).classes("w-full")

        coord_label = ui.label("📍 Kliknite na kartu za odabir lokacije").classes(
            "text-subtitle1 q-mb-sm"
        )
        species_select = ui.select(
            label="Vrste Riba (možete odabrati više)",
            options={
                "mahi-mahi": "🐟 Mahi-Mahi",
                "strijelka": "🦁 Strijelka",
                "tuna": "🐟 Tuna",
                "palamida": "🐟 Palamida",
                "zubatac": "🐟 Zubatac",
                "lubin": "🐟 Lubin",
            },
            multiple=True,
            value=[],
        ).classes("w-full")
        ui.button("✅ Pretplati se", on_click=submit_subscription).props(
            "color=primary size=lg"
        ).classes("w-full")

        with ui.card().classes("w-full"):
            ui.label("ℹ️ Kako Funkcionira").classes("text-subtitle2")
            ui.label("1. Odaberite lokaciju klikom na kartu")
            ui.label("2. Unesite email i odaberite vrste riba")
            ui.label("3. Dobit ćete email kada su uvjeti idealni za pecanje!")

    # DESNA STRANA: Mapa
    with ui.column().classes("w-2/4 gap-4 pl-20 pr-0"):  

        ui.label("🗺️ Odabir Lokacije").classes("text-h6 q-mb-sm")
        with (ui.card().classes("w-full").style("height: 80vh")):
            map = ui.leaflet(
                center=(45.134174458769174, 14.175779430348852),
                zoom=7.5, # type: ignore
            ).classes("w-full h-full")

            map.on("map-click", on_map_click)

            map.tile_layer(
                url_template="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                options={"attribution": "© OpenStreetMap contributors"},
            )

ui.run(title="Location Picker", port=8080)
