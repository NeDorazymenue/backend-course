


async def test_get_hotels(ac):
    responose = await ac.get(
        "/hotels",
        params={
            "date_from": "2025-03-15",
            "date_to": "2025-03-22",
        }
    )
    print(f"{responose.json()=}")

    assert responose.status_code == 200