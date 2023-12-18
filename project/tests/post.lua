-- post.lua
wrk.method = "POST"
wrk.body   = '{"user_id": 1, "gender": "M", "country": "KR"}'
wrk.headers["Content-Type"] = "application/json"
