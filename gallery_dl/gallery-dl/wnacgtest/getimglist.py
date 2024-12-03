import requests
import re
import json

def fetch_image_list(aid, proxies=None):
    """
    give aid
    return json in current dir
    """
    # Construct the URL
    base_url = "https://www.wnacg.com/photos-gallery-aid-{}.html"
    url = base_url.format(aid)

    try:
        # Send GET request to fetch the content
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        content = response.text
        img_list_pattern = r'imglist\s*=\s*(\[.*?}\]);'
        match = re.search(img_list_pattern, content)

        if match:
            imglist_content = match.group(1)
            url_pattern = r'url:\s*fast_img_host\+\\"([^\"]+)\\"'
            # url_pattern = r'data(.*?\.webp)'
            img_urls = re.findall(url_pattern, imglist_content)

            # Construct the full URLs
            fast_img_host = "https:"  # Assuming `fast_img_host` is `https:` as inferred from the content
            img_list = [fast_img_host + url for url in img_urls]
            img_list.pop()

            # Save to JSON file
            json_file = f"{aid}.json"
            with open(json_file, "w", encoding="utf-8") as file:
                json.dump(img_list, file, indent=2, ensure_ascii=False)

            print(f"Image list saved to {json_file}")
            return img_list
        else:
            print("No imglist found in the response content.")
            return []

        print(f"Image list saved to {json_file}")
        return img_list

    except requests.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return []

# Example usage
if __name__ == "__main__":
    # Replace '12345' with the actual aid value
    aid = input("Enter the aid: ")
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }
    image_list = fetch_image_list(aid, proxies=proxies)
    print(f"Fetched {len(image_list)} image URLs.")
