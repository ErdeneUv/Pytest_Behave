from tests.utilities.Link.redirections import *
from tests.utilities.api_utilities import build_link

def get_bc_links(target_url):
    response = build_link('LOCAL_API', 'user', 'user', url, False).json()
    print(f'TargetURL: {target_url}')
    print(f"Response: {response}\n")
    return response['url']


if __name__ == '__main__':
    load_dotenv()
    sheet_id = os.getenv('GSHEET_ID')
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

    target_urls = df["Product URL"]
    bc_links = []
    all_redirections = []

    for url in target_urls:
        try:
            bc_links.append(get_bc_links(url))
        except Exception as e:
            bc_links.append("https://www.target.com/DO_IT_MANUALLY")
            print(f'"\033[31m" Brand is not in local, do following target url manually: {url}"\033[0m"\n\n')
    print(f"BC_LINKS: {bc_links}")

    for link, p_url in zip(bc_links, target_urls):
        redirections = []
        if 'https:' not in link:
            all_redirections.append("https://www.target.com/DO_IT_MANUALLY")
            pass
        all_redirections.append(get_location(link, p_url))

    redirections_to_csv('BC_redirs.csv', bc_links, all_redirections)

