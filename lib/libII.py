"""
main
----
"""
def on_hit_enter(input_url)
	url=input_url
	content= url.content
	soup = soup(content)
    name = get_app_name(soup)
    version = get_app_version(soup)
    get_app_download_count(soup)
    get_app_release_date()
    get_app_description
    
    return name, version, download_count, release_date, description
    
	
	