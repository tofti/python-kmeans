#include <stdint.h>

uint64_t max(uint64_t x, uint64_t y) { return x > y ? x : y; }


struct point {
    uint8_t r, g, b;
    uint8_t center;
    uint32_t count;
};


struct center {
    uint64_t r, g, b;
    uint32_t count;
};


void centers_zero(struct center *centers, uint8_t n)
{
    for (uint8_t i = 0; i < n; i++) {
        centers[i].r = 0;
        centers[i].g = 0;
        centers[i].b = 0;
        centers[i].count = 0;
    }
}

void center_normalize(struct center *center)
{
    /* No need to change center->count since the center will
       get cleared before it's used again */
    uint32_t w = center->count;

    if (w == 0) {
        return;
    }
    center->r /= w;
    center->g /= w;
    center->b /= w;
}

void center_copy(struct center *dst, struct center *other)
{
    /* Don't copy center count */
    dst->r = other->r;
    dst->g = other->g;
    dst->b = other->b;
}

void center_accumulate(struct center *c, struct point *p)
{
    /* Multiply by count since we're "expanding" the other point */
    uint32_t count = p->count;

    c->r += count * p->r;
    c->g += count * p->g;
    c->b += count * p->b;
    c->count += count;
}

uint64_t center_center_distance(struct center *c1, struct center *c2)
{
    /* count does not impact distance */
    return (c1->r - c2->r) * (c1->r - c2->r)
         + (c1->g - c2->g) * (c1->g - c2->g)
         + (c1->b - c2->b) * (c1->b - c2->b);
}

uint64_t point_center_distance(struct point *p, struct center *c)
{
    /* count does not impact distance */
    return (p->r - c->r) * (p->r - c->r)
         + (p->g - c->g) * (p->g - c->g)
         + (p->b - c->b) * (p->b - c->b);
}


void kmeans_assign(
    struct point *points, uint32_t npoints,
    struct center *centers, uint8_t ncenters)
{

    for (uint32_t i = 0; i < npoints; ++i) {
        uint64_t min_dist = UINT64_MAX;

        for (uint8_t j = 0; j < ncenters; ++j) {
            uint64_t dist =
                point_center_distance(&points[i], &centers[j]);
            if (dist < min_dist) {
                min_dist = dist;
                points[i].center = j;
            }
        }
    }
}

uint64_t kmeans_update(
    struct point *points, uint32_t npoints,
    struct center *centers, struct center *temp_centers,
    uint8_t ncenters)
{
    uint8_t j;
    uint64_t diff = 0;

    centers_zero(temp_centers, ncenters);
    for (uint32_t i = 0; i < npoints; ++i) {
        j = points[i].center;
        center_accumulate(&temp_centers[j], &points[i]);
    }

    for (j = 0; j < ncenters; ++j) {
        center_normalize(&temp_centers[j]);
        diff = max(
            diff,
            center_center_distance(&centers[j], &temp_centers[j])
        );
        center_copy(&centers[j], &temp_centers[j]);
    }
    return diff;
}

void kmeans(
    struct point *points, uint32_t npoints,
    struct center *centers, uint8_t ncenters,
    uint16_t tolerance, uint16_t max_iterations)
{
    uint16_t delta, remaining_iterations;
    struct center temp_centers[ncenters];

    if (max_iterations <= 0) {
        delta = 0;
        remaining_iterations = 1;
    } else {
        delta = 1;
        remaining_iterations = max_iterations;
    }

    while (remaining_iterations > 0) {
        remaining_iterations -= delta;

        kmeans_assign(points, npoints, centers, ncenters);
        uint64_t diff = kmeans_update(points, npoints,
            centers, temp_centers, ncenters);

        if (diff <= tolerance || remaining_iterations < 1) {
            return;
        }
    }
}
