# Simple object to hold whether or not a seat is reserved and
# what the distance is from the best location
class Seat:
    def __init__(self, distance):
        self.reserved = False
        self.distance = distance


# Handles reserving seats, checking reservations, and booking by groups
class SeatingChart:
    distanceList = []

    def __init__(self, rows, seats):
        self.rows = rows
        self.seats = seats

        # This is the location that represents the best possible seat
        self.bestLocation = (1, (seats + 1) / 2.0)

        # Initialize seat array including availability and how ideal the location is
        self.chart = [
            [
                Seat(self.calculateManhattanDistance(i + 1, j + 1))
                for j in range(seats)
            ]
            for i in range(rows)
        ]

        # Create list of seats ordered by how ideal they are
        for row in range(rows):
            for seat in range(seats):
                self.distanceList.append(
                    (row + 1, seat + 1, self.calculateManhattanDistance(row + 1, seat + 1)))

        self.distanceList.sort(key=lambda seat: seat[2])

    # Marks a single seat as reserved
    def ReserveSeat(self, row, seat):
        if row > 0 and seat > 0 and row <= len(self.chart) and seat <= len(self.chart[row - 1]):
            self.chart[row - 1][seat - 1].reserved = True

    # Checks if a given seat is reserved
    def CheckSeatReserved(self, row, seat):
        if row > 0 and seat > 0 and row <= len(self.chart) and seat <= len(self.chart[row - 1]):
            return self.chart[row - 1][seat - 1].reserved
        else:
            return False

    # Returns the total number of unreserved seats currently left
    def TotalUnreservedSeats(self):
        totalSeats = 0

        for row in self.chart:
            for seat in row:
                if not seat.reserved:
                    totalSeats += 1

        return totalSeats

    # Calculates the distance of a seat from the best location
    # NOTE: This should only be used on setup of the initial chart to 
    # avoid extra work. Use getManhattanDistance after the chart is setup
    def calculateManhattanDistance(self, row, seat):
        (bestRow, bestSeat) = self.bestLocation
        return abs(bestRow - row) + abs(bestSeat - seat)

    # Retrieves the distance from best location for a given seat location
    def getManhattanDistance(self, row, seat):
        return self.chart[row - 1][seat - 1].distance

    # Gets all seats in a row that are adjacent to the given seat
    def getSurroundingSeats(self, row, seat, numSeats):
        seatList = []

        # Check current seat and ones to the right
        for i in range(seat, self.seats + 1):
            if self.CheckSeatReserved(row, i):
                break
            else:
                seatList.append((row, i, self.getManhattanDistance(row, i)))

        # Original seat was taken, exit
        if len(seatList) == 0:
            return []

        # Check seats to the left of current seat
        for i in range(seat - 1, 1, -1):
            if self.CheckSeatReserved(row, i):
                break
            else:
                seatList.append((row, i, self.getManhattanDistance(row, i)))

        return seatList

    # Finds the best seats on the chart given a certain number
    # of seats that must be adjacent to one another
    def FindBestSeats(self, numSeats):
        # Iterate from best to worst seats
        for (row, seat, _) in self.distanceList:
            seats = self.getSurroundingSeats(row, seat, numSeats)
            if len(seats) == numSeats:
                return seats
            elif len(seats) > numSeats:
                seats.sort(key=lambda s: s[2]) # sorts by distance
                return seats[:numSeats]

        return -1
