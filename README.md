# K-Means Clustering for Image Segmentation

This project implements **K-means clustering**, a form of unsupervised machine learning, for basic image segmentation using the Pillow (PIL) library.

The program:

1. Loads an image
2. Randomly initializes `k` color centroids (means)
3. Assigns each pixel to the nearest mean using Euclidean distance
4. Recomputes the cluster means iteratively
5. Recolors the image using the final clustered colors
6. Uses BFS to count connected color regions

---

## How K-Means Works

Each pixel in the image is represented as an RGB tuple:

```python
eg: (255, 120, 30)
```

The algorithm:

1. Selects `k` random colors as initial means
2. Computes the Euclidean distance from each pixel to every mean
3. Assigns pixels to the closest mean
4. Computes new average colors for each cluster
5. Repeats until the means stop changing

The result is an image reduced to only `k` colors.

---

## Image Segmentation with BFS

After clustering, the program performs basic image segmentation.

BFS works by:

1. Traverse neighboring pixels
2. Detect connected regions of the same clustered color
3. Count separate segmented regions

---

## Install Dependencies

```bash
pip install pillow
```

---

## Running the Program

Run the Python file:

```bash
python kmeans.py
```

The program will prompt for:

```text
k:
image file:
```

Example:

```text
k: 6
image file: turtle.jpg
```

---

## Example Output

```text
Size: 800 x 600
Pixels: 480000
Distinct pixel count: 102394
Most common pixel: (255, 255, 255) => 20389

Final means:
1 : (155.75, 113.44, 68.41) => 20389
2 : (202.10, 170.10, 121.78) => 9154
```
---

## Complexity

Time complexity per iteration:

```text
O(nk)
```

Where:

* `n` = number of pixels
* `k` = number of clusters

---
