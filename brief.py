import cv2
import time
# import numpy as np

imgs = []

img = cv2.imread('./1.jpg', 0)
imgs.append(img)

img = cv2.imread('./2.jpg', 0)
imgs.append(img)

img = cv2.imread('./3.jpg', 0)
imgs.append(img)

star = cv2.xfeatures2d.StarDetector_create()
brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()

# brute-force matcher
bf = cv2.BFMatcher()
# bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
# bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

# FLANN matcher
# FLANN_INDEX_LSH = 6
# index_params= dict(algorithm = FLANN_INDEX_LSH,
#                    table_number = 6, # 12
#                    key_size = 12,     # 20
#                    multi_probe_level = 1) #2
# search_params = dict(checks=50)   # or pass empty dictionary
# flann = cv2.FlannBasedMatcher(index_params,search_params)

for i in range(3):
    for j in range(i, 3):
        if(i == j):
            continue
        
        print('{} : {}'.format(i, j))
        img1 = imgs[i]
        img2 = imgs[j]

        start_time = time.time()
        kp1 = star.detect(img1,None)
        kp2 = star.detect(img2,None)
        kp1, des1 = brief.compute(img1, kp1)
        kp2, des2 = brief.compute(img2, kp2)

        # Brute-Force matching
        # matches = bf.match(des1, des2)
        # print('key points : {}'.format(len(kp2)))
        # print('match points : {}'.format(len(matches)))
        # print("match : {}".format(len(matches) / len(kp2) * 100))
        # img = cv2.drawMatches(img1,kp1,img2,kp2,matches, img2, flags=2)

        good = []
        rate = 0
        try:
            matches = bf.knnMatch(des1, des2, k=2)
            print("exec time : %s sec" % (time.time() - start_time))
            for m,n in matches:
                if m.distance < 0.8*n.distance:
                    good.append([m])
        except:
            pass
        
        if(len(kp1) + len(kp2) != 0):
            rate = len(good) * 2 / (len(kp1) + len(kp2)) * 100
        print('kp1 : {}'.format(len(kp1)))
        print('kp2 : {}'.format(len(kp2)))
        print('match points : {}'.format(len(good)))
        print("match : {}".format(rate))        
        
        # cv.drawMatchesKnn expects list of lists as matches.
        img = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        # # FLANN based matching
        # matches = flann.knnMatch(des1,des2,k=2)
        # # Need to draw only good matches, so create a mask
        # matchesMask = [[0,0] for i in range(len(matches))]

        # # ratio test as per Lowe's paper
        # count = 0
        # for k,(m,n) in enumerate(matches):
        #     # if m.distance < 0.7*n.distance:
        #     if m.distance < 0.9*n.distance:
        #         count += 1
        #         matchesMask[k]=[1,0]
        
        # print('key points : {}'.format(len(kp2)))
        # print('match points : {}'.format(count))
        # print("match : {}".format(count / len(kp2) * 100))

        # draw_params = dict(matchColor = (0,255,0),
        #                 singlePointColor = (255,0,0),
        #                 matchesMask = matchesMask,
        #                 flags = cv2.DrawMatchesFlags_DEFAULT)

        # img = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
        
        cv2.imwrite('./output/{}.png'.format(str(i+j)), img)


