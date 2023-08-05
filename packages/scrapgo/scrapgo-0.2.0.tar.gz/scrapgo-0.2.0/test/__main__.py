import argparse
import os
import sys
from pprint import pprint
# import pandas as pd

from practice.naver_kin_scraper.kin import naver_kin_with_image
from practice.naver_webtoon_scraper.webtoon2 import retrive_webtoon
from practice.durginfo.druginfo_scraper import drug_search
from practice.codingforentrepreneurs import download_courses, download_projects
# from practice.dailypharm import get_dailypharm_recruit

sys.path.append('.')


MEDIA_ROOT = 'media'


def main():
    argparser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="TEST Scraper"
    )
    argparser.add_argument('keywords', help='검색할 키워드들 나열', nargs='*')
    argparser.add_argument('-titleId', '--titleId')

    argparser.add_argument('-search', '--search', nargs='?')

    argparser.add_argument('-start', '--start', type=int, default=0)
    argparser.add_argument('-end', '--end', type=int, default=0)
    argparser.add_argument('-sd', '--start_date', type=str)
    argparser.add_argument('-ed', '--end_date', type=str)
    argparser.add_argument('-o', '--output', type=str)
    argparser.add_argument('-fund_std_code', '--fund_std_code')
    argparser.add_argument('-cd', '--code')
    argparser.add_argument('-conn', '--db_conf_path', type=str)
    argparser.add_argument('-pg', '--page_limit', type=int)

    args = argparser.parse_args()
    try:
        app = args.keywords[0]
    except:
        return

    context = {
        'save_to': MEDIA_ROOT
    }

    if app in ['daily', 'dp']:
        r = get_dailypharm_recruit(
            page_limit=args.page_limit
        )
        pprint(r[0])

    if app in ['webtoon', 'toon']:
        context['titleId'] = args.titleId
        retrive_webtoon(context)

    if app in ['kin']:
        context['save_to'] = os.path.join(MEDIA_ROOT, 'kin')
        naver_kin_with_image(params={'query': args.search}, context=context)

    if app in ['druginfo', 'di']:
        params = {
            'q': args.search
        }
        drug_search(params)

    if app in ['codingforentrepreneurs', 'cf']:
        params = {
            'base_dir': 'media/codingforentrepreneurs'
        }
        for ctg in args.keywords[1:]:
            if ctg == 'courses':
                download_courses(params)
            if ctg == 'projects':
                download_projects(params)



if __name__ == "__main__":
    main()
