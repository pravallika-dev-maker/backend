import requests

def test_api():
    try:
        r_projects = requests.get("https://backend-production-42b0.up.railway.app/projects/")
        print(f"Projects Status: {r_projects.status_code}")
        print(f"Projects Count: {len(r_projects.json())}")
        print(f"Projects Data: {r_projects.json()[:2]}")
        
        r_stages = requests.get("https://backend-production-42b0.up.railway.app/stages/")
        print(f"Stages Status: {r_stages.status_code}")
        print(f"Stages Count: {len(r_stages.json())}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
