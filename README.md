# Handwritten Digit Recognition Based on Correlation and Discrimination

> [!NOTE]
> This project was created by myself, but since it's too late — already 2:20 a.m. on October 25, 2026—I'm extremely tired, so this README was written with help from Claude. The original text is !!!! readme.txt !!!! Suggest reading this directly

---

## 📖 Purpose

While studying Week 5 of **Communication Systems**, I came across **Auto-correlation** and **Cross-correlation**. I found that in the one-dimensional case, they can be used to search a continuous, very long signal for the corresponding sync code and compare it. Using **Discrimination** to get the peak value, this project achieves the distinction and recognition of digits.

---

## 🧠 Principle

The learning material mentions:

$$
R(k) = \sum_{n} x[n] \cdot y[n-k]
$$

The purpose is to do a convolution: keep signal $x$ fixed, shift signal $y$ to the left each time to get the products, and add all the products together to get $R$. Then use $R(0) / |R(k)|$ to get $D$:

$$
D = \frac{R(0)}{|R(k)|}
$$

$D$ is the **discrimination**.

But I found that for a 2D signal, the left shift by $k$ can be changed into moving up, down, left and right ($r_x$ and $r_y$):

$$
R_{xy}(r_x, r_y) = \sum_{i}\sum_{j} x[i, j] \cdot y[i - r_x,\ j - r_y]
$$

Using Cross-correlation in 2D gives **25 groups** of $R_{xy}(k)$. Compare the 25 groups across digits **1–9** to find the maximum value. The maximum value is the **similarity** — the higher the similarity, the closer the match.

---

## ⚠️ Problems Found

After building the basic principle, I found that the recognition error was very large (for details, see `Cross-Correlation.py` and `identify.py`).

So on top of that, I added **NCC** to remove the bias of the white background — the mean value produced between the white and black pixels that get added after shifting with offsets $r_x$ and $r_y$. Formula:

$$
\text{mean} = \frac{(\text{Black} \times 1) + \big((400 - \text{Black}) \times (-1)\big)}{400}
$$

**400** is because the recognized image size is **20 × 20 px**. The size I originally used was 10 × 10, but while adjusting the bias I found that image size doesn't really help much with recognition.

### 🤔 A Strange Phenomenon

Although the formula was used to remove the white background interference, I eventually found that in:

```python
new = Moving_Data(C_data_L, dx, dy)
C_ave = aveList(C_data_L)
```

the value passed into the `aveList` function is still the original, **unshifted** value. So the conclusion is: **using `C_data_L` gives a higher success rate than using `new`**. This is a very strange phenomenon.

---

## 📁 Project Structure

```
├── 1.png ~ 9.png            # Templates for digits 1–9
├── drawing.png              # Handwritten input image
├── Cross-Correlation.py     # Basic cross-correlation implementation
├── identify.py              # Recognition logic
└── Drawing_and_identify.py  # Draw a digit and identify it
```
