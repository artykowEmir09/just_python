API = "/api/v1"


def test_note_crud(client):
    r = client.post(f"{API}/notes", json={"title": "Idea", "content": "build OS"})
    assert r.status_code == 201
    note_id = r.json()["id"]

    assert client.get(f"{API}/notes/{note_id}").json()["title"] == "Idea"
    assert len(client.get(f"{API}/notes").json()) == 1

    r = client.put(f"{API}/notes/{note_id}", json={"is_archived": True})
    assert r.json()["is_archived"] is True
    assert r.json()["title"] == "Idea"  # untouched

    assert client.delete(f"{API}/notes/{note_id}").status_code == 204
    assert client.get(f"{API}/notes/{note_id}").status_code == 404


def test_note_validation(client):
    assert client.post(f"{API}/notes", json={"title": ""}).status_code == 422


def test_task_complete_flow(client):
    r = client.post(f"{API}/tasks", json={"title": "Write code", "priority": 3})
    task = r.json()
    assert task["status"] == "todo" and task["completed_at"] is None

    r = client.patch(f"{API}/tasks/{task['id']}/complete")
    assert r.json()["status"] == "done"
    assert r.json()["completed_at"] is not None

    r = client.put(f"{API}/tasks/{task['id']}", json={"status": "todo"})
    assert r.json()["completed_at"] is None


def test_task_priority_validation(client):
    assert client.post(f"{API}/tasks", json={"title": "x", "priority": 9}).status_code == 422


def test_tags_attach_detach(client):
    tag = client.post(f"{API}/tags", json={"name": "  Work "}).json()
    assert tag["name"] == "work"
    assert client.post(f"{API}/tags", json={"name": "WORK"}).status_code == 409

    note = client.post(f"{API}/notes", json={"title": "n"}).json()
    task = client.post(f"{API}/tasks", json={"title": "t"}).json()

    r = client.post(f"{API}/notes/{note['id']}/tags/{tag['id']}")
    assert [t["name"] for t in r.json()["tags"]] == ["work"]
    r = client.post(f"{API}/tasks/{task['id']}/tags/{tag['id']}")
    assert [t["name"] for t in r.json()["tags"]] == ["work"]

    r = client.delete(f"{API}/notes/{note['id']}/tags/{tag['id']}")
    assert r.json()["tags"] == []

    # deleting a tag removes it from tasks too
    assert client.delete(f"{API}/tags/{tag['id']}").status_code == 204
    assert client.get(f"{API}/tasks/{task['id']}").json()["tags"] == []


def test_not_found(client):
    assert client.get(f"{API}/tasks/999").status_code == 404
    assert client.delete(f"{API}/tags/999").status_code == 404
