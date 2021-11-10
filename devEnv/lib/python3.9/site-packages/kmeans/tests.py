from kmeans import kmeans


def test_single_point():
    value = [0, 10, 20]
    points = [
        [value, 1]
    ]
    k = 1
    means = kmeans(points, k)
    assert 1 == len(means)
    assert value == means[0]


def test_single_point_with_guess():
    value = [0, 10, 20]
    guess = [(20, 50, 100), 1]
    points = [
        [value, 1]
    ]
    k = 1
    centers = [
        guess
    ]
    means = kmeans(points, k, centers=centers)
    assert 1 == len(means)
    assert value == means[0]


def test_two_points():
    real_mean = [10, 10, 10]
    points = [
        [(0, 0, 0), 1],
        [(20, 20, 20), 1]
    ]
    k = 1
    means = kmeans(points, k)
    assert 1 == len(means)
    assert real_mean == means[0]


def test_two_points_two_centers():
    values = [
        [0, 10, 20],
        [100, 144, 64]
    ]
    points = [
        [value, 1] for value in values
    ]
    k = 2
    means = kmeans(points, k)
    assert 2 == len(means)
    for value in values:
        assert value in means


def test_two_points_with_weights():
    real_mean = [20, 20, 20]
    points = [
        [(0, 0, 0), 1],
        [(30, 30, 30), 2]
    ]
    k = 1
    means = kmeans(points, k)
    assert 1 == len(means)
    assert real_mean == means[0]
