GB = 1024 * 1024 * 1024




def test_upload_fat_file():
    with open("ignore.test_upload_fat_file.dat", "wb") as f:
        f.write(b"0" * 3 * GB)





async def test_bug_routing_paths_with_colon_prefix(
    mocker,
    app: FastAPI,
    client: httpx.AsyncClient,
    faker: Faker,
    auth: HTTPBasicAuth,
):
    """
    After an upgrade the url parser was matching ':start' as part of the job_id, i.e. requesting in

        /v0/solvers/{solver_key}/release/{version}/jobs/{job_id}:start

    would route to

        /v0/solvers/{solver_key}/release/{version}/jobs/{job_id}

    This was working before as ':' would be considered as '/' and
    https://fastapi.tiangolo.com/tutorial/path-params/#order-matters was also considered.
    """
    # auth client
    client.auth = httpx.BasicAuth(auth.username, auth.password)

    # mock server handlers
    mock_handler: dict[str, MagicMock] = {}
    for action in ("get", "start", "stop", "inspect"):
        mock_handler[f"{action}_job"] = mocker.patch(
            f"simcore_service_api_server.api.routes.solvers_jobs.{action}_job",
            return_value=fastapi.responses.JSONResponse(),
        )

    # fake job name
    solver_key = Solver.Config.schema_extra["example"]["id"]
    version = Solver.Config.schema_extra["example"]["version"]
    job_id = faker.uuid4()

    # check

    expected_url = app.router.url_path_for(
        "start_job", solver_key=solver_key, version=version, job_id=job_id
    )
    resp = await client.post(
        f"/v0/solvers/{solver_key}/releases/{version}/jobs/{job_id}:start"
    )
    assert f"{resp.url.path}" == expected_url

    assert mock_handler["start_job"].call_count == 1

    resp = await client.post(
        f"/v0/solvers/{solver_key}/release/{version}/jobs/{job_id}:stop",
    )
    assert mock_handler["stop_job"].call_count == 1

    resp = await client.post(
        f"/v0/solvers/{solver_key}/release/{version}/jobs/{job_id}:inspect"
    )
    assert mock_handler["inspect_job"].call_count == 1
