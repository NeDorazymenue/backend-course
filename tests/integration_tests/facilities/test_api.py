

async def test_get_facilities(ac):
    responose = await ac.get("/facilities")
    assert responose.status_code == 200
    assert isinstance(responose.json(), list)


async def test_post_facilities(ac):
    facility_title = "обед"
    responose = await ac.post("/facilities", json={"title": facility_title})
    assert responose.status_code == 200
    res = responose.json()
    assert isinstance(res, dict)
    assert res["data"]["title"] == facility_title
    assert "data" in res