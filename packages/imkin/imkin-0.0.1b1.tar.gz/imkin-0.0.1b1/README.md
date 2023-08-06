Lightweight a movie data parser like title, original title, release date and duration from imdb.com and kinopoisk.ru without using third-party packages.

Install:

    pip install imkin

Example:

    import imkin
    
    film = imkin.new('https://www.imdb.com/title/tt0068646/')
    
    print(film.title)
    
    print(film.original)
    
    print(film.year)
    
    print(film.duration)
    
    print(film)
