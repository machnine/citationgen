from habanero import Crossref
from datetime import datetime

class Article:
    
    def __init__(self, doi):
        cr = Crossref()
        try:
            message = cr.works(doi)['message']
        except:
            message = None
            
        if message:
            metadata = {}
            
            metadata['doi'] = doi
            
            journal_info = {x['name']:x['value'] for x in message['assertion']}            
            metadata.update(journal_info)
            
            metadata['page'] = message['page'].replace('-', '--')
            metadata['volume'] = message['volume']
            metadata['author'] = ' and '.join([ f"{x['given']} {x['family']}" for x in message['author']])

            ts = message['license'][0]['start']['date-time']
            metadata['date'] = datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ').date()
                                               
            metadata['article_name'] = f"{message['author'][0]['family']}_{metadata['date'].year}"
                                               
            self.metadata = metadata    
                                               
    def bibtex(self, filepath=None):
        meta = self.metadata
        bibtex_str =  f'''@article{{ {meta['article_name']},
                       doi = { {meta['doi']} }, 
                       url = { {meta['articlelink']} },
                       year = { {meta['date'].year} },
                       month = { {meta['date'].month} },
                       publisher = { {meta['publisher']} },
                       volume = { {meta['volume']} },
                       pages = { {meta['page']} },
                       author = { {meta['author']} },
                       title = { {meta['articletitle']} },
                       journal = { {meta['journaltitle']} } 
                    }}
                    '''.replace('{\'', '{').replace('\'}', '}')
        if filepath:
            with open(filepath, 'w') as f:
                f.write(bibtex_str)
        else:
            return bibtex_str