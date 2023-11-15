#################################################
# hw7.py
#
# Full Name: Khasanboy Khakimjanov

# This assignment is SOLO!
#################################################

#################################################


def hashValue(s):
    # convert the letters ordered in lower case
    return "".join(sorted(s.lower()))


# functions swap first and last elements of lst


def slow1(lst):  # N is the length of the list lst
    assert len(lst) >= 2  # O(1)
    a = lst.pop()  # O(1)
    b = lst.pop(0)  # O(1)
    lst.insert(0, a)  # O(1)
    lst.append(b)  # O(1)
    # function time complexity is O(1)


def fast1(lst):
    assert len(lst) >= 2  # O(1)
    lst[0], lst[-1] = lst[-1], lst[0]  # O(1)
    # function time complexity is O(1)


# functions counts distinct number of elements in lst


def slow2(lst):  # N is the length of the list lst
    counter = 0  # O(1)
    for i in range(len(lst)):  # O(N)
        if lst[i] not in lst[:i]:  # O(N)
            counter += 1  # O(1)
    return counter  # O(1)
    # function time complexity is O(N^2)


def fast2(lst):  # N is the length of the list lst
    counter = 0  # O(1)
    lstSet = set(lst)  # O(N)
    return len(lstSet)  # O(1)
    # function time complexity is O(N)


# function calculates most occurent lower case letter in given string

import string


def slow3(s):  # N is the length of the string s

    maxLetter = ""  # O(1)
    maxCount = 0  # O(1)
    for c in s:  # O(N)
        for letter in string.ascii_lowercase:  # O(26)
            if c == letter:  # O(1)
                if (
                    s.count(c) > maxCount
                    or s.count(c) == maxCount
                    and c < maxLetter
                ):  # O(2N)
                    maxCount = s.count(c)  # O(N)
                    maxLetter = c  # O(1)
    return maxLetter
    # function time complexity is O(N^2)


def fast3(s):  # N is the length of the string s
    maxLetter = ""  # O(1)
    maxCount = 0  # O(1)
    letters = {}  # O(1)
    for c in s:  # O(N)
        value = letters.get(c, 0)  # O(1)
        value += 1  # O(1)
        letters[c] = value  # O(1)
    for letter in string.ascii_lowercase:  # O(26)
        value = letters.get(letter, None)
        if value is not None:
            if (
                value > maxCount or value == maxCount and letter < maxLetter
            ):  # O(1)
                maxCount = value  # O(1)
                maxLetter = letter  # O(1)
    return maxLetter
    # function time complexity is O(N)


# function calculates biggest difference elements of 2 lists


def slow4(a, b):  # a and b are lists with the same length N
    n = len(a)  # O(1)
    assert n == len(b)  # O(1)
    result = abs(a[0] - b[0])  # O(1)
    for c in a:  # O(N)
        for d in b:  # O(N)
            delta = abs(c - d)  # O(1)
            if delta > result:
                result = delta
    return result
    # function time complexity is O(N^2)


def fast4(a, b):
    assert len(a) == len(b)  # O(1)
    minA, maxA, minB, maxB = a[0], a[0], b[0], b[0]
    for i in range(len(a)):  # O(N)
        minA, minB = min(minA, a[i]), min(minB, b[i])  # O(1)
        maxA, maxB = max(maxA, a[i]), max(maxB, b[i])  # O(1)
    return max(maxA - minB, maxB - minA)  # O(1)
    # function time complexity is O(N)


#################################################

import math


def invertDictionary(d):
    # final result to collect values form d
    result = {}
    for key in d:
        # check for key existance and add new element to dict value
        value = result.get(d[key], set())
        value.add(key)
        result[d[key]] = value
    return result


def destinationCity(paths):
    # go through each city and check if destination exists in paths as a key
    for city in paths:
        if paths.get(paths[city], None) is None:
            return paths[city]
    return None


def groupAnagrams(S):
    # dict to store anagram words
    anagramDict = {}
    # go through every word and group them to anagrams
    for word in S:
        value = anagramDict.get(hashValue(word), set())
        value.add(word)
        anagramDict[hashValue(word)] = value
    # return dict values as a list
    return list(anagramDict.values())


def movieAwards(oscarResults):
    # dictionary to store movies
    movies = {}
    # go through oscar results and movie in the dict
    for award, movie in oscarResults:
        value = movies.get(movie, 0)
        value += 1
        movies[movie] = value
    return movies


def containsPythagoreanTriple(a):
    # create set containing numbers in a
    numbersSet = set(a)
    # iterate every 2 elements of list and check if hypotenuse exists
    for i in range(len(a) - 1):
        for j in range(i + 1, len(a)):
            # calculate hypotenuse
            cSquared = a[i] ** 2 + a[j] ** 2
            c = int(cSquared**0.5)
            if c * c == cSquared and c in numbersSet:
                return True
    return False


