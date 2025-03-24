

async def test_get_facilities(ac):
    responose = await ac.get("/facilities")
    print(f"{responose.json()=}")
    assert responose.status_code == 200


async def test_add_facilities(ac):
    responose = await ac.post("/facilities", json={"title": "обед"})
    assert responose.status_code == 200