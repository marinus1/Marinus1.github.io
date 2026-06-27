import feedparser
import requests

# This connects directly to your live Google Web App macro link
WEBAPP_URL = "https://script.google.com/macros/s/AKfycbxoXeYqSMXP4LDg-NpOhl9ZBS-8TAtJN-VhW8yOHVp9vXMH6YqEb18_1cXzE5CO1E4A/exec"

# Target RSS tech/security feeds (including Broad Media/MyBroadband streams)
FEEDS = [
    "https://mybroadband.co.za/news/feed",
    "https://www.securitymagazine.com/rss"
]

def scan_radar():
    print("🛰️ Starting autonomous radar array sweep...")
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]: # Grab the 5 latest updates from each stream
            title = entry.title
            link = entry.link
            
            # Link Safety Filter: Fixes the 404 issue by forcing absolute URLs
            if link.startswith("//"):
                link = f"https:{link}"
            elif not link.startswith("http://") and not link.startswith("https://"):
                link = f"https://{link}"
                
            summary = entry.get("summary", "No technical summary provided by target array.")[:200] + "..."
            
            # Simple keyword categorization mapping engine
            title_lower = title.lower()
            if any(w in title_lower for w in ["drone", "uav", "ugv", "aircraft", "autonomous"]):
                category = "Drones & Autonomous Systems"
            elif any(w in title_lower for w in ["spy", "covert", "camera", "cctv", "surveillance", "video"]):
                category = "Surveillance & AI Analytics"
            elif any(w in title_lower for w in ["cyber", "hack", "ransomware", "network", "software"]):
                category = "Cybersecurity & Network Defense"
            else:
                category = "Physical & Electronic Security"
            
            # Send data over to your Google Sheet deployment hub
            try:
                payload = {
                    "action": "append",
                    "title": title,
                    "category": category,
                    "summary": summary,
                    "link": link
                }
                response = requests.post(WEBAPP_URL, json=payload)
                print(f"📡 Found: {title} -> Sent status: {response.status_code}")
            except Exception as e:
                print(f"⚠️ Transmission error: {e}")

if __name__ == "__main__":
    scan_radar()
