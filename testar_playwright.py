from bot_playwright import TikTokBot

print("?? Testando Playwright...")
bot = TikTokBot()
print(f"?? URLs carregadas: {len(bot.urls)}")
print(f"?? URLs: {bot.urls}")

print("\n?? Executando 1 visualiza??o...")
print("?? O navegador vai abrir. N?o feche!")
resultado = bot.executar(num_views=1, modo='normal')

print(f"\n?? Resultado:")
print(f"? Views: {resultado['total_views']}")
print(f"?? Likes: {resultado['total_likes']}")
