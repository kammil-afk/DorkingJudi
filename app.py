from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse

app = Flask(__name__)

# Fungsi untuk pencarian dork dengan logging
def google_dork_search_with_logs(domain, keywords):
    detected_results = []
    log = []  # Buffer untuk menyimpan log proses
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    base_url = "https://www.google.com/search"

    for keyword in keywords:
        query = f"site:*.{domain} {keyword}"
        log.append(f"🔍 Mencari: {query}")
        params = {"q": query, "hl": "id"}

        try:
            response = requests.get(base_url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                log.append(f"✅ Pencarian '{query}' berhasil.")
                soup = BeautifulSoup(response.text, "html.parser")
                for g in soup.find_all('div', class_='tF2Cxc'):
                    link = g.find('a')['href'] if g.find('a') else None
                    snippet = g.find('span', class_='aCOpRe').text if g.find('span', class_='aCOpRe') else ""
                    if link:
                        parsed_url = urlparse(link)
                        detected_domain = parsed_url.netloc
                        detected_results.append({
                            "domain": detected_domain,
                            "reason": f"Keyword '{keyword}' ditemukan.",
                            "snippet": snippet,
                            "link": link  # Tambahkan link untuk digunakan di template
                        })
                        log.append(f"🔗 Hasil ditemukan: {detected_domain} - {link}")
            else:
                log.append(f"⚠️ Error {response.status_code} saat mencari: {query}")
        except requests.RequestException as e:
            log.append(f"❌ Error saat mencari '{query}': {e}")

        # Tambahkan jeda untuk menghindari pemblokiran
        time.sleep(1)  # Jeda dipersingkat
    
    return detected_results, log


@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    log = []
    if request.method == "POST":
        domain = request.form.get("domain")
        keywords = [
            "slot",
            "judi",
            "gacor",
            "bonus",
            "jackpot"
        ]
        results, log = google_dork_search_with_logs(domain, keywords)
    return render_template("index.html", results=results, log=log)


if __name__ == "__main__":
    app.run(debug=True)
