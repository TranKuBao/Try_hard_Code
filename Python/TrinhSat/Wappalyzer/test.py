from Wappalyzer import Wappalyzer, WebPage

# Lấy thông tin của trang web
webpage = WebPage.new_from_url('https://vi.wordpress.org/')

# Lấy Wappalyzer mới nhất
wappalyzer = Wappalyzer.latest()

# Phân tích công nghệ và phiên bản
technologies = wappalyzer.analyze_with_versions(webpage)

# In ra các công nghệ và phiên bản
for tech, data in technologies.items():
    print(f"Technology: {tech}", end=' - ')
    if 'versions' in data and data['versions']:
        print(f"Ver: {', '.join(data['versions'])}")
    else:
        print("Versions: Unknown")
