def test_create_adoption_flow(client, auth_headers):
    r = client.post("/api/pets", headers=auth_headers, json={
        "species": "dog",
        "name": "Reks",
        "age_years": 3,
        "sex": "male",
        "size": "medium",
        "description": "Dobar i nežan pas, traži dom.",
    })
    assert r.status_code == 201, r.text
    pet_id = r.json()["id"]

    r2 = client.post("/api/adoption", headers=auth_headers, json={
        "pet_id": pet_id, "city": "Beograd",
    })
    assert r2.status_code == 201
    listing_id = r2.json()["id"]

    r3 = client.get("/api/adoption")
    assert r3.status_code == 200
    ids = [l["id"] for l in r3.json()]
    assert listing_id in ids

    r4 = client.get(f"/api/adoption?species=cat")
    assert r4.status_code == 200
    assert listing_id not in [l["id"] for l in r4.json()]
