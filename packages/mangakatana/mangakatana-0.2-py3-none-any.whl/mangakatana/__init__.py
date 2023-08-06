
def search(*, title: str):
	from mangakatana import mangasearch

	return mangasearch.perform_search(title)


def chapter_list(*, url: str):
	from mangakatana.chapterlist import ChapterList

	return ChapterList(url).get()
