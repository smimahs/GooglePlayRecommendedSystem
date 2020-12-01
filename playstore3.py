from google_play_scraper.scraper import PlayStoreScraper
import pandas as pd


import play_scraper
category = play_scraper.categories()
category_list=category.keys()
#df=pd.DataFrame(category_list)
#df.to_csv('category.csv')
'''
for i in category_list:
    scraper = PlayStoreScraper()
    results = scraper.get_app_ids_for_query(str(i))
    df=pd.DataFrame(list(results))
    df.to_csv('id'+i+'.csv')
'''
category=pd.read_csv('category.csv')
scraper = PlayStoreScraper()
for i in list(category_list)[33:51]:
    resulatlist=pd.read_csv('./csvgame/id'+i+'.csv')
    print(resulatlist)
    for r in (resulatlist['0']):
        try:
            print(r)
            similar = scraper.get_similar_app_ids_for_app(r)

            app_details = scraper.get_multiple_app_details(similar)
            df=pd.DataFrame(list(app_details))
            df.to_csv('detail-'+i+'-'+r+''+'.csv')
        except:
            pass
#print(list(app_details))
