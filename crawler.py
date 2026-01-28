def crawl_page(page):
    url = page['url']
    lastmod_remote = page.get('lastmod')
    attempt = 0
    sleep_interval = retry_interval

    while attempt < retry_times:
        attempt += 1
        try:
            info = fetch_page_info(url, wiki_name)
            page_id = info.get('pageId')

            if page_id:
                if fetch_rating:
                    info['rating'] = get_page_rating(wiki_name, page_id, wikidot_token, use_ssl)
                if fetch_history:
                    info['history'] = get_page_history(wiki_name, page_id, wikidot_token, use_ssl)
                if fetch_source:
                    info['pageSource'] = get_page_source(wiki_name, page_id, wikidot_token, use_ssl)

            info['lastmod'] = lastmod_remote

            output_dir = "pageinfo"
            os.makedirs(output_dir, exist_ok=True)
            with open(os.path.join(output_dir, f"{page_id}.json"), "w", encoding="utf-8") as f:
                json.dump(info, f, ensure_ascii=False, indent=2)

            return page_id, url, True
        except Exception:
            sleep(sleep_interval)
            sleep_interval *= 2

    with open(failed_list_file, "a", encoding="utf-8") as f:
        f.write(url + "\n")
    return None, url, False
