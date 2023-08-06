[![Downloads](https://pepy.tech/badge/mangakatana)](https://pepy.tech/project/mangakatana) [![Downloads](https://pepy.tech/badge/mangakatana/month)](https://pepy.tech/project/mangakatana/month) [![Downloads](https://pepy.tech/badge/mangakatana/week)](https://pepy.tech/project/mangakatana/week)

# Unofficial Mangakatana API

###### Package to scrape the Mangakatana website. Want to contribute? Pull requests are encouraged!

Installation
-
**Python 3.7+**
```cmd
pip install manganelo
```

Examples
-
```python
import mangakatana

results = mangakatana.search(title="Naruto")

first = results[0]

chapters = first.chapter_list()
# mangakatana.chapter_list(url=first.url)
```