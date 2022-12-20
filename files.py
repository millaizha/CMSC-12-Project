def addMovieToFile(movies, booked):
    fpReadMovies = open("movies.txt", "r")
    intMovieID = int(fpReadMovies.readline()) + 1
    fpReadMovies.close()

    fpAddMovie = open("movies.txt", "w")
    fpAddMovie.write(str(intMovieID) + "\n")
    fpAddMovie.write(str(len(movies)) + "\n")
    for ID in movies:
        fpAddMovie.write(f"{ID}\n{movies[ID][0]}\n{movies[ID][1]}\n{movies[ID][2]}\n{movies[ID][3]}\n{movies[ID][4]}\n{movies[ID][5]}\n{movies[ID][6]}\n{movies[ID][7]}\n")
    fpAddMovie.close()

    fpAddSeats = open("booked.txt", "w")
    fpAddSeats.write(str(len(movies)) + "\n")
    for ID in movies:
        fpAddSeats.write(ID + "\n")
        fpAddSeats.write(str(len(booked[ID])) + "\n")
        if len(booked[ID]) != 0:
            for i in booked[ID]:
                fpAddSeats.write(i)
    fpAddSeats.close()

def updateMovie(movies):
    fpRead = open("movies.txt", "r")
    intMovieID = int(fpRead.readline())
    fpRead.close()

    fpAddMovie = open("movies.txt", "w")
    fpAddMovie.write(str(intMovieID) + "\n")
    fpAddMovie.write(str(len(movies)) + "\n")
    for ID in movies:
        fpAddMovie.write(f"{ID}\n{movies[ID][0]}\n{movies[ID][1]}\n{movies[ID][2]}\n{movies[ID][3]}\n{movies[ID][4]}\n{movies[ID][5]}\n{movies[ID][6]}\n{movies[ID][7]}\n")
    fpAddMovie.close()

def updateBooked(booked, movies):
    fpUpdateBooked = open("booked.txt", "w")

    fpUpdateBooked.write(str(len(movies)) + "\n")
    for ID in movies:
        fpUpdateBooked.write(ID + "\n")
        fpUpdateBooked.write(str(len(booked[ID])) + "\n")
        if len(booked[ID]) != 0:
            for i in booked[ID]:
                fpUpdateBooked.write(i)
    fpUpdateBooked.close()


def loadMovies():
    fpMovies = open("movies.txt", "r")
    movies = {}
    IDs = fpMovies.readline()
    if IDs != "0":
        num = int(fpMovies.readline()[:-1])
        for i in range(num):
            movieID = fpMovies.readline()[:-1]
            movieName = fpMovies.readline()[:-1]
            genre = fpMovies.readline()[:-1]
            restrict = fpMovies.readline()[:-1]
            venue = fpMovies.readline()[:-1]
            date = fpMovies.readline()[:-1]
            startTime = fpMovies.readline()[:-1]
            endTime = fpMovies.readline()[:-1]
            price = fpMovies.readline()[:-1]

            movies[movieID] = [movieName, genre, restrict, venue, date, startTime, endTime, price]
    fpMovies.close()

    return movies

def loadSeats():
    fpSeats = open("seats.txt", "r")
    seats = []
    for i in range(4):
        col1 = fpSeats.readline()[:-1]
        col2 = fpSeats.readline()[:-1]
        col3 = fpSeats.readline()[:-1]
        col4 = fpSeats.readline()[:-1]
        col5 = fpSeats.readline()[:-1]

        row = [col1, col2, col3, col4, col5]
        seats.append(row)
    fpSeats.close()        
    return seats

def loadBooked():
    fpBooked = open("booked.txt", "r")
    booked = {}
    numMovies = int(fpBooked.readline()[:1])
    for i in range(numMovies):
        ID = fpBooked.readline()[:-1]
        numSeats = int(fpBooked.readline()[:-1])
        seats = []
        if numSeats != 0:
            for j in range(numSeats):
                seats.append(fpBooked.readline()[:-1])

        booked[ID] = seats
    fpBooked.close()
    return booked