# Function to add movie to files
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
                fpAddSeats.write(f"{i[0]} {i[1]}\n")
    fpAddSeats.close()

# Function to update movie in the file
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

# Function to add the booked seats to file
def updateBooked(booked, movies):
    fpUpdateBooked = open("booked.txt", "w")

    fpUpdateBooked.write(str(len(movies)) + "\n")
    for ID in movies:
        fpUpdateBooked.write(ID + "\n")
        fpUpdateBooked.write(str(len(booked[ID])) + "\n")
        if len(booked[ID]) != 0:
            for i in booked[ID]:
                fpUpdateBooked.write(f"{i[0]} {i[1]}\n")
    fpUpdateBooked.close()

# Function to update discount codes in the file
def updateDiscount(discount):
    fpUpdateDiscount = open("discount.txt", "w")

    for code in discount:
        fpUpdateDiscount.write(f"{code} {discount[code]}\n")
    fpUpdateDiscount.close()

# Function to load movies in the file to a dictionary
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

            movies[movieID] = [movieName, genre, restrict, venue, date, startTime, endTime, int(price)]
    fpMovies.close()

    return movies

# Function to load seats in the file to a dictionary
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

# Function to load booked seats in the file to a dictionary
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
                (seatNum, price) = (fpBooked.readline()[:-1]).split(" ")
                seats.append([seatNum, float(price)])

        booked[ID] = seats
    fpBooked.close()
    return booked

# Function to load discount codes in the file to a dictionary
def loadDiscount():
    fpDiscount = open("discount.txt", "r")
    discount = {}

    for line in fpDiscount.readlines():
        code, off = line.split()
        discount[code] = int(off)

    fpDiscount.close()

    return discount