def test_InvertDictionary():
    print("Testing invertDictionary()... ", end="")
    assert invertDictionary({1: 2, 2: 3, 3: 4, 5: 3}) == {
        2: set([1]),
        3: set([2, 5]),
        4: set([3]),
    }
    assert invertDictionary({"a": "b", "b": "c", "c": "b", "d": "e"}) == {"b": set(["a", "c"]),
        "c": set(["b"]),
        "e": set(["d"]),
    }
    assert invertDictionary({"a": 1, "b": "c", 3: "c"}) == {
        1: set(["a"]),
        "c": set(["b", 3]),
    }
    assert invertDictionary({}) == {}
    assert invertDictionary({1: 1, 2: 2, 3: 3}) == {
        1: set([1]),
        2: set([2]),
        3: set([3]),
    }
    print("Passed!")


def testDestinationCity():
    print("Testing destinationCity()... ", end="")
    paThs1 = {"London": "New York", "New York": "Lima", "Lima": "Sao Paulo"}
    assert destinationCity(paThs1) == "Sao Paulo"

    paths2 = {"B": "C", "D": "B", "C": "A"}
    assert destinationCity(paths2) == "A"
    paths3 = {"Tokyo": "Osaka"}
    assert destinationCity(paths3) == "Osaka"
    paths4 = {"A": "B", "B": "C", "C": "D", "D": "E", "E": "F"}
    assert destinationCity(paths4) == "F"
    paths5 = {}
    assert destinationCity(paths5) is None

    print("Passed!")


def testGroupAnagrams():
    print("Testing groupAnagrams()... ", end="")

    # Given examples
    S1 = ["eat", "tea", "tan", "ate", "nat", "bat"]
    result1 = groupAnagrams(S1)
    assert {"bat"} in result1
    assert {"nat", "tan"} in result1
    assert {"ate", "eat", "tea"} in result1
    assert len(result1) == 3

    S2 = [
        "own",
        "read",
        "dare",
        "eat",
        "now",
        "stop",
        "now",
        "spot",
        "15112",
        "tea",
    ]
    result2 = groupAnagrams(S2)
    assert {"own", "now"} in result2
    assert {"read", "dare"} in result2
    assert {"eat", "tea"} in result2
    assert {"stop", "spot"} in result2
    assert {"15112"} in result2
    assert len(result2) == 5

    # Additional tests
    # No words
    S3 = []
    result3 = groupAnagrams(S3)
    assert result3 == []

    # Single word
    S4 = ["apple"]
    result4 = groupAnagrams(S4)
    assert {"apple"} in result4
    assert len(result4) == 1

    # Case sensitivity
    S5 = ["Aa", "aA", "bB", "Bb", "Cc"]
    result5 = groupAnagrams(S5)
    assert {"Aa", "aA"} in result5
    assert {"bB", "Bb"} in result5
    assert {"Cc"} in result5
    assert len(result5) == 3

    print("Passed!")


def testMovieAwards():
    print("Testing movieAwards()... ", end="")

    # Given example
    oscarResults1 = {
        ("Best Picture", "The Shape of Water"),
        ("Best Actor", "Darkest Hour"),
        ("Best Actress", "Three Billboards Outside Ebbing, Missouri"),
        ("Best Director", "The Shape of Water"),
        ("Best Supporting Actor", "Three Billboards Outside Ebbing, Missouri"),
        ("Best Supporting Actress", "I, Tonya"),
        ("Best Original Score", "The Shape of Water"),
    }
    expected1 = {
        "Darkest Hour": 1,
        "Three Billboards Outside Ebbing, Missouri": 2,
        "The Shape of Water": 3,
        "I, Tonya": 1,
    }
    assert movieAwards(oscarResults1) == expected1

    # Additional tests
    # No awards
    oscarResults2 = set()
    expected2 = {}
    assert movieAwards(oscarResults2) == expected2

    # Single award
    oscarResults3 = {("Best Picture", "Titanic")}
    expected3 = {"Titanic": 1}
    assert movieAwards(oscarResults3) == expected3

    # Multiple awards for same movie
    oscarResults4 = {        ("Best Picture", "Inception"),        ("Best Director", "Inception"),
        ("Best Cinematography", "Inception"),
    }
    expected4 = {"Inception": 3}
    assert movieAwards(oscarResults4) == expected4

    # Multiple awards for multiple movies
    oscarResults5 = {
        ("Best Picture", "A Beautiful Mind"),
        ("Best Director", "A Beautiful Mind"),
        ("Best Actor", "Gladiator"),
        ("Best Supporting Actor", "Gladiator"),
    }
    expected5 = {"A Beautiful Mind": 2, "Gladiator": 2}
    assert movieAwards(oscarResults5) == expected5

    print("Passed!")


