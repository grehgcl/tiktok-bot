import time
import random
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

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
                with open('dados/urls.txt', 'r') as f:
                    urls = [line.strip() for line in f if line.strip()]
                if urls:
                    self.urls = urls
                    return
        except:
            pass
        self.urls = ["https://www.tiktok.com/@seeagende/video/7669632240116124949"]
    
    def configurar_driver(self):
        options = Options()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--log-level=3')
        
        # 🔴 Remova o # da linha abaixo para ver o navegador:
        # options.add_argument('--headless')
        
        try:
            driver = webdriver.Chrome(options=options)
        except:
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            except:
                try:
                    service = Service('drivers/chromedriver.exe')
                    driver = webdriver.Chrome(service=service, options=options)
                except:
                    driver = webdriver.Chrome(options=options)
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    
    def log(self, msg):
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_msg = f"[{timestamp}] {msg}"
        self.stats['logs'].append(log_msg)
        print(log_msg)
    
    def assistir_video(self, url, driver):
        try:
            self.log(f"🌐 Acessando: {url}")
            driver.get(url)
            time.sleep(5)
            
            driver.execute_script("window.scrollBy(0, 300)")
            time.sleep(2)
            
            try:
                video = driver.find_element(By.TAG_NAME, "video")
                driver.execute_script("arguments[0].play();", video)
                self.log("🎬 Reproduzindo vídeo...")
            except:
                try:
                    driver.find_element(By.TAG_NAME, 'body').click()
                    self.log("🎬 Clicou na tela")
                except:
                    pass
            
            duracao = random.uniform(30, 60)
            self.log(f"⏳ Assistindo por {duracao:.0f} segundos...")
            time.sleep(duracao)
            
            if random.random() > 0.4:
                try:
                    like_btn = driver.find_element(By.CSS_SELECTOR, '[data-e2e="like-icon"]')
                    like_btn.click()
                    self.stats['total_likes'] += 1
                    self.log("❤️ Curtiu o vídeo!")
                    time.sleep(2)
                except:
                    self.log("⚠️ Não foi possível curtir")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Erro: {e}")
            return False
    
    def executar(self, num_views=1, modo='normal'):
        self.rodando = True
        self.log(f"🚀 Iniciando bot com {num_views} visualizações")
        self.log(f"📋 Total de URLs: {len(self.urls)}")
        
        for i in range(num_views):
            if not self.rodando:
                break
            
            url = random.choice(self.urls)
            self.log(f"\n📱 Visualização {i+1}/{num_views}")
            
            try:
                driver = self.configurar_driver()
                
                if modo == 'stealth':
                    resolucoes = [(1920,1080), (1366,768), (1536,864)]
                    resolucao = random.choice(resolucoes)
                    driver.set_window_size(resolucao[0], resolucao[1])
                
                sucesso = self.assistir_video(url, driver)
                
                if sucesso:
                    self.stats['total_views'] += 1
                    self.stats['videos_visitados'].append({
                        'url': url,
                        'timestamp': datetime.now().isoformat()
                    })
                    self.log(f"✅ Visualização {i+1} concluída!")
                else:
                    self.log(f"❌ Falha na visualização {i+1}")
                
                driver.quit()
                
            except Exception as e:
                self.log(f"❌ Erro: {e}")
                continue
            
            if i < num_views - 1:
                pausa = random.uniform(30, 60)
                self.log(f"⏳ Aguardando {pausa:.0f} segundos...")
                time.sleep(pausa)
        
        self.log("✅ Processo concluído!")
        self.rodando = False
        return self.stats
    
    def parar(self):
        self.rodando = False
        self.log("🛑 Bot interrompido")
    
    def adicionar_url(self, url):
        if url not in self.urls:
            self.urls.append(url)
            os.makedirs('dados', exist_ok=True)
            with open('dados/urls.txt', 'w') as f:
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