# Get the largest blank square area in a picture

<img src="https://github.com/hansalemaos/screenshots/raw/main/cv2_putTrueTypeText_000015.png"/>
<img src="https://github.com/hansalemaos/screenshots/raw/main/findsquare.png"/>

```python
$pip install a-cv2-find-biggest-square

#adding to cv2
from a_cv2_imshow_thread import add_imshow_thread_to_cv2
add_imshow_thread_to_cv2()
from a_cv2_find_biggest_square import add_find_biggest_square_to_cv2
add_find_biggest_square_to_cv2()
import cv2
bil = r"https://github.com/hansalemaos/screenshots/raw/main/cv2_putTrueTypeText_000015.png"
box, resultpic, length = cv2.find_largest_square(
    image=bil, scale_percent=30, gaussian_blur=6, draw_result=True
)

cv2.imshow_thread(resultpic)


#without adding to cv
from a_cv2_imshow_thread import add_imshow_thread_to_cv2
add_imshow_thread_to_cv2()
from a_cv2_find_biggest_square import find_largest_square
import cv2
bil = r"https://github.com/hansalemaos/screenshots/raw/main/cv2_putTrueTypeText_000015.png"
box, resultpic, length = find_largest_square(
    image=bil, scale_percent=30, gaussian_blur=6, draw_result=True
)




```