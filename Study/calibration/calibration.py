
import cv2, numpy as np
import math

img1 = cv2.imread('C:/Users/1315/Desktop/cal/2/img_1_00013.jpg')
img2 = cv2.imread('C:/Users/1315/Desktop/cal/2/img_2_00000.jpg')
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# ORB, BF-Hamming 로 knnMatch
detector = cv2.ORB_create()
kp1, desc1 = detector.detectAndCompute(gray1, None)
kp2, desc2 = detector.detectAndCompute(gray2, None)
matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = matcher.match(desc1, desc2)

matches = sorted(matches, key=lambda x:x.distance)
good_matches = matches[:4]

print('# of kp1:', len(kp1))
print('# of kp2:', len(kp2))
print('# of matches:', len(matches))
print('# of good_matches:', len(good_matches))


# 근매칭점으로 원 변환 및 영역 표시
src_pts = np.float32([ kp1[m.queryIdx].pt for m in good_matches ]).reshape(-1, 1, 2).astype(np.float32)
dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good_matches ]).reshape(-1, 1, 2).astype(np.float32)

# RANSAC으로 변환 행렬 근사 계산
mtrx, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 0.8)

h,w = img1.shape[:2]
pts = np.float32([ [[0,0]],[[0,h-1]],[[w-1,h-1]],[[w-1,0]] ])
dst = cv2.perspectiveTransform(pts,mtrx)
if np.shape(mtrx) == ():
    print("No transformation possible")

# ## derive rotation angle from homography
# theta = - math.atan2(mtrx[0, 1], mtrx[0, 0]) * 180 / math.pi
#
# print('rotation angle',theta)
# for m in matches:
#     print(kp1[m.queryIdx].pt,kp2[m.trainIdx].pt)

print('H:',mtrx)


# 정상치 매칭만 그리기
matchesMask = mask.ravel().tolist()

res2 = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, \
                    matchesMask = matchesMask,
                    flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

# 모든 매칭점과 정상치 비율 ---⑧
# accuracy=float(mask.sum()) / mask.size
# print("accuracy: %d/%d(%.2f%%)"% (mask.sum(), mask.size, accuracy))

# 결과 출력
#cv2.imshow('Matching-All', res1)
cv2.imshow('Matching-Inlier ', res2)

cv2.waitKey()
cv2.destroyAllWindows()