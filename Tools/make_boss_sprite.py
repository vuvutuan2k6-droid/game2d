# Tách nền caro khỏi ảnh boss gốc (JPEG, nền trắng/xám), lật sang phải, cắt sát hình, phóng 2x -> Assets/Resources/Sprites/boss.png
# Chạy: python3 Tools/make_boss_sprite.py ảnh_gốc.jpeg     (cần numpy, opencv-python, scipy)
import sys, numpy as np, cv2
from scipy import ndimage as ndi
src = sys.argv[1]
im = cv2.imread(src)
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32)
cand = (hsv[..., 1] < 38) & (hsv[..., 2] > 175)
lab, _ = ndi.label(cand)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = ndi.binary_closing(np.isin(lab, list(border)), iterations=2)
fg = ndi.binary_opening(~bg, iterations=1)
lab2, n2 = ndi.label(fg)
fg = lab2 == (1 + int(np.argmax(ndi.sum(fg, lab2, range(1, n2 + 1)))))
fg = ndi.binary_erosion(ndi.binary_fill_holes(fg), iterations=1)
ys, xs = np.where(fg); S = 2
big = cv2.resize(im, (im.shape[1] * S, im.shape[0] * S), interpolation=cv2.INTER_LANCZOS4)
a = cv2.GaussianBlur(cv2.resize(fg.astype(np.float32), (fg.shape[1] * S, fg.shape[0] * S)), (0, 0), 1.1)
a = np.clip((a - 0.5) * 2.2 + 0.5, 0, 1)
rgba = np.dstack([big, (a * 255).astype(np.uint8)])[max(ys.min() * S - 2, 0):ys.max() * S + 3, max(xs.min() * S - 2, 0):xs.max() * S + 3]
cv2.imwrite("Assets/Resources/Sprites/boss.png", rgba[:, ::-1].copy())  # lật: boss nhìn sang PHẢI