def testContainsPythagoreanTriple():
    print("Testing containsPythagoreanTriple()... ", end="")

    assert containsPythagoreanTriple([1, 3, 6, 2, 5, 1, 4]) == True
    assert containsPythagoreanTriple([3, 4, 5, 10, 20, 30]) == True
    assert containsPythagoreanTriple([1, 2, 3, 4, 12, 5, 13, 6, 7]) == True
    assert containsPythagoreanTriple(list(range(1, 1000))) == True
    assert (
        containsPythagoreanTriple(list(range(1, 1000)) + [5, 12, 13]) == True
    )
    assert containsPythagoreanTriple([3, 3, 4, 4, 5, 5]) == True
    assert containsPythagoreanTriple([5, 3, 4]) == True
    assert containsPythagoreanTriple([5, 12, 13, 8, 15, 17, 3, 4, 5]) == True
    assert containsPythagoreanTriple([3, 4, 6]) == False
    assert containsPythagoreanTriple([]) == False
    assert containsPythagoreanTriple([8, 7, 2, math.sqrt(8)]) == False
    assert containsPythagoreanTriple([5, 3, 4]) == True

    print("Passed!")


def testSwapFunctions():
    print("Testing slow1 and fast1... ", end="")

    # Case: Basic swap test
    lst1 = [1, 2, 3, 4, 5]
    lst2 = lst1.copy()
    slow1(lst1)
    fast1(lst2)
    assert lst1 == [5, 2, 3, 4, 1]
    assert lst2 == [5, 2, 3, 4, 1]

    # Case: Larger list
    lst1 = list(range(1000))
    lst2 = lst1.copy()
    slow1(lst1)
    fast1(lst2)
    assert (
        lst1[0] == 999 and lst1[-1] == 0 and lst1[1:-1] == list(range(1, 999))
    )
    assert (
        lst2[0] == 999 and lst2[-1] == 0 and lst2[1:-1] == list(range(1, 999))
    )

    # Case: List with repeated elements
    lst1 = [1, 2, 2, 2, 3, 3, 3, 4]
    lst2 = lst1.copy()
    slow1(lst1)
    fast1(lst2)
    assert lst1 == [4, 2, 2, 2, 3, 3, 3, 1]
    assert lst2 == [4, 2, 2, 2, 3, 3, 3, 1]

    # Case: Minimum size list
    lst1 = [5, 7]
    lst2 = lst1.copy()
    slow1(lst1)
    fast1(lst2)
    assert lst1 == [7, 5]
    assert lst2 == [7, 5]

    print("Passed!")


def testDistinctCountFunctions():
    print("Testing slow2 and fast2... ", end="")

    # Case: List with no duplicate elements
    lst = [1, 2, 3, 4, 5]
    assert slow2(lst) == 5
    assert fast2(lst) == 5

    # Case: List with all duplicate elements
    lst = [2, 2, 2, 2, 2]
    assert slow2(lst) == 1
    assert fast2(lst) == 1

    # Case: List with some duplicate elements
    lst = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]
    assert slow2(lst) == 5
    assert fast2(lst) == 5

    # Case: Empty list
    lst = []
    assert slow2(lst) == 0
    assert fast2(lst) == 0

    # Case: Larger list with mixed duplicates
    lst = list(range(1000)) + list(range(500, 1500))
    assert slow2(lst) == 1500
    assert fast2(lst) == 1500

    print("Passed!")


def testMostOccurrentLetterFunctions():
    print("Testing slow3 and fast3... ", end="")

    # Case: One letter clearly occurs the most
    s = "aabbccddeee"
    assert slow3(s) == "e"
    assert fast3(s) == "e"

    # Case: Tie in frequency, 'a' is lexicographically smaller than 'b'
    s = "aaabbb"
    assert slow3(s) == "a"
    assert fast3(s) == "a"

    # Case: No lowercase letters
    s = "12345ABCDE"
    assert slow3(s) == ""
    assert fast3(s) == ""

    # Case: Empty string
    s = ""
    assert slow3(s) == ""
    assert fast3(s) == ""

    # Case: Large string with mixed duplicates
    s = "a" * 10000 + "b" * 9999 + "c" * 5000
    assert slow3(s) == "a"
    assert fast3(s) == "a"

    print("Passed!")


def testBiggestDifferenceFunctions():
    print("Testing slow4 and fast4... ", end="")

    # Case: Clear big difference between elements of both lists
    a, b = [1, 2, 3], [10, 20, 30]
    assert slow4(a, b) == 29
    assert fast4(a, b) == 29

    # Case: All elements are equal in both lists
    a, b = [5, 5, 5], [5, 5, 5]
    assert slow4(a, b) == 0
    assert fast4(a, b) == 0

    # Case: Mixed positive and negative numbers
    a, b = [-5, 0, 5], [5, 0, -5]
    assert slow4(a, b) == 10
    assert fast4(a, b) == 10

    # Case: Large lists
    a = list(range(1, 10001))
    b = list(range(10000, 0, -1))
    assert slow4(a, b) == 9999
    assert fast4(a, b) == 9999

    print("Passed!")


def testAll():
    # comment out the tests you do not wish to run!
    # testInvertDictionary()
    testDestinationCity()
    testGroupAnagrams()
    testMovieAwards()
    testContainsPythagoreanTriple()
    testSwapFunctions()
    testDistinctCountFunctions()
    testMostOccurrentLetterFunctions()
    testBiggestDifferenceFunctions()


def main():
    testAll()


if __name__ == "__main__":
    main()