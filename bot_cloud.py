import time
import random
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

class TikTokBot:
    def __init__(self):
        self.rodando = False
        self.stats = {
            'total_views': 0,
            'total_likes': 0,
            'videos_visitados': [],
            'logs': []
        }
        self.urls = []
        self.carregar_urls()
    
    def carregar_urls(self):
        try:
            if os.path.exists('dados/urls.txt'):
                with open('dados/urls.txt', 'r', encoding='utf-8-sig') as f:
                    urls = [line.strip() for line in f if line.strip()]
                if urls:
                    self.urls = [url.replace('\ufeff', '').strip() for url in urls]
                    return
        except:
            pass
        self.urls = ["https://www.tiktok.com/@seeagende/video/7669632240116124949"]
    
    def log(self, msg):
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_msg = f"[{timestamp}] {msg}"
        self.stats['logs'].append(log_msg)
        print(log_msg)
    
    def executar(self, num_views=1, modo='normal'):
        self.rodando = True
        self.log(f"🚀 Iniciando bot com {num_views} visualizações")
        self.log(f"📋 Total de URLs: {len(self.urls)}")
        
        try:
            with sync_playwright() as p:
                for i in range(num_views):
                    if not self.rodando:
                        break
                    
                    url = random.choice(self.urls)
                    self.log(f"\n📱 Visualização {i+1}/{num_views}")
                    
                    try:
                        # MODO HEADLESS (sem interface gráfica) para servidor
                        browser = p.chromium.launch(
                            headless=True,  # Modo headless para servidor
                            args=[
                                '--disable-blink-features=AutomationControlled',
                                '--no-sandbox',
                                '--disable-dev-shm-usage',
                                '--disable-gpu'
                            ]
                        )
                        context = browser.new_context(
                            viewport={'width': random.choice([1920, 1366, 1536]), 'height': 1080},
                            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                        )
                        page = context.new_page()
                        
                        self.log(f"🌐 Acessando: {url}")
                        page.goto(url, timeout=30000)
                        time.sleep(5)
                        
                        page.evaluate("window.scrollBy(0, 300)")
                        time.sleep(2)
                        
                        try:
                            page.evaluate("document.querySelector('video')?.play()")
                            self.log("🎬 Reproduzindo vídeo...")
                        except:
                            page.click('body')
                            self.log("🎬 Clicou na tela")
                        
                        duracao = random.uniform(30, 60)
                        self.log(f"⏳ Assistindo por {duracao:.0f} segundos...")
                        time.sleep(duracao)
                        
                        if random.random() > 0.4:
                            try:
                                page.click('[data-e2e="like-icon"]', timeout=5000)
                                self.stats['total_likes'] += 1
                                self.log("❤️ Curtiu o vídeo!")
                                time.sleep(2)
                            except:
                                try:
                                    page.evaluate("document.querySelector('[data-e2e=\"like-icon\"]')?.click()")
                                    self.stats['total_likes'] += 1
                                    self.log("❤️ Curtiu via JS!")
                                    time.sleep(2)
                                except:
                                    self.log("⚠️ Não foi possível curtir")
                        
                        browser.close()
                        self.stats['total_views'] += 1
                        self.stats['videos_visitados'].append({
                            'url': url,
                            'timestamp': datetime.now().isoformat()
                        })
                        self.log(f"✅ Visualização {i+1} concluída!")
                        
                    except Exception as e:
                        self.log(f"❌ Erro na visualização: {e}")
                        try:
                            browser.close()
                        except:
                            pass
                        continue
                    
                    if i < num_views - 1:
                        pausa = random.uniform(30, 60)
                        self.log(f"⏳ Aguardando {pausa:.0f} segundos...")
                        time.sleep(pausa)
        except Exception as e:
            self.log(f"❌ Erro no Playwright: {e}")
        
        self.log("✅ Processo concluído!")
        self.rodando = False
        return self.stats
    
    def parar(self):
        self.rodando = False
        self.log("🛑 Bot interrompido")
    
    def adicionar_url(self, url):
        url = url.replace('\ufeff', '').strip()
        if url not in self.urls and url.startswith('https://'):
            self.urls.append(url)
            os.makedirs('dados', exist_ok=True)
            with open('dados/urls.txt', 'w', encoding='utf-8-sig') as f:
                for u in self.urls:
                    f.write(f"{u}\n")
            return True
        return False

bot_instance = None

def get_bot():
    global bot_instance
    if bot_instance is None:
        bot_instance = TikTokBot()
    return bot_instance