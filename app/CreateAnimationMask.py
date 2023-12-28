import os
import Utils
dir_path = os.path.dirname(os.path.realpath(__file__))
import cv2 as cv

# capture = cv.VideoCapture(dir_path+"\\images\\AvoidObjectsApp\\Animations\\test.mp4")
toSave = cv.VideoWriter(dir_path+'\\images\\AvoidObjectsApp\\Animations\\test3_makse.avi',  
                         cv.VideoWriter_fourcc(*'MJPG'), 
                         24, (1920,1080))
path =dir_path+"\\images\\AvoidObjectsApp\\Animations\\animationTest\\"
allImages = Utils.getAllFilesPathFromFolder(path) 
i = 1
for image in allImages:
    print(image)
    frame = cv.imread(image, cv.IMREAD_UNCHANGED)
    frameTosave = Utils.CreateMask(frame, (255,255,255))
    frameTosave = cv.cvtColor(frameTosave, cv.COLOR_GRAY2BGR)
    
    #toSave.write(frameTosave)
    cv.imwrite(dir_path+"\\images\\AvoidObjectsApp\\Animations\\animationsImagesMask\\%04d.png" % i, frameTosave)
    i+=1
    cv.imshow("Frameto sva", cv.resize(frameTosave, (1280,720)))

# while capture.isOpened():
#     result, frame = capture.read()
#     if not result:
#         break
#     print(frame.shape, "i:", i)
#     i+=1
#     frame = cv.imread(dir_path+"\\images\\AvoidObjectsApp\\Animations\\animationTest/0023.png")
#     frameTosave = Utils.CreateMask(frame, (255,255,255))
#     frameTosave = cv.cvtColor(frameTosave, cv.COLOR_GRAY2BGR)
    
#     #toSave.write(frameTosave)
    
#     cv.imshow("Frameto sva", cv.resize(frameTosave, (1280,720)))
#     if cv.waitKey(1) == ord('q'):
#         break
    
# capture.release() 
toSave.release()

cv.destroyAllWindows() 
print("Done")