# Submission info

### The result of applying the exercise on the attached image (Lenna.png) and mask (Mask.png) with 8-connectivity and the default weighting function using 𝑧 = 3 and ϵ = 0. 01. The mask represents hole pixels as any pixel with an intensity value of less than 0.5.

```sh
Result: resources/Filled_c8_111524_112702.png
```

![Result](resources/Filled_c8_111524_112702.png)

# Answers to questions

### Q1: If there are 𝑚 boundary pixels and 𝑛 pixels inside the hole, what’s the complexity of the algorithm that fills the hole, assuming that the hole and boundary were already found? Try to also express the complexity only in terms of 𝑛.

The overall time complexity is O(n * m).

**Expressing Complexity in Terms of n Only:**

If we assume m (number of boundary pixels) is proportional to the size of the hole (e.g., it scales as √n or log(n) depending on the shape and size of the hole), we can approximate m in terms of n:

If the boundary is roughly proportional to the perimeter of a region (2D), m could scale as O(√n).
Thus, the worst-case time complexity in terms of n would be:

O(n * m) ≈ O(n * √n) (if m scales as O(√n)).

---

### Q2: Describe an algorithm that approximates the result in 𝑂(𝑛) to a high degree of accuracy.

### Flood Fill

A simple flood fill algorithm:
 - iterates through each pixel in the image
 - when a hole is detected
 - calculates the mean value of its neighboring non-hole pixels
 - This value is then assigned as the new value for the hole.
    
This implementation allows configuration of the number of neighboring pixels to consider,
supporting both 4-connected and 8-connected neighbors, with a default setting of 4-connected.

- **Time Complexity**: The algorithm has a time complexity of O(n), where n
is the total number of pixels in the image. Each pixel is processed once,
ensuring efficient traversal.


```sh
python q2_flood_fill.py ./resources/Lenna.png ./resources/Mask.png --connectivity 8
```

![Flood Fill](resources/Filled_floodFill_c8_111524_120225.png)

---

### Q3: Describe and implement an algorithm that finds the exact solution in 𝑂(𝑛𝑙𝑜𝑔𝑛). 

### OpenCV - Fast Marching Method

[Fast marching method](https://en.wikipedia.org/wiki/Fast_marching_method) is a
numerical algorithm used for solving problems related to the propagation of a
moving front or wave.  In the context of region filling in images, FMM can be
thought of as simulating how information (e.g., pixel values) spreads from known
regions into unknown regions (holes) in an ordered manner.

Brief Mechanism of Fast Marching in Region Filling:

Initialization:
 - Identify boundary pixels of the hole and label them as known (accepted).
 - Place these boundary pixels in a priority queue (min-heap) based on their initial distance or order of influence.

Propagation:
 - Continuously extract the pixel with the smallest distance (i.e., highest priority) from the queue.
 - Label this pixel as accepted and consider it part of the known region.
 - For each neighboring pixel that is not yet known:
 - Estimate its value based on its surrounding known pixels.
 - Add the pixel to the priority queue with an updated distance value to indicate when it should be processed.

Updating Values:
 - Use neighboring accepted pixel values to compute an approximation of the current pixel's value, typically by averaging or weighted methods.
 - This ensures that the value is smoothly propagated into the hole in a consistent manner.

Completion:
 - The process continues until all pixels in the hole are labeled as accepted and filled with appropriate values.

Key Points:
 - **Priority Queue**: Ensures that pixels are processed in an order that mimics wavefront propagation.
 - **Distance Metric**: Helps determine the order of propagation, ensuring the algorithm fills the region smoothly from the boundaries inward.
 - **Efficiency**: The use of a priority queue gives the method a time complexity of O(nlogn), where n is the number of pixels being processed.

This mechanism results in a natural and efficient way of propagating known values
into unknown areas, ideal for filling holes in images with realistic gradients.

[OpenCV](https://docs.opencv.org/3.4/df/d3d/tutorial_py_inpainting.html#:~:text=Once%20a%20pixel%20is%20inpainted,by%20using%20the%20flag%2C%20cv.) provides built-in support to FMM.

```sh
python q3_fmm.py ./resources/Lenna.png ./resources/Mask.png
```

![FMM](resources/Filled_fmm_111524_120325.png)
