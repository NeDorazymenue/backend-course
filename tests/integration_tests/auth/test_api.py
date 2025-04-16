async def test_auth_flow_api(authenticated_ac):
    register_response = await authenticated_ac.post(
        "/auth/register",
        json={
            "email": "user1@user.ru",
            "password": "usEr_1"
        }
    )
    assert register_response.status_code == 200

    login_response = await authenticated_ac.post(
        "/auth/login",
        json={
            "email": "user1@user.ru",
            "password": "usEr_1"
        }
    )
    cookies = login_response.cookies
    assert "access_token" in cookies, "Токен не установлен в cookies"
    access_token = cookies["access_token"]
    assert access_token, "Токен пустой"

    me_response = await authenticated_ac.get(
        "/auth/me"
    )
    assert me_response.status_code == 200
    user_data = me_response.json()
    assert "email" in user_data
    assert user_data["email"] == "user1@user.ru"
    assert "id" in user_data

    logout_response = await authenticated_ac.post(
        "/auth/logout"
    )
    assert logout_response.status_code == 200
    logout_cookies = logout_response.cookies
    assert "access_token" not in logout_cookies

    me_after_logout = await authenticated_ac.get("/auth/me")
    assert me_after_logout.status_code == 401