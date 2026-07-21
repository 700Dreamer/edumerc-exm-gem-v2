import asyncio
import httpx
import json

async def main():
    async with httpx.AsyncClient(timeout=120) as client:
        # Register if not exists
        reg_payload = {
            "email": "tester@eduquest.com",
            "password": "SecurePassword123!",
            "role": "staff"
        }
        try:
            await client.post("http://127.0.0.1:8000/api/auth/register", json=reg_payload)
        except Exception:
            pass

        # Login
        login_res = await client.post("http://127.0.0.1:8000/api/auth/jwt/login", data={
            "username": "tester@eduquest.com",
            "password": "SecurePassword123!"
        })
        if login_res.status_code != 200:
            print("Login failed:", login_res.text)
            return
            
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Generate P7 Math Exam (5 questions)
        payload = {
            "mode": "Exams",
            "subject": "Mathematics",
            "level": "Primary 7",
            "term": "Term 1",
            "question_count": 5,
            "ai_model": "gpt-4o",
            "topic": ""
        }
        print("Calling /api/generate...")
        res = await client.post("http://127.0.0.1:8000/api/generate", json=payload, headers=headers)
        print("Status:", res.status_code)
        if res.status_code == 200:
            data = res.json()
            print("Paper generated successfully! Title:", data.get("title"))
            
            # Print questions
            raw_questions = json.loads(data.get("raw_questions", "{}")).get("questions", [])
            print(f"Total questions returned: {len(raw_questions)}")
            for q in raw_questions:
                print(f"Q{q.get('number')}: {q.get('text')[:60]}... [Origin: {q.get('origin_class')}]")
                
            # Print if html contains reference map and marking guide
            html = data.get("html", "")
            print("HTML contains Reference Map container:", "id=\"refMapP\"" in html)
            print("HTML contains Syllabus Saturation Audit title:", "Syllabus Saturation Audit" in html)
            print("HTML contains Confidential Marking Guide:", "Confidential Marking Guide" in html)
            print("HTML contains 'Primary 6' origin tag:", "Primary 6" in html)
        else:
            print("Response:", res.text)

asyncio.run(main())
