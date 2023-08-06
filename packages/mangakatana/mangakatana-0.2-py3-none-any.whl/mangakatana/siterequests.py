
import requests

_ROOT_URL = "http://mangakatana.com/"


def get(url):
	return requests.get(url, stream=True, timeout=10)


def search(title: str):
	return get(f"{_ROOT_URL}?search={title}&search_by=book_name")